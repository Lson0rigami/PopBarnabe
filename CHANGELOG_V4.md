# Barnabé Ops 4.0 — resumo da atualização

## Operação
- Mensagens das rotinas padronizadas entre os dias.
- Nova atividade explícita de rota externa (15 pontos) em segunda, quarta e sexta.
- Nova atividade de compras externas (12 pontos) na terça para compensar o tempo fora da operação interna.
- Bloqueio removido da interface para simplificar o fluxo.
- Voltar etapa exige responsável + motivo e preserva o histórico.

## Pontuação
- Segunda-feira revisada foi usada como referência de balanceamento para os demais dias.
- Pontuação continua configurável em `data/config_operacional.py`.
- O perfil Administrador demonstra a opção `conta_pontos=False`, ficando fora da soma individual.
- Em atividades compartilhadas, os pontos são divididos apenas entre participantes elegíveis.
- Nova coluna `points_distribution_json` é adicionada automaticamente ao banco existente.

## Complementares
- Separar e embalar mais de 500 caixas e bases P/G — 7 pts.
- Trocar o lixo de todos os setores do estoque — 2 pts.
- Separar mais de 15 pacotes de panfletos com 100 unidades — 5 pts.

## Experiência no tablet
- Atividades a partir de 8 pontos recebem aura/🔥.
- Atividades a partir de 12 pontos recebem destaque mais forte.
- Histórico individual de cada atividade disponível no modal.
- CSS e JS recebem `?v=4.0.0` para reduzir problemas de cache após atualização.

## Painel RH
- Visão individual por semana ou mês.
- Atividades concluídas, pontos, complementares, validações e dias com atividade.
- Frequência agrupada por tipo, por exemplo `Separação de tabuleiros — 3x`.
- Histórico recente e distribuição das atividades por dia.
- Sem ranking automático; os números são apresentados como contexto operacional.

## Dados
- O atualizador preserva `instance/`, `backups/` e `venv/`.
- Antes da atualização, cria snapshot do SQLite e backup do código anterior.
