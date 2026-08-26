# Segurança

Esta versão pública foi preparada para não versionar banco, backups ou segredos.

## Recomendações mínimas de produção

1. Defina `BARNABE_OPS_SECRET` com uma chave aleatória forte.
2. Use `BARNABE_OPS_PIN` ou outra camada de autenticação se a aplicação estiver exposta à internet.
3. Nunca coloque `instance/barnabe_ops.sqlite3` no Git.
4. Nunca armazene PINs, senhas ou chaves diretamente em arquivos versionados.
5. Mantenha todas as operações SQL parametrizadas.
6. Valide no backend IDs de tarefas, colaboradores e transições de estado.
7. Faça backup consistente do SQLite antes de atualizações.
8. Em instalações maiores ou com alta concorrência, avalie migrar o banco para PostgreSQL/MySQL.

## Arquivos ignorados

O `.gitignore` cobre, entre outros:

- `.env`;
- `instance/*`;
- `*.sqlite3`;
- `backups/*`;
- ambientes virtuais.

## Divulgação responsável

Este projeto nasceu de uma operação real. Antes de publicar dados operacionais, nomes, fotos ou procedimentos completos, valide o que pode ser exposto publicamente.
