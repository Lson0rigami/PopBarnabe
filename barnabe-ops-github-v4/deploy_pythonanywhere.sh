#!/usr/bin/env bash
set -euo pipefail

# Uso:
#   BARNABE_LIVE_DIR="$HOME/barnabe-ops" ./deploy_pythonanywhere.sh
#
# O script atualiza apenas código. `instance/`, `backups/` e `venv/` são preservados.

SOURCE="$(cd "$(dirname "$0")" && pwd)"
LIVE="${BARNABE_LIVE_DIR:-$HOME/barnabe-ops}"
STAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP_DIR="${BARNABE_CODE_BACKUP_DIR:-$HOME/barnabe_code_backups}"
CODE_BACKUP="$BACKUP_DIR/pre_deploy_$STAMP.tar.gz"

CODE_ITEMS=(app.py requirements.txt README.md CHANGELOG_V4.md CONFIGURACAO_RAPIDA.md SECURITY.md data services templates static scripts docs)

if [ "$SOURCE" = "$LIVE" ]; then
  echo "ERRO: SOURCE e LIVE são a mesma pasta. Use git pull para atualizar esta instalação."
  exit 1
fi

if [ ! -d "$LIVE" ]; then
  echo "ERRO: instalação alvo não encontrada: $LIVE"
  exit 1
fi

if [ ! -x "$LIVE/venv/bin/python" ]; then
  echo "ERRO: virtualenv não encontrado em $LIVE/venv"
  exit 1
fi

mkdir -p "$LIVE/instance" "$LIVE/backups" "$BACKUP_DIR"

echo "[1/4] Backup do código atual..."
tar --exclude='venv' --exclude='instance' --exclude='backups' -czf "$CODE_BACKUP" -C "$LIVE" .

echo "[2/4] Backup consistente do banco..."
if [ -f "$LIVE/instance/barnabe_ops.sqlite3" ]; then
  source "$LIVE/venv/bin/activate"
  python "$LIVE/scripts/backup_db.py" || true
fi

echo "[3/4] Dependências e cópia de código..."
source "$LIVE/venv/bin/activate"
python -m pip install -r "$SOURCE/requirements.txt"
for item in "${CODE_ITEMS[@]}"; do
  if [ -e "$SOURCE/$item" ]; then
    rm -rf "$LIVE/$item"
    cp -r "$SOURCE/$item" "$LIVE/$item"
  fi
done

echo "[4/4] Conferência..."
cd "$LIVE"
python scripts/check_install.py

echo ""
echo "Deploy concluído. Código anterior: $CODE_BACKUP"
echo "Agora use Reload na aba Web do PythonAnywhere."
