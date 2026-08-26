"""Configurações operacionais fáceis de ajustar sem alterar o front-end.

Este arquivo concentra nomes, pontuação, validações, destaques visuais e
atividades complementares. A ideia é permitir que futuras otimizações do
processo alterem o balanceamento sem exigir mudanças no HTML/JavaScript.
"""

APP_VERSION = "4.0.0"
APP_TIMEZONE = "America/Fortaleza"

# ---------------------------------------------------------------------------
# COLABORADORES
# ---------------------------------------------------------------------------
# - `id` deve permanecer único e sem acentos porque é uma identificação interna.
# - `ativo=False` remove a pessoa das novas seleções sem apagar o histórico.
# - `conta_pontos=False` mantém todas as atividades/histórico, porém essa pessoa
#   não participa da soma individual de pontos. Na versão pública, o perfil Administrador demonstra como excluir um perfil da soma de pontos.
COLABORADORES = [
    {"id": "admin", "nome": "Administrador", "ativo": True, "conta_pontos": False},
    {"id": "colaborador-a", "nome": "Colaborador A", "ativo": True, "conta_pontos": True},
    {"id": "colaborador-b", "nome": "Colaborador B", "ativo": True, "conta_pontos": True},
    {"id": "colaborador-c", "nome": "Colaborador C", "ativo": True, "conta_pontos": True},
]

# ---------------------------------------------------------------------------
# PONTUAÇÃO DAS ATIVIDADES PRINCIPAIS
# ---------------------------------------------------------------------------
# Referência usada no balanceamento:
#   0 pt  -> organização/alinhamento administrativo sem execução operacional;
#   1-3   -> ação curta ou simples;
#   4-6   -> atividade operacional moderada;
#   7-10  -> atividade longa/pesada ou com responsabilidade elevada;
#   12-15 -> atividade externa/longa que retira a pessoa das tarefas internas.
#
# IMPORTANTE: pontos representam esforço/responsabilidade operacional, NÃO um
# ranking automático de funcionário. Para recalibrar uma atividade, altere só
# o número ao lado do ID e faça Reload no site.
PONTOS_TAREFAS = {
    # ============================ SEGUNDA-FEIRA ============================
    "seg_in_01": 2,   # Retirar insumos previamente separados para Produção e Cocção.
    "seg_in_02": 1,   # Retirar laranjas higienizadas para produção de suco.
    "seg_in_03": 2,   # Contagem inicial da Câmara 1 (tabuleiros e empadas pet).
    "seg_al_01": 0,   # Dividir as atribuições da equipe.
    "seg_al_02": 0,   # Definir responsáveis por separações e rota.
    "seg_al_03": 0,   # Organizar horários de almoço.
    "seg_rm_01": 6,   # Separar tabuleiros da rota da manhã.
    "seg_rm_02": 6,   # Separar bebidas da rota da manhã.
    "seg_rm_03": 9,   # Carregar a rota da manhã.
    "seg_av_01": 5,   # Processar avarias do fim de semana.
    "seg_rt_01": 4,   # Separar bebidas e itens extras da rota da tarde.
    "seg_rt_02": 8,   # Contar bebidas, cereais e frios.
    "seg_rt_03": 6,   # Separar tabuleiros da rota da tarde.
    "seg_rt_04": 3,   # Separar sucos para as lojas.
    "seg_rt_05": 9,   # Carregar a rota da tarde.
    "seg_ro_01": 15,  # Acompanhar a rota da tarde e apoiar as entregas externas.
    "seg_ff_01": 3,   # Processar avarias retornadas da rota da manhã.
    "seg_ff_02": 6,   # Separar/atender transferências internas.
    "seg_ff_03": 2,   # Contagem final de tabuleiros.
    "seg_ff_04": 8,   # Organização e fechamento do setor.

    # ============================= TERÇA-FEIRA =============================
    "ter_al_01": 0,   # Definir responsável pelas compras externas.
    "ter_al_02": 0,   # Dividir avarias e apoio aos descartáveis.
    "ter_al_03": 0,   # Definir responsável pelos descartáveis.
    "ter_cp_01": 12,  # Acompanhar compras externas do dia.
    "ter_ad_01": 5,   # Processar avarias da segunda-feira.
    "ter_ad_02": 8,   # Separar pedidos de descartáveis das lojas.
    "ter_ad_03": 8,   # Contar descartáveis, limpeza e escritório.
    "ter_ce_01": 9,   # Receber e conferir CEASA.
    "ter_ce_02": 6,   # Separar/armazenar itens da CEASA conforme destino.
    "ter_ff_01": 6,   # Separar/atender transferências internas.
    "ter_ff_02": 8,   # Organização e fechamento do setor.
    "ter_ff_03": 9,   # Descarregar e organizar compras recebidas.

    # ============================ QUARTA-FEIRA =============================
    "qua_in_01": 2,   # Retirar insumos previamente separados para Produção e Cocção.
    "qua_in_02": 2,   # Contagem inicial da Câmara 1.
    "qua_al_01": 0,   # Dividir atribuições e definir responsável pela rota.
    "qua_rm_01": 6,   # Separar tabuleiros e itens solicitados da rota da manhã.
    "qua_rm_02": 4,   # Conferir descartáveis da rota da manhã com o motorista.
    "qua_rm_03": 9,   # Carregar a rota da manhã.
    "qua_ac_01": 4,   # Reorganizar o setor após a saída da carga.
    "qua_rt_01": 6,   # Separar tabuleiros da rota da tarde.
    "qua_rt_02": 4,   # Conferir descartáveis da rota da tarde.
    "qua_rt_03": 4,   # Conferir tabuleiros da rota da tarde com o motorista.
    "qua_ro_01": 15,  # Acompanhar a rota/entregas externas do dia.
    "qua_ff_01": 3,   # Processar avarias retornadas da rota da manhã.
    "qua_ff_02": 6,   # Separar/atender transferências internas.
    "qua_ff_03": 2,   # Contagem final de tabuleiros.
    "qua_ff_04": 8,   # Organização e fechamento do setor.

    # ============================ QUINTA-FEIRA =============================
    "qui_in_01": 2,   # Retirar insumos previamente separados para Produção e Cocção.
    "qui_in_02": 2,   # Contagem inicial da Câmara 1.
    "qui_al_01": 0,   # Dividir avarias, limpeza e organização.
    "qui_av_01": 5,   # Processar avarias da quarta-feira.
    "qui_av_02": 7,   # Limpar e lavar as docas.
    "qui_av_03": 10,  # Limpar e lavar as três câmaras frias.
    "qui_av_04": 7,   # Limpar almoxarifados e áreas secas.
    "qui_or_01": 8,   # Organização geral do estoque.
    "qui_or_02": 8,   # Conferência ampla de PVP/validade.
    "qui_or_03": 4,   # Sinalizar e encaminhar itens próximos do vencimento.
    "qui_fe_01": 6,   # Separar/atender transferências internas.
    "qui_fe_02": 2,   # Contagem final de tabuleiros.

    # ============================= SEXTA-FEIRA =============================
    "sex_in_01": 2,   # Retirar insumos previamente separados para Produção e Cocção.
    "sex_in_02": 1,   # Retirar laranjas higienizadas para produção de suco.
    "sex_in_03": 2,   # Contagem inicial da Câmara 1.
    "sex_al_01": 0,   # Dividir atribuições, rota e horários de almoço.
    "sex_rm_01": 6,   # Separar itens principais da rota da manhã.
    "sex_rm_02": 9,   # Carregar a rota da manhã.
    "sex_av_01": 5,   # Processar avarias.
    "sex_rt_01": 4,   # Separar bebidas e itens extras da rota da tarde.
    "sex_rt_02": 6,   # Separar tabuleiros da rota da tarde.
    "sex_rt_03": 3,   # Separar sucos para a rota da tarde.
    "sex_rt_04": 9,   # Carregar a rota da tarde.
    "sex_ro_01": 15,  # Acompanhar a rota da tarde e apoiar as entregas externas.
    "sex_ff_01": 3,   # Processar avarias retornadas da rota da manhã.
    "sex_ff_02": 6,   # Separar/atender transferências internas.
    "sex_ff_03": 2,   # Contagem final de tabuleiros.
    "sex_ff_04": 8,   # Organização e fechamento do setor.

    # ============================== SÁBADO ==================================
    "sab_al_01": 0,   # Dividir as atribuições entre as pessoas da escala.
    "sab_al_02": 0,   # Definir pedidos/romaneio e separações.
    "sab_pa_01": 2,   # Emitir/consultar pedidos e romaneios.
    "sab_pa_02": 6,   # Processar avarias e limpar a doca.
    "sab_rm_01": 6,   # Separar tabuleiros da rota da manhã.
    "sab_rm_02": 4,   # Ajustar romaneio e conferir a rota da manhã.
    "sab_rm_03": 9,   # Carregar a rota da manhã.
    "sab_rt_01": 6,   # Separar tabuleiros da rota da tarde.
    "sab_rt_02": 4,   # Ajustar romaneio e preparar conferência da tarde.
    "sab_cf_01": 2,   # Contagem de tabuleiros para controle.
    "sab_cf_02": 3,   # Contagem de bebidas.
    "sab_cf_03": 10,  # Organização, carga final e fechamento do setor.
}

# ---------------------------------------------------------------------------
# DESTAQUE VISUAL DOS PONTOS
# ---------------------------------------------------------------------------
# O front-end lê estes limites para deixar atividades de maior esforço mais
# atraentes visualmente sem transformar a tela em ranking.
DESTAQUE_PONTOS = {
    "aura": 8,   # brilho amarelo/laranja e selo 🔥
    "forte": 12, # brilho mais intenso para atividade longa/externa
}

# IDs que exigem conferência por OUTRA pessoa antes de pontuar como concluídos.
# Mantenha apenas tarefas em que uma segunda checagem agrega segurança real.
VALIDACAO_OBRIGATORIA = [
    "seg_rm_03", "seg_rt_05", "seg_ff_03",
    "ter_ce_01",
    "qua_rm_03", "qua_ff_03",
    "qui_fe_02",
    "sex_rm_02", "sex_rt_04", "sex_ff_03",
    "sab_rm_03", "sab_cf_03",
]

# ---------------------------------------------------------------------------
# ATIVIDADES COMPLEMENTARES
# ---------------------------------------------------------------------------
# São oportunidades extras para quando a pessoa encerrou a atividade principal.
# Para adicionar uma nova, copie um bloco e altere id/título/descrição/pontos.
ATIVIDADES_COMPLEMENTARES = [
    {
        "id": "extra_pvp_secos",
        "titulo": "Revisar PVP da matéria-prima seca",
        "descricao": "Conferir organização por validade e sinalizar itens que precisam de atenção.",
        "pontos": 3,
        "validacao": False,
        "dias": ["segunda", "terca", "quarta", "quinta", "sexta", "sabado"],
    },
    {
        "id": "extra_etiquetas",
        "titulo": "Conferir etiquetas e identificação",
        "descricao": "Verificar presença, legibilidade, nome e validade nas áreas permitidas.",
        "pontos": 3,
        "validacao": False,
        "dias": ["segunda", "terca", "quarta", "quinta", "sexta", "sabado"],
    },
    {
        "id": "extra_organizacao_descartaveis",
        "titulo": "Organizar a área de descartáveis",
        "descricao": "Reorganizar itens e deixar a área pronta para novas separações.",
        "pontos": 2,
        "validacao": False,
        "dias": ["segunda", "terca", "quarta", "quinta", "sexta", "sabado"],
    },
    {
        "id": "extra_reciclaveis",
        "titulo": "Organizar a área de recicláveis",
        "descricao": "Direcionar papelões e manter a área de recicláveis organizada.",
        "pontos": 2,
        "validacao": False,
        "dias": ["segunda", "terca", "quarta", "quinta", "sexta", "sabado"],
    },
    {
        "id": "extra_apoio_contagem",
        "titulo": "Apoiar uma contagem de estoque",
        "descricao": "Ajudar em uma contagem solicitada e informar qualquer divergência encontrada.",
        "pontos": 3,
        "validacao": True,
        "dias": ["segunda", "terca", "quarta", "quinta", "sexta", "sabado"],
    },
    {
        "id": "extra_laranjas",
        "titulo": "Apoiar a higienização e organização das laranjas",
        "descricao": "Executar conforme necessidade e conforme o POP de armazenamento/higienização.",
        "pontos": 4,
        "validacao": False,
        "pop_slug": "armazenamento-laranja",
        "dias": ["segunda", "terca", "quarta", "quinta", "sexta", "sabado"],
    },
    {
        "id": "extra_caixas_bases_500",
        "titulo": "Separar e embalar mais de 500 caixas e bases P/G",
        "descricao": "Concluir um lote superior a 500 unidades somando caixas e bases dos tamanhos P e G.",
        "pontos": 7,
        "validacao": False,
        "dias": ["segunda", "terca", "quarta", "quinta", "sexta", "sabado"],
    },
    {
        "id": "extra_lixo_setores",
        "titulo": "Trocar o lixo de todos os setores do estoque",
        "descricao": "Realizar a troca dos sacos/recipientes de lixo das áreas do estoque e deixar os pontos organizados.",
        "pontos": 2,
        "validacao": False,
        "dias": ["segunda", "terca", "quarta", "quinta", "sexta", "sabado"],
    },
    {
        "id": "extra_panfletos_15",
        "titulo": "Separar mais de 15 pacotes de panfletos com 100 unidades",
        "descricao": "Montar mais de 15 pacotes, cada um contendo 100 panfletos, e deixar o material organizado.",
        "pontos": 5,
        "validacao": False,
        "dias": ["segunda", "terca", "quarta", "quinta", "sexta", "sabado"],
    },
]

# ---------------------------------------------------------------------------
# CATEGORIAS DO PAINEL RH
# ---------------------------------------------------------------------------
# Agrupam tarefas equivalentes de dias diferentes. Assim o painel consegue
# mostrar leituras como “Colaborador A realizou Separação de tabuleiros 3 vezes na
# semana”, mesmo que cada dia use um ID operacional diferente.
CATEGORIAS_RH = {
    # Separação de tabuleiros
    "seg_rm_01": "Separação de tabuleiros",
    "seg_rt_03": "Separação de tabuleiros",
    "qua_rm_01": "Separação de tabuleiros",
    "qua_rt_01": "Separação de tabuleiros",
    "sex_rm_01": "Separação de tabuleiros",
    "sex_rt_02": "Separação de tabuleiros",
    "sab_rm_01": "Separação de tabuleiros",
    "sab_rt_01": "Separação de tabuleiros",

    # Bebidas / sucos
    "seg_rm_02": "Separação de bebidas",
    "seg_rt_01": "Separação de bebidas",
    "sex_rt_01": "Separação de bebidas",
    "seg_rt_04": "Separação de sucos",
    "sex_rt_03": "Separação de sucos",

    # Carga e expedição
    "seg_rm_03": "Carregamento e conferência de rota",
    "seg_rt_05": "Carregamento e conferência de rota",
    "qua_rm_03": "Carregamento e conferência de rota",
    "sex_rm_02": "Carregamento e conferência de rota",
    "sex_rt_04": "Carregamento e conferência de rota",
    "sab_rm_03": "Carregamento e conferência de rota",
    "sab_cf_03": "Carga e fechamento do setor",

    # Trabalho externo
    "seg_ro_01": "Rota externa / entregas",
    "qua_ro_01": "Rota externa / entregas",
    "sex_ro_01": "Rota externa / entregas",
    "ter_cp_01": "Compras externas",

    # Avarias
    "seg_av_01": "Avarias",
    "seg_ff_01": "Avarias",
    "ter_ad_01": "Avarias",
    "qua_ff_01": "Avarias",
    "qui_av_01": "Avarias",
    "sex_av_01": "Avarias",
    "sex_ff_01": "Avarias",
    "sab_pa_02": "Avarias e doca",

    # Transferências internas
    "seg_ff_02": "Transferências internas",
    "ter_ff_01": "Transferências internas",
    "qua_ff_02": "Transferências internas",
    "qui_fe_01": "Transferências internas",
    "sex_ff_02": "Transferências internas",

    # Complementares mais relevantes
    "extra_pvp_secos": "PVP / validade",
    "extra_etiquetas": "Etiquetas e identificação",
    "extra_apoio_contagem": "Apoio a contagens",
    "extra_laranjas": "Higienização / organização de laranjas",
    "extra_caixas_bases_500": "Caixas e bases P/G",
    "extra_lixo_setores": "Organização / lixo dos setores",
    "extra_panfletos_15": "Separação de panfletos",
}

# ---------------------------------------------------------------------------
# BACKUP
# ---------------------------------------------------------------------------
BACKUP = {
    "intervalo_dias": 7,
    "manter_ultimos": 12,
}
