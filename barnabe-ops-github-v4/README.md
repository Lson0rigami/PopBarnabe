# 🧩 Barnabé Ops

> Sistema web interno para transformar POPs, rotinas e checklists operacionais em uma experiência simples de usar no tablet.

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)
![Status](https://img.shields.io/badge/status-em%20evolu%C3%A7%C3%A3o-6f42c1)

<p align="center">
  <img src="static/img/logo-barnabe.png" alt="Logo Barnabé" width="180">
</p>

## 💡 Sobre o projeto

O **Barnabé Ops** nasceu da observação de uma operação real de estoque e expedição. A primeira versão digitalizava POPs e a rotina semanal. Com o uso no tablet, o projeto evoluiu para registrar execução, responsáveis, horários, validações, histórico e indicadores.

Fluxo de evolução do produto:

```text
POP digital
   ↓
Rotina semanal
   ↓
Checklist no tablet
   ↓
Responsáveis e horários
   ↓
Validação e histórico
   ↓
Atividades complementares
   ↓
Painel operacional e visão individual
```

Esta pasta é uma **versão preparada para GitHub**. Dados de execução, banco SQLite, backups, segredos, caminhos pessoais do servidor e nomes reais de colaboradores não fazem parte do repositório.

> **Nota de privacidade:** alguns textos operacionais foram generalizados para demonstração pública. A instalação usada em produção deve manter seus dados e configurações fora do Git.

## ✨ Funcionalidades

- POPs digitais organizados por categoria;
- rotina semanal por dia;
- atividades com estados de execução;
- seleção de um ou mais responsáveis somente no momento da atividade;
- registro de início, conclusão e validação;
- validação por outra pessoa em atividades críticas;
- ação **Voltar etapa** com motivo e histórico;
- atividades complementares;
- pesos de esforço configuráveis no backend;
- destaque visual 🔥 para atividades de maior peso;
- distribuição de pontos somente entre perfis elegíveis;
- painel operacional com linha do tempo;
- painel individual com visão semanal/mensal;
- SQLite com migrações aditivas;
- backup do banco;
- cache-busting de CSS/JS para reduzir arquivos antigos em tablets.

## 🧱 Stack

- **Backend:** Python + Flask
- **Banco:** SQLite
- **Frontend:** HTML, CSS e JavaScript sem framework
- **Templates:** Jinja2
- **Deploy original:** PythonAnywhere

## 📁 Estrutura

```text
barnabe-ops-github-v4/
├── app.py
├── requirements.txt
├── data/
│   ├── config_operacional.py
│   ├── procedimentos.py
│   ├── referencias.py
│   └── rotinas.py
├── services/
│   ├── backup.py
│   └── storage.py
├── templates/
├── static/
│   ├── css/
│   ├── js/
│   └── img/
├── scripts/
├── instance/          # banco local ignorado pelo Git
├── backups/           # backups ignorados pelo Git
└── docs/
```

## 🚀 Rodando localmente

### Windows

```powershell
python -m venv venv
.\venv\Scripts\activate
python -m pip install -r requirements.txt
python app.py
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Abra:

```text
http://127.0.0.1:5000
```

O banco é criado automaticamente em:

```text
instance/barnabe_ops.sqlite3
```

## 🧪 Dados de demonstração

Para gerar um pequeno histórico fictício para testar o painel:

```bash
python scripts/seed_demo.py
```

O script usa apenas os perfis fictícios presentes nesta versão pública.

## ⚙️ Configuração operacional

As configurações que mudam com mais frequência ficam em:

```text
data/config_operacional.py
```

Lá é possível alterar:

- colaboradores;
- quem participa da soma de pontos;
- peso de cada atividade;
- tarefas que exigem validação;
- limites da aura visual;
- atividades complementares;
- agrupamentos usados no painel individual.

Exemplo:

```python
COLABORADORES = [
    {"id": "admin", "nome": "Administrador", "ativo": True, "conta_pontos": False},
    {"id": "colaborador-a", "nome": "Colaborador A", "ativo": True, "conta_pontos": True},
]
```

Os pesos representam **esforço/responsabilidade operacional**, não um ranking automático.

## 🔐 Segurança e dados

Este repositório não inclui banco real nem credenciais.

Antes de publicar uma instalação:

```text
BARNABE_OPS_SECRET = chave aleatória forte
BARNABE_OPS_PIN    = PIN interno opcional
```

Consulte [`SECURITY.md`](SECURITY.md) para as recomendações básicas.

## ☁️ PythonAnywhere

Existe um guia genérico em [`docs/DEPLOY_PYTHONANYWHERE.md`](docs/DEPLOY_PYTHONANYWHERE.md). O script não contém nome de usuário nem caminho pessoal fixo.

## 🧭 Decisões de produto

O projeto evita um ranking simples de funcionários. Os pontos funcionam como uma medida configurável de esforço e ajudam a entender a distribuição de trabalho, enquanto o painel mostra contexto como frequência de atividades, complementares, validações e participação por período.

A arquitetura e as principais decisões estão em [`docs/ARQUITETURA.md`](docs/ARQUITETURA.md).

## 📌 Status

Versão de portfólio baseada na **V4** do Barnabé Ops. O projeto continua em evolução conforme o uso operacional gera novas necessidades.
