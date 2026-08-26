"""Rotinas operacionais padronizadas por dia.

Regra de escrita: começar por verbo no infinitivo e manter nomes semelhantes
para a mesma atividade em dias diferentes. Isso facilita leitura no tablet,
relatórios do RH e futuras comparações no histórico.
"""

DIAS_ORDEM = ["segunda", "terca", "quarta", "quinta", "sexta", "sabado"]

ROTINAS = {
    "segunda": {
        "titulo": "Segunda-feira",
        "observacao": "Dia forte de expedição, contagens e avarias do fim de semana.",
        "blocos": [
            {"titulo": "Início do dia", "tarefas": [
                {"id": "seg_in_01", "texto": "Retirar os insumos previamente separados para Produção e Cocção."},
                {"id": "seg_in_02", "texto": "Retirar as laranjas higienizadas para a produção de suco.", "pop_slug": "armazenamento-laranja"},
                {"id": "seg_in_03", "texto": "Realizar a contagem inicial da Câmara 1 — tabuleiros e empadas pet; comunicar divergências à Produção e à Gerência."},
            ]},
            {"titulo": "Alinhamento", "tarefas": [
                {"id": "seg_al_01", "texto": "Dividir as atribuições do dia entre a equipe."},
                {"id": "seg_al_02", "texto": "Definir os responsáveis pelas separações e pela rota da tarde."},
                {"id": "seg_al_03", "texto": "Organizar os horários de almoço da equipe."},
            ]},
            {"titulo": "Rota da manhã", "tarefas": [
                {"id": "seg_rm_01", "texto": "Separar os tabuleiros da rota da manhã — Loja A, Loja B e Loja C.", "pop_slug": "separacao-tabuleiros"},
                {"id": "seg_rm_02", "texto": "Separar as bebidas da rota da manhã.", "pop_slug": "separacao-bebidas"},
                {"id": "seg_rm_03", "texto": "Carregar e conferir a rota da manhã com o motorista."},
            ]},
            {"titulo": "Avarias", "tarefas": [
                {"id": "seg_av_01", "texto": "Processar as avarias retornadas das lojas no fim de semana.", "pop_slug": "avarias-lojas"},
            ]},
            {"titulo": "Rota da tarde", "tarefas": [
                {"id": "seg_rt_01", "texto": "Separar as bebidas e os itens extras da rota da tarde — suspiros, cafés e similares.", "pop_slug": "separacao-bebidas"},
                {"id": "seg_rt_02", "texto": "Realizar a contagem de bebidas, cereais e produtos refrigerados."},
                {"id": "seg_rt_03", "texto": "Separar os tabuleiros da rota da tarde.", "pop_slug": "separacao-tabuleiros"},
                {"id": "seg_rt_04", "texto": "Separar os sucos da rota da tarde.", "pop_slug": "separacao-sucos"},
                {"id": "seg_rt_05", "texto": "Carregar e conferir a rota da tarde com o motorista."},
                {"id": "seg_ro_01", "texto": "Acompanhar a rota da tarde e apoiar as entregas externas às lojas."},
            ]},
            {"titulo": "Quem ficar na fábrica", "tarefas": [
                {"id": "seg_ff_01", "texto": "Processar as avarias retornadas da rota da manhã.", "pop_slug": "avarias-lojas"},
                {"id": "seg_ff_02", "texto": "Separar e atender as transferências solicitadas pelos setores internos."},
                {"id": "seg_ff_03", "texto": "Realizar a contagem final da Câmara 1 — tabuleiros."},
                {"id": "seg_ff_04", "texto": "Organizar o setor, trancar os portões e deixar a chave no ADM."},
            ]},
        ],
    },
    "terca": {
        "titulo": "Terça-feira",
        "observacao": "Dia forte de compras, descartáveis, recebimentos e CEASA.",
        "blocos": [
            {"titulo": "Alinhamento", "tarefas": [
                {"id": "ter_al_01", "texto": "Definir o responsável pelas compras externas do dia."},
                {"id": "ter_al_02", "texto": "Dividir as atividades de avarias e apoio aos descartáveis."},
                {"id": "ter_al_03", "texto": "Definir o responsável principal pela separação de descartáveis."},
            ]},
            {"titulo": "Compras externas", "tarefas": [
                {"id": "ter_cp_01", "texto": "Acompanhar as compras externas do dia e apoiar a conferência dos itens adquiridos."},
            ]},
            {"titulo": "Avarias e descartáveis", "tarefas": [
                {"id": "ter_ad_01", "texto": "Processar as avarias retornadas das lojas na segunda-feira.", "pop_slug": "avarias-lojas"},
                {"id": "ter_ad_02", "texto": "Separar os pedidos de descartáveis de todas as lojas.", "pop_slug": "separacao-descartaveis"},
                {"id": "ter_ad_03", "texto": "Realizar a contagem de descartáveis, materiais de limpeza e materiais de escritório."},
            ]},
            {"titulo": "Recebimento CEASA", "tarefas": [
                {"id": "ter_ce_01", "texto": "Receber e conferir os itens da CEASA.", "pop_slug": "recebimento-ceasa"},
                {"id": "ter_ce_02", "texto": "Separar e armazenar os itens da CEASA conforme o destino indicado.", "pop_slug": "recebimento-ceasa"},
            ]},
            {"titulo": "Quem ficar na fábrica", "tarefas": [
                {"id": "ter_ff_01", "texto": "Separar e atender as transferências solicitadas pelos setores internos."},
                {"id": "ter_ff_02", "texto": "Organizar o setor, trancar os portões e deixar a chave no ADM."},
                {"id": "ter_ff_03", "texto": "Descarregar e organizar os produtos recebidos das compras."},
            ]},
        ],
    },
    "quarta": {
        "titulo": "Quarta-feira",
        "observacao": "Dia de expedição com tabuleiros, descartáveis e conferências de carga.",
        "blocos": [
            {"titulo": "Início do dia", "tarefas": [
                {"id": "qua_in_01", "texto": "Retirar os insumos previamente separados para Produção e Cocção."},
                {"id": "qua_in_02", "texto": "Realizar a contagem inicial da Câmara 1 — tabuleiros e empadas pet; comunicar divergências à Produção e à Gerência."},
            ]},
            {"titulo": "Alinhamento", "tarefas": [
                {"id": "qua_al_01", "texto": "Dividir as atribuições do dia e definir o responsável pela rota externa."},
            ]},
            {"titulo": "Rota da manhã", "tarefas": [
                {"id": "qua_rm_01", "texto": "Separar os tabuleiros e os itens extras solicitados para a rota da manhã.", "pop_slug": "separacao-tabuleiros"},
                {"id": "qua_rm_02", "texto": "Conferir os descartáveis da rota da manhã com o motorista.", "pop_slug": "separacao-descartaveis"},
                {"id": "qua_rm_03", "texto": "Carregar e conferir a rota da manhã com o motorista."},
            ]},
            {"titulo": "Após a carga", "tarefas": [
                {"id": "qua_ac_01", "texto": "Reorganizar o setor após a saída da rota da manhã."},
            ]},
            {"titulo": "Rota da tarde", "tarefas": [
                {"id": "qua_rt_01", "texto": "Separar os tabuleiros da rota da tarde.", "pop_slug": "separacao-tabuleiros"},
                {"id": "qua_rt_02", "texto": "Conferir os descartáveis da rota da tarde com o motorista."},
                {"id": "qua_rt_03", "texto": "Conferir os tabuleiros da rota da tarde com o motorista."},
                {"id": "qua_ro_01", "texto": "Acompanhar a rota do dia e apoiar as entregas externas às lojas."},
            ]},
            {"titulo": "Quem ficar na fábrica", "tarefas": [
                {"id": "qua_ff_01", "texto": "Processar as avarias retornadas da rota da manhã.", "pop_slug": "avarias-lojas"},
                {"id": "qua_ff_02", "texto": "Separar e atender as transferências solicitadas pelos setores internos."},
                {"id": "qua_ff_03", "texto": "Realizar a contagem final da Câmara 1 — tabuleiros."},
                {"id": "qua_ff_04", "texto": "Organizar o setor, trancar os portões e deixar a chave no ADM."},
            ]},
        ],
    },
    "quinta": {
        "titulo": "Quinta-feira",
        "observacao": "Dia dedicado a avarias, limpeza, organização, PVP e validade, sem saída de caminhão.",
        "blocos": [
            {"titulo": "Início do dia", "tarefas": [
                {"id": "qui_in_01", "texto": "Retirar os insumos previamente separados para Produção e Cocção."},
                {"id": "qui_in_02", "texto": "Realizar a contagem inicial da Câmara 1 — tabuleiros e empadas pet; comunicar divergências à Produção e à Gerência."},
            ]},
            {"titulo": "Alinhamento", "tarefas": [
                {"id": "qui_al_01", "texto": "Dividir as atividades de avarias, limpeza e organização entre a equipe."},
            ]},
            {"titulo": "Avarias e limpeza", "tarefas": [
                {"id": "qui_av_01", "texto": "Processar as avarias retornadas da carga de quarta-feira.", "pop_slug": "avarias-lojas"},
                {"id": "qui_av_02", "texto": "Limpar e lavar as docas."},
                {"id": "qui_av_03", "texto": "Limpar e lavar as três câmaras frias."},
                {"id": "qui_av_04", "texto": "Limpar os almoxarifados e as áreas de matéria-prima seca."},
            ]},
            {"titulo": "Organização e validade", "tarefas": [
                {"id": "qui_or_01", "texto": "Realizar a organização geral dos setores de estoque."},
                {"id": "qui_or_02", "texto": "Conferir PVP e validade dos produtos das câmaras e da matéria-prima seca."},
                {"id": "qui_or_03", "texto": "Sinalizar produtos próximos do vencimento e comunicar o responsável para definição do destino."},
            ]},
            {"titulo": "Fechamento", "tarefas": [
                {"id": "qui_fe_01", "texto": "Separar e atender as transferências solicitadas pelos setores internos."},
                {"id": "qui_fe_02", "texto": "Realizar a contagem final da Câmara 1 — tabuleiros."},
            ]},
        ],
    },
    "sexta": {
        "titulo": "Sexta-feira",
        "observacao": "Dia forte de expedição, semelhante à segunda-feira.",
        "blocos": [
            {"titulo": "Início do dia", "tarefas": [
                {"id": "sex_in_01", "texto": "Retirar os insumos previamente separados para Produção e Cocção."},
                {"id": "sex_in_02", "texto": "Retirar as laranjas higienizadas para a produção de suco.", "pop_slug": "armazenamento-laranja"},
                {"id": "sex_in_03", "texto": "Realizar a contagem inicial da Câmara 1 — tabuleiros e empadas pet; comunicar divergências à Produção e à Gerência."},
            ]},
            {"titulo": "Alinhamento", "tarefas": [
                {"id": "sex_al_01", "texto": "Dividir as atribuições do dia, definir a rota externa e organizar os horários de almoço."},
            ]},
            {"titulo": "Rota da manhã", "tarefas": [
                {"id": "sex_rm_01", "texto": "Separar os tabuleiros, as bebidas e os itens solicitados para a rota da manhã.", "pop_slug": "separacao-tabuleiros"},
                {"id": "sex_rm_02", "texto": "Carregar e conferir a rota da manhã com o motorista."},
            ]},
            {"titulo": "Avarias", "tarefas": [
                {"id": "sex_av_01", "texto": "Processar as avarias retornadas das lojas.", "pop_slug": "avarias-lojas"},
            ]},
            {"titulo": "Rota da tarde", "tarefas": [
                {"id": "sex_rt_01", "texto": "Separar as bebidas e os itens extras da rota da tarde — suspiros, cafés e similares.", "pop_slug": "separacao-bebidas"},
                {"id": "sex_rt_02", "texto": "Separar os tabuleiros da rota da tarde.", "pop_slug": "separacao-tabuleiros"},
                {"id": "sex_rt_03", "texto": "Separar os sucos da rota da tarde.", "pop_slug": "separacao-sucos"},
                {"id": "sex_rt_04", "texto": "Carregar e conferir a rota da tarde com o motorista."},
                {"id": "sex_ro_01", "texto": "Acompanhar a rota da tarde e apoiar as entregas externas às lojas."},
            ]},
            {"titulo": "Quem ficar na fábrica", "tarefas": [
                {"id": "sex_ff_01", "texto": "Processar as avarias retornadas da rota da manhã.", "pop_slug": "avarias-lojas"},
                {"id": "sex_ff_02", "texto": "Separar e atender as transferências solicitadas pelos setores internos."},
                {"id": "sex_ff_03", "texto": "Realizar a contagem final da Câmara 1 — tabuleiros."},
                {"id": "sex_ff_04", "texto": "Organizar o setor, trancar os portões e deixar a chave no ADM."},
            ]},
        ],
    },
    "sabado": {
        "titulo": "Sábado",
        "observacao": "Dia com equipe reduzida e foco em pedidos, rotas, contagens e fechamento.",
        "blocos": [
            {"titulo": "Alinhamento", "tarefas": [
                {"id": "sab_al_01", "texto": "Dividir as atribuições entre as pessoas da escala."},
                {"id": "sab_al_02", "texto": "Definir os responsáveis por pedidos, romaneio e separações."},
            ]},
            {"titulo": "Pedidos e avarias", "tarefas": [
                {"id": "sab_pa_01", "texto": "Emitir e consultar os pedidos/romaneios do dia."},
                {"id": "sab_pa_02", "texto": "Processar as avarias e limpar a doca.", "pop_slug": "avarias-lojas"},
            ]},
            {"titulo": "Rota da manhã", "tarefas": [
                {"id": "sab_rm_01", "texto": "Separar os tabuleiros da rota da manhã.", "pop_slug": "separacao-tabuleiros"},
                {"id": "sab_rm_02", "texto": "Ajustar o romaneio e conferir a rota da manhã com o motorista."},
                {"id": "sab_rm_03", "texto": "Carregar e conferir a rota da manhã com o motorista."},
            ]},
            {"titulo": "Rota da tarde", "tarefas": [
                {"id": "sab_rt_01", "texto": "Separar os tabuleiros da rota da tarde.", "pop_slug": "separacao-tabuleiros"},
                {"id": "sab_rt_02", "texto": "Ajustar o romaneio e preparar a conferência da rota da tarde."},
            ]},
            {"titulo": "Contagens e fechamento", "tarefas": [
                {"id": "sab_cf_01", "texto": "Realizar a contagem de tabuleiros após as separações para controle."},
                {"id": "sab_cf_02", "texto": "Realizar a contagem de bebidas."},
                {"id": "sab_cf_03", "texto": "Organizar o setor, carregar e conferir a rota final, trancar os portões e deixar a chave no ADM."},
            ]},
        ],
    },
}
