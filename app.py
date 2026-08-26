import calendar
import os
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta

from flask import Flask, abort, jsonify, redirect, render_template, request, session, url_for

from data.config_operacional import (
    APP_TIMEZONE,
    APP_VERSION,
    ATIVIDADES_COMPLEMENTARES,
    CATEGORIAS_RH,
    COLABORADORES,
    DESTAQUE_PONTOS,
    PONTOS_TAREFAS,
    VALIDACAO_OBRIGATORIA,
)
from data.procedimentos import PROCEDIMENTOS
from data.referencias import GLOSSARIO_LOCAIS, GUIA_SABORES, REGRAS_FIXAS, TERMOS
from data.rotinas import DIAS_ORDEM, ROTINAS
from services.backup import backup_status, create_backup, ensure_weekly_backup
from services.storage import (
    agora_iso,
    agora_local,
    get_events_between,
    get_state,
    get_states,
    get_states_between,
    get_task_events,
    init_db,
    log_event,
    recent_events,
    upsert_state,
)

app = Flask(__name__)
# Fallback apenas para desenvolvimento local. Em produção, defina BARNABE_OPS_SECRET.
app.secret_key = os.environ.get("BARNABE_OPS_SECRET", "dev-only-change-this-secret")
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)

MAPA_DIAS = {
    "monday": "segunda",
    "tuesday": "terca",
    "wednesday": "quarta",
    "thursday": "quinta",
    "friday": "sexta",
    "saturday": "sabado",
    "sunday": "domingo",
}
ROTULOS_DIAS = {
    "segunda": "Segunda-feira",
    "terca": "Terça-feira",
    "quarta": "Quarta-feira",
    "quinta": "Quinta-feira",
    "sexta": "Sexta-feira",
    "sabado": "Sábado",
    "domingo": "Domingo",
}
DAY_INDEX = {dia: idx for idx, dia in enumerate(DIAS_ORDEM)}

init_db()


# ---------------------------------------------------------------------------
# Helpers gerais
# ---------------------------------------------------------------------------
def get_today_key():
    english = agora_local().strftime("%A").lower()
    return MAPA_DIAS.get(english, "segunda")


def week_monday(anchor=None):
    anchor = anchor or agora_local().date()
    return anchor - timedelta(days=anchor.weekday())


def work_date_for_day(dia):
    idx = DAY_INDEX.get(dia, 0)
    return (week_monday() + timedelta(days=idx)).isoformat()


def buscar_procedimento(slug):
    return next((item for item in PROCEDIMENTOS if item["slug"] == slug), None)


def active_collaborators():
    return [c for c in COLABORADORES if c.get("ativo", True)]


def collaborator_names():
    return {c["nome"] for c in active_collaborators()}


def all_collaborator_names():
    return {c["nome"] for c in COLABORADORES}


def collaborator_config_by_name(name):
    return next((c for c in COLABORADORES if c.get("nome") == name), None)


def counts_points(name):
    cfg = collaborator_config_by_name(name)
    # `ativo` controla apenas novas seleções. O histórico de uma pessoa que
    # futuramente ficar inativa continua usando a regra de pontuação gravada.
    return bool(cfg and cfg.get("conta_pontos", True))


def calculate_point_distribution(contributors, task_points):
    """Divide os pontos só entre pessoas elegíveis.

    Exemplo: se Administrador (fora da pontuação) e Colaborador A fizerem juntos uma atividade
    de 6 pontos, Colaborador A recebe os 6 pontos e Administrador continua registrado como
    participante, porém com 0 ponto.
    """
    eligible = [name for name in contributors if counts_points(name)]
    distribution = {name: 0.0 for name in contributors}
    if not eligible:
        return distribution, 0.0, 0.0

    task_points = round(float(task_points), 1)
    base = round(task_points / len(eligible), 1)
    running = 0.0
    for idx, name in enumerate(eligible):
        if idx == len(eligible) - 1:
            value = round(task_points - running, 1)
        else:
            value = base
            running = round(running + value, 1)
        distribution[name] = value

    total = round(sum(distribution.values()), 1)
    each_reference = round(task_points / len(eligible), 1)
    return distribution, total, each_reference


def complementares_for_day(dia):
    return [item for item in ATIVIDADES_COMPLEMENTARES if dia in item.get("dias", DIAS_ORDEM)]


def priority_for_points(points):
    points = float(points or 0)
    if points >= DESTAQUE_PONTOS.get("forte", 12):
        return "fire"
    if points >= DESTAQUE_PONTOS.get("aura", 8):
        return "hot"
    return "normal"


def find_task(task_id, dia):
    for bloco in ROTINAS[dia]["blocos"]:
        for tarefa in bloco["tarefas"]:
            if tarefa["id"] == task_id:
                points = float(PONTOS_TAREFAS.get(task_id, 2))
                return {
                    "id": tarefa["id"],
                    "titulo": tarefa["texto"],
                    "kind": "routine",
                    "points": points,
                    "priority": priority_for_points(points),
                    "requires_validation": task_id in VALIDACAO_OBRIGATORIA,
                    "pop_slug": tarefa.get("pop_slug"),
                    "bloco": bloco["titulo"],
                }
    for extra in complementares_for_day(dia):
        if extra["id"] == task_id:
            points = float(extra.get("pontos", 2))
            return {
                "id": extra["id"],
                "titulo": extra["titulo"],
                "kind": "extra",
                "points": points,
                "priority": priority_for_points(points),
                "requires_validation": bool(extra.get("validacao", False)),
                "pop_slug": extra.get("pop_slug"),
                "bloco": "Atividade complementar",
            }
    return None


def task_title_for_id(task_id):
    for dia in DIAS_ORDEM:
        for bloco in ROTINAS[dia]["blocos"]:
            for tarefa in bloco["tarefas"]:
                if tarefa["id"] == task_id:
                    return tarefa["texto"]
    for extra in ATIVIDADES_COMPLEMENTARES:
        if extra["id"] == task_id:
            return extra["titulo"]
    return task_id


def task_category_for_id(task_id):
    return CATEGORIAS_RH.get(task_id, task_title_for_id(task_id))


def serialize_task_config(task_id):
    points = float(PONTOS_TAREFAS.get(task_id, 2))
    return {
        "points": points,
        "priority": priority_for_points(points),
        "requires_validation": task_id in VALIDACAO_OBRIGATORIA,
    }


def validate_people(names):
    known = collaborator_names()
    clean = []
    for name in names or []:
        name = str(name).strip()
        if name and name in known and name not in clean:
            clean.append(name)
    return clean


def state_payload(dia):
    work_date = work_date_for_day(dia)
    states = get_states(work_date)
    routine = []
    for bloco in ROTINAS[dia]["blocos"]:
        for tarefa in bloco["tarefas"]:
            cfg = serialize_task_config(tarefa["id"])
            routine.append(
                {
                    "id": tarefa["id"],
                    "title": tarefa["texto"],
                    "kind": "routine",
                    "block": bloco["titulo"],
                    "points": cfg["points"],
                    "priority": cfg["priority"],
                    "requires_validation": cfg["requires_validation"],
                    "state": states.get(tarefa["id"]),
                }
            )
    extras = []
    for extra in complementares_for_day(dia):
        points = float(extra.get("pontos", 2))
        extras.append(
            {
                "id": extra["id"],
                "title": extra["titulo"],
                "description": extra.get("descricao", ""),
                "kind": "extra",
                "points": points,
                "priority": priority_for_points(points),
                "requires_validation": bool(extra.get("validacao", False)),
                "pop_slug": extra.get("pop_slug"),
                "state": states.get(extra["id"]),
            }
        )
    return {
        "dia": dia,
        "work_date": work_date,
        "routine": routine,
        "extras": extras,
        "collaborators": active_collaborators(),
    }


def _task_rows():
    for dia in DIAS_ORDEM:
        for bloco in ROTINAS[dia]["blocos"]:
            for task in bloco["tarefas"]:
                yield dia, bloco["titulo"], task["id"], task["texto"], task.get("pop_slug")


@app.context_processor
def inject_app_version():
    return {"app_version": APP_VERSION}


# ---------------------------------------------------------------------------
# Acesso e backup
# ---------------------------------------------------------------------------
@app.before_request
def internal_access_and_backup():
    if request.endpoint == "static":
        return None
    pin = os.environ.get("BARNABE_OPS_PIN", "").strip()
    if pin and request.endpoint not in {"acesso", "health"} and not session.get("barnabe_access"):
        if request.path.startswith("/api/"):
            return jsonify({"ok": False, "error": "Acesso não autorizado."}), 401
        return redirect(url_for("acesso", next=request.path))
    try:
        ensure_weekly_backup()
    except Exception:
        # Backup nunca deve derrubar a operação do dia.
        app.logger.exception("Falha ao verificar backup semanal")
    return None


@app.route("/acesso", methods=["GET", "POST"])
def acesso():
    pin = os.environ.get("BARNABE_OPS_PIN", "").strip()
    if not pin:
        return redirect(url_for("index"))
    error = None
    if request.method == "POST":
        if request.form.get("pin", "") == pin:
            session["barnabe_access"] = True
            return redirect(request.args.get("next") or url_for("index"))
        error = "PIN incorreto."
    return render_template("acesso.html", error=error)


@app.route("/health")
def health():
    return jsonify({"ok": True, "version": APP_VERSION})


# ---------------------------------------------------------------------------
# Operação
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    dia = request.args.get("dia", "").strip().lower() or get_today_key()
    if dia not in ROTINAS:
        dia = get_today_key()
    rotina = ROTINAS[dia]
    total_tarefas = sum(len(bloco["tarefas"]) for bloco in rotina["blocos"])
    extras = complementares_for_day(dia)
    return render_template(
        "index.html",
        dia=dia,
        dia_label=ROTULOS_DIAS.get(dia, dia.title()),
        rotina=rotina,
        dias_ordem=DIAS_ORDEM,
        total_tarefas=total_tarefas,
        regras_fixas=REGRAS_FIXAS,
        glossario_locais=GLOSSARIO_LOCAIS,
        task_config={tid: serialize_task_config(tid) for _, _, tid, _, _ in _task_rows()},
        extras=extras,
        colaboradores=active_collaborators(),
        work_date=work_date_for_day(dia),
    )


@app.route("/api/operacao/<dia>")
def api_operacao(dia):
    if dia not in ROTINAS:
        return jsonify({"ok": False, "error": "Dia inválido."}), 404
    payload = state_payload(dia)
    payload["ok"] = True
    return jsonify(payload)


@app.route("/api/tarefa/<task_id>/acao", methods=["POST"])
def api_task_action(task_id):
    data = request.get_json(silent=True) or {}
    dia = str(data.get("dia", "")).strip().lower()
    action = str(data.get("action", "")).strip().lower()
    if dia not in ROTINAS:
        return jsonify({"ok": False, "error": "Dia inválido."}), 400

    task = find_task(task_id, dia)
    if not task:
        return jsonify({"ok": False, "error": "Atividade não encontrada."}), 404

    work_date = work_date_for_day(dia)
    current = get_state(work_date, task_id) or {}
    people = validate_people(data.get("contributors") or [])
    note = str(data.get("note", current.get("note", "")) or "").strip()[:500]
    points = float(task["points"])
    requires_validation = bool(task["requires_validation"])
    now = agora_iso()

    base = {
        "requires_validation": requires_validation,
        "note": note,
        "points_total": current.get("points_total", 0) or 0,
        "points_each": current.get("points_each", 0) or 0,
        "points_distribution": current.get("points_distribution") or {},
    }

    if action == "start":
        if not people:
            return jsonify({"ok": False, "error": "Selecione quem está assumindo a atividade."}), 400
        base.update(
            {
                "status": "in_progress",
                "contributors": people,
                "started_at": current.get("started_at") or now,
                "blocked_reason": "",
                "blocked_at": None,
                "completed_at": None,
                "validated_at": None,
                "validator": None,
                "points_total": 0,
                "points_each": 0,
                "points_distribution": {},
            }
        )
        state = upsert_state(work_date, task_id, task["kind"], base)
        log_event(work_date, task_id, task["kind"], "started", people, {"title": task["titulo"]})

    elif action == "complete":
        final_people = people or current.get("contributors") or []
        if not final_people:
            return jsonify({"ok": False, "error": "Selecione quem realizou a atividade."}), 400

        status = "awaiting_validation" if requires_validation else "completed"
        distribution, total_points, each = calculate_point_distribution(final_people, points)
        if requires_validation:
            distribution, total_points, each = {}, 0, 0

        base.update(
            {
                "status": status,
                "contributors": final_people,
                "started_at": current.get("started_at") or now,
                "completed_at": now,
                "blocked_at": None,
                "blocked_reason": "",
                "validated_at": None,
                "validator": None,
                "points_total": total_points,
                "points_each": each,
                "points_distribution": distribution,
            }
        )
        state = upsert_state(work_date, task_id, task["kind"], base)
        log_event(
            work_date,
            task_id,
            task["kind"],
            "awaiting_validation" if requires_validation else "completed",
            final_people,
            {
                "title": task["titulo"],
                "points_total": total_points,
                "points_each": each,
                "points_distribution": distribution,
            },
        )

    elif action == "validate":
        validator = str(data.get("validator", "")).strip()
        if validator not in collaborator_names():
            return jsonify({"ok": False, "error": "Selecione quem está validando."}), 400
        contributors = current.get("contributors") or []
        if validator in contributors:
            return jsonify({"ok": False, "error": "A validação precisa ser feita por outra pessoa."}), 400
        if current.get("status") != "awaiting_validation":
            return jsonify({"ok": False, "error": "Esta atividade não está aguardando validação."}), 400

        distribution, total_points, each = calculate_point_distribution(contributors, points)
        base.update(
            {
                "status": "completed",
                "contributors": contributors,
                "started_at": current.get("started_at"),
                "completed_at": current.get("completed_at") or now,
                "validated_at": now,
                "validator": validator,
                "points_total": total_points,
                "points_each": each,
                "points_distribution": distribution,
                "blocked_at": None,
                "blocked_reason": "",
            }
        )
        state = upsert_state(work_date, task_id, task["kind"], base)
        log_event(
            work_date,
            task_id,
            task["kind"],
            "validated",
            [validator],
            {
                "title": task["titulo"],
                "contributors": contributors,
                "points_total": total_points,
                "points_each": each,
                "points_distribution": distribution,
            },
        )

    elif action == "back_step":
        actor = str(data.get("actor", "")).strip()
        reason = str(data.get("reason", "")).strip()[:300]
        if actor not in collaborator_names():
            return jsonify({"ok": False, "error": "Selecione quem está voltando a etapa."}), 400
        if not reason:
            return jsonify({"ok": False, "error": "Informe o motivo para voltar a etapa."}), 400

        old_status = current.get("status", "available")
        contributors = current.get("contributors") or []
        removed_points = float(current.get("points_total") or 0)

        if old_status == "completed":
            new_status = "awaiting_validation" if requires_validation else "in_progress"
            base.update(
                {
                    "status": new_status,
                    "contributors": contributors,
                    "started_at": current.get("started_at"),
                    "completed_at": current.get("completed_at") if requires_validation else None,
                    "validated_at": None,
                    "validator": None,
                    "points_total": 0,
                    "points_each": 0,
                    "points_distribution": {},
                    "blocked_at": None,
                    "blocked_reason": "",
                }
            )
        elif old_status == "awaiting_validation":
            new_status = "in_progress"
            base.update(
                {
                    "status": new_status,
                    "contributors": contributors,
                    "started_at": current.get("started_at") or now,
                    "completed_at": None,
                    "validated_at": None,
                    "validator": None,
                    "points_total": 0,
                    "points_each": 0,
                    "points_distribution": {},
                    "blocked_at": None,
                    "blocked_reason": "",
                }
            )
        elif old_status == "in_progress":
            new_status = "available"
            base.update(
                {
                    "status": new_status,
                    "contributors": [],
                    "started_at": None,
                    "completed_at": None,
                    "validated_at": None,
                    "validator": None,
                    "points_total": 0,
                    "points_each": 0,
                    "points_distribution": {},
                    "blocked_at": None,
                    "blocked_reason": "",
                }
            )
        elif old_status == "blocked":
            # Compatibilidade com registros criados na V3. Novos bloqueios não
            # aparecem mais na interface da V4.
            new_status = "in_progress"
            base.update(
                {
                    "status": new_status,
                    "contributors": contributors,
                    "started_at": current.get("started_at") or now,
                    "completed_at": None,
                    "validated_at": None,
                    "validator": None,
                    "points_total": 0,
                    "points_each": 0,
                    "points_distribution": {},
                    "blocked_at": None,
                    "blocked_reason": "",
                }
            )
        else:
            return jsonify({"ok": False, "error": "A atividade já está disponível."}), 400

        state = upsert_state(work_date, task_id, task["kind"], base)
        log_event(
            work_date,
            task_id,
            task["kind"],
            "step_back",
            [actor],
            {
                "title": task["titulo"],
                "reason": reason,
                "from_status": old_status,
                "to_status": new_status,
                "removed_points": removed_points,
            },
        )

    elif action == "resume":
        # Mantido somente para recuperar eventual tarefa bloqueada na V3.
        final_people = people or current.get("contributors") or []
        if not final_people:
            return jsonify({"ok": False, "error": "Selecione quem vai continuar a atividade."}), 400
        base.update(
            {
                "status": "in_progress",
                "contributors": final_people,
                "started_at": current.get("started_at") or now,
                "completed_at": None,
                "validated_at": None,
                "validator": None,
                "blocked_at": None,
                "blocked_reason": "",
                "points_total": 0,
                "points_each": 0,
                "points_distribution": {},
            }
        )
        state = upsert_state(work_date, task_id, task["kind"], base)
        log_event(work_date, task_id, task["kind"], "resumed", final_people, {"title": task["titulo"]})

    elif action == "note":
        base.update(
            {
                "status": current.get("status", "available"),
                "contributors": current.get("contributors") or [],
                "started_at": current.get("started_at"),
                "completed_at": current.get("completed_at"),
                "validated_at": current.get("validated_at"),
                "validator": current.get("validator"),
                "blocked_at": current.get("blocked_at"),
                "blocked_reason": current.get("blocked_reason", ""),
            }
        )
        state = upsert_state(work_date, task_id, task["kind"], base)
        log_event(
            work_date,
            task_id,
            task["kind"],
            "note",
            current.get("contributors") or [],
            {"title": task["titulo"]},
        )

    else:
        return jsonify({"ok": False, "error": "Ação inválida."}), 400

    return jsonify({"ok": True, "state": state, "task": task})


@app.route("/api/tarefa/<task_id>/historico")
def api_task_history(task_id):
    dia = str(request.args.get("dia", "")).strip().lower()
    if dia not in ROTINAS:
        return jsonify({"ok": False, "error": "Dia inválido."}), 400
    task = find_task(task_id, dia)
    if not task:
        return jsonify({"ok": False, "error": "Atividade não encontrada."}), 404
    work_date = work_date_for_day(dia)
    return jsonify(
        {
            "ok": True,
            "task": task,
            "work_date": work_date,
            "events": get_task_events(work_date, task_id, 80),
        }
    )


# ---------------------------------------------------------------------------
# Painel operacional
# ---------------------------------------------------------------------------
@app.route("/painel")
def painel():
    dia = request.args.get("dia", "").strip().lower() or get_today_key()
    if dia not in ROTINAS:
        dia = get_today_key()
    return render_template(
        "painel.html",
        dia=dia,
        dia_label=ROTULOS_DIAS[dia],
        dias_ordem=DIAS_ORDEM,
        work_date=work_date_for_day(dia),
        backup=backup_status(),
    )


@app.route("/api/painel/<dia>")
def api_painel(dia):
    if dia not in ROTINAS:
        return jsonify({"ok": False, "error": "Dia inválido."}), 404
    payload = state_payload(dia)
    states = [item.get("state") for item in payload["routine"] + payload["extras"] if item.get("state")]
    counts = {k: 0 for k in ["available", "in_progress", "blocked", "awaiting_validation", "completed"]}
    points = 0.0
    for state in states:
        status = state.get("status", "available")
        counts[status] = counts.get(status, 0) + 1
        points += float(state.get("points_total") or 0)
    total = len(payload["routine"]) + len(payload["extras"])
    counts["available"] = total - sum(v for k, v in counts.items() if k != "available")
    # Registros antigos bloqueados são apresentados junto do fluxo em andamento;
    # a V4 não oferece mais a ação de criar novos bloqueios.
    visible_progress = counts.get("in_progress", 0) + counts.get("blocked", 0)
    return jsonify(
        {
            "ok": True,
            "dia": dia,
            "work_date": payload["work_date"],
            "counts": {
                "available": counts.get("available", 0),
                "in_progress": visible_progress,
                "awaiting_validation": counts.get("awaiting_validation", 0),
                "completed": counts.get("completed", 0),
            },
            "total": total,
            "points_distributed": round(points, 1),
            "events": recent_events(payload["work_date"], 50),
            "backup": backup_status(),
        }
    )


@app.route("/api/backup/manual", methods=["POST"])
def api_backup_manual():
    path = create_backup("manual")
    return jsonify({"ok": True, "file": path.name if path else None, "backup": backup_status()})


# ---------------------------------------------------------------------------
# Painel individual do RH / gestão
# ---------------------------------------------------------------------------
def _period_bounds(periodo):
    today = agora_local().date()
    if periodo == "mes":
        start = today.replace(day=1)
        last_day = calendar.monthrange(today.year, today.month)[1]
        end = today.replace(day=last_day)
        label = today.strftime("%m/%Y")
    else:
        start = week_monday(today)
        end = start + timedelta(days=6)
        label = f"{start.strftime('%d/%m')} a {end.strftime('%d/%m/%Y')}"
        periodo = "semana"
    return periodo, start, end, label


def _event_actor_names(event):
    return [name.strip() for name in str(event.get("actor_names") or "").split(",") if name.strip()]


def _legacy_points_for_person(state, collaborator_name):
    distribution = state.get("points_distribution") or {}
    if collaborator_name in distribution:
        return float(distribution.get(collaborator_name) or 0)
    if not counts_points(collaborator_name):
        return 0.0
    # Compatibilidade com registros da V3, que possuíam apenas points_each.
    if collaborator_name in (state.get("contributors") or []):
        return float(state.get("points_each") or 0)
    return 0.0


def build_rh_summary(collaborator_name, periodo):
    periodo, start, end, label = _period_bounds(periodo)
    states = get_states_between(start.isoformat(), end.isoformat())
    events = get_events_between(start.isoformat(), end.isoformat(), 1500)

    completed = []
    activity_counter = Counter()
    daily = defaultdict(lambda: {"atividades": 0, "pontos": 0.0, "extras": 0})
    points_total = 0.0
    extra_count = 0

    for state in states:
        if state.get("status") != "completed":
            continue
        contributors = state.get("contributors") or []
        if collaborator_name not in contributors:
            continue

        person_points = round(_legacy_points_for_person(state, collaborator_name), 1)
        points_total = round(points_total + person_points, 1)
        title = task_title_for_id(state.get("task_id"))
        category = task_category_for_id(state.get("task_id"))
        activity_counter[category] += 1
        is_extra = state.get("task_kind") == "extra"
        if is_extra:
            extra_count += 1

        day_bucket = daily[state.get("work_date")]
        day_bucket["atividades"] += 1
        day_bucket["pontos"] = round(day_bucket["pontos"] + person_points, 1)
        if is_extra:
            day_bucket["extras"] += 1

        completed.append(
            {
                "date": state.get("work_date"),
                "task_id": state.get("task_id"),
                "title": title,
                "kind": state.get("task_kind"),
                "points": person_points,
                "completed_at": state.get("completed_at"),
            }
        )

    validations = [
        event
        for event in events
        if event.get("action") == "validated" and collaborator_name in _event_actor_names(event)
    ]

    top_activities = [
        {"title": title, "count": count}
        for title, count in activity_counter.most_common(8)
    ]

    active_days = len([day for day, values in daily.items() if values["atividades"] > 0])
    series = []
    cursor = start
    while cursor <= end:
        values = daily.get(cursor.isoformat(), {"atividades": 0, "pontos": 0.0, "extras": 0})
        series.append(
            {
                "date": cursor.isoformat(),
                "label": cursor.strftime("%d/%m"),
                "activities": values["atividades"],
                "points": round(values["pontos"], 1),
                "extras": values["extras"],
            }
        )
        cursor += timedelta(days=1)

    highlights = []
    for item in top_activities[:3]:
        times = item["count"]
        suffix = "vez" if times == 1 else "vezes"
        highlights.append(f"{collaborator_name} realizou {times} {suffix}: {item['title']}")

    cfg = collaborator_config_by_name(collaborator_name) or {}
    return {
        "collaborator": {
            "name": collaborator_name,
            "counts_points": bool(cfg.get("conta_pontos", True)),
        },
        "period": periodo,
        "period_label": label,
        "start": start.isoformat(),
        "end": end.isoformat(),
        "metrics": {
            "completed": len(completed),
            "points": round(points_total, 1),
            "extras": extra_count,
            "validations": len(validations),
            "active_days": active_days,
        },
        "top_activities": top_activities,
        "highlights": highlights,
        "daily_series": series,
        "recent_completed": sorted(completed, key=lambda x: (x["date"], x.get("completed_at") or ""), reverse=True)[:20],
    }


@app.route("/rh")
def rh_dashboard():
    # O RH enxerga também colaboradores marcados como inativos para não perder
    # acesso ao histórico quando alguém sair da operação.
    colaboradores = COLABORADORES
    selected = request.args.get("colaborador", "").strip()
    if selected not in {c["nome"] for c in colaboradores}:
        selected = next((c["nome"] for c in colaboradores if c.get("conta_pontos", True)), colaboradores[0]["nome"] if colaboradores else "")
    periodo = request.args.get("periodo", "semana").strip().lower()
    if periodo not in {"semana", "mes"}:
        periodo = "semana"
    return render_template("rh.html", colaboradores=colaboradores, selected=selected, periodo=periodo)


@app.route("/api/rh/resumo")
def api_rh_summary():
    collaborator = request.args.get("colaborador", "").strip()
    periodo = request.args.get("periodo", "semana").strip().lower()
    if collaborator not in all_collaborator_names():
        return jsonify({"ok": False, "error": "Colaborador inválido."}), 400
    if periodo not in {"semana", "mes"}:
        periodo = "semana"
    return jsonify({"ok": True, **build_rh_summary(collaborator, periodo)})


# ---------------------------------------------------------------------------
# POPs e referências
# ---------------------------------------------------------------------------
@app.route("/procedimentos")
def procedimentos():
    busca = request.args.get("busca", "").strip().lower()
    area = request.args.get("area", "").strip().lower()
    categoria = request.args.get("categoria", "").strip().lower()
    itens = PROCEDIMENTOS
    if busca:
        itens = [
            p
            for p in itens
            if busca in p["titulo"].lower()
            or busca in p["area"].lower()
            or busca in p["categoria"].lower()
            or busca in p["local_armazenamento"].lower()
            or busca in p["resumo"].lower()
        ]
    if area:
        itens = [p for p in itens if p["area"].lower() == area]
    if categoria:
        itens = [p for p in itens if p["categoria"].lower() == categoria]
    return render_template(
        "procedimentos.html",
        procedimentos=itens,
        busca=busca,
        area=area,
        categoria=categoria,
        areas=sorted(set(p["area"] for p in PROCEDIMENTOS)),
        categorias=sorted(set(p["categoria"] for p in PROCEDIMENTOS)),
    )


@app.route("/procedimento/<slug>")
def procedimento(slug):
    item = buscar_procedimento(slug)
    if not item:
        abort(404)
    return render_template("procedimento.html", procedimento=item)


@app.route("/rotinas")
def rotinas():
    return render_template("rotinas.html", rotinas=ROTINAS, dias_ordem=DIAS_ORDEM, rotulos=ROTULOS_DIAS)


@app.route("/rotina/<dia>")
def rotina_dia(dia):
    dia = dia.lower().strip()
    if dia not in ROTINAS:
        abort(404)
    rotina = ROTINAS[dia]
    total_tarefas = sum(len(bloco["tarefas"]) for bloco in rotina["blocos"])
    return render_template(
        "rotina_dia.html",
        dia=dia,
        dia_label=ROTULOS_DIAS[dia],
        rotina=rotina,
        total_tarefas=total_tarefas,
        task_config={tid: serialize_task_config(tid) for _, _, tid, _, _ in _task_rows()},
        extras=complementares_for_day(dia),
        colaboradores=active_collaborators(),
        work_date=work_date_for_day(dia),
    )


@app.route("/sabores")
def sabores():
    return render_template("sabores.html", sabores=GUIA_SABORES)


@app.route("/glossario")
def glossario():
    return render_template("glossario.html", glossario_locais=GLOSSARIO_LOCAIS, termos=TERMOS)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
