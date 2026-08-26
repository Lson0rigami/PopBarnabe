# Deploy genérico no PythonAnywhere

Este guia não contém usuário, domínio ou caminho pessoal.

## 1. Envie o projeto

Faça upload do ZIP ou clone o repositório para uma pasta no seu diretório pessoal.

Exemplo:

```bash
cd ~
git clone URL_DO_REPOSITORIO barnabe-ops
cd barnabe-ops
```

## 2. Crie o virtualenv

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

## 3. Configure o Web App

Use **Manual configuration** e configure:

```text
Source code:      /home/SEU_USUARIO/barnabe-ops
Working directory:/home/SEU_USUARIO/barnabe-ops
Virtualenv:       /home/SEU_USUARIO/barnabe-ops/venv
```

## 4. WSGI

```python
import os
import sys

path = "/home/SEU_USUARIO/barnabe-ops"
if path not in sys.path:
    sys.path.insert(0, path)

os.environ["BARNABE_OPS_SECRET"] = "COLOQUE_UMA_CHAVE_FORTE_AQUI"
# os.environ["BARNABE_OPS_PIN"] = "PIN_INTERNO"

from app import app as application
```

## 5. Static files

```text
URL:       /static/
Directory: /home/SEU_USUARIO/barnabe-ops/static
```

## 6. Atualizações

Antes de atualizar, faça backup do banco. O script `scripts/backup_db.py` pode ser usado manualmente:

```bash
source venv/bin/activate
python scripts/backup_db.py
```

Depois atualize o código e clique em **Reload** na aba Web.
