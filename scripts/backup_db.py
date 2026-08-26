from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from services.storage import init_db
from services.backup import create_backup
init_db()
p = create_backup('manual-cli')
print(p or 'Nenhum banco para backup')
