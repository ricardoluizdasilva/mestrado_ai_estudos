# Introdução à Ciência de Dados

**Tutorial de ciência de dados, do problema à decisão, em notebooks Jupyter e em português europeu.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![Notebooks](https://img.shields.io/badge/notebooks-53-orange) ![Idioma](https://img.shields.io/badge/idioma-português%20(PT)-green) [![Licença: CC BY-NC-SA 4.0](https://img.shields.io/badge/licen%C3%A7a-CC%20BY--NC--SA%204.0-lightgrey)](LICENSE.md) [![Código: MIT](https://img.shields.io/badge/c%C3%B3digo-MIT-yellow)](LICENSE-MIT.txt) [![Verificação dos notebooks](https://github.com/ricardoluizdasilva/mestrado_ai_estudos/actions/workflows/notebooks_ciencia_dados.yml/badge.svg)](https://github.com/ricardoluizdasilva/mestrado_ai_estudos/actions/workflows/notebooks_ciencia_dados.yml)

Este tutorial ensina a pensar como um cientista de dados antes de ensinar técnicas: que pergunta fazer, que dados a podem responder, como avaliar uma previsão pela decisão que ela permite e como organizar o trabalho. Cada capítulo combina explicações curtas, esquemas, gráficos gerados pelo próprio código, exemplos executáveis e exercícios com soluções.

Cada módulo acompanha um caso do princípio ao fim, com **dados sintéticos** gerados dentro de cada notebook: no módulo 1, uma rede de clínicas que quer reduzir as faltas a consultas; no módulo 2, uma cadeia de padarias que quer prever em que lojas o pão vai esgotar; no módulo 3, o consumo de eletricidade das escolas de um município; no módulo 4, um stand que quer propor o preço de carros usados; no módulo 5, uma empresa de painéis solares que quer estimar a produção de cada telhado; no módulo 6, uma empresa de distribuição que quer prever as entregas atrasadas; no módulo 7, uma aplicação de aprendizagem de línguas que quer conhecer os seus utilizadores; no módulo 8, um centro de formação que quer saber que formandos estão em risco de desistir.

Os notebooks funcionam no **Google Colab** (sem instalar nada), no **Jupyter** e no **VS Code**. Cada notebook tem um botão «Abrir no Colab».

---

## Para quem é

- Quem está a começar em ciência de dados e quer perceber o raciocínio antes das ferramentas.
- Quem já sabe treinar modelos e quer aprender a ligá-los a decisões.
- Formadores que procuram materiais prontos a usar.

## O que vais aprender

- Distinguir dado, informação, conhecimento e decisão.
- Classificar uma pergunta como descritiva, explicativa, preditiva ou de decisão, e escolher a abordagem certa.
- Desconfiar de associações, identificar variáveis de confusão e fugas de informação.
- Avaliar um modelo contra uma linha de base, ler uma matriz de confusão e escolher um limiar a partir dos custos dos erros.
- Reconhecer dados incompletos, ruidosos, enviesados e dependentes do contexto.
- Seguir o processo CRISP-DM e enquadrar um problema numa ficha de uma página.
- Escolher fontes de dados para uma pergunta e saber o que verificar em cada uma.
- Ler o significado de uma variável antes de calcular: tipos, unidades, datas e valores em falta.
- Levar dados em CSV, JSON, XML, HTML e texto livre até uma tabela.
- Auditar a qualidade de uma tabela, reparar com evidência e documentar o que fica por resolver.
- Aplicar o método científico: formular hipóteses testáveis, amostrar sem enviesar e quantificar a incerteza.
- Explorar dados: agrupar, resumir, visualizar, medir associações e analisar séries temporais.
- Preparar dados para um modelo: dividir em treino e teste, imputar, mudar escalas, codificar categorias e montar um *pipeline* sem fugas de informação.
- Construir e interpretar modelos lineares: regressão linear e logística de raiz, leitura dos coeficientes, regularização Ridge e Lasso.
- Treinar e avaliar modelos supervisionados: escolher métricas, implementar de raiz um KNN, uma árvore de decisão, uma floresta e um boosting, diagnosticar sobreajuste e escolher hiperparâmetros com validação cruzada.
- Encontrar estrutura sem alvo: agrupar com K-Means e com métodos hierárquicos, avaliar um agrupamento sem rótulos e reduzir dimensões com PCA.
- Levar um projeto do enquadramento à recomendação, combinando todas as etapas.
- Comunicar resultados a quem decide, dizer a incerteza, documentar um modelo, avaliá-lo por grupo e proteger os dados pessoais.
- Trabalhar com dados reais: lacunas na documentação, valores em falta disfarçados, mudanças ao longo do tempo e resultados que só se confirmam em dados posteriores.

---

## Estrutura do curso

O tutorial tem oito módulos, que devem ser feitos por ordem, e um projeto com dados reais, para fazer no fim. Os capítulos de cada módulo devem ser feitos por ordem.

### Módulo 1 – Do problema à decisão

Pasta [`modulo_1_do_problema_a_decisao`](modulo_1_do_problema_a_decisao).

| N.º | Capítulo | Conteúdos | Colab |
| --- | --- | --- | --- |
| 01 | [Dos dados à decisão](modulo_1_do_problema_a_decisao/01_Dos_Dados_a_Decisao.ipynb) | Porque ter dados não é ter respostas, *big data* e os cinco V, as quatro etapas de dados a decisão, o que é a ciência de dados e que competências junta, áreas de aplicação. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_1_do_problema_a_decisao/01_Dos_Dados_a_Decisao.ipynb) |
| 02 | [Da pergunta ao enquadramento](modulo_1_do_problema_a_decisao/02_Da_Pergunta_ao_Enquadramento.ipynb) | Perguntas descritivas, explicativas, preditivas e de decisão aplicadas aos mesmos dados; associação e causalidade (variável de confusão, paradoxo de Simpson); fuga de informação; cinco perguntas de enquadramento; da previsão à ação. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_1_do_problema_a_decisao/02_Da_Pergunta_ao_Enquadramento.ipynb) |
| 03 | [Uma boa previsão não garante uma boa decisão](modulo_1_do_problema_a_decisao/03_Previsao_nao_e_Decisao.ipynb) | Um modelo com 93% de exatidão que quase não ajuda; linha de base, matriz de confusão, sensibilidade e precisão; o limiar como decisão; custos dos erros e ponto de equilíbrio; limites de recursos; definir o sucesso antes de começar. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_1_do_problema_a_decisao/03_Previsao_nao_e_Decisao.ipynb) |
| 04 | [Dados imperfeitos e o processo de trabalho](modulo_1_do_problema_a_decisao/04_Dados_Imperfeitos_e_Processo.ipynb) | Fontes de dados; dados incompletos, ruidosos, enviesados e dependentes do contexto, cada um simulado; as seis fases do CRISP-DM; onde se gasta o tempo; ferramentas e reprodutibilidade. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_1_do_problema_a_decisao/04_Dados_Imperfeitos_e_Processo.ipynb) |
| 05 | [Método científico, amostragem e inferência](modulo_1_do_problema_a_decisao/05_Metodo_Cientifico_Amostragem_Inferencia.ipynb) | O método científico e a sua ligação ao CRISP-DM; hipóteses testáveis; população e amostra; amostragem aleatória, estratificada e por conveniência; intervalos de confiança por reamostragem; teste de hipóteses por permutação; comparações múltiplas. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_1_do_problema_a_decisao/05_Metodo_Cientifico_Amostragem_Inferencia.ipynb) |
| 06 | [Projeto: enquadrar um problema](modulo_1_do_problema_a_decisao/06_Projeto_Enquadrar_um_Problema.ipynb) | Ficha de enquadramento com oito componentes, exemplo resolvido, três cenários (perdas de água, livros esgotados, bicicletas partilhadas) e fichas possíveis. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_1_do_problema_a_decisao/06_Projeto_Enquadrar_um_Problema.ipynb) |

### Módulo 2 – Fontes, tipos e estruturas de dados

Pasta [`modulo_2_fontes_tipos_estruturas`](modulo_2_fontes_tipos_estruturas). Caso do módulo: uma cadeia de padarias que quer prever em que lojas o pão vai esgotar no dia seguinte.

| N.º | Capítulo | Conteúdos | Colab |
| --- | --- | --- | --- |
| 01 | [Fontes de dados](modulo_2_fontes_tipos_estruturas/01_Fontes_de_Dados.ipynb) | O contexto de um valor; fontes geradas por pessoas e por máquinas, primárias e secundárias; origem, acesso e conteúdo; alvo, momento da previsão e regra do rótulo; juntar fontes por chaves; cinco verificações antes de confiar numa fonte. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_2_fontes_tipos_estruturas/01_Fontes_de_Dados.ipynb) |
| 02 | [Tipos de dados: o que significam os valores](modulo_2_fontes_tipos_estruturas/02_Tipos_de_Dados.ipynb) | Variáveis nominais, ordinais, discretas e contínuas e as operações válidas em cada uma; significado e armazenamento; identificadores que parecem números; unidades, datas, fusos horários e valores em falta. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_2_fontes_tipos_estruturas/02_Tipos_de_Dados.ipynb) |
| 03 | [Estruturas e formatos](modulo_2_fontes_tipos_estruturas/03_Estruturas_e_Formatos.ipynb) | Dados estruturados, semiestruturados e não estruturados; esquema e a sua verificação; CSV (incluindo o formato português), JSON aninhado, XML e HTML; extrair variáveis de texto livre; comparação das três organizações. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_2_fontes_tipos_estruturas/03_Estruturas_e_Formatos.ipynb) |
| 04 | [Qualidade dos dados](modulo_2_fontes_tipos_estruturas/04_Qualidade_dos_Dados.ipynb) | Consistência, completude, validade, duplicação e enviesamento; auditoria passo a passo a um ficheiro com problemas; reparar com evidência e registar as decisões; o que a limpeza não corrige. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_2_fontes_tipos_estruturas/04_Qualidade_dos_Dados.ipynb) |
| 05 | [Projeto: desenhar um plano de dados](modulo_2_fontes_tipos_estruturas/05_Projeto_Plano_de_Dados.ipynb) | Plano de dados de uma página (previsão, fontes, variáveis e riscos), exemplo resolvido, três cenários (parque de estacionamento, biblioteca, recolha de resíduos) e planos possíveis. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_2_fontes_tipos_estruturas/05_Projeto_Plano_de_Dados.ipynb) |

### Módulo 3 – Explorar os dados

Pasta [`modulo_3_explorar_os_dados`](modulo_3_explorar_os_dados). Caso do módulo: o consumo diário de eletricidade de 30 escolas de um município, ao longo de um ano letivo.

| N.º | Capítulo | Conteúdos | Colab |
| --- | --- | --- | --- |
| 01 | [Revisão de Python, NumPy e pandas](modulo_3_explorar_os_dados/01_Revisao_Python_NumPy_Pandas.ipynb) | Revisão rápida em quatro partes, cada uma com um exercício de reforço: tipos e operadores; estruturas de dados e ciclos; vetores, operações vetorizadas e *broadcasting*; fatiamento, `loc` e `iloc`. Remete para os capítulos do tutorial de Python. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_3_explorar_os_dados/01_Revisao_Python_NumPy_Pandas.ipynb) |
| 02 | [Agrupar e remodelar](modulo_3_explorar_os_dados/02_Agrupar_e_Remodelar.ipynb) | Dados transversais, séries temporais e dados em painel; dividir–aplicar–combinar com `groupby`; agregar e transformar; formato longo e formato largo; juntar tabelas e comparar taxas. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_3_explorar_os_dados/02_Agrupar_e_Remodelar.ipynb) |
| 03 | [Medidas descritivas](modulo_3_explorar_os_dados/03_Medidas_Descritivas.ipynb) | Análise exploratória; média, mediana e moda; variância, desvio padrão e amplitude interquartil; porquê n − 1; quantis e diagrama de caixa; assimetria; medidas robustas; resumos que misturam grupos. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_3_explorar_os_dados/03_Medidas_Descritivas.ipynb) |
| 04 | [Visualização](modulo_3_explorar_os_dados/04_Visualizacao.ipynb) | O mesmo resumo com quatro formas diferentes; escolher o gráfico pela pergunta; classes de um histograma; eixos truncados, eixos duplos e gráficos circulares; do rascunho ao gráfico final; pequenos múltiplos. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_3_explorar_os_dados/04_Visualizacao.ipynb) |
| 05 | [Associação e correlações espúrias](modulo_3_explorar_os_dados/05_Associacao_e_Correlacoes_Espurias.ipynb) | Gráfico de dispersão; covariância; Pearson e Spearman; relações que a correlação não vê; matriz de correlações; terceira variável, tendência comum e comparações múltiplas. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_3_explorar_os_dados/05_Associacao_e_Correlacoes_Espurias.ipynb) |
| 06 | [Séries temporais](modulo_3_explorar_os_dados/06_Series_Temporais.ipynb) | Índice de datas; reamostragem e médias móveis; tendência, sazonalidade e resto; autocorrelação; variações e período homólogo; linhas de base de previsão; divisão temporal entre treino e teste. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_3_explorar_os_dados/06_Series_Temporais.ipynb) |
| 07 | [Projeto: análise exploratória de ponta a ponta](modulo_3_explorar_os_dados/07_Projeto_Analise_Exploratoria.ipynb) | Roteiro de sete passos aplicado a dados novos (entradas em 12 bibliotecas municipais), com soluções possíveis e um resumo de cinco frases para quem decide. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_3_explorar_os_dados/07_Projeto_Analise_Exploratoria.ipynb) |

### Módulo 4 – Preparar os dados para modelar

Pasta [`modulo_4_preparar_os_dados`](modulo_4_preparar_os_dados). Caso do módulo: um stand que quer propor o preço de anúncio de carros usados.

| N.º | Capítulo | Conteúdos | Colab |
| --- | --- | --- | --- |
| 01 | [O que é aprender com dados](modulo_4_preparar_os_dados/01_O_que_e_Aprender_com_Dados.ipynb) | Regras escritas e regras aprendidas; a definição de Mitchell (tarefa, experiência, desempenho); atributos, alvo, treinar e prever; regressão, classificação e aprendizagem não supervisionada; o que é ajustar um modelo; quando não usar aprendizagem automática. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_4_preparar_os_dados/01_O_que_e_Aprender_com_Dados.ipynb) |
| 02 | [Treino, teste e linha de base](modulo_4_preparar_os_dados/02_Treino_Teste_e_Linha_de_Base.ipynb) | Porque o erro de treino engana; dividir em treino e teste; estratificar; linhas de base; conjunto de validação; porque o teste só se usa uma vez; quando não dividir ao acaso. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_4_preparar_os_dados/02_Treino_Teste_e_Linha_de_Base.ipynb) |
| 03 | [Valores em falta e imputação](modulo_4_preparar_os_dados/03_Valores_em_Falta_e_Imputacao.ipynb) | Quanto falta e porquê; três mecanismos de falta; remover, preencher com a mediana, preencher por grupo e indicador de falta; efeito na distribuição e no modelo; aprender no treino e aplicar no teste. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_4_preparar_os_dados/03_Valores_em_Falta_e_Imputacao.ipynb) |
| 04 | [Escalas](modulo_4_preparar_os_dados/04_Escalas.ipynb) | Porque o maior número manda nas distâncias; padronização, Min-Max e escala robusta; efeito dos valores extremos; que modelos precisam de escala; o logaritmo para variáveis assimétricas e para o alvo. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_4_preparar_os_dados/04_Escalas.ipynb) |
| 05 | [Codificar categorias](modulo_4_preparar_os_dados/05_Codificar_Categorias.ipynb) | Porque não se numeram categorias nominais; codificação *one-hot*; variáveis ordinais; categorias raras, desconhecidas e numerosas; atributos a partir de datas; engenharia de atributos. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_4_preparar_os_dados/05_Codificar_Categorias.ipynb) |
| 06 | [*Pipelines* sem fuga de informação](modulo_4_preparar_os_dados/06_Pipelines_sem_Fuga_de_Informacao.ipynb) | Formas de fuga de informação; uma fuga que fabrica um modelo a partir de ruído; `Pipeline` e `ColumnTransformer`; quanto valeu cada passo de preparação; oito verificações antes de confiar num resultado. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_4_preparar_os_dados/06_Pipelines_sem_Fuga_de_Informacao.ipynb) |

### Módulo 5 – Modelos lineares

Pasta [`modulo_5_modelos_lineares`](modulo_5_modelos_lineares). Caso do módulo: uma empresa de painéis solares que quer estimar a produção de cada telhado e saber que orçamentos vão ser aceites.

| N.º | Capítulo | Conteúdos | Colab |
| --- | --- | --- | --- |
| 01 | [Regressão linear simples](modulo_5_modelos_lineares/01_Regressao_Linear_Simples.ipynb) | Declive e ordenada na origem; resíduos e mínimos quadrados; a reta calculada de raiz com a covariância e a variância; declive e correlação; R²; o que os resíduos mostram; quando uma reta engana; extrapolação. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_5_modelos_lineares/01_Regressao_Linear_Simples.ipynb) |
| 02 | [Regressão linear múltipla](modulo_5_modelos_lineares/02_Regressao_Linear_Multipla.ipynb) | Equação normal e descida do gradiente em NumPy; coeficientes «mantendo o resto constante»; categorias e referência; coeficientes normalizados; efeitos que se multiplicam e o logaritmo; colinearidade; pressupostos. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_5_modelos_lineares/02_Regressao_Linear_Multipla.ipynb) |
| 03 | [Regressão logística](modulo_5_modelos_lineares/03_Regressao_Logistica.ipynb) | Porque uma reta não serve para uma classe; sigmoide; possibilidades e razões de possibilidades; perda logarítmica; treino de raiz por descida do gradiente; fronteira de decisão linear; calibração das probabilidades. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_5_modelos_lineares/03_Regressao_Logistica.ipynb) |
| 04 | [Regularização: Ridge e Lasso](modulo_5_modelos_lineares/04_Regularizacao.ipynb) | Sobreajuste com muitos atributos e poucos dados; penalizar coeficientes; Ridge de raiz; escolher α com validação; Lasso e seleção de atributos; porque normalizar; o parâmetro C da regressão logística. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_5_modelos_lineares/04_Regularizacao.ipynb) |
| 05 | [Projeto: um modelo linear que se explica](modulo_5_modelos_lineares/05_Projeto_Modelo_Linear.ipynb) | Estimar o custo de obras de remodelação, em sete passos: uma reta que esconde três grupos, modelo múltiplo, resíduos e logaritmo, colinearidade e regularização, teste e uma previsão explicada parcela a parcela. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_5_modelos_lineares/05_Projeto_Modelo_Linear.ipynb) |

### Módulo 6 – Modelos supervisionados

Pasta [`modulo_6_modelos_supervisionados`](modulo_6_modelos_supervisionados). Caso do módulo: uma empresa de distribuição urbana que quer prever que entregas vão atrasar e quanto tempo demora cada uma.

| N.º | Capítulo | Conteúdos | Colab |
| --- | --- | --- | --- |
| 01 | [Métricas de avaliação](modulo_6_modelos_supervisionados/01_Metricas_de_Avaliacao.ipynb) | Matriz de confusão; exatidão, precisão, sensibilidade, especificidade e F1; o limiar; curvas precisão–sensibilidade e ROC, AUC; MAE, MSE, RMSE, MAPE e R²; efeito dos valores extremos; análise de resíduos. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_6_modelos_supervisionados/01_Metricas_de_Avaliacao.ipynb) |
| 02 | [K vizinhos mais próximos: classificação](modulo_6_modelos_supervisionados/02_KNN_Classificacao.ipynb) | Aprender por semelhança; distâncias euclidiana e de Manhattan; KNN implementado em NumPy; normalização; fronteiras de decisão; escolha de k; atributos irrelevantes; votos ponderados. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_6_modelos_supervisionados/02_KNN_Classificacao.ipynb) |
| 03 | [K vizinhos mais próximos: regressão](modulo_6_modelos_supervisionados/03_KNN_Regressao.ipynb) | Média simples e média ponderada pelo inverso da distância, implementadas de raiz; curva de previsão e efeito de k; comparação com a regressão linear pelos resíduos; extrapolação; maldição da dimensionalidade. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_6_modelos_supervisionados/03_KNN_Regressao.ipynb) |
| 04 | [Árvores de decisão](modulo_6_modelos_supervisionados/04_Arvores_de_Decisao.ipynb) | Ler uma árvore; índice de Gini e ganho; procura da melhor divisão e crescimento recursivo implementados de raiz; regiões retangulares; profundidade e tamanho das folhas; importância dos atributos; árvores de regressão; instabilidade; KNN ou árvore. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_6_modelos_supervisionados/04_Arvores_de_Decisao.ipynb) |
| 05 | [Sobreajuste, viés e variância](modulo_6_modelos_supervisionados/05_Sobreajuste_Vies_e_Variancia.ipynb) | Subajuste e sobreajuste num mundo simulado; um modelo que memoriza ruído; decomposição do erro em viés, variância e ruído, medida por simulação; diagnóstico com os erros de treino e de validação; curvas de aprendizagem; que remédio para que problema. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_6_modelos_supervisionados/05_Sobreajuste_Vies_e_Variancia.ipynb) |
| 06 | [Validação cruzada e escolha de hiperparâmetros](modulo_6_modelos_supervisionados/06_Validacao_Cruzada.ipynb) | Porque uma divisão é um sorteio; validação cruzada com K partes implementada de raiz; variantes estratificada, por grupos e temporal; procura em grelha; a fuga de preparar antes de dividir; o protocolo completo até ao teste. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_6_modelos_supervisionados/06_Validacao_Cruzada.ipynb) |
| 07 | [Florestas aleatórias](modulo_6_modelos_supervisionados/07_Florestas_Aleatorias.ipynb) | A média de muitas árvores; amostras bootstrap; bagging implementado de raiz; sorteio de atributos; erro out-of-bag; hiperparâmetros; importância por permutação; o que se ganha e o que se perde. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_6_modelos_supervisionados/07_Florestas_Aleatorias.ipynb) |
| 08 | [Boosting](modulo_6_modelos_supervisionados/08_Boosting.ipynb) | Corrigir erros em sequência; gradient boosting implementado de raiz; taxa de aprendizagem e número de árvores; paragem antecipada; implementações por histograma; bagging e boosting; que modelo escolher. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_6_modelos_supervisionados/08_Boosting.ipynb) |
| 09 | [Projeto: um modelo supervisionado de ponta a ponta](modulo_6_modelos_supervisionados/09_Projeto_Modelo_Supervisionado.ipynb) | Cancelamentos num ginásio, em oito passos: enquadrar, detetar uma fuga, pipeline, KNN, árvore, diagnóstico, limiar pelo custo e teste, explicação; resumo para quem decide. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_6_modelos_supervisionados/09_Projeto_Modelo_Supervisionado.ipynb) |

### Módulo 7 – Aprendizagem não supervisionada

Pasta [`modulo_7_aprendizagem_nao_supervisionada`](modulo_7_aprendizagem_nao_supervisionada). Caso do módulo: uma aplicação de aprendizagem de línguas que quer conhecer os tipos de utilizadores que tem.

| N.º | Capítulo | Conteúdos | Colab |
| --- | --- | --- | --- |
| 01 | [Agrupar sem rótulos: K-Means](modulo_7_aprendizagem_nao_supervisionada/01_KMeans.ipynb) | Aprendizagem supervisionada e não supervisionada; atribuir e atualizar; K-Means implementado em NumPy; inércia; inicialização e mínimos locais; efeito da escala; descrever os grupos e dar-lhes nome; limitações. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_7_aprendizagem_nao_supervisionada/01_KMeans.ipynb) |
| 02 | [Quantos grupos? Avaliar sem rótulos](modulo_7_aprendizagem_nao_supervisionada/02_Avaliar_sem_Rotulos.ipynb) | O método do cotovelo e os seus limites; coeficiente de silhueta calculado de raiz; gráfico de silhuetas; estabilidade e índice de Rand ajustado; comparação com dados sem estrutura; validação interna, externa e por utilidade. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_7_aprendizagem_nao_supervisionada/02_Avaliar_sem_Rotulos.ipynb) |
| 03 | [Agrupamento hierárquico](modulo_7_aprendizagem_nao_supervisionada/03_Agrupamento_Hierarquico.ipynb) | Algoritmo aglomerativo implementado de raiz; ligações simples, completa, média e de Ward; ler e cortar um dendrograma; efeito de cadeia; hierarquia de perfis; K-Means ou hierárquico. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_7_aprendizagem_nao_supervisionada/03_Agrupamento_Hierarquico.ipynb) |
| 04 | [Reduzir dimensões: análise de componentes principais](modulo_7_aprendizagem_nao_supervisionada/04_PCA.ipynb) | Colunas correlacionadas e redundância; a direção de maior variância; PCA em NumPy (covariâncias, valores e vetores próprios); variância explicada; interpretar os pesos; mapa dos dados em duas componentes; reconstrução; cuidados. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_7_aprendizagem_nao_supervisionada/04_PCA.ipynb) |
| 05 | [Projeto final: do problema à decisão](modulo_7_aprendizagem_nao_supervisionada/05_Projeto_Final.ipynb) | Onde instalar 15 postos de carregamento, em oito passos que percorrem os seis módulos: enquadrar, verificar, explorar, segmentar, preparar, modelar, decidir e comunicar; as ideias que atravessam o tutorial. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_7_aprendizagem_nao_supervisionada/05_Projeto_Final.ipynb) |

### Módulo 8 – Comunicar e usar com responsabilidade

Pasta [`modulo_8_comunicar_e_usar_com_responsabilidade`](modulo_8_comunicar_e_usar_com_responsabilidade). Caso do módulo: um centro de formação profissional que quer saber que formandos estão em risco de desistir.

| N.º | Capítulo | Conteúdos | Colab |
| --- | --- | --- | --- |
| 01 | [Do resultado à mensagem](modulo_8_comunicar_e_usar_com_responsabilidade/01_Do_Resultado_a_Mensagem.ipynb) | Resultado e mensagem; o leitor e a decisão; frequências naturais; termos de comparação; a conclusão primeiro; título-mensagem; o relatório de uma página; o mesmo trabalho para leitores diferentes. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_8_comunicar_e_usar_com_responsabilidade/01_Do_Resultado_a_Mensagem.ipynb) |
| 02 | [Gráficos para explicar](modulo_8_comunicar_e_usar_com_responsabilidade/02_Graficos_para_Explicar.ipynb) | Explorar e explicar; um gráfico antes e depois; escolher o gráfico pela mensagem; cor, nomes diretos e anotações; retirar o que não informa; eixos cortados, eixos duplos e janelas escolhidas; acessibilidade. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_8_comunicar_e_usar_com_responsabilidade/02_Graficos_para_Explicar.ipynb) |
| 03 | [Comunicar a incerteza](modulo_8_comunicar_e_usar_com_responsabilidade/03_Comunicar_a_Incerteza.ipynb) | Uma métrica é uma estimativa; intervalos por bootstrap para qualquer métrica; tamanho da amostra; intervalo da diferença entre dois modelos; grupos pequenos e gráfico em funil; o que significa um risco de 30%; o que um intervalo não cobre. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_8_comunicar_e_usar_com_responsabilidade/03_Comunicar_a_Incerteza.ipynb) |
| 04 | [Documentar e acompanhar um modelo](modulo_8_comunicar_e_usar_com_responsabilidade/04_Documentar_e_Acompanhar_um_Modelo.ipynb) | Ficha do modelo e ficha dos dados; documentação gerada a partir do código; guardar o pipeline; deriva das entradas, da relação e da medição; vigiar entradas, previsões e desempenho; quando rever ou suspender. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_8_comunicar_e_usar_com_responsabilidade/04_Documentar_e_Acompanhar_um_Modelo.ipynb) |
| 05 | [Equidade: para quem é que o modelo funciona?](modulo_8_comunicar_e_usar_com_responsabilidade/05_Equidade.ipynb) | Avaliação por grupo; quem é prejudicado depende do uso; calibração por grupo; porque retirar o atributo não resolve; paridade, igualdade de oportunidades e significado da pontuação; o custo de cada política; origens do enviesamento. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_8_comunicar_e_usar_com_responsabilidade/05_Equidade.ipynb) |
| 06 | [Privacidade e dados pessoais](modulo_8_comunicar_e_usar_com_responsabilidade/06_Privacidade_e_Dados_Pessoais.ipynb) | Dados pessoais e quase-identificadores; princípios do RGPD; pseudonimizar e anonimizar; reidentificação por ligação; k-anonimato, generalização e supressão; células pequenas; hábitos de trabalho. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_8_comunicar_e_usar_com_responsabilidade/06_Privacidade_e_Dados_Pessoais.ipynb) |
| 07 | [Projeto: um relatório e uma ficha de modelo](modulo_8_comunicar_e_usar_com_responsabilidade/07_Projeto_Relatorio_e_Ficha.ipynb) | Uma empresa de águas e os atrasos de pagamento, em sete passos: leitor, números em pessoas, margem, um gráfico, avaliação por grupo, dados pessoais, relatório de uma página e ficha do modelo. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_8_comunicar_e_usar_com_responsabilidade/07_Projeto_Relatorio_e_Ficha.ipynb) |

### Projeto com dados reais

Pasta [`projeto_dados_reais`](projeto_dados_reais). Os módulos usam dados sintéticos; este projeto aplica o percurso completo a **dados reais**: mais de 41 000 chamadas de campanhas de telemarketing de um banco português (2008 a 2010), do conjunto *Bank Marketing* (S. Moro, P. Cortez e P. Rita, 2014; UCI Machine Learning Repository; CC BY 4.0). O ficheiro está na pasta [`dados`](projeto_dados_reais/dados), com a descrição da fonte.

| Parte | Notebook | Conteúdos | Colab |
| --- | --- | --- | --- |
| 1 | [Enquadrar o problema e auditar os dados](projeto_dados_reais/01_Enquadrar_e_Auditar_os_Dados.ipynb) | Avaliar a fonte; ficha de enquadramento; dicionário de dados; valores em falta disfarçados (`unknown` e 999); duplicados sem identificador; reconstruir o tempo a partir da documentação; campanhas que mudam; o que se conhece no momento da previsão. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/projeto_dados_reais/01_Enquadrar_e_Auditar_os_Dados.ipynb) |
| 2 | [Explorar, dividir e modelar](projeto_dados_reais/02_Explorar_Dividir_e_Modelar.ipynb) | Separar o teste pelo tempo; explorar sem misturar épocas; divisão aleatória contra divisão temporal; uma fuga e colunas que são calendário; métrica ligada à decisão; uma regra simples contra regressão logística e boosting; teste com intervalo. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/projeto_dados_reais/02_Explorar_Dividir_e_Modelar.ipynb) |
| 3 | [Decidir, verificar e comunicar](projeto_dados_reais/03_Decidir_Verificar_e_Comunicar.ipynb) | Resultado por capacidade; o que mudou entre o desenvolvimento e o teste; probabilidades que não resistem à mudança; acompanhamento mensal; avaliação por idade; quase-identificadores e minimização; ficha da solução e relatório de uma página. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/projeto_dados_reais/03_Decidir_Verificar_e_Comunicar.ipynb) |

---

## Fichas de consulta rápida

Pasta [`consulta_rapida`](consulta_rapida). São resumos em PDF (A4 na horizontal), um por módulo, para imprimir ou ter abertos ao lado do notebook. Cada bloco indica o capítulo onde o tema é explicado, e a maior parte das fichas inclui blocos com as armadilhas mais frequentes.

| Ficha | Conteúdos | Módulo |
| --- | --- | --- |
| [Do problema à decisão](consulta_rapida/Consulta_Rapida_1_Do_Problema_a_Decisao.pdf) | 2 páginas: de dados a decisão, tipos de pergunta, ficha de enquadramento, métricas e limiar; dados imperfeitos, CRISP-DM, amostragem, intervalos de confiança e testes de hipóteses. | 1 |
| [Fontes, tipos e estruturas](consulta_rapida/Consulta_Rapida_2_Fontes_Tipos_Estruturas.pdf) | 2 páginas: alvo e momento da previsão, classificar e verificar fontes, tipos de variáveis e armadilhas; formatos (CSV, JSON, XML), esquema, auditoria de qualidade e plano de dados. | 2 |
| [Explorar os dados](consulta_rapida/Consulta_Rapida_3_Explorar_os_Dados.pdf) | 2 páginas: selecionar, agrupar, remodelar e juntar com pandas, medidas descritivas; escolha de gráficos, matplotlib, correlação e séries temporais. | 3 |
| [Preparar os dados](consulta_rapida/Consulta_Rapida_4_Preparar_os_Dados.pdf) | 2 páginas: vocabulário, treino e teste, linha de base, valores em falta; escalas, codificação de categorias, pipelines e fugas de informação. | 4 |
| [Modelos lineares](consulta_rapida/Consulta_Rapida_5_Modelos_Lineares.pdf) | 2 páginas: regressão linear de raiz e com o scikit-learn, leitura de coeficientes e pressupostos; regressão logística, calibração, Ridge e Lasso. | 5 |
| [Modelos supervisionados](consulta_rapida/Consulta_Rapida_6_Modelos_Supervisionados.pdf) | 3 páginas: métricas e KNN; árvores, viés e variância, validação cruzada e procura em grelha; florestas aleatórias, boosting e escolha do modelo. | 6 |
| [Aprendizagem não supervisionada](consulta_rapida/Consulta_Rapida_7_Aprendizagem_Nao_Supervisionada.pdf) | 2 páginas: K-Means, silhueta, validação e agrupamento hierárquico; PCA de raiz e com o scikit-learn, o percurso completo e as ideias que atravessam o tutorial. | 7 |
| [Comunicar e usar com responsabilidade](consulta_rapida/Consulta_Rapida_8_Comunicar_e_Responsabilidade.pdf) | 2 páginas: mensagem, relatório de uma página, gráficos para explicar e incerteza; ficha do modelo, deriva, equidade e dados pessoais. | 8 |

---

## Como usar

### No Google Colab (recomendado para começar)

1. Carrega no botão **«Abrir no Colab»** do capítulo que queres estudar.
2. Para guardar as tuas alterações, usa **Ficheiro → Guardar uma cópia no Drive**.
3. Executa as células por ordem, com `Shift + Enter`.

### No computador (Jupyter ou VS Code)

```bash
git clone https://github.com/ricardoluizdasilva/mestrado_ai_estudos.git
cd "mestrado_ai_estudos/Introdução à Ciência de Dados/tutorial_ciencia_dados"
python -m pip install -r requirements.txt
```

Depois abre a pasta no Jupyter (`jupyter lab`) ou no VS Code (com a extensão Jupyter) e escolhe um kernel **Python 3.10 ou superior**.

Se ainda não programas em Python, começa pelo tutorial [Introdução ao Python](../../Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python). O módulo 3 abre com uma revisão rápida, e cada capítulo indica os capítulos desse tutorial onde a sintaxe é explicada.

### Glossário

O tutorial usa os termos em português. O [glossário português–inglês](GLOSSARIO.md) faz a correspondência com os termos da documentação em inglês e indica o capítulo em que cada um é apresentado.

### Convenções dos notebooks

- Cada capítulo abre com os **objetivos** e os **pré-requisitos**.
- Os gráficos de dados são desenhados pelo código das células. Os esquemas são imagens embutidas no notebook ou, nos capítulos mais recentes, desenhados com as funções `tela`, `caixa` e `seta` definidas no início de cada notebook.
- 💡 **Soluções:** os exercícios têm uma solução escondida num bloco «Ver uma solução possível». Tenta primeiro sozinho!
- ✅ **Verifica o que aprendeste:** cada capítulo termina com uma lista de verificação.
- Os notebooks são guardados **com as saídas** de uma execução de referência, para que os esquemas e os gráficos se vejam diretamente no GitHub.
- Os dados são gerados com uma semente fixa, por isso os números do texto coincidem com os que obténs ao executar.

### Verificação automática

Sempre que o tutorial é alterado, o GitHub executa todos os notebooks (fluxo [`notebooks_ciencia_dados.yml`](../../.github/workflows/notebooks_ciencia_dados.yml)) e o selo no início desta página mostra o resultado. A verificação também corre no dia 1 de cada mês, para detetar alterações nas bibliotecas.

Para fazer a mesma verificação no teu computador, a partir desta pasta:

```bash
python ferramentas/verificar_notebooks.py
```

Os notebooks são executados numa cópia temporária, por isso os originais não são alterados.

---

## Requisitos

| Componente | Versão |
| --- | --- |
| Python | 3.10 ou superior |
| NumPy | 2.x |
| pandas | 2.2 ou superior (testado com 3.0) |
| scikit-learn | 1.6 ou superior (módulo 1, capítulo 3, e módulos 4 a 8) |
| SciPy | 1.13 ou superior (módulos 7 e 8; é instalado com o scikit-learn) |
| matplotlib | 3.10 ou superior |

O Google Colab já inclui todas estas bibliotecas.

## Estrutura do repositório

```text
tutorial_ciencia_dados/
├── README.md                          ← este ficheiro
├── GLOSSARIO.md                       ← termos em português e em inglês
├── LICENSE.md                         ← licenças (conteúdos e código)
├── LICENSE-CC-BY-NC-SA-4.0.txt
├── LICENSE-MIT.txt
├── requirements.txt
├── ferramentas/
│   └── verificar_notebooks.py         ← executa os notebooks e procura erros
├── consulta_rapida/                   ← fichas de consulta rápida em PDF, uma por módulo
├── modulo_1_do_problema_a_decisao/
│   ├── 01_Dos_Dados_a_Decisao.ipynb
│   ├── 02_Da_Pergunta_ao_Enquadramento.ipynb
│   ├── 03_Previsao_nao_e_Decisao.ipynb
│   ├── 04_Dados_Imperfeitos_e_Processo.ipynb
│   ├── 05_Metodo_Cientifico_Amostragem_Inferencia.ipynb
│   └── 06_Projeto_Enquadrar_um_Problema.ipynb
├── modulo_2_fontes_tipos_estruturas/
│   ├── 01_Fontes_de_Dados.ipynb
│   ├── 02_Tipos_de_Dados.ipynb
│   ├── 03_Estruturas_e_Formatos.ipynb
│   ├── 04_Qualidade_dos_Dados.ipynb
│   └── 05_Projeto_Plano_de_Dados.ipynb
├── modulo_3_explorar_os_dados/
│   ├── 01_Revisao_Python_NumPy_Pandas.ipynb
│   ├── 02_Agrupar_e_Remodelar.ipynb
│   ├── 03_Medidas_Descritivas.ipynb
│   ├── 04_Visualizacao.ipynb
│   ├── 05_Associacao_e_Correlacoes_Espurias.ipynb
│   ├── 06_Series_Temporais.ipynb
│   └── 07_Projeto_Analise_Exploratoria.ipynb
├── modulo_4_preparar_os_dados/
│   ├── 01_O_que_e_Aprender_com_Dados.ipynb
│   ├── 02_Treino_Teste_e_Linha_de_Base.ipynb
│   ├── 03_Valores_em_Falta_e_Imputacao.ipynb
│   ├── 04_Escalas.ipynb
│   ├── 05_Codificar_Categorias.ipynb
│   └── 06_Pipelines_sem_Fuga_de_Informacao.ipynb
├── modulo_5_modelos_lineares/
│   ├── 01_Regressao_Linear_Simples.ipynb
│   ├── 02_Regressao_Linear_Multipla.ipynb
│   ├── 03_Regressao_Logistica.ipynb
│   ├── 04_Regularizacao.ipynb
│   └── 05_Projeto_Modelo_Linear.ipynb
├── modulo_6_modelos_supervisionados/
│   ├── 01_Metricas_de_Avaliacao.ipynb
│   ├── 02_KNN_Classificacao.ipynb
│   ├── 03_KNN_Regressao.ipynb
│   ├── 04_Arvores_de_Decisao.ipynb
│   ├── 05_Sobreajuste_Vies_e_Variancia.ipynb
│   ├── 06_Validacao_Cruzada.ipynb
│   ├── 07_Florestas_Aleatorias.ipynb
│   ├── 08_Boosting.ipynb
│   └── 09_Projeto_Modelo_Supervisionado.ipynb
├── modulo_7_aprendizagem_nao_supervisionada/
│   ├── 01_KMeans.ipynb
│   ├── 02_Avaliar_sem_Rotulos.ipynb
│   ├── 03_Agrupamento_Hierarquico.ipynb
│   ├── 04_PCA.ipynb
│   └── 05_Projeto_Final.ipynb
├── modulo_8_comunicar_e_usar_com_responsabilidade/
│   ├── 01_Do_Resultado_a_Mensagem.ipynb
│   ├── 02_Graficos_para_Explicar.ipynb
│   ├── 03_Comunicar_a_Incerteza.ipynb
│   ├── 04_Documentar_e_Acompanhar_um_Modelo.ipynb
│   ├── 05_Equidade.ipynb
│   ├── 06_Privacidade_e_Dados_Pessoais.ipynb
│   └── 07_Projeto_Relatorio_e_Ficha.ipynb
└── projeto_dados_reais/
    ├── dados/
    │   ├── bank-additional-full.csv   ← dados reais (Bank Marketing, CC BY 4.0)
    │   └── LEIA-ME.md                 ← fonte, citação e licença dos dados
    ├── 01_Enquadrar_e_Auditar_os_Dados.ipynb
    ├── 02_Explorar_Dividir_e_Modelar.ipynb
    └── 03_Decidir_Verificar_e_Comunicar.ipynb
```

## Licença

- **Conteúdos** (textos, exercícios, imagens e notebooks): [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.pt). Podes partilhar e adaptar para fins não comerciais, indicando o autor e mantendo a mesma licença.
- **Código** (ficheiros `.py`, código das células e verificação automática): [MIT](LICENSE-MIT.txt).

Os detalhes e a sugestão de atribuição estão em [`LICENSE.md`](LICENSE.md).

## Autor

Desenvolvido por **RLdS** (Ricardo Luiz da Silva). Sugestões e correções são bem-vindas através de *issues* ou *pull requests*.
