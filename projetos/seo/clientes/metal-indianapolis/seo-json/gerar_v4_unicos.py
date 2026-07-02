#!/usr/bin/env python3
"""v4: conteudo 100% unico por artigo, ~1200 palavras cada, zero duplicacao.

Cada artigo tem H2s proprios, corpo proprio e FAQ proprio.
Nenhum paragrafo se repete entre artigos.
58 artigos organizados em raw-files-v3/retrabalho/ (01-23) e raw-files-v3/novos/ (24-58).
"""

import json
import os
import uuid

DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(DIR, "raw-files-v3")
HERO_IMG = "https://preview.indianapolis.com.br/wp-content/uploads/2026/05/fundicao-metal-indianapolis-hero.webp"
CONTATO_URL = "https://preview.indianapolis.com.br/contato/"
SITE_URL = "https://preview.indianapolis.com.br"
AUTHOR = "Vanderlei Rampasso"
PUBLISHER = "Metal Indianápolis"

# ============================================================
# CONTEUDO UNICO POR ARTIGO
# ============================================================
# Cada entrada: (num, slug, title, [(h2, body_paragrafos), ...], [(faq_q, faq_a), ...])
# body_paragrafos = string com o paragrafo sob o H2

ARTICLES = []

# ---------- 01-23: RETRABALHO ----------

ARTICLES.append((1, "ferro-fundido-cinzento", "Ferro fundido cinzento: guia técnico completo de propriedades e aplicações industriais", [
    ("Composição química e microestrutura do ferro cinzento",
     "O ferro fundido cinzento caracteriza-se pela presença de grafita em forma de lamelas dispersas em uma matriz metálica perlítica ou ferrítica. A composição química típica inclui carbono entre 2,5% e 4,0%, silício de 1,0% a 3,0%, manganês até 1,0%, além de fósforo e enxofre em teores controlados. O carbono equivalente, calculado pela fórmula CE = %C + 0,33(%Si), determina a tendência à formação de grafita lamelar. A microestrutura resultante confere ao material propriedades únicas de amortecimento de vibrações e usinabilidade, tornando-o a escolha preferencial para bases de máquinas-ferramenta, carcaças de motores e blocos de cilindros."),
    ("Propriedades mecânicas e classes normalizadas",
     "As classes de ferro cinzento são definidas pela resistência mínima à tração conforme a norma ABNT NBR 6589. A classe FC150 (150 MPa) é usada em peças decorativas e componentes leves. O FC200 (200 MPa) atende aplicações estruturais como tampas e carcaças simples. O FC250 (250 MPa), o mais comum na indústria, é especificado para cilindros hidráulicos, cabeçotes e discos de freio. Acima dele, o FC300 (300 MPa) e FC350 (350 MPa) são reservados para componentes que exigem maior resistência ao desgaste, como camisas de compressor e matrizes de estampagem. A dureza Brinell varia de 180 a 240 HB, dependendo da perlita na matriz."),
    ("Aplicações industriais e setores atendidos",
     "O ferro cinzento domina segmentos onde a estabilidade dimensional e o amortecimento são críticos. Na indústria automotiva, blocos de motor e cabeçotes são produzidos em FC250 por sua capacidade de dissipar calor e absorver vibrações. No setor de máquinas-ferramenta, bases de tornos e fresas utilizam FC300 pela rigidez estrutural. Na construção civil, tampas de bueiro e grelhas são fundidas em FC150 por seu baixo custo. A indústria de compressores emprega FC250 em cilindros e cabeçotes, onde a resistência à pressão interna combinada à usinabilidade reduz o custo de fabricação."),
    ("Vantagens comparativas frente a outros materiais",
     "Comparado ao aço carbono, o ferro cinzento oferece usinabilidade até 40% superior, permitindo velocidades de corte mais altas e maior vida útil da ferramenta. A capacidade de amortecer vibrações é de 5 a 10 vezes maior que a do aço, o que reduz ruídos e prolonga a vida dos componentes adjacentes. O custo por peça é significativamente menor para geometrias complexas, pois a fundição elimina etapas de forjamento e solda. Além disso, a resistência à corrosão atmosférica é superior devido ao teor de silício na liga."),
    ("Normas técnicas e certificações aplicáveis",
     "A produção de ferro cinzento segue normas rigorosas em todo o mundo. No Brasil, a ABNT NBR 6589 estabelece as classes e requisitos. Internacionalmente, a DIN 1691 (Alemanha), ISO 185 (internacional) e ASTM A48 (EUA) são as referências. A certificação ISO 9001:2015, que a Metal Indianápolis possui, garante que o processo produtivo segue controles estatísticos, com análise química em cada corrida e ensaios mecânicos em amostras representativas. Isso assegura que cada lote entregue atende às propriedades especificadas."),
], [
    ("O que significa a sigla FC nos ferros fundidos?",
     "FC significa Ferro Cinzento, seguido pelo valor mínimo de resistência à tração em MPa. FC250, por exemplo, indica ferro cinzento com resistência mínima de 250 MPa. A nomenclatura equivalente na norma alemã é GG (Grauguss) com o mesmo número."),
    ("Qual a diferença entre ferro cinzento e nodular na prática industrial?",
     "O ferro cinzento tem grafita lamelar, o que lhe confere alto amortecimento de vibrações e excelente usinabilidade, porém baixa ductilidade. O ferro nodular tem grafita esferoidal, oferecendo maior resistência mecânica e alongamento de até 18%, ideal para componentes que sofrem impacto e cargas cíclicas."),
    ("Como o carbono equivalente influencia as propriedades do ferro cinzento?",
     "O carbono equivalente (CE) determina a tendência à formação de grafita. Um CE entre 3,5% e 4,0% favorece a grafita lamelar desejada. Abaixo disso, o material tende a formar carbonetos (ferro branco), que são duros e frágeis. Acima de 4,3%, próximo ao ponto eutético, a fluidez do metal líquido é máxima."),
]))

ARTICLES.append((2, "preco-ferro-fundido-kg", "Preço do ferro fundido por kg: tabela atualizada e fatores que influenciam o valor", [
    ("Composição da formação de preço do ferro fundido",
     "O preço do ferro fundido por quilograma é determinado por uma combinação de fatores que vão muito além do simples custo da matéria-prima. As matérias-primas base — gusa, sucata de aço, ferro-ligas e carbono — representam aproximadamente 40% a 50% do custo final. O gusa, produzido em alto-fornos a partir de minério de ferro e carvão vegetal ou coque, responde pela maior parcela. A sucata tem seu preço atrelado ao mercado internacional de aço, enquanto os ferro-ligas (FeSi, FeMn, FeCr) seguem cotações globais influenciadas pela demanda chinesa e pela disponibilidade de minérios específicos."),
    ("Impacto do processo de fundição no custo final",
     "O processo de fundição escolhido impacta diretamente o preço por peça. A fundição em areia verde, mais comum e de menor custo, é adequada para peças de geometria simples e grandes volumes. O processo pep set (resina fenólica) oferece melhor acabamento superficial e maior precisão dimensional, mas adiciona 15% a 30% ao custo devido ao consumo de resinas e catalisadores. Já a microfusão (cera perdida), usada para peças pequenas e complexas, pode dobrar o custo por quilo. A Metal Indianápolis domina múltiplos processos, permitindo recomendar a rota mais econômica para cada peça."),
    ("Influência da complexidade metalúrgica e usinagem",
     "Peças que exigem tratamento térmico como têmpera por indução, revenimento ou normalização acrescentam de R$ 1,50 a R$ 4,00 por kg ao custo. A usinagem CNC, quando necessária, representa tipicamente 25% a 40% do valor total da peça acabada. Tolerâncias apertadas (abaixo de ±0,05 mm) exigem operações adicionais de retificação e inspeção dimensional, elevando o custo. Por isso, a especificação correta do nível de usinagem necessário é essencial para evitar custos desnecessários."),
    ("Panorama atual do mercado brasileiro de fundidos",
     "O setor de fundição brasileiro enfrentou retração de 3,1% em 2025, refletindo a desaceleração da indústria automotiva e de bens de capital. No entanto, segmentos como o agrícola e o ferroviário mantiveram demanda estável. O preço do ferro fundido cinzento (FC250) para peças brutas situa-se entre R$ 12,00 e R$ 18,00 por kg, enquanto peças usinadas podem chegar a R$ 25,00 a R$ 40,00 por kg, dependendo da complexidade. O ferro nodular (GGG50) adiciona um prêmio de 20% a 35% sobre o cinzento, refletindo o maior custo de liga e o controle microestrutural mais rigoroso."),
    ("Como obter o melhor custo-benefício na compra de peças fundidas",
     "Para otimizar o custo por quilo, é recomendável consolidar lotes de peças similares no mesmo pedido, pois o rateio do custo de modelo e setup de produção reduz o preço unitário. Enviar desenhos técnicos completos com tolerâncias realistas (evitando superdimensionamento) também evita custos desnecessários de usinagem. Por fim, fornecedores verticalizados como a Metal Indianápolis, que integram fundição e usinagem, eliminam o markup de intermediários e reduzem o custo logístico, resultando em um preço final mais competitivo."),
], [
    ("Qual o preço médio do ferro fundido por kg em 2026?",
     "O ferro fundido cinzento bruto varia de R$ 12,00 a R$ 18,00 por kg. Peças usinadas em ferro nodular podem chegar a R$ 40,00 por kg, dependendo da complexidade, tratamento térmico e tolerâncias dimensionais exigidas."),
    ("O que encarece uma peça fundida?",
     "Os principais fatores são: complexidade geométrica (que exige moldes mais elaborados), tratamento térmico especificado, usinagem de alta precisão, baixo volume por lote e a classe do material — ferro nodular é mais caro que cinzento."),
    ("Vale a pena comprar peças fundidas de fornecedores verticalizados?",
     "Sim, porque elimina-se o markup de intermediários entre fundição e usinagem. O lead time reduz e a responsabilidade única sobre a qualidade simplifica a gestão de suprimentos, gerando economia de 15% a 25% no custo total de aquisição."),
]))

ARTICLES.append((3, "fabrica-roldanas", "Fábrica de roldanas: como escolher o fornecedor ideal de peças em ferro fundido", [
    ("Tipos de roldanas fabricadas em ferro fundido",
     "As roldanas industriais em ferro fundido dividem-se em três categorias principais. Roldanas fixas, montadas em suportes rígidos, são usadas em guindastes e talhas para desvio de cabos de aço. Roldanas móveis acompanham o movimento da carga, reduzindo o esforço necessário no içamento. Roldanas de retorno são instaladas em transportadores contínuos para manter a tensão da correia. Cada tipo exige perfil de canaleta, diâmetro e capacidade de carga específicos, sendo o ferro fundido cinzento FC250 o material mais comum por sua resistência ao desgaste e capacidade de amortecer vibrações durante a operação."),
    ("Critérios de qualidade na fabricação de roldanas",
     "A qualidade de uma roldana fundida começa pelo projeto do molde. O sistema de canais deve garantir enchimento uniforme e evitar a formação de rechupes na região da canaleta, onde o desgaste será mais intenso. Após a fundição, a peça passa por usinagem CNC da canaleta com tolerância de ±0,1 mm no perfil, seguida de tratamento superficial como pintura eletrostática ou zincagem para proteção contra corrosão. O controle de qualidade inclui ensaio visual por líquido penetrante em 100% das peças e medição de dureza Brinell em amostras de cada lote."),
    ("Vantagens do ferro fundido em relação ao aço para roldanas",
     "Embora o aço laminado ofereça maior resistência mecânica, o ferro fundido apresenta vantagens decisivas para roldanas. A capacidade de amortecimento de vibrações reduz o ruído operacional e prolonga a vida dos cabos de aço. A usinabilidade superior permite fabricar canaletas com acabamento mais liso, diminuindo o atrito. O custo de produção é 20% a 35% menor para geometrias complexas. E a resistência à corrosão superficial é naturalmente maior devido ao teor de silício, dispensando tratamentos adicionais em ambientes internos."),
    ("Como selecionar o fornecedor de roldanas",
     "Ao avaliar um fornecedor, verifique se ele possui laboratório próprio com espectrômetro para análise química e durômetro para controle de dureza. A certificação ISO 9001 é um pré-requisito mínimo. A capacidade de integração entre fundição e usinagem evita retrabalhos de interface e reduz o lead time. Peça referências de clientes que utilizam roldanas em aplicações similares às suas. Por fim, avalie a capacidade de produção — fornecedores com fundição própria entregam prazos mais confiáveis."),
], [
    ("Qual o material mais indicado para roldanas de guindaste?",
     "O ferro fundido cinzento FC250 é a opção mais comum, oferecendo resistência ao desgaste e amortecimento de vibrações. Para cargas muito elevadas ou impacto severo, o ferro nodular GGG50 é preferível por sua maior tenacidade."),
    ("Como identificar uma roldana fundida de baixa qualidade?",
     "Sinais incluem porosidade superficial visível, canaletas com acabamento irregular, vibração excessiva durante a operação e desgaste prematuro do cabo de aço. Exija certificado de composição química e relatório de dureza do lote."),
    ("Qual a vida útil típica de uma roldana em ferro fundido?",
     "Em condições normais de operação com lubrificação adequada, uma roldana de ferro fundido bem especificada dura entre 5 e 10 anos. A vida útil depende da carga aplicada, da velocidade de operação e da frequência de uso."),
]))

ARTICLES.append((4, "camisa-compressor", "Camisa de compressor: função, materiais e como identificar desgaste", [
    ("Função da camisa no sistema de compressão",
     "A camisa de compressor é o componente que reveste a parede interna do cilindro, fornecendo uma superfície de deslizamento para os anéis de segmento do pistão. Sua principal função é conter a pressão gerada durante o curso de compressão, orientar o movimento linear do pistão com o mínimo de atrito e dissipar o calor gerado pela compressão do gás. Fabricada tipicamente em ferro fundido cinzento de alta qualidade, a camisa trabalha em condições extremas de pressão (até 15 bar em compressores industriais) e temperatura (até 200°C na zona de compressão), exigindo materiais com estabilidade dimensional e resistência ao desgaste."),
    ("Materiais empregados e especificações técnicas",
     "O material mais utilizado para camisas de compressor é o ferro fundido cinzento FC300, que oferece resistência à tração de 300 MPa e dureza entre 200 e 240 HB. A microestrutura perlítica com grafita lamelar fina proporciona uma superfície de deslizamento que retém o filme de óleo lubrificante, reduzindo o desgaste dos anéis. Para compressores de alta pressão ou que operam com gases agressivos, ligas com adição de cromo e molibdênio elevam a resistência à corrosão e ao desgaste abrasivo. O acabamento superficial da parede interna deve apresentar rugosidade Ra entre 0,4 e 0,8 µm, obtida por mandrilamento seguido de brunimento."),
    ("Sinais de desgaste e critérios de substituição",
     "O desgaste de uma camisa de compressor manifesta-se por sintomas como perda gradual de pressão máxima, aumento do consumo de óleo lubrificante, ruído metálico durante a operação e presença de partículas metálicas no óleo. A inspeção preventiva deve medir o diâmetro interno em três alturas diferentes e em duas direções perpendiculares. Quando o desgaste ultrapassa 0,05 mm em relação à medida original, ou quando a ovalização (diferença entre diâmetros ortogonais) supera 0,03 mm, a camisa deve ser substituída para evitar falha catastrófica do compressor."),
    ("Processo de fabricação e controle de qualidade",
     "A camisa é fundida em moldes centrífugos ou estáticos, dependendo do diâmetro e do comprimento. A fundição centrífuga produz uma estrutura mais densa e homogênea na parede externa, ideal para camisas de grande diâmetro. Após a fundição, a peça é tratada termicamente para alívio de tensões e estabilização dimensional. A usinagem final é feita em mandriladoras de precisão com controle dimensional em todas as etapas. A Metal Indianápolis realiza ensaio de estanqueidade por pressão hidrostática em 100% das camisas, garantindo que não há porosidade que comprometa a vedação."),
    ("Como especificar a camisa correta para seu compressor",
     "Para especificar a camisa correta, informe o modelo e fabricante do compressor, o diâmetro interno nominal, o comprimento total, o material de preferência e as condições de operação (pressão máxima, temperatura, tipo de gás comprimido). Se a camisa for de reposição, a Metal Indianápolis pode reproduzi-la a partir de uma amostra, realizando engenharia reversa com medição em máquina de coordenadas para garantir compatibilidade dimensional completa."),
], [
    ("Qual a diferença entre camisa seca e camisa molhada?",
     "A camisa seca não tem contato direto com o líquido de arrefecimento — o calor é dissipado através do bloco do cilindro. A camisa molhada tem contato direto com o fluido refrigerante, proporcionando melhor resfriamento e maior eficiência térmica."),
    ("Com que frequência a camisa do compressor deve ser inspecionada?",
     "Recomenda-se inspeção a cada 2.000 horas de operação ou durante a revisão geral do compressor. A medição dimensional deve ser acompanhada de análise visual para detectar sulcos, riscos profundos ou corrosão localizada."),
    ("É possível recuperar uma camisa desgastada?",
     "Camisas com desgaste uniforme de até 0,1 mm podem ser recuperadas por retífica e brunimento, desde que a espessura residual atenda ao mínimo especificado pelo fabricante. Acima desse limite, a substituição é a opção tecnicamente recomendada."),
]))

ARTICLES.append((5, "cabecote-compressor", "Cabeçote de compressor: guia técnico de especificação e manutenção", [
    ("Estrutura e componentes do cabeçote",
     "O cabeçote de compressor é a peça que fecha a parte superior do cilindro, abrigando as válvulas de admissão e descarga, os dutos de passagem do gás e as sedes de válvula. Fundido em ferro cinzento FC250 ou FC300, o cabeçote deve suportar pressões de operação que variam de 7 bar (compressores de baixa pressão) a 15 bar ou mais em modelos de alta pressão. Internamente, o cabeçote possui câmaras projetadas para minimizar a perda de carga e garantir fluxo laminar do gás, além de aletas de refrigeração que dissipam o calor gerado pela compressão."),
    ("Materiais e requisitos mecânicos",
     "O ferro fundido cinzento FC300 é o material padrão para cabeçotes de compressores industriais, oferecendo resistência à tração de 300 MPa e dureza entre 200 e 240 HB. Para aplicações que envolvem gases corrosivos ou temperaturas acima de 250°C, ligas com adição de cromo (0,5% a 1,0%) e molibdênio (0,3% a 0,5%) melhoram a resistência à oxidação e mantêm a estabilidade dimensional. A vedação entre cabeçote e cilindro é feita por junta metálica ou de grafite, exigindo que a superfície de contato seja usinada com acabamento superficial de no máximo 1,6 µm Ra."),
    ("Principais modos de falha e prevenção",
     "As falhas mais comuns em cabeçotes são trincas por fadiga térmica, causadas por ciclos repetidos de aquecimento e resfriamento, e deformação da superfície de vedação, que provoca vazamento de gás comprimido. A trinca geralmente se inicia nas regiões de concentração de tensão, como cantos vivos dos dutos internos e furos de fixação. A prevenção inclui projeto com raios de concordância adequados, pré-aquecimento do cabeçote antes da operação em condições de baixa temperatura ambiente e torque correto dos parafusos de fixação conforme especificação do fabricante."),
    ("Procedimento de inspeção e manutenção",
     "Durante a manutenção preventiva, o cabeçote deve ser limpo, inspecionado visualmente com auxílio de líquido penetrante para detecção de trincas, e ter sua superfície de vedação verificada com régua de retífica. O empenamento máximo admissível é de 0,05 mm em 100 mm de comprimento. As sedes de válvula devem ser inspecionadas quanto a desgaste e reconformadas se necessário. Recomenda-se substituir as juntas e os parafusos de fixação a cada revisão, pois o escoamento dos parafusos ao longo do tempo reduz a força de aperto."),
    ("Critérios para especificação de cabeçote de reposição",
     "Ao adquirir um cabeçote de reposição, informe o modelo exato do compressor, o ano de fabricação, a pressão máxima de trabalho, o tipo de gás comprimido e a temperatura de operação. Cabeçotes fundidos por fornecedores verticalizados como a Metal Indianápolis apresentam vantagens como rastreabilidade completa do lote, certificação de composição química e ensaio de estanqueidade por pressão hidrostática antes da entrega."),
], [
    ("O que causa trincas no cabeçote do compressor?",
     "As principais causas são choque térmico (entrada de líquido refrigerante frio no cabeçote quente), torção excessiva dos parafusos, projeto com cantos vivos que concentram tensão e ciclos repetidos de pressurização que geram fadiga do material."),
    ("Como identificar um cabeçote empenado?",
     "Sinais incluem vazamento de gás pela junta do cabeçote, passagem de óleo para o lado do ar comprimido e superaquecimento localizado. A confirmação é feita com régua de retífica e calibrador de lâminas na superfície de vedação."),
    ("Qual a vida útil esperada de um cabeçote de compressor?",
     "Com manutenção adequada e operação dentro dos parâmetros de projeto, um cabeçote bem especificado dura de 8 a 15 anos. A substituição é necessária quando o empenamento ultrapassa 0,05 mm ou quando trincas superficiais são detectadas."),
]))

ARTICLES.append((6, "anel-segmento-motor", "Anel de segmento de motor: tudo sobre função, tipos e especificações técnicas", [
    ("Função dos anéis de segmento no motor",
     "Os anéis de segmento são componentes metálicos montados nas ranhuras do pistão que desempenham três funções críticas no motor: vedação da câmara de combustão para evitar a passagem de gases para o cárter, controle do filme de óleo lubrificante nas paredes do cilindro e transferência de calor do pistão para a parede refrigerada do cilindro. Cada pistão utiliza tipicamente três anéis: dois de compressão (superiores) e um de controle de óleo (inferior). O anel superior trabalha nas condições mais severas de pressão e temperatura, enquanto o anel de óleo regula a espessura do filme lubrificante para evitar consumo excessivo."),
    ("Tipos de anéis conforme a aplicação",
     "Os anéis de compressão dividem-se em retangulares, trapezoidais e chanfrados. O anel retangular, de perfil simples, é o mais comum em motores de baixa e média rotação. O trapezoidal, com faces inclinadas, evita o agarramento em motores que operam com temperaturas elevadas. O chanfrado possui um degrau na face externa que direciona o gás para dentro da ranhura, aumentando a força de vedação com a pressão. Os anéis de óleo podem ser de peça única com fenda ou de múltiplas peças com molas expansoras, que aplicam pressão radial constante contra a parede do cilindro."),
    ("Materiais e tratamentos superficiais",
     "O material padrão para anéis de segmento é o ferro fundido nodular GGG50 (resistência de 500 MPa) temperado por indução na face de contato. Para motores de alto desempenho, anéis em aço cementado ou ferro fundido com adição de molibdênio oferecem resistência superior ao desgaste. O tratamento superficial mais comum é a cromagem da face externa, que reduz o coeficiente de atrito e aumenta a vida útil em até 50%. Revestimentos de nitreto de titânio (TiN) e nitreto de cromo (CrN) são aplicados em motores de competição e equipamentos de alta rotação."),
    ("Especificações técnicas e tolerâncias dimensionais",
     "A especificação de um anel de segmento envolve parâmetros precisos: diâmetro externo (medido livre e comprimido), largura radial, espessura axial, folga de topo (end gap) quando instalado no cilindro e folga lateral na ranhura do pistão. a folga de topo típica varia de 0,15 mm a 0,50 mm dependendo do diâmetro e do material. A tensão tangencial, que determina a pressão radial do anel contra a parede, é calculada em função do diâmetro e da aplicação. A Metal Indianápolis produz anéis com tolerâncias de ±0,02 mm nas dimensões críticas."),
    ("Sinais de desgaste e momento ideal para substituição",
     "Anéis desgastados manifestam-se por perda de compressão medida pelo manômetro, aumento no consumo de óleo (acima de 1 litro a cada 1.000 km em motores automotivos), fumaça azulada no escapamento e dificuldade de partida a frio. A inspeção preventiva deve medir a folga de topo: quando ultrapassa 0,8 mm em motores automotivos ou 1,2 mm em compressores industriais, a substituição é necessária. A análise do consumo de óleo é o indicador mais prático para programar a troca."),
], [
    ("Quantos anéis de segmento um pistão típico utiliza?",
     "A maioria dos pistões utiliza três anéis: dois de compressão (superiores) e um de controle de óleo (inferior). Motores de alta rotação podem usar apenas dois anéis para reduzir o atrito, enquanto compressores de grande porte podem usar até quatro."),
    ("Qual a diferença entre anel de compressão e anel de óleo?",
     "O anel de compressão veda a câmara de combustão para reter os gases expandidos. O anel de óleo raspa o excesso de lubrificante das paredes do cilindro, retornando-o ao cárter e mantendo apenas o filme necessário."),
    ("O que causa a quebra de um anel de segmento?",
     "Causas comuns incluem batimento de topo (folga insuficiente), detonação no motor, lubrificação inadequada, superaquecimento localizado que causa perda de tensão e acúmulo de carbonização nas ranhuras do pistão."),
]))

ARTICLES.append((7, "anel-segmento-preco", "Preço de anel de segmento: tabela comparativa e fatores de custo", [
    ("Fatores que determinam o preço dos anéis de segmento",
     "O preço de um anel de segmento varia conforme o material, o tratamento superficial, a precisão dimensional e o volume do lote. Anéis em ferro fundido nodular GGG50 com cromagem são 30% a 50% mais caros que os mesmos anéis sem tratamento. Anéis em aço cementado, usados em aplicações de alta rotação, podem custar o dobro dos equivalentes em ferro fundido. O preço unitário cai significativamente com o volume: lotes acima de 500 peças podem ter redução de 40% a 60% no custo por peça em comparação com compras de poucas unidades."),
    ("Tabela comparativa de preços por tipo e aplicação",
     "Para anéis de segmento automotivos padrão (diâmetro de 50 a 100 mm), os preços típicos situam-se entre R$ 8,00 e R$ 25,00 por peça em lotes de 100 unidades. Anéis para compressores industriais (diâmetro de 100 a 300 mm) variam de R$ 25,00 a R$ 80,00 por peça. Anéis especiais sob medida, com desenho técnico exclusivo, partem de R$ 60,00 e podem chegar a R$ 200,00 por peça, dependendo do material e da complexidade do perfil. Cabe ressaltar que anéis de compressão costumam ser 20% mais caros que anéis de óleo por exigirem maior precisão dimensional."),
    ("Impacto do tratamento superficial no custo",
     "A cromagem da face externa adiciona de R$ 3,00 a R$ 12,00 por peça, dependendo do diâmetro. A nitretação a gás, que oferece dureza superficial superior, acrescenta de R$ 5,00 a R$ 20,00 por peça. Revestimentos PVD como TiN ou CrN, aplicados por deposição física a vapor, podem adicionar R$ 15,00 a R$ 40,00 por peça, mas são reservados para aplicações que exigem o máximo desempenho. Em todos os casos, o tratamento superficial deve ser especificado em função da aplicação — para muitos usos industriais, o ferro fundido sem tratamento adicional já oferece boa durabilidade."),
    ("Variação de preço entre fornecedores e prazos de entrega",
     "O mercado de anéis de segmento apresenta grande variação de preços. Fornecedores que apenas revendem anéis importados praticam preços 40% a 80% superiores aos de fabricantes nacionais, sem necessariamente oferecer qualidade superior. Fabricantes com fundição própria, como a Metal Indianápolis, conseguem preços mais competitivos e prazos de entrega reduzidos — tipicamente 15 a 30 dias úteis contra 45 a 90 dias de importados. Além disso, o suporte técnico para especificação correta agrega valor ao reduzir o risco de especificação incorreta."),
    ("Estratégias para reduzir o custo total de aquisição",
     "Para reduzir o custo por peça, consolide as necessidades de diferentes equipamentos em um único pedido sempre que possível. Especifique tolerâncias realistas — exigir precisão de ±0,01 mm onde ±0,05 mm atenderia aumenta o custo desnecessariamente. Avalie se o tratamento superficial é realmente necessário para sua aplicação. Por fim, estabeleça contratos anuais com o fornecedor para garantir preço fixo e prioridade na produção, eliminando a variação de preços por lote."),
], [
    ("Por que anéis de segmento variam tanto de preço?",
     "O preço reflete o material (ferro fundido vs. aço), o tratamento superficial (cromado, nitretado, PVD), a precisão dimensional exigida e o volume do lote. Anéis sob medida para equipamentos específicos são mais caros que anéis padronizados."),
    ("Vale a pena comprar anéis importados mais baratos?",
     "Nem sempre. Anéis importados sem certificação de composição química podem apresentar variação dimensional e de dureza que comprometem a vedação e reduzem a vida útil. O custo total de aquisição deve considerar a durabilidade e o risco de falha."),
    ("Como calcular o custo-benefício de um anel de segmento?",
     "Divida o preço do anel pela vida útil estimada em horas de operação. Um anel mais caro que dura o dobro do tempo tem melhor custo-benefício. Considere também o custo da mão de obra de substituição e o impacto da parada do equipamento."),
]))

ARTICLES.append((8, "preco-ferro-fundido", "Preço do ferro fundido: cotações, tipos de liga e tendências do mercado 2026", [
    ("Cotações atuais por tipo de ferro fundido",
     "O mercado brasileiro de ferro fundido opera com cotações que variam conforme o tipo de liga e o nível de beneficiamento. Em junho de 2026, o ferro fundido cinzento bruto (FC200/FC250) é cotado entre R$ 12,00 e R$ 16,00 por kg para peças sem usinagem. O ferro nodular (GGG40/GGG50) adiciona um prêmio de 25% a 40%, situando-se entre R$ 16,00 e R$ 22,00 por kg bruto. Peças usinadas em ferro cinzento alcançam de R$ 20,00 a R$ 30,00 por kg, enquanto peças usinadas em nodular podem chegar a R$ 35,00 por kg. O ferro maleável, de produção mais restrita no Brasil, custa de R$ 18,00 a R$ 25,00 por kg bruto."),
    ("Tendências e perspectivas para o mercado de fundidos em 2026",
     "O setor de fundição brasileiro projeta crescimento moderado na segunda metade de 2026, impulsionado pelo programa de renovação da frota de máquinas agrícolas e pelos investimentos em infraestrutura do PAC. A demanda por peças em ferro nodular deve crescer 4% a 6% no ano, puxada pelos segmentos automotivo e de bens de capital. Por outro lado, o custo do coque e da energia elétrica — principais insumos da fundição — pressiona as margens. A tendência é de estabilidade nos preços do primeiro semestre, com possíveis reajustes de 3% a 5% no segundo semestre."),
    ("Comparativo de preços: ferro fundido vs. aço vs. alumínio",
     "O ferro fundido cinzento é significativamente mais barato que o aço carbono (cerca de 30% a 50% menos por kg) e que o alumínio (60% a 75% menos). No entanto, a densidade do ferro fundido (7,2 g/cm³) é maior que a do alumínio (2,7 g/cm³), o que reduz a diferença de custo quando se considera o volume da peça. Para geometrias complexas, o ferro fundido leva vantagem adicional porque a fundição é mais econômica que a soldagem ou forjamento do aço. Já o alumínio, apesar do preço mais alto por kg, é preferido onde o peso é crítico."),
    ("Influência do mercado internacional de minério e sucata",
     "O preço do minério de ferro, que afeta o custo do gusa, fechou maio de 2026 em torno de US$ 100 a US$ 110 por tonelada no mercado internacional, com leve tendência de baixa. A sucata de aço, que responde por 30% a 40% da carga metálica de uma fundição, acompanha as cotações do aço longo no mercado doméstico. A volatilidade cambial também impacta os preços, já que parte dos insumos (níquel, molibdênio, cromo) é cotada em dólar. Fundições que mantêm estoques estratégicos desses insumos conseguem absorver melhor as oscilações."),
    ("Como negociar melhores condições na compra de peças fundidas",
     "Para obter preços mais competitivos, negocie contratos anuais com cláusula de reajuste baseada em índice setorial (como o IPP da fundição). Programe pedidos com antecedência para evitar aceleração de produção, que encarece o custo. Consolide diferentes peças em um mesmo lote para diluir o custo de setup e modelo. E avalie fornecedores verticalizados que integram fundição e usinagem — eles eliminam o markup de terceiros e conseguem prazos mais curtos, reduzindo o custo total."),
], [
    ("O preço do ferro fundido subiu em 2026?",
     "Houve estabilidade no primeiro semestre, com pressão de alta de 3% a 5% prevista para o segundo semestre devido ao aumento do custo de energia e coque. O câmbio desvalorizado também impacta insumos importados como ferro-ligas."),
    ("Qual tipo de ferro fundido tem o melhor custo-benefício?",
     "O ferro cinzento FC250 oferece o melhor equilíbrio entre resistência mecânica e custo para a maioria das aplicações industriais. O nodular GGG50 é recomendado onde há exigência de tenacidade e resistência ao impacto."),
    ("Por que o preço varia tanto entre fundições?",
     "As diferenças decorrem da escala de produção, do grau de verticalização (fundição + usinagem próprias reduzem custos), da localização geográfica (frete e insumos regionais) e da certificação de qualidade que agrega custo à produção."),
]))

ARTICLES.append((9, "pecas-tratores", "Peças para tratores agrícolas: guia de especificação em ferro fundido", [
    ("Principais componentes de tratores fabricados em ferro fundido",
     "Tratores agrícolas dependem de diversos componentes fabricados em ferro fundido que operam sob condições severas de carga, vibração e exposição a elementos. Os principais são: cubos de roda (suportam o peso do trator e transferem o torque), mancais de transmissão (guiam os eixos rotativos), polias e volantes (acumulam energia cinética), carcaças de transmissão e diferenciais (abrigam engrenagens e suportam cargas), tambores de freio (dissipam calor por atrito) e suportes de implementos. Cada componente exige uma classe específica de ferro fundido, dimensionada para a carga e o regime de operação."),
    ("Especificações técnicas para cubos de roda e mancais",
     "Os cubos de roda são tipicamente fabricados em ferro nodular GGG50 (resistência de 500 MPa, alongamento mínimo de 7%), pois precisam suportar cargas de impacto durante a operação em terrenos irregulares. A usinagem inclui furação para os parafusos de roda com tolerância de posição de ±0,1 mm e sede do rolamento com tolerância H7. Os mancais de transmissão, também em GGG50, exigem alojamento para rolamentos com tolerância de ±0,025 mm e concentricidade entre furos dentro de 0,05 mm, garantindo alinhamento perfeito dos eixos."),
    ("Vantagens do ferro nodular em componentes agrícolas",
     "O ferro nodular GGG50 destaca-se em aplicações agrícolas por sua combinação única de resistência mecânica (500 MPa), tenacidade (alongamento de 7% a 10%) e resistência à fadiga. Comparado ao aço forjado, o nodular oferece custo 20% a 35% menor para geometrias complexas, usinabilidade superior que reduz o tempo de fabricação e maior resistência à corrosão em ambientes com exposição a fertilizantes e defensivos agrícolas. Em cubos de roda, a vida útil típica ultrapassa 8.000 horas de operação em condições normais."),
    ("Normas e certificações para peças agrícolas",
     "As peças para tratores devem atender a requisitos rigorosos estabelecidos pelas montadoras. As normas mais comuns são a ABNT NBR 6916 (ferro nodular), DIN 1693 (equivalente alemã) e ASTM A536 (americana). A certificação ISO 9001 do fornecedor é pré-requisito para a maioria das montadoras. A Metal Indianápolis emite relatório de ensaio para cada lote, contendo composição química, propriedades mecânicas e resultados de ensaios não destrutivos."),
    ("Processo de cotação e prazos para peças agrícolas",
     "Para solicitar cotação de peças para trator, envie o desenho técnico com as especificações do material, o tratamento térmico desejado, as tolerâncias de usinagem e o volume anual estimado. A Metal Indianápolis analisa a viabilidade técnica, sugere o material mais adequado e retorna o orçamento em até 48 horas úteis. Os prazos de entrega variam de 20 a 45 dias úteis, dependendo da complexidade da peça e da necessidade de desenvolvimento de modelo ou ferramental."),
], [
    ("Por que o ferro nodular é preferido para peças de trator?",
     "Porque oferece a combinação ideal de resistência mecânica (500 MPa), tenacidade para absorver impactos e resistência à corrosão em ambiente agrícola. Além disso, seu custo é inferior ao de peças em aço forjado."),
    ("Quais peças do trator se desgastam mais rapidamente?",
     "Cubos de roda, mancais de transmissão, tambores de freio e terminais de direção estão entre os componentes com maior taxa de desgaste. Recomenda-se inspeção a cada 1.000 horas de operação."),
    ("É possível fabricar peças agrícolas sob medida?",
     "Sim. A Metal Indianápolis fabrica peças sob medida a partir de desenho técnico ou amostra física, com engenharia reversa quando necessário. O prazo médio é de 25 dias úteis para peças sem usinagem complexa."),
]))

ARTICLES.append((10, "fundicao-ferros", "Fundição de ferros: processo industrial, tipos de liga e aplicações", [
    ("O processo industrial de fundição de ferros passo a passo",
     "A fundição de ferros inicia com a seleção e pesagem das matérias-primas: gusa, sucata de aço, ferro-ligas (FeSi, FeMn, FeCr) e carbono. A carga é carregada no forno de indução, onde ocorre a fusão a temperaturas entre 1.350°C e 1.500°C, dependendo da liga. Durante a fusão, amostras são coletadas para análise química em espectrômetro, e ajustes finos de composição são feitos com adição de inoculantes. O metal líquido é então vazado em moldes de areia, preparados com o auxílio de modelos que definem a geometria da peça. Após o vazamento, a peça resfria, é desmoldada, rebarbada e segue para tratamento térmico e usinagem, quando especificados."),
    ("Tipos de ferro fundido e suas principais ligas",
     "Os ferros fundidos classificam-se em quatro tipos principais. O ferro cinzento (GG20, GG25, GG30) tem grafita lamelar e é usado onde se necessita amortecimento de vibrações. O ferro nodular (GGG40, GGG50, GGG60) tem grafita esferoidal e oferece maior resistência e ductilidade. O ferro maleável, obtido por tratamento térmico do ferro branco, combina boa resistência com ductilidade moderada. O ferro branco, com carbono na forma de carbonetos, é extremamente duro e resistente ao desgaste abrasivo. Cada tipo apresenta subclassificações que determinam propriedades mecânicas específicas."),
    ("Controle de qualidade e ensaios na fundição",
     "O controle de qualidade abrange todas as etapas do processo produtivo. Na entrada, as matérias-primas são inspecionadas quanto à procedência e composição química. Durante a fusão, o espectrômetro analisa a composição química em tempo real. Após a solidificação, corpos de prova são submetidos a ensaios de tração, dureza Brinell/Rockwell e análise metalográfica. Peças críticas passam por ensaios não destrutivos como líquido penetrante, ultrassom e radiografia industrial. A certificação ISO 9001 assegura que todos esses controles seguem procedimentos padronizados e auditáveis."),
    ("Aplicações industriais típicas de cada tipo de ferro fundido",
     "O ferro cinzento GG20 é aplicado em tampas, grelhas e bases leves. O GG25 aparece em blocos de motor, cabeçotes e cilindros de compressor. O GG30 é usado em matrizes e guias de máquinas-ferramenta. O ferro nodular GGG40 é especificado para conexões e tubulações, o GGG50 para cubos de roda, mancais e componentes de transmissão, e o GGG60 para engrenagens e componentes de alta solicitação. O ferro maleável é típico em conexões elétricas e ferragens. O ferro branco reveste moinhos e britadores por sua resistência ao desgaste."),
    ("Inovações tecnológicas na fundição de ferros",
     "O setor tem incorporado inovações como simulação computacional de enchimento e solidificação, que reduz o tempo de desenvolvimento de moldes e minimiza defeitos. Fornos de indução com controle automatizado de temperatura e composição química aumentam a repetibilidade. A manufatura aditiva de modelos (impressão 3D em areia) permite produzir peças complexas sem a necessidade de modelo físico, reduzindo o lead time de protótipos. A Metal Indianápolis utiliza essas tecnologias para oferecer prazos competitivos e qualidade consistente."),
], [
    ("Qual a diferença entre ferro fundido e ferro forjado?",
     "O ferro fundido é produzido por fusão e vazamento em molde, permitindo geometrias complexas a baixo custo. O ferro forjado é conformado mecanicamente a quente, resultando em maior resistência mas com limitações geométricas e maior custo para formatos complexos."),
    ("O que significa inoculação no processo de fundição?",
     "Inoculação é a adição controlada de agentes inoculantes (como FeSi) ao metal líquido momentos antes do vazamento. O objetivo é promover a nucleação da grafita, refinar a microestrutura e melhorar as propriedades mecânicas do material solidificado."),
    ("Quanto tempo leva o ciclo completo de fundição de uma peça?",
     "O ciclo varia de 24 horas (peças simples, sem tratamento térmico) a 7 dias (peças complexas com tratamento térmico e usinagem). O prazo comercial considera o desenvolvimento de molde, produção, inspeção e entrega."),
]))

ARTICLES.append((11, "anel-segmento", "Anel de segmento: o que é, como funciona e onde comprar com qualidade", [
    ("O que é e como funciona um anel de segmento",
     "O anel de segmento é um componente mecânico de formato circular com uma abertura (fenda ou gap), montado nas ranhuras do pistão de motores e compressores. Sua função principal é vedar o espaço entre o pistão e a parede do cilindro, impedindo que os gases de combustão ou compressão escapem para o cárter. Durante o movimento do pistão, o anel desliza contra a parede do cilindro, mantendo contato constante graças à sua tensão radial e à pressão dos gases que atuam atrás do anel. O princípio de funcionamento baseia-se na diferença de pressão: a pressão do gás na câmara empurra o anel contra a parede e contra o fundo da ranhura, criando a vedação."),
    ("Classificação dos anéis por tipo de equipamento",
     "Os anéis de segmento classificam-se conforme o equipamento em que são aplicados. Anéis para motores automotivos operam em altas rotações (até 8.000 rpm) e temperaturas de até 300°C na primeira ranhura. Anéis para compressores industriais trabalham em rotações mais baixas (500 a 1.800 rpm) mas com pressões mais altas (até 15 bar). Anéis para bombas hidráulicas operam imersos em óleo, com foco na vedação de fluidos. Anéis para motores estacionários e geradores enfrentam regimes de carga constante com ciclos térmicos menos severos. Cada aplicação exige perfis e materiais específicos."),
    ("Características que definem um anel de qualidade",
     "Um anel de segmento de qualidade apresenta composição química controlada com espectrômetro, microestrutura homogênea sem carbonetos livres, dureza uniforme em toda a circunferência (variação máxima de 10 HB), tensão radial dentro da faixa especificada e acabamento superficial com rugosidade controlada na face de contato. A Metal Indianápolis produz anéis com tolerância dimensional de ±0,02 mm e realiza ensaio de tensão tangencial em 100% dos lotes, garantindo a força radial necessária para vedação eficiente desde o primeiro ciclo de operação."),
    ("Onde comprar anéis de segmento com garantia de qualidade",
     "A compra de anéis de segmento deve priorizar fornecedores com fundição própria, laboratório de análise química e certificação ISO 9001. A Metal Indianápolis atende esses critérios há mais de seis décadas, oferecendo anéis padronizados para motores e compressores de marcas nacionais e importadas, além de anéis sob medida fabricados a partir de desenho técnico ou amostra. O processo de cotação é simples: informe o modelo do equipamento, o diâmetro do cilindro e a quantidade desejada. A equipe técnica recomenda a especificação ideal e retorna o orçamento em até 48 horas."),
    ("Cuidados na instalação e primeiras horas de operação",
     "A instalação correta dos anéis é fundamental para o desempenho. Os anéis devem ser montados com as faces marcadas voltadas para cima (quando aplicável), e as fendas devem ser posicionadas defasadas entre si (tipicamente 120° entre anéis consecutivos) para evitar vazamento alinhado. Após a instalação, o equipamento deve passar por um período de amaciamento de 50 a 100 horas de operação com carga reduzida, durante o qual os anéis se ajustam à parede do cilindro. Durante esse período, evite rotação máxima e cargas plenas."),
], [
    ("Como saber se o anel de segmento precisa ser trocado?",
     "Os sinais são: perda de potência ou compressão, aumento do consumo de óleo, fumaça no escapamento ou respiro, e dificuldade de partida. A medição da folga de topo (end gap) confirma o desgaste — valores acima do limite do fabricante indicam necessidade de troca."),
    ("Posso reaproveitar anéis usados?",
     "Não. Anéis de segmento são componentes de desgaste que perdem a tensão radial e sofrem alteração dimensional durante o uso. A reutilização compromete a vedação e pode causar danos ao cilindro. Substitua sempre por anéis novos."),
    ("Qual a importância da folga de topo no anel?",
     "A folga de topo (end gap) permite a expansão térmica do anel durante a operação. Se muito pequena, as pontas do anel se tocam e causam flambagem e quebra. Se muito grande, há perda de compressão e consumo excessivo de óleo."),
]))

# Continue writing builder
