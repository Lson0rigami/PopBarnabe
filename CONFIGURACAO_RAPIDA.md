# Configuração rápida

As regras operacionais mais fáceis de ajustar ficam em `data/config_operacional.py`.

## Colaboradores

```python
COLABORADORES = [
    {"id": "admin", "nome": "Administrador", "ativo": True, "conta_pontos": False},
    {"id": "colaborador-a", "nome": "Colaborador A", "ativo": True, "conta_pontos": True},
]
```

- `ativo=False`: remove a pessoa das novas seleções sem apagar histórico.
- `conta_pontos=False`: mantém participação e histórico, mas exclui a pessoa da soma individual.
- não altere um `id` depois que ele já tiver sido usado em uma instalação real.

## Pesos das atividades

Procure por `PONTOS_TAREFAS`. Cada ID possui um comentário com a atividade correspondente.

```python
"seg_rm_01": 6,  # Separar tabuleiros da rota da manhã.
```

Recalibrar uma atividade exige apenas alterar o número e reiniciar/recarregar a aplicação.

## Atividades complementares

Procure por `ATIVIDADES_COMPLEMENTARES`. Cada item possui:

- `id`;
- `titulo`;
- `descricao`;
- `pontos`;
- `validacao`;
- `dias`.

## Destaque visual

```python
DESTAQUE_PONTOS = {
    "aura": 8,
    "forte": 12,
}
```

## Validação obrigatória

Os IDs em `VALIDACAO_OBRIGATORIA` exigem uma segunda pessoa para concluir a validação.

## Perfil que não soma pontos

Nesta versão pública, `Administrador` usa `conta_pontos=False` apenas para demonstrar a regra. Em uma tarefa de 6 pontos executada por Administrador + Colaborador A, o Administrador registra participação com 0 e o Colaborador A recebe os 6 pontos elegíveis.

## Categorias do painel individual

`CATEGORIAS_RH` agrupa IDs equivalentes de dias diferentes para gerar leituras como:

```text
Separação de tabuleiros — 3x
```
