const BarnabeOps = (() => {
    const STATUS = {
        available: { label: 'Disponível', className: 'status-available', meta: 'Disponível • toque para assumir' },
        in_progress: { label: 'Em andamento', className: 'status-progress', meta: 'Em andamento' },
        // Compatibilidade visual com registros antigos da V3. A V4 não cria novos bloqueios.
        blocked: { label: 'Em andamento', className: 'status-progress', meta: 'Registro antigo • toque para retomar' },
        awaiting_validation: { label: 'Aguardando validação', className: 'status-validation', meta: 'Aguardando validação' },
        completed: { label: 'Concluída', className: 'status-completed', meta: 'Concluída' },
    };

    let currentDay = null;
    let payload = null;
    let cardMap = new Map();

    const modal = () => document.querySelector('[data-ops-modal]');
    const modalContent = () => document.querySelector('[data-modal-content]');

    function apiUrl(path) {
        return `${window.BARNABE?.apiBase || ''}${path}`;
    }

    function esc(value = '') {
        return String(value).replace(/[&<>'"]/g, ch => ({
            '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
        }[ch]));
    }

    function timeLabel(iso) {
        if (!iso) return '';
        const d = new Date(iso);
        return Number.isNaN(d.getTime()) ? '' : d.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
    }

    function dateLabel(isoDate) {
        if (!isoDate) return '';
        const [y, m, d] = isoDate.split('-');
        return `${d}/${m}/${y}`;
    }

    function toast(message, tone = 'info') {
        const stack = document.querySelector('[data-toast-stack]');
        if (!stack) return;
        const el = document.createElement('div');
        el.className = `ops-toast toast-${tone}`;
        el.innerHTML = `<span>${esc(message)}</span>`;
        stack.appendChild(el);
        requestAnimationFrame(() => el.classList.add('show'));
        setTimeout(() => {
            el.classList.remove('show');
            setTimeout(() => el.remove(), 250);
        }, 3200);
    }

    function vibrate(pattern = 25) {
        if (navigator.vibrate) navigator.vibrate(pattern);
    }

    function confetti() {
        const canvas = document.querySelector('[data-confetti-canvas]');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        const dpr = Math.min(devicePixelRatio || 1, 2);
        canvas.width = innerWidth * dpr;
        canvas.height = innerHeight * dpr;
        canvas.style.display = 'block';
        ctx.scale(dpr, dpr);
        const colors = ['#ffd51f', '#16a34a', '#ef4444', '#0878d8', '#ffffff'];
        const pieces = Array.from({ length: 110 }, () => ({
            x: innerWidth / 2 + (Math.random() - .5) * 140,
            y: innerHeight * .35,
            vx: (Math.random() - .5) * 11,
            vy: -Math.random() * 9 - 4,
            g: .24 + Math.random() * .15,
            r: 3 + Math.random() * 5,
            a: Math.random() * Math.PI,
            c: colors[Math.floor(Math.random() * colors.length)]
        }));
        let frame = 0;
        function tick() {
            ctx.clearRect(0, 0, innerWidth, innerHeight);
            pieces.forEach(p => {
                p.x += p.vx; p.y += p.vy; p.vy += p.g; p.a += .15;
                ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.a);
                ctx.fillStyle = p.c; ctx.fillRect(-p.r, -p.r / 2, p.r * 2, p.r); ctx.restore();
            });
            if (frame++ < 110) requestAnimationFrame(tick);
            else { ctx.clearRect(0, 0, innerWidth, innerHeight); canvas.style.display = 'none'; }
        }
        tick();
    }

    function ripple(button, evt) {
        const r = document.createElement('span');
        r.className = 'touch-ripple';
        const rect = button.getBoundingClientRect();
        const x = (evt.clientX || rect.left + rect.width / 2) - rect.left;
        const y = (evt.clientY || rect.top + rect.height / 2) - rect.top;
        r.style.left = `${x}px`; r.style.top = `${y}px`;
        button.appendChild(r);
        setTimeout(() => r.remove(), 600);
    }

    async function fetchJSON(url, options = {}) {
        const response = await fetch(apiUrl(url), {
            headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
            cache: 'no-store',
            ...options,
        });
        const data = await response.json().catch(() => ({ ok: false, error: 'Resposta inválida do servidor.' }));
        if (!response.ok || !data.ok) throw new Error(data.error || 'Não foi possível concluir a ação.');
        return data;
    }

    function defaultState() {
        return {
            status: 'available', contributors: [], note: '', blocked_reason: '',
            points_total: 0, points_each: 0, points_distribution: {}
        };
    }

    function itemById(id) {
        return [...(payload?.routine || []), ...(payload?.extras || [])].find(t => t.id === id);
    }

    function renderCard(card, item) {
        const s = item.state || defaultState();
        const meta = STATUS[s.status] || STATUS.available;
        card.classList.remove(...Object.values(STATUS).map(v => v.className));
        card.classList.add(meta.className);
        card.querySelector('[data-status-pill]').textContent = meta.label;

        const people = card.querySelector('[data-task-people]');
        const live = card.querySelector('[data-task-live-meta]');
        let peopleText = s.contributors?.length ? s.contributors.join(' + ') : 'Ninguém assumiu';
        if (s.status === 'completed' && s.validator) peopleText += ` • validado por ${s.validator}`;
        people.textContent = peopleText;

        let detail = meta.meta;
        if ((s.status === 'in_progress' || s.status === 'blocked') && s.started_at) detail += ` • desde ${timeLabel(s.started_at)}`;
        if (s.status === 'completed' && s.completed_at) detail += ` às ${timeLabel(s.completed_at)}`;
        if (s.status === 'awaiting_validation' && s.completed_at) detail += ` • finalizada ${timeLabel(s.completed_at)}`;
        if (s.note) detail += ` • Obs.: ${s.note}`;
        live.textContent = detail;
        card.dataset.status = s.status;
    }

    function renderAll() {
        if (!payload) return;
        [...payload.routine, ...payload.extras].forEach(item => {
            const card = cardMap.get(item.id);
            if (card) renderCard(card, item);
        });
        renderSummary();
    }

    function renderSummary() {
        const summary = document.querySelector('[data-ops-summary]');
        if (!summary || !payload) return;
        const items = [...payload.routine, ...payload.extras];
        const states = items.map(i => i.state || defaultState());
        const count = st => states.filter(s => s.status === st).length;
        const done = count('completed');
        const progress = count('in_progress') + count('blocked');
        const total = items.length;
        const percent = total ? Math.round(done / total * 100) : 0;
        summary.querySelector('[data-summary-percent]').textContent = `${percent}%`;
        summary.querySelector('[data-summary-progress]').style.width = `${percent}%`;
        summary.querySelector('[data-summary-done]').textContent = done;
        summary.querySelector('[data-summary-progress-count]').textContent = progress;
        summary.querySelector('[data-summary-validation]').textContent = count('awaiting_validation');
    }

    function peoplePicker(selected = [], single = false, exclude = []) {
        return `<div class="people-picker" data-people-picker data-single="${single ? '1' : '0'}">${(payload?.collaborators || [])
            .filter(c => !exclude.includes(c.nome))
            .map(c => `
                <button type="button" class="person-chip ${selected.includes(c.nome) ? 'selected' : ''}" data-person="${esc(c.nome)}">
                    <span class="person-avatar">${esc(c.nome).charAt(0).toUpperCase()}</span>
                    <span class="person-chip-copy"><strong>${esc(c.nome)}</strong>${c.conta_pontos === false ? '<small>fora da soma de pontos</small>' : ''}</span>
                </button>`).join('')}</div>`;
    }

    function actionButtons(item) {
        const s = item.state || defaultState();
        const history = `<button class="action-link history-link" data-action="history">Ver histórico</button>`;
        if (s.status === 'available') {
            return `<button class="action-big action-yellow" data-action="start">Assumir atividade</button>
                    <button class="action-big action-green" data-action="complete">Concluir direto</button>${history}`;
        }
        if (s.status === 'in_progress') {
            return `<button class="action-big action-green" data-action="complete">Concluir atividade</button>
                    <button class="action-link" data-action="note">Adicionar observação</button>
                    <button class="action-link subtle-danger" data-action="back_step">↶ Voltar etapa</button>${history}`;
        }
        if (s.status === 'blocked') {
            return `<button class="action-big action-yellow" data-action="resume">Retomar atividade</button>
                    <button class="action-link" data-action="note">Adicionar observação</button>${history}`;
        }
        if (s.status === 'awaiting_validation') {
            return `<button class="action-big action-green" data-action="validate">Validar conclusão</button>
                    <button class="action-link" data-action="note">Adicionar observação</button>
                    <button class="action-link subtle-danger" data-action="back_step">↶ Voltar etapa</button>${history}`;
        }
        return `<button class="action-big action-blue" data-action="note">Adicionar observação</button>
                <button class="action-link subtle-danger" data-action="back_step">↶ Voltar etapa</button>${history}`;
    }

    function openTask(item) {
        const s = item.state || defaultState();
        const meta = STATUS[s.status] || STATUS.available;
        const heat = item.priority === 'fire' ? '🔥🔥' : item.priority === 'hot' ? '🔥' : '';
        modalContent().innerHTML = `
            <div class="modal-status-row">
                <span class="status-pill ${meta.className}">${meta.label}</span>
                <span class="modal-points ${item.priority !== 'normal' ? 'modal-points-hot' : ''}">${heat} ${item.points > 0 ? `${item.points} pts` : 'apoio'}</span>
                ${item.requires_validation ? '<span class="validation-badge">exige validação</span>' : ''}
            </div>
            <h2 id="ops-modal-title">${esc(item.title)}</h2>
            ${item.description ? `<p class="modal-description">${esc(item.description)}</p>` : ''}
            ${s.contributors?.length ? `<div class="current-team"><span>Responsável(is)</span><strong>${esc(s.contributors.join(' + '))}</strong></div>` : ''}
            ${s.note ? `<div class="note-box"><strong>Observação</strong><p>${esc(s.note)}</p></div>` : ''}
            <div class="modal-actions">${actionButtons(item)}</div>`;
        modal().hidden = false;
        document.body.classList.add('modal-open');
        modalContent().querySelectorAll('[data-action]').forEach(btn => {
            btn.addEventListener('click', () => prepareAction(item, btn.dataset.action));
        });
    }

    function closeModal() {
        if (!modal()) return;
        modal().hidden = true;
        document.body.classList.remove('modal-open');
    }

    function setupPicker(container) {
        container.querySelectorAll('[data-person]').forEach(btn => btn.addEventListener('click', () => {
            const picker = btn.closest('[data-people-picker]');
            if (picker.dataset.single === '1') picker.querySelectorAll('[data-person]').forEach(b => b.classList.remove('selected'));
            btn.classList.toggle('selected');
            vibrate(15);
        }));
    }

    function selectedPeople(container) {
        return [...container.querySelectorAll('[data-person].selected')].map(b => b.dataset.person);
    }

    async function openHistory(item) {
        modalContent().innerHTML = `<p class="eyebrow">Histórico</p><h2>${esc(item.title)}</h2><p class="empty-state">Carregando movimentações…</p>`;
        try {
            const data = await fetchJSON(`/api/tarefa/${encodeURIComponent(item.id)}/historico?dia=${encodeURIComponent(currentDay)}`);
            const events = data.events || [];
            modalContent().innerHTML = `
                <p class="eyebrow">Histórico da atividade</p>
                <h2>${esc(item.title)}</h2>
                <p class="modal-description">${dateLabel(data.work_date)} • alterações preservadas mesmo quando uma etapa é desfeita.</p>
                <div class="task-history-list">
                    ${events.length ? events.map(event => historyEventHTML(event)).join('') : '<p class="empty-state">Ainda não existem movimentações registradas.</p>'}
                </div>
                <button class="action-link" data-history-back>Voltar para atividade</button>`;
            modalContent().querySelector('[data-history-back]').onclick = () => openTask(item);
        } catch (err) {
            modalContent().innerHTML = `<p class="eyebrow danger-text">Erro</p><h2>Não foi possível carregar o histórico</h2><p>${esc(err.message)}</p><button class="action-link" data-history-back>Voltar</button>`;
            modalContent().querySelector('[data-history-back]').onclick = () => openTask(item);
        }
    }

    function historyEventHTML(event) {
        const detail = event.details || {};
        const reason = detail.reason ? `<small>Motivo: ${esc(detail.reason)}</small>` : '';
        const transition = detail.from_status && detail.to_status ? `<small>${esc(statusText(detail.from_status))} → ${esc(statusText(detail.to_status))}</small>` : '';
        return `<article class="task-history-item event-${esc(event.action)}">
            <span class="event-dot"></span>
            <div>
                <strong>${esc(event.actor_names || 'Sistema')} ${esc(actionLabel(event.action))}</strong>
                ${reason}${transition}
            </div>
            <time>${timeLabel(event.created_at)}</time>
        </article>`;
    }

    function statusText(status) {
        return (STATUS[status] || STATUS.available).label;
    }

    function prepareAction(item, action) {
        const s = item.state || defaultState();
        if (action === 'history') {
            openHistory(item);
            return;
        }
        if (action === 'back_step') {
            modalContent().innerHTML = `
                <p class="eyebrow danger-text">Voltar etapa</p>
                <h2>Voltar esta atividade uma etapa?</h2>
                <p class="modal-description">Nada será apagado do histórico. Se houver pontos desta conclusão, eles serão retirados até a atividade ser concluída novamente.</p>
                <label class="field-label" for="back-reason">Motivo</label>
                <textarea id="back-reason" class="modal-textarea" data-reason maxlength="300" placeholder="Ex.: marcado por engano, faltou finalizar uma parte, precisa refazer…"></textarea>
                <p class="picker-label">Quem está fazendo a correção?</p>
                ${peoplePicker([], true)}
                <button class="action-big action-red-soft" data-confirm>Voltar uma etapa</button>
                <button class="action-link" data-cancel>Cancelar</button>`;
            setupPicker(modalContent());
            modalContent().querySelector('[data-confirm]').onclick = () => submitAction(item, 'back_step', {
                reason: modalContent().querySelector('[data-reason]').value,
                actor: selectedPeople(modalContent())[0] || ''
            });
            modalContent().querySelector('[data-cancel]').onclick = () => openTask(item);
            return;
        }
        if (action === 'note') {
            modalContent().innerHTML = `
                <p class="eyebrow">Observação</p>
                <h2>${esc(item.title)}</h2>
                <textarea class="modal-textarea" data-note maxlength="500" placeholder="Registre uma observação curta…">${esc(s.note || '')}</textarea>
                <button class="action-big action-blue" data-confirm>Salvar observação</button>
                <button class="action-link" data-cancel>Voltar</button>`;
            modalContent().querySelector('[data-confirm]').onclick = () => submitAction(item, 'note', { note: modalContent().querySelector('[data-note]').value });
            modalContent().querySelector('[data-cancel]').onclick = () => openTask(item);
            return;
        }
        if (action === 'validate') {
            modalContent().innerHTML = `
                <p class="eyebrow green-text">Validação</p>
                <h2>Quem conferiu esta atividade?</h2>
                <p class="modal-description">A validação deve ser feita por outra pessoa, diferente de quem executou.</p>
                ${peoplePicker([], true, s.contributors || [])}
                <button class="action-big action-green" data-confirm>Validar e finalizar</button>
                <button class="action-link" data-cancel>Voltar</button>`;
            setupPicker(modalContent());
            modalContent().querySelector('[data-confirm]').onclick = () => submitAction(item, 'validate', { validator: selectedPeople(modalContent())[0] || '' });
            modalContent().querySelector('[data-cancel]').onclick = () => openTask(item);
            return;
        }

        const title = action === 'complete' ? 'Quem realizou esta atividade?' : action === 'resume' ? 'Quem vai continuar?' : 'Quem vai assumir?';
        const selected = s.contributors || [];
        modalContent().innerHTML = `
            <p class="eyebrow">Responsáveis</p>
            <h2>${title}</h2>
            <p class="modal-description">Pode selecionar mais de uma pessoa. Os nomes são escolhidos apenas nesta ação.</p>
            ${peoplePicker(selected)}
            <button class="action-big ${action === 'complete' ? 'action-green' : 'action-yellow'}" data-confirm>
                ${action === 'complete' ? (item.requires_validation ? 'Finalizar e enviar para validação' : 'Concluir atividade') : action === 'resume' ? 'Retomar atividade' : 'Assumir atividade'}
            </button>
            <button class="action-link" data-cancel>Voltar</button>`;
        setupPicker(modalContent());
        modalContent().querySelector('[data-confirm]').onclick = () => submitAction(item, action, { contributors: selectedPeople(modalContent()) });
        modalContent().querySelector('[data-cancel]').onclick = () => openTask(item);
    }

    function completionToast(result, item) {
        const state = result.state || {};
        const total = Number(state.points_total || 0);
        const distribution = state.points_distribution || {};
        const positive = Object.entries(distribution).filter(([, value]) => Number(value) > 0);
        confetti();
        if (total <= 0) {
            toast('Atividade concluída! Registro salvo sem pontuação individual.', 'success');
            return;
        }
        if (positive.length === 1) {
            toast(`🔥 +${positive[0][1]} pts para ${positive[0][0]}! Atividade concluída.`, 'success');
            return;
        }
        if (positive.length > 1) {
            const split = positive.map(([name, value]) => `${name}: ${value}`).join(' • ');
            toast(`🔥 ${total} pts distribuídos • ${split}`, 'success');
            return;
        }
        toast(`+${total} pontos! Atividade concluída.`, 'success');
    }

    async function submitAction(item, action, extra) {
        try {
            const button = modalContent().querySelector('[data-confirm]');
            if (button) { button.disabled = true; button.textContent = 'Salvando…'; }
            const result = await fetchJSON(`/api/tarefa/${encodeURIComponent(item.id)}/acao`, {
                method: 'POST',
                body: JSON.stringify({ dia: currentDay, action, ...extra })
            });
            item.state = result.state;
            renderAll();
            closeModal();
            vibrate(action === 'complete' || action === 'validate' ? [30, 40, 30] : 25);

            if (action === 'complete' && item.requires_validation) {
                toast('Atividade finalizada. Agora aguarda validação.', 'warning');
            } else if (action === 'complete' || action === 'validate') {
                completionToast(result, item);
            } else if (action === 'back_step') {
                const removed = Number(result.state?.points_total || 0);
                toast('Etapa anterior restaurada. O histórico foi preservado.', 'warning');
            } else if (action === 'start' || action === 'resume') {
                toast('Atividade em andamento.', 'warning');
            } else {
                toast('Atualização salva.', 'info');
            }
        } catch (err) {
            toast(err.message, 'danger');
            const button = modalContent().querySelector('[data-confirm]');
            if (button) { button.disabled = false; button.textContent = 'Tentar novamente'; }
        }
    }

    async function initBoard() {
        const board = document.querySelector('[data-ops-board]');
        if (!board) return;
        currentDay = board.dataset.day;
        cardMap = new Map([...document.querySelectorAll('[data-task-card]')].map(card => [card.dataset.taskCard, card]));
        cardMap.forEach(card => {
            const btn = card.querySelector('[data-task-open]');
            btn.addEventListener('click', evt => {
                ripple(btn, evt);
                const item = itemById(card.dataset.taskCard);
                if (item) openTask(item);
            });
        });
        try {
            payload = await fetchJSON(`/api/operacao/${currentDay}`);
            renderAll();
        } catch (err) {
            toast(`Falha ao sincronizar: ${err.message}`, 'danger');
        }
    }

    function actionLabel(action) {
        return ({
            started: 'assumiu a atividade',
            completed: 'concluiu',
            awaiting_validation: 'finalizou e enviou para validação',
            validated: 'validou a conclusão',
            blocked: 'registrou bloqueio',
            resumed: 'retomou',
            reopened: 'reabriu',
            step_back: 'voltou uma etapa',
            note: 'registrou observação'
        })[action] || action;
    }

    async function loadPanel() {
        const root = document.querySelector('[data-panel]');
        if (!root) return;
        const day = root.dataset.day;
        try {
            const data = await fetchJSON(`/api/painel/${day}`);
            root.querySelector('[data-panel-completed]').textContent = data.counts.completed || 0;
            root.querySelector('[data-panel-progress]').textContent = data.counts.in_progress || 0;
            root.querySelector('[data-panel-validation]').textContent = data.counts.awaiting_validation || 0;
            root.querySelector('[data-panel-points]').textContent = data.points_distributed || 0;

            const timeline = document.querySelector('[data-event-timeline]');
            timeline.innerHTML = data.events.length ? data.events.map(e => `
                <article class="event-item event-${esc(e.action)}">
                    <span class="event-dot"></span>
                    <div>
                        <strong>${esc(e.actor_names || 'Sistema')} ${esc(actionLabel(e.action))}</strong>
                        <p>${esc(e.details?.title || e.task_id)}</p>
                        ${e.details?.reason ? `<small>${esc(e.details.reason)}</small>` : ''}
                    </div>
                    <time>${timeLabel(e.created_at)}</time>
                </article>`).join('') : '<p class="empty-state">Ainda não há movimentações neste dia.</p>';

            const bd = document.querySelector('[data-backup-date]');
            const bf = document.querySelector('[data-backup-file]');
            if (bd) bd.textContent = data.backup?.ultimo ? new Date(data.backup.ultimo).toLocaleString('pt-BR') : 'Ainda não criado';
            if (bf) bf.textContent = data.backup?.arquivo || '';
        } catch (err) {
            toast(err.message, 'danger');
        }
    }

    function initPanelControls() {
        const refresh = document.querySelector('[data-panel-refresh]');
        if (refresh) refresh.onclick = loadPanel;
        const backup = document.querySelector('[data-backup-now]');
        if (backup) backup.onclick = async () => {
            try {
                backup.disabled = true;
                backup.textContent = 'Criando…';
                const data = await fetchJSON('/api/backup/manual', { method: 'POST', body: '{}' });
                toast(`Backup criado: ${data.file}`, 'success');
                loadPanel();
            } catch (err) {
                toast(err.message, 'danger');
            } finally {
                backup.disabled = false;
                backup.textContent = 'Criar backup agora';
            }
        };
    }

    // ---------------------------------------------------------------------
    // Painel individual do RH
    // ---------------------------------------------------------------------
    let rhPerson = '';
    let rhPeriod = 'semana';

    function setRhActive(root) {
        root.querySelectorAll('[data-rh-person]').forEach(btn => btn.classList.toggle('active', btn.dataset.rhPerson === rhPerson));
        root.querySelectorAll('[data-rh-period]').forEach(btn => btn.classList.toggle('active', btn.dataset.rhPeriod === rhPeriod));
    }

    function renderRh(root, data) {
        root.querySelector('[data-rh-person-title]').textContent = data.collaborator.name;
        root.querySelector('[data-rh-period-label]').textContent = data.period_label;
        root.querySelector('[data-rh-completed]').textContent = data.metrics.completed;
        root.querySelector('[data-rh-points]').textContent = data.metrics.points;
        root.querySelector('[data-rh-extras]').textContent = data.metrics.extras;
        root.querySelector('[data-rh-validations]').textContent = data.metrics.validations;
        root.querySelector('[data-rh-days]').textContent = data.metrics.active_days;

        const scoreNote = root.querySelector('[data-rh-score-note]');
        const pointsCaption = root.querySelector('[data-rh-points-caption]');
        if (data.collaborator.counts_points) {
            scoreNote.textContent = 'Pontuação ativa';
            scoreNote.className = 'rh-score-note score-active';
            pointsCaption.textContent = 'soma individual';
        } else {
            scoreNote.textContent = 'Fora da soma de pontos';
            scoreNote.className = 'rh-score-note score-off';
            pointsCaption.textContent = 'registro sem pontuação';
        }

        const highlights = root.querySelector('[data-rh-highlights]');
        highlights.innerHTML = data.highlights.length ? data.highlights.map((text, idx) => `
            <div class="rh-highlight"><span>${idx === 0 ? '🔥' : idx === 1 ? '⭐' : '✓'}</span><p>${esc(text)}</p></div>`).join('') : '<p class="empty-state">Ainda não há atividades concluídas neste período.</p>';

        const top = root.querySelector('[data-rh-top-activities]');
        const maxCount = Math.max(1, ...data.top_activities.map(x => x.count));
        top.innerHTML = data.top_activities.length ? data.top_activities.map(item => `
            <div class="rh-top-item">
                <div><strong>${esc(item.title)}</strong><span>${item.count}x</span></div>
                <div class="rh-mini-track"><i style="width:${Math.max(8, item.count / maxCount * 100)}%"></i></div>
            </div>`).join('') : '<p class="empty-state">Sem frequência suficiente para exibir.</p>';

        const bars = root.querySelector('[data-rh-bars]');
        const maxActivities = Math.max(1, ...data.daily_series.map(x => x.activities));
        bars.innerHTML = data.daily_series.map(day => `
            <div class="rh-bar-column" title="${day.activities} atividades • ${day.points} pts">
                <div class="rh-bar-value">${day.activities || ''}</div>
                <div class="rh-bar-track"><i style="height:${day.activities ? Math.max(12, day.activities / maxActivities * 100) : 4}%"></i></div>
                <span>${esc(day.label)}</span>
            </div>`).join('');
        root.querySelector('[data-rh-chart-label]').textContent = `${data.metrics.completed} atividades no período`;

        const recent = root.querySelector('[data-rh-recent]');
        recent.innerHTML = data.recent_completed.length ? data.recent_completed.map(item => `
            <article class="rh-recent-item">
                <span class="rh-recent-icon">${item.kind === 'extra' ? '✦' : '✓'}</span>
                <div><strong>${esc(item.title)}</strong><small>${dateLabel(item.date)}${item.completed_at ? ` • ${timeLabel(item.completed_at)}` : ''}</small></div>
                <b>${item.points > 0 ? `+${item.points}` : '—'}</b>
            </article>`).join('') : '<p class="empty-state">Nenhuma atividade concluída neste período.</p>';
    }

    async function loadRh(root) {
        root.classList.add('is-loading');
        try {
            const data = await fetchJSON(`/api/rh/resumo?colaborador=${encodeURIComponent(rhPerson)}&periodo=${encodeURIComponent(rhPeriod)}`);
            renderRh(root, data);
        } catch (err) {
            toast(err.message, 'danger');
        } finally {
            root.classList.remove('is-loading');
        }
    }

    function initRh() {
        const root = document.querySelector('[data-rh-dashboard]');
        if (!root) return;
        rhPerson = root.dataset.selected || '';
        rhPeriod = root.dataset.period || 'semana';
        root.querySelectorAll('[data-rh-person]').forEach(btn => btn.addEventListener('click', () => {
            rhPerson = btn.dataset.rhPerson;
            setRhActive(root);
            loadRh(root);
        }));
        root.querySelectorAll('[data-rh-period]').forEach(btn => btn.addEventListener('click', () => {
            rhPeriod = btn.dataset.rhPeriod;
            setRhActive(root);
            loadRh(root);
        }));
        setRhActive(root);
        loadRh(root);
    }

    function initModal() {
        document.querySelectorAll('[data-modal-close]').forEach(el => el.addEventListener('click', closeModal));
        document.addEventListener('keydown', e => {
            if (e.key === 'Escape' && modal() && !modal().hidden) closeModal();
        });
    }

    function init() {
        initModal();
        initBoard();
        loadPanel();
        initPanelControls();
        initRh();
    }

    return { init };
})();

document.addEventListener('DOMContentLoaded', BarnabeOps.init);
