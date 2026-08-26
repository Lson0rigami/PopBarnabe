from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import app
from data.config_operacional import APP_VERSION
from services.storage import DB_PATH

print(f"Barnabe Ops {APP_VERSION} OK")
print("DB:", DB_PATH)
print("Rotas:", len(list(app.url_map.iter_rules())))
