# Arquitetura

## Visão geral

```text
Navegador / Tablet
       │
       │ HTTP + JSON
       ▼
   Flask / app.py
       │
       ├── data/       regras e conteúdo operacional
       ├── services/   persistência e backup
       ├── templates/  Jinja2
       └── static/     CSS + JavaScript
       │
       ▼
     SQLite
```

## Princípios usados

### Configuração fora do front-end
Pesos, colaboradores, validações e atividades complementares ficam em `data/config_operacional.py`. Isso permite recalibrar o processo sem alterar HTML ou JavaScript.

### Estado no servidor
A aplicação não depende do `localStorage` para o estado operacional. O SQLite centraliza atividades, responsáveis, horários e histórico, permitindo que mais de um dispositivo enxergue a mesma operação.

### Histórico em eventos
Além do estado atual de uma tarefa, `activity_events` guarda ações relevantes. Isso permite reabrir uma atividade sem apagar o que aconteceu anteriormente.

### Migrações aditivas
`services/storage.py` cria tabelas e adiciona colunas quando necessário sem apagar os registros existentes.

### Pontuação contextual
Pontuação não é enviada pelo navegador. O backend consulta a configuração da atividade e calcula a distribuição somente entre participantes elegíveis.

### UX para tablet
O JavaScript prioriza alvos de toque grandes, feedback visual, modal de responsáveis, estados claros e animações curtas para tornar o uso operacional mais agradável.
