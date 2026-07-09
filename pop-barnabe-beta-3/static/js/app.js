function getWeekStamp() {
    const today = new Date();
    const day = (today.getDay() + 6) % 7;
    const monday = new Date(today);
    monday.setDate(today.getDate() - day);
    return monday.toISOString().slice(0, 10);
}

function buildStorageKey(scope, weekday) {
    return `barnabe-ops::${scope}::${weekday}::${getWeekStamp()}`;
}

function loadCheckedIds(scope, weekday) {
    const key = buildStorageKey(scope, weekday);
    try {
        return JSON.parse(localStorage.getItem(key)) || [];
    } catch (err) {
        return [];
    }
}

function saveCheckedIds(scope, weekday, ids) {
    const key = buildStorageKey(scope, weekday);
    localStorage.setItem(key, JSON.stringify(ids));
}

function updateProgress(container, checkedIds) {
    const scope = container.dataset.scope;
    const weekday = container.dataset.weekday;
    const progressWrap = document.querySelector(`[data-progress-wrap][data-scope="${scope}"][data-weekday="${weekday}"]`);
    if (!progressWrap) return;

    const allInputs = Array.from(container.querySelectorAll('input[type="checkbox"][data-task-id]'));
    const total = allInputs.length;
    const done = checkedIds.length;
    const fill = progressWrap.querySelector('.progress-bar-fill');
    const label = progressWrap.querySelector('.progress-label');
    const percent = total ? (done / total) * 100 : 0;
    fill.style.width = `${percent}%`;
    label.textContent = `${done} / ${total} concluídas`;
}

function initChecklist(container) {
    const scope = container.dataset.scope;
    const weekday = container.dataset.weekday;
    let checkedIds = loadCheckedIds(scope, weekday);
    const inputs = Array.from(container.querySelectorAll('input[type="checkbox"][data-task-id]'));

    inputs.forEach((input) => {
        const id = input.dataset.taskId;
        const item = input.closest('.task-item');

        if (checkedIds.includes(id)) {
            input.checked = true;
            if (item) item.classList.add('is-checked');
        }

        input.addEventListener('change', () => {
            const currentId = input.dataset.taskId;
            if (input.checked) {
                if (!checkedIds.includes(currentId)) checkedIds.push(currentId);
                if (item) item.classList.add('is-checked');
            } else {
                checkedIds = checkedIds.filter((value) => value !== currentId);
                if (item) item.classList.remove('is-checked');
            }
            saveCheckedIds(scope, weekday, checkedIds);
            updateProgress(container, checkedIds);
        });
    });

    updateProgress(container, checkedIds);
}

function initResetButtons() {
    const buttons = document.querySelectorAll('.reset-checklist');
    buttons.forEach((button) => {
        button.addEventListener('click', () => {
            const scope = button.dataset.scope;
            const weekday = button.dataset.weekday;
            const key = buildStorageKey(scope, weekday);
            localStorage.removeItem(key);

            const container = document.querySelector(`.checklist[data-scope="${scope}"][data-weekday="${weekday}"]`);
            if (!container) return;

            const inputs = Array.from(container.querySelectorAll('input[type="checkbox"][data-task-id]'));
            inputs.forEach((input) => {
                input.checked = false;
                const item = input.closest('.task-item');
                if (item) item.classList.remove('is-checked');
            });

            updateProgress(container, []);
        });
    });
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.checklist[data-scope][data-weekday]').forEach(initChecklist);
    initResetButtons();
});
