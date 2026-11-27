# Estudo de caso: modelos fundacionais para dados tabulares (TabPFN)

**Um estudo prático, em notebooks e em português europeu, sobre quando um modelo fundacional tabular compensa face às árvores com *gradient boosting*.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![Estado](https://img.shields.io/badge/estado-fase%201%20de%207-orange) ![Idioma](https://img.shields.io/badge/idioma-português%20(PT)-green) [![Licença: CC BY-NC-SA 4.0](https://img.shields.io/badge/licen%C3%A7a-CC%20BY--NC--SA%204.0-lightgrey)](LICENSE.md) [![Código: MIT](https://img.shields.io/badge/c%C3%B3digo-MIT-yellow)](LICENSE-MIT.txt)

Durante mais de uma década, os algoritmos de árvores com *gradient boosting* (XGBoost, LightGBM, CatBoost) foram a escolha por omissão para dados tabulares. Os modelos fundacionais tabulares, de que o **TabPFN** é o exemplo mais conhecido, propõem outra forma de trabalhar: um *Transformer* pré-treinado em dados sintéticos recebe a tabela de treino como contexto e prevê diretamente, sem treino nem afinação.

Este estudo testa essa proposta com um protocolo que distingue uma diferença real de ruído de amostragem, primeiro em conjuntos de dados clássicos e depois numa base original, recente e que não faz parte de nenhum *benchmark*: a **abstenção nas eleições gerais do Brasil de 2026, por município**.

> **Estado atual (27 de novembro de 2026):** fase 0 concluída, fase 1 a começar. O plano completo, com datas e entregáveis, está em [`CRONOGRAMA.md`](CRONOGRAMA.md). Este repositório é atualizado à medida que o estudo avança.

---

## Perguntas do estudo

1. Sem afinação, o TabPFN iguala ou supera um LightGBM afinado em conjuntos pequenos e médios?
2. Essa conclusão mantém-se entre domínios, tipos de variáveis e graus de desequilíbrio das classes?
3. Como se comporta numa base real e nova, em regressão e com validação por grupos geográficos?
4. Quanto custa em tempo de inferência, hardware e restrições de licença?
5. Em que situações práticas vale a pena usá-lo?

## Onde está o estudo

| Fase | Tema | Estado | Conteúdo |
| --- | --- | --- | --- |
| 0 | Trabalho preliminar | Concluída | [`fase_0_preliminar`](fase_0_preliminar) |
| 1 | Fundamentos e primeira execução | A começar | – |
| 2 | Robustez em classificação | Planeada | – |
| 3 | Preparar a base de abstenção para modelar | Planeada | – |
| 4 | Regressão na base de abstenção | Planeada | – |
| 5 | Classificação, calibração e decisão | Planeada | – |
| 6 | Aprofundamento: versões, escala, custo e interpretação | Planeada | – |
| 7 | Síntese e conclusões | Planeada | – |

### Fase 0 – Trabalho preliminar

| N.º | Notebook | Conteúdos | Estado | Colab |
| --- | --- | --- | --- | --- |
| 01 | [TabPFN contra LightGBM num problema de crédito](fase_0_preliminar/01_TabPFN_vs_LightGBM_Credito.ipynb) | Como funciona o TabPFN; licença e autenticação; cinco modelos comparados no conjunto `credit-g`; validação cruzada repetida, intervalos *bootstrap* e teste emparelhado corrigido; tempos de `fit` e `predict` em separado; conclusões geradas a partir dos resultados. | Escrito e testado com um modelo de substituição. **Falta executar com o TabPFN real** (fase 1). | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Estudos%20de%20Caso/estudo_caso_tabpfn/fase_0_preliminar/01_TabPFN_vs_LightGBM_Credito.ipynb) |
| 02 | [Recolha da base por município: IBGE e TSE](fase_0_preliminar/02_Recolha_Base_Municipios_IBGE_TSE.ipynb) | Extração de indicadores do Censo 2022 (SIDRA), resultados e perfil do eleitorado das eleições de 2026 (TSE); correspondência de códigos de município; validação e dicionário de variáveis. | Executado com dados reais e validado. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Estudos%20de%20Caso/estudo_caso_tabpfn/fase_0_preliminar/02_Recolha_Base_Municipios_IBGE_TSE.ipynb) |

## A base de dados do estudo de caso

A pasta [`dados`](dados) contém a base construída no notebook 02: **5 571 municípios e 61 colunas**, com uma linha por município.

| Grupo de variáveis | Origem | Exemplos |
| --- | --- | --- |
| Alvo | TSE, resultados de 2026 | Taxa de abstenção na 1.ª e na 2.ª volta |
| Composição do eleitorado | TSE, eleitorado de 2026 | Grupos de idade, níveis de escolaridade, voto facultativo |
| Qualidade do cadastro | TSE, eleitorado de 2026 | Eleitores com biometria, registos sem escolaridade informada |
| Condições socioeconómicas | IBGE, Censo 2022 | Rendimento domiciliar per capita, nível de ocupação, classes de rendimento |
| Geografia | IBGE | Estado, região, regiões intermédia e imediata |

O que já se sabe sobre esta base:

- A abstenção nacional foi de 20,84 % na 1.ª volta e de 18,99 % na 2.ª (sem o voto no exterior), e variou entre 7,3 % e 40,1 % de município para município.
- O rendimento quase não se associa à abstenção (correlação de Spearman de 0,02). A associação mais forte é com a percentagem de eleitores com biometria (−0,33).
- Há um padrão geográfico marcado, o que obriga a validar os modelos por estado e não por partições aleatórias.

A proveniência, as licenças e as limitações dos dados estão em [`dados/LEIA-ME.md`](dados/LEIA-ME.md).

## Como executar

Os notebooks foram pensados para o **Google Colab** com GPU (`Ambiente de execução > Alterar tipo de ambiente de execução > GPU T4`). Também correm em Jupyter ou VS Code, depois de instalar as bibliotecas:

```
pip install -r requirements.txt
```

Três coisas a saber antes de correr o TabPFN:

- **Versão fixa.** O pacote `tabpfn` muda o modelo por omissão entre versões. O estudo fixa a versão 10.2.0, em que o modelo por omissão é o TabPFN-3.5.
- **Licença dos pesos.** Os pesos das versões 2.5 e posteriores têm licença **não comercial** e exigem uma conta na Prior Labs e um *token* (`TABPFN_TOKEN`). Os pesos da versão 2 são abertos e não exigem autenticação. O notebook 01 explica o processo e usa a versão 2 quando não encontra o *token*.
- **GPU.** Em CPU, o pacote recusa por omissão conjuntos de treino com mais de 1 000 linhas. A base de abstenção tem cerca de 4 500 linhas de treino por partição, pelo que precisa de GPU.

## Método de comparação

Todas as comparações deste estudo seguem as mesmas regras, descritas em pormenor na [wiki](https://github.com/ricardoluizdasilva/mestrado_ai_estudos/wiki):

- Uma linha de base trivial e um modelo linear em todas as comparações.
- LightGBM avaliado com os valores de fábrica e também afinado, com a afinação feita dentro de cada partição.
- Pré-processamento dentro de *pipelines*, ajustado só nos dados de treino.
- Validação cruzada repetida; por grupos, quando os dados têm estrutura geográfica.
- Diferenças entre modelos avaliadas partição a partição, com um teste corrigido para reamostragem.
- Tempos de preparação e de previsão medidos em separado.
- Conclusões escritas a partir dos resultados de cada execução, e não antes.

## Estrutura de pastas

```
estudo_caso_tabpfn/
├── README.md                  ← este ficheiro
├── CRONOGRAMA.md              ← plano, datas, entregáveis e registo de alterações
├── requirements.txt           ← bibliotecas e versões
├── LICENSE.md                 ← licenças dos conteúdos, do código e dos dados
├── dados/
│   ├── base_municipios_eleicoes2026_censo2022.csv   ← base por município (TSE + IBGE)
│   ├── base_municipios_dicionario.csv               ← dicionário de variáveis
│   └── LEIA-ME.md                                   ← fontes, licenças e limitações
└── fase_0_preliminar/
    ├── 01_TabPFN_vs_LightGBM_Credito.ipynb
    └── 02_Recolha_Base_Municipios_IBGE_TSE.ipynb
```

As pastas das fases seguintes são criadas à medida que cada uma começa.

## Referências

- Hollmann et al., *Accurate predictions on small data with a tabular foundation model*, Nature, 2025 (TabPFN v2).
- Prior Labs, *TabPFN-2.5: Advancing the State of the Art in Tabular Foundation Models*, 2025: <https://arxiv.org/abs/2511.08667>
- Erickson et al., *TabArena: A Living Benchmark for Machine Learning on Tabular Data*, 2025.
- Nadeau e Bengio, *Inference for the Generalization Error*, Machine Learning, 2003.
- Repositório e documentação do TabPFN: <https://github.com/PriorLabs/TabPFN> e <https://docs.priorlabs.ai>

## Licença

- **Conteúdos** (textos e notebooks): [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.pt).
- **Código** (células dos notebooks e ficheiros `.py`): [MIT](LICENSE-MIT.txt).
- **Dados**: mantêm as licenças das fontes originais, indicadas em [`dados/LEIA-ME.md`](dados/LEIA-ME.md).

Os detalhes estão em [`LICENSE.md`](LICENSE.md).

## Autor

Desenvolvido por **RLdS** (Ricardo Luiz da Silva). É um estudo pessoal e independente: não tem ligação à Prior Labs nem a qualquer entidade que desenvolva os modelos analisados. Sugestões e correções são bem-vindas através de *issues* ou *pull requests*.
