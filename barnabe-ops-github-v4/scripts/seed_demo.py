"""Cria dados fictícios para explorar os dashboards localmente.

Use apenas em uma instalação de demonstração. Não execute em produção.
"""
from datetime import timedelta
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from services.storage import agora_local, log_event, upsert_state


def main():
    today = agora_local().date()
    monday = today - timedelta(days=today.weekday())
    samples = [
        (0, "seg_rm_01", ["Colaborador A"], 6.0),
        (0, "seg_av_01", ["Colaborador B"], 5.0),
        (1, "ter_ad_02", ["Colaborador A", "Colaborador C"], 8.0),
        (2, "qua_rm_01", ["Colaborador A"], 6.0),
        (3, "qui_or_02", ["Colaborador B"], 8.0),
        (4, "sex_rt_02", ["Colaborador A"], 6.0),
    ]

    for day_offset, task_id, contributors, points in samples:
        work_date = (monday + timedelta(days=day_offset)).isoformat()
        each = round(points / len(contributors), 1)
        distribution = {name: each for name in contributors}
        state = upsert_state(
            work_date,
            task_id,
            "routine",
            {
                "status": "completed",
                "contributors": contributors,
                "completed_at": agora_local().isoformat(timespec="seconds"),
                "points_total": points,
                "points_each": each,
                "points_distribution": distribution,
                "requires_validation": False,
            },
        )
        log_event(
            work_date,
            task_id,
            "routine",
            "completed",
            contributors,
            {"demo": True, "points_distribution": distribution},
        )
        print("Demo:", work_date, task_id, state["status"], contributors)

    print("Dados fictícios criados. Abra /rh e /painel para explorar.")


if __name__ == "__main__":
    main()
