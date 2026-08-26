from __future__ import annotations

import sqlite3
import tempfile
import zipfile
from datetime import timedelta
from pathlib import Path

from data.config_operacional import BACKUP
from services.storage import DB_PATH, BASE_DIR, agora_local, get_meta, set_meta, event_count

BACKUP_DIR = BASE_DIR / "backups"


def create_backup(label="weekly"):
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    if not DB_PATH.exists():
        return None

    stamp = agora_local().strftime("%Y%m%d_%H%M%S")
    zip_path = BACKUP_DIR / f"barnabe_ops_{label}_{stamp}.zip"

    with tempfile.TemporaryDirectory() as tmp:
        snapshot = Path(tmp) / "barnabe_ops.sqlite3"
        source = sqlite3.connect(DB_PATH)
        dest = sqlite3.connect(snapshot)
        try:
            source.backup(dest)
        finally:
            dest.close(); source.close()

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            z.write(snapshot, "barnabe_ops.sqlite3")
            for rel in [Path("data/config_operacional.py"), Path("data/rotinas.py")]:
                file_path = BASE_DIR / rel
                if file_path.exists():
                    z.write(file_path, str(rel))

    prune_backups()
    set_meta("last_weekly_backup", agora_local().isoformat(timespec="seconds"))
    set_meta("last_backup_file", zip_path.name)
    return zip_path


def prune_backups():
    keep = int(BACKUP.get("manter_ultimos", 12))
    files = sorted(BACKUP_DIR.glob("barnabe_ops_*.zip"), key=lambda p: p.stat().st_mtime, reverse=True)
    for old in files[keep:]:
        old.unlink(missing_ok=True)


def ensure_weekly_backup():
    if event_count() == 0:
        return None
    last = get_meta("last_weekly_backup")
    now = agora_local()
    if last:
        try:
            from datetime import datetime
            dt = datetime.fromisoformat(last)
            if now - dt < timedelta(days=int(BACKUP.get("intervalo_dias", 7))):
                return None
        except Exception:
            pass
    return create_backup("weekly")


def backup_status():
    return {
        "ultimo": get_meta("last_weekly_backup"),
        "arquivo": get_meta("last_backup_file"),
        "quantidade": len(list(BACKUP_DIR.glob("barnabe_ops_*.zip"))) if BACKUP_DIR.exists() else 0,
    }
