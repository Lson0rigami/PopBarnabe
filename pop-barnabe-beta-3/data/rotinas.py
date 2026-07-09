DIAS_ORDEM = ["segunda", "terca", "quarta", "quinta", "sexta", "sabado"]

ROTINAS = {
    "segunda": {
        "titulo": "Segunda-feira",
        "observacao": "Dia forte de rota, contagens e avarias do fim de semana.",
        "blocos": [
            {"titulo": "Início do dia", "tarefas": [
                {"id": "seg_in_01", "texto": "Retirar da Câmara 1 e demais locais os insumos separados na sexta-feira para produção e cocção."},
                {"id": "seg_in_02", "texto": "Retirar as caixas de laranja higienizadas para a produção de suco.", "pop_slug": "armazenamento-laranja"},
                {"id": "seg_in_03", "texto": "Realizar contagem da Câmara 1 — Tabuleiros e empadas pet; se houver observação, avisar Produção e Gerência."}
            ]},
            {"titulo": "Alinhamento", "tarefas": [
                {"id": "seg_al_01", "texto": "Dividir as atribuições do dia de forma justa."},
                {"id": "seg_al_02", "texto": "Definir quem separa bebidas, quem separa tabuleiros e quem sai para a rota da tarde."},
                {"id": "seg_al_03", "texto": "Dividir os horários de almoço: 11:00, 11:30 e 12:00."}
            ]},
            {"titulo": "Rota da manhã", "tarefas": [
                {"id": "seg_rm_01", "texto": "Separar tabuleiros da manhã: Manaíra, Uniesp e Tambiá.", "pop_slug": "separacao-tabuleiros"},
                {"id": "seg_rm_02", "texto": "Separar bebidas da manhã.", "pop_slug": "separacao-bebidas"},
                {"id": "seg_rm_03", "texto": "Carregar o caminhão com os produtos e itens das lojas da manhã."}
            ]},
            {"titulo": "Avarias", "tarefas": [
                {"id": "seg_av_01", "texto": "Fazer as avarias que voltaram das lojas do fim de semana.", "pop_slug": "avarias-lojas"}
            ]},
            {"titulo": "Rota da tarde", "tarefas": [
                {"id": "seg_rt_01", "texto": "Separar bebidas da tarde e itens extras fora da câmara fria (suspiros, cafés etc).", "pop_slug": "separacao-bebidas"},
                {"id": "seg_rt_02", "texto": "Realizar contagem de bebidas, cereais e frios."},
                {"id": "seg_rt_03", "texto": "Iniciar separação de tabuleiros da tarde.", "pop_slug": "separacao-tabuleiros"},
                {"id": "seg_rt_04", "texto": "Separar sucos para as lojas.", "pop_slug": "separacao-sucos"},
                {"id": "seg_rt_05", "texto": "Carregar o caminhão com tabuleiros, bebidas, sucos, suspiros, cafés e demais itens."}
            ]},
            {"titulo": "Quem ficar na fábrica", "tarefas": [
                {"id": "seg_ff_01", "texto": "Realizar avarias que voltaram da loja da manhã.", "pop_slug": "avarias-lojas"},
                {"id": "seg_ff_02", "texto": "Fazer a lista de transferência dos setores internos."},
                {"id": "seg_ff_03", "texto": "Realizar a contagem final do dia da Câmara 1 — Tabuleiros."},
                {"id": "seg_ff_04", "texto": "Fazer organização diária dos setores, trancar portões e deixar a chave no ADM."}
            ]}
        ]
    },
    "terca": {
        "titulo": "Terça-feira",
        "observacao": "Dia forte de compras, descartáveis e recebimento CEASA.",
        "blocos": [
            {"titulo": "Alinhamento", "tarefas": [
                {"id": "ter_al_01", "texto": "Definir quem vai para as compras."},
                {"id": "ter_al_02", "texto": "Definir quem faz avaria primeiro e depois ajuda nos descartáveis."},
                {"id": "ter_al_03", "texto": "Definir quem vai direto para os descartáveis."}
            ]},
            {"titulo": "Avarias e descartáveis", "tarefas": [
                {"id": "ter_ad_01", "texto": "Realizar as avarias que vieram das lojas na segunda-feira.", "pop_slug": "avarias-lojas"},
                {"id": "ter_ad_02", "texto": "Pegar pedidos de descartáveis de todas as lojas e separar.", "pop_slug": "separacao-descartaveis"},
                {"id": "ter_ad_03", "texto": "Após separar, realizar a contagem de descartáveis, material de limpeza e material de escritório."}
            ]},
            {"titulo": "Recebimento CEASA", "tarefas": [
                {"id": "ter_ce_01", "texto": "Receber os itens da CEASA."},
                {"id": "ter_ce_02", "texto": "Separar e guardar itens do refeitório, Câmara 2 e matéria-prima seca conforme a nota."}
            ]},
            {"titulo": "Quem ficar na fábrica", "tarefas": [
                {"id": "ter_ff_01", "texto": "Fazer a lista de transferência dos setores internos."},
                {"id": "ter_ff_02", "texto": "Fazer a organização diária, trancar portões e deixar a chave no ADM."},
                {"id": "ter_ff_03", "texto": "Aguardar o caminhão das compras e descarregar."}
            ]}
        ]
    },
    "quarta": {
        "titulo": "Quarta-feira",
        "observacao": "Rota com tabuleiros e descartáveis.",
        "blocos": [
            {"titulo": "Início do dia", "tarefas": [
                {"id": "qua_in_01", "texto": "Retirar os insumos separados na terça-feira para produção e cocção."},
                {"id": "qua_in_02", "texto": "Realizar contagem da Câmara 1 — Tabuleiros e empadas pet; se houver observação, avisar Produção e Gerência."}
            ]},
            {"titulo": "Alinhamento", "tarefas": [
                {"id": "qua_al_01", "texto": "Definir as atribuições do dia e quem vai para as entregas."}
            ]},
            {"titulo": "Rota da manhã", "tarefas": [
                {"id": "qua_rm_01", "texto": "Separar os tabuleiros da manhã e também suspiros/cafés solicitados.", "pop_slug": "separacao-tabuleiros"},
                {"id": "qua_rm_02", "texto": "Conferir junto ao motorista os descartáveis separados na terça-feira.", "pop_slug": "separacao-descartaveis"},
                {"id": "qua_rm_03", "texto": "Carregar o caminhão com tabuleiros, descartáveis e demais itens."}
            ]},
            {"titulo": "Após a carga", "tarefas": [
                {"id": "qua_ac_01", "texto": "Realizar organização diária dos setores."}
            ]},
            {"titulo": "Rota da tarde", "tarefas": [
                {"id": "qua_rt_01", "texto": "Separar os tabuleiros da tarde.", "pop_slug": "separacao-tabuleiros"},
                {"id": "qua_rt_02", "texto": "Conferir junto ao motorista a carga de descartáveis da tarde."},
                {"id": "qua_rt_03", "texto": "Conferir tabuleiros com o motorista durante a carga."}
            ]},
            {"titulo": "Quem ficar na fábrica", "tarefas": [
                {"id": "qua_ff_01", "texto": "Realizar avarias que voltaram da loja da manhã.", "pop_slug": "avarias-lojas"},
                {"id": "qua_ff_02", "texto": "Fazer a lista de transferência dos setores internos."},
                {"id": "qua_ff_03", "texto": "Realizar a contagem final da Câmara 1 — Tabuleiros."},
                {"id": "qua_ff_04", "texto": "Fazer organização diária, trancar portões e deixar a chave no ADM."}
            ]}
        ]
    },
    "quinta": {
        "titulo": "Quinta-feira",
        "observacao": "Dia exclusivo para limpeza e organização, sem saída de caminhão.",
        "blocos": [
            {"titulo": "Início do dia", "tarefas": [
                {"id": "qui_in_01", "texto": "Retirar os insumos separados na quarta-feira para produção e cocção."},
                {"id": "qui_in_02", "texto": "Realizar contagem da Câmara 1 — Tabuleiros e empadas pet; se houver observação, avisar Produção e Gerência."}
            ]},
            {"titulo": "Alinhamento", "tarefas": [
                {"id": "qui_al_01", "texto": "Definir quem faz avarias primeiro e quem já inicia a limpeza."}
            ]},
            {"titulo": "Avarias e limpeza", "tarefas": [
                {"id": "qui_av_01", "texto": "Realizar as avarias que vieram da carga de quarta-feira.", "pop_slug": "avarias-lojas"},
                {"id": "qui_av_02", "texto": "Fazer limpeza e lavagem das docas."},
                {"id": "qui_av_03", "texto": "Fazer limpeza e lavagem das 3 câmaras frias."},
                {"id": "qui_av_04", "texto": "Limpar e, se necessário, lavar almoxarifados e áreas de secos."}
            ]},
            {"titulo": "Organização e validade", "tarefas": [
                {"id": "qui_or_01", "texto": "Fazer organização geral dos setores."},
                {"id": "qui_or_02", "texto": "Conferir datas dos produtos das câmaras e da matéria-prima seca."},
                {"id": "qui_or_03", "texto": "Tomar medidas rápidas para itens perto do vencimento."}
            ]},
            {"titulo": "Fechamento", "tarefas": [
                {"id": "qui_fe_01", "texto": "Fazer lista de transferência dos setores internos."},
                {"id": "qui_fe_02", "texto": "Realizar a contagem final da Câmara 1 — Tabuleiros."}
            ]}
        ]
    },
    "sexta": {
        "titulo": "Sexta-feira",
        "observacao": "Rotina parecida com a segunda-feira.",
        "blocos": [
            {"titulo": "Início do dia", "tarefas": [
                {"id": "sex_in_01", "texto": "Retirar da câmara fria os insumos separados na quinta-feira para produção e cocção."},
                {"id": "sex_in_02", "texto": "Retirar as caixas de laranja higienizadas para a produção de suco.", "pop_slug": "armazenamento-laranja"},
                {"id": "sex_in_03", "texto": "Realizar contagem da Câmara 1 — Tabuleiros e empadas pet; se houver observação, avisar Produção e Gerência."}
            ]},
            {"titulo": "Alinhamento", "tarefas": [
                {"id": "sex_al_01", "texto": "Dividir atribuições, rota da tarde e horários de almoço."}
            ]},
            {"titulo": "Rota da manhã", "tarefas": [
                {"id": "sex_rm_01", "texto": "Separar tabuleiros e bebidas da manhã.", "pop_slug": "separacao-tabuleiros"},
                {"id": "sex_rm_02", "texto": "Carregar o caminhão com os produtos e itens das lojas da manhã."}
            ]},
            {"titulo": "Avarias", "tarefas": [
                {"id": "sex_av_01", "texto": "Fazer avarias que voltaram das lojas.", "pop_slug": "avarias-lojas"}
            ]},
            {"titulo": "Rota da tarde", "tarefas": [
                {"id": "sex_rt_01", "texto": "Separar bebidas da tarde e itens extras (suspiros, cafés etc).", "pop_slug": "separacao-bebidas"},
                {"id": "sex_rt_02", "texto": "Iniciar separação dos tabuleiros da tarde.", "pop_slug": "separacao-tabuleiros"},
                {"id": "sex_rt_03", "texto": "Separar sucos da Câmara 1.", "pop_slug": "separacao-sucos"},
                {"id": "sex_rt_04", "texto": "Carregar o caminhão com tabuleiros, bebidas, sucos e demais itens."}
            ]},
            {"titulo": "Quem ficar na fábrica", "tarefas": [
                {"id": "sex_ff_01", "texto": "Realizar avarias da loja da manhã.", "pop_slug": "avarias-lojas"},
                {"id": "sex_ff_02", "texto": "Fazer lista de transferência dos setores internos."},
                {"id": "sex_ff_03", "texto": "Realizar a contagem final da Câmara 1 — Tabuleiros."},
                {"id": "sex_ff_04", "texto": "Fazer organização diária, trancar portões e deixar a chave no ADM."}
            ]}
        ]
    },
    "sabado": {
        "titulo": "Sábado",
        "observacao": "Dia mais tranquilo, normalmente com 2 pessoas em escala.",
        "blocos": [
            {"titulo": "Alinhamento", "tarefas": [
                {"id": "sab_al_01", "texto": "Definir como as tarefas serão divididas entre as 2 pessoas do dia."},
                {"id": "sab_al_02", "texto": "Definir quem puxa pedidos/romaneio e quem foca na separação."}
            ]},
            {"titulo": "Pedidos e avarias", "tarefas": [
                {"id": "sab_pa_01", "texto": "Puxar os pedidos do sistema."},
                {"id": "sab_pa_02", "texto": "Fazer avaria e limpeza da doca.", "pop_slug": "avarias-lojas"}
            ]},
            {"titulo": "Rota da manhã", "tarefas": [
                {"id": "sab_rm_01", "texto": "Separar tabuleiros da manhã.", "pop_slug": "separacao-tabuleiros"},
                {"id": "sab_rm_02", "texto": "Ajustar romaneio e conferir junto ao motorista."},
                {"id": "sab_rm_03", "texto": "Carregar o caminhão."}
            ]},
            {"titulo": "Rota da tarde", "tarefas": [
                {"id": "sab_rt_01", "texto": "Separar tabuleiros da tarde.", "pop_slug": "separacao-tabuleiros"},
                {"id": "sab_rt_02", "texto": "Ajustar romaneio e esperar o motorista."}
            ]},
            {"titulo": "Contagens e fechamento", "tarefas": [
                {"id": "sab_cf_01", "texto": "Realizar a contagem dos tabuleiros após a separação para controle."},
                {"id": "sab_cf_02", "texto": "Realizar a contagem das bebidas."},
                {"id": "sab_cf_03", "texto": "Fazer organização diária, carregar o caminhão após conferência com o motorista, trancar portões e deixar a chave no ADM."}
            ]}
        ]
    }
}
