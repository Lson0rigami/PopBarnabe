from datetime import datetime
from flask import Flask, render_template, abort, request

from data.procedimentos import PROCEDIMENTOS
from data.rotinas import ROTINAS, DIAS_ORDEM
from data.referencias import GUIA_SABORES, GLOSSARIO_LOCAIS, TERMOS, REGRAS_FIXAS

app = Flask(__name__)

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


def get_today_key():
    english = datetime.now().strftime("%A").lower()
    return MAPA_DIAS.get(english, "segunda")


def buscar_procedimento(slug):
    for item in PROCEDIMENTOS:
        if item["slug"] == slug:
            return item
    return None


@app.route("/")
def index():
    dia = request.args.get("dia", "").strip().lower() or get_today_key()
    if dia not in ROTINAS:
        dia = get_today_key()

    rotina = ROTINAS[dia]
    total_tarefas = sum(len(bloco["tarefas"]) for bloco in rotina["blocos"])

    return render_template(
        "index.html",
        dia=dia,
        dia_label=ROTULOS_DIAS.get(dia, dia.title()),
        rotina=rotina,
        dias_ordem=DIAS_ORDEM,
        total_tarefas=total_tarefas,
        regras_fixas=REGRAS_FIXAS,
        glossario_locais=GLOSSARIO_LOCAIS,
    )


@app.route("/procedimentos")
def procedimentos():
    busca = request.args.get("busca", "").strip().lower()
    area = request.args.get("area", "").strip().lower()
    categoria = request.args.get("categoria", "").strip().lower()

    itens = PROCEDIMENTOS

    if busca:
        itens = [
            p for p in itens
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

    areas = sorted(set(p["area"] for p in PROCEDIMENTOS))
    categorias = sorted(set(p["categoria"] for p in PROCEDIMENTOS))

    return render_template(
        "procedimentos.html",
        procedimentos=itens,
        busca=busca,
        area=area,
        categoria=categoria,
        areas=areas,
        categorias=categorias,
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
        dia_label=ROTULOS_DIAS.get(dia, dia.title()),
        rotina=rotina,
        total_tarefas=total_tarefas,
    )


@app.route("/sabores")
def sabores():
    return render_template("sabores.html", sabores=GUIA_SABORES)


@app.route("/glossario")
def glossario():
    return render_template(
        "glossario.html",
        glossario_locais=GLOSSARIO_LOCAIS,
        termos=TERMOS
    )


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
