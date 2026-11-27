# Aprendizagem Automática (Machine Learning)

**Tutorial de aprendizagem automática, dos dados à previsão, em notebooks Jupyter e em português europeu.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![Notebooks](https://img.shields.io/badge/notebooks-3-orange) ![Idioma](https://img.shields.io/badge/idioma-português%20(PT)-green) [![Licença: CC BY-NC-SA 4.0](https://img.shields.io/badge/licen%C3%A7a-CC%20BY--NC--SA%204.0-lightgrey)](LICENSE.md) [![Código: MIT](https://img.shields.io/badge/c%C3%B3digo-MIT-yellow)](LICENSE-MIT.txt) [![Verificação dos notebooks](https://github.com/ricardoluizdasilva/mestrado_ai_estudos/actions/workflows/notebooks_machine_learning.yml/badge.svg)](https://github.com/ricardoluizdasilva/mestrado_ai_estudos/actions/workflows/notebooks_machine_learning.yml)

Este tutorial trata dos modelos de aprendizagem automática (*machine learning*): como funcionam por dentro, como se afinam e comparam de forma justa, como se explicam e como se põem a funcionar. Cada capítulo combina explicações curtas, esquemas, gráficos gerados pelo próprio código, exemplos executáveis e exercícios com soluções.

É a continuação de dois tutoriais do mesmo repositório:

- [Introdução ao Python](../../Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python), para a linguagem e as bibliotecas;
- [Introdução à Ciência de Dados](../../Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados), para o raciocínio do problema à decisão e para uma primeira passagem pelos modelos.

Quando um assunto já foi tratado num deles, este tutorial não o repete: o módulo abre com um capítulo **«Relembrar»**, com um resumo, exercícios de reforço com soluções e a ligação para o capítulo de origem. Os capítulos seguintes tratam do que é novo.

Cada módulo acompanha um caso do princípio ao fim, com **dados sintéticos** gerados dentro de cada notebook. No módulo 1, um lagar cooperativo que quer confirmar a variedade dos lotes de azeitona, prever o rendimento em azeite e escolher o programa de extração.

Os notebooks funcionam no **Google Colab** (sem instalar nada), no **Jupyter** e no **VS Code**. Cada notebook tem um botão «Abrir no Colab».

---

## Para quem é

- Quem já treinou os primeiros modelos e quer perceber o que eles fazem e como os melhorar.
- Quem fez o tutorial de ciência de dados e quer ir mais longe nos modelos.
- Formadores que procuram materiais prontos a usar.

## Estrutura do curso

O tutorial está organizado em três partes e catorze módulos, que devem ser feitos por ordem. Está em construção: o módulo 1 está disponível e os restantes serão acrescentados por esta ordem.

### Parte I – Fundamentos

#### Módulo 1 – Aprender com dados

Pasta [`modulo_1_aprender_com_dados`](modulo_1_aprender_com_dados). Caso do módulo: os lotes de azeitona de um lagar cooperativo.

| N.º | Capítulo | Conteúdos | Colab |
| --- | --- | --- | --- |
| 01 | [Relembrar: o essencial antes de começar](modulo_1_aprender_com_dados/01_Relembrar_o_Essencial.ipynb) | Revisão em cinco partes, com seis exercícios de reforço: atributos, alvo, treinar e prever; treino, teste e linha de base; fugas de informação e *pipelines*; matriz de confusão, precisão, sensibilidade e limiar; sobreajuste e validação cruzada. Remete para os capítulos do tutorial de ciência de dados. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Aprendizagem%20Autom%C3%A1tica/tutorial_machine_learning/modulo_1_aprender_com_dados/01_Relembrar_o_Essencial.ipynb) |
| 02 | [Inteligência artificial, aprendizagem automática e os tipos de aprendizagem](modulo_1_aprender_com_dados/02_IA_Aprendizagem_e_Tipos.ipynb) | Inteligência artificial, aprendizagem automática e aprendizagem profunda; o mesmo problema com regras, com um modelo clássico e com uma rede neuronal; aprendizagem supervisionada e não supervisionada; aprendizagem por reforço de raiz, com o problema das máquinas de moedas e a estratégia ε-gulosa; explorar ou aproveitar. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Aprendizagem%20Autom%C3%A1tica/tutorial_machine_learning/modulo_1_aprender_com_dados/02_IA_Aprendizagem_e_Tipos.ipynb) |
| 03 | [A interface do scikit-learn e o fluxo de um projeto](modulo_1_aprender_com_dados/03_Interface_scikit_learn_e_Fluxo.ipynb) | A forma de `X` e de `y`; estimador, preditor e transformador; hiperparâmetros e parâmetros aprendidos; um classificador 1R escrito de raiz e usado em validação cruzada e numa procura em grelha; as sete etapas de um projeto supervisionado; os riscos de usar modelos aprendidos. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Aprendizagem%20Autom%C3%A1tica/tutorial_machine_learning/modulo_1_aprender_com_dados/03_Interface_scikit_learn_e_Fluxo.ipynb) |

#### Módulos seguintes

| Módulo | Tema | Estado |
| --- | --- | --- |
| 2 | Regressão linear: função de custo, mínimos quadrados, descida do gradiente, regressão polinomial, métricas | em preparação |
| 3 | Regressão logística e avaliação: sigmoide, possibilidades, regularização, métricas, escolha do limiar | em preparação |
| 4 | Preparar os dados sem fugas: limpeza, valores atípicos, escalas, codificação, classes desequilibradas, validação, *pipelines* | em preparação |
| 5 | Métodos por distância: KNN, centroide mais próximo, métricas de distância, maldição da dimensionalidade | em preparação |
| 6 | Árvores e florestas: entropia, Gini, árvores de regressão, poda, procura em grelha, *bagging*, florestas aleatórias | em preparação |

### Parte II – Intermédio

| Módulo | Tema | Estado |
| --- | --- | --- |
| 7 | *Boosting* (XGBoost, LightGBM, CatBoost) e outros classificadores (SVM, Naive Bayes) | em preparação |
| 8 | Otimização e avaliação rigorosa: Optuna, curvas ROC e de precisão-sensibilidade, calibração | em preparação |
| 9 | Engenharia de atributos e redução de dimensionalidade | em preparação |
| 10 | Interpretabilidade: importância por permutação, dependência parcial, SHAP | em preparação |
| 11 | Aprendizagem não supervisionada: DBSCAN, deteção de anomalias, sistemas de recomendação | em preparação |

### Parte III – Avançado

| Módulo | Tema | Estado |
| --- | --- | --- |
| 12 | Séries temporais | em preparação |
| 13 | Aprendizagem profunda | em preparação |
| 14 | Do notebook à produção | em preparação |

---

## Como usar

### No Google Colab (recomendado para começar)

1. Carrega no botão **«Abrir no Colab»** do capítulo que queres estudar.
2. Para guardar as tuas alterações, usa **Ficheiro → Guardar uma cópia no Drive**.
3. Executa as células por ordem, com `Shift + Enter`.

### No computador (Jupyter ou VS Code)

```bash
git clone https://github.com/ricardoluizdasilva/mestrado_ai_estudos.git
cd "mestrado_ai_estudos/Introdução à Aprendizagem Automática/tutorial_machine_learning"
python -m pip install -r requirements.txt
```

Depois abre a pasta no Jupyter (`jupyter lab`) ou no VS Code (com a extensão Jupyter) e escolhe um kernel **Python 3.10 ou superior**.

### Convenções dos notebooks

- Cada capítulo abre com o banner do curso, os **objetivos** e os **pré-requisitos**.
- Os gráficos de dados são desenhados pelo código das células. Os esquemas são desenhados com as funções `tela`, `caixa` e `seta`, definidas no início de cada notebook.
- 💡 **Soluções:** os exercícios têm uma solução escondida num bloco «Ver uma solução possível». Tenta primeiro sozinho!
- ✅ **Verifica o que aprendeste:** cada capítulo termina com uma lista de verificação.
- Os notebooks são guardados **com as saídas** de uma execução de referência, para que os esquemas e os gráficos se vejam diretamente no GitHub.
- Os dados são gerados com uma semente fixa, por isso os números do texto coincidem com os que obténs ao executar.
- Os termos estão em português, com o termo inglês entre parênteses na primeira vez que aparecem.

### Verificação automática

Sempre que o tutorial é alterado, o GitHub executa todos os notebooks (fluxo [`notebooks_machine_learning.yml`](../../.github/workflows/notebooks_machine_learning.yml)) e o selo no início desta página mostra o resultado. A verificação também corre no dia 1 de cada mês, para detetar alterações nas bibliotecas.

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
| scikit-learn | 1.6 ou superior |
| matplotlib | 3.10 ou superior |

O Google Colab já inclui todas estas bibliotecas. Os módulos da parte II vão acrescentar outras (XGBoost, LightGBM, CatBoost, Optuna, imbalanced-learn, SHAP), indicadas no início de cada módulo.

## Estrutura do repositório

```
tutorial_machine_learning/
├── README.md
├── LICENSE.md
├── requirements.txt
├── ferramentas/
│   └── verificar_notebooks.py
└── modulo_1_aprender_com_dados/
    ├── 01_Relembrar_o_Essencial.ipynb
    ├── 02_IA_Aprendizagem_e_Tipos.ipynb
    └── 03_Interface_scikit_learn_e_Fluxo.ipynb
```

## Licença

- **Conteúdos** (textos, exercícios, imagens e notebooks): [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.pt). Podes partilhar e adaptar para fins não comerciais, indicando o autor e mantendo a mesma licença.
- **Código** (ficheiros `.py`, código das células e verificação automática): [MIT](LICENSE-MIT.txt).

Os detalhes e a sugestão de atribuição estão em [`LICENSE.md`](LICENSE.md).

## Autor

Desenvolvido por **RLdS** (Ricardo Luiz da Silva). Sugestões e correções são bem-vindas através de *issues* ou *pull requests*.
