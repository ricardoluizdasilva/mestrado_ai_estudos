# Introdução à Ciência de Dados

**Tutorial de ciência de dados, do problema à decisão, em notebooks Jupyter e em português europeu.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![Notebooks](https://img.shields.io/badge/notebooks-5-orange) ![Idioma](https://img.shields.io/badge/idioma-português%20(PT)-green) [![Licença: CC BY-NC-SA 4.0](https://img.shields.io/badge/licen%C3%A7a-CC%20BY--NC--SA%204.0-lightgrey)](LICENSE.md) [![Código: MIT](https://img.shields.io/badge/c%C3%B3digo-MIT-yellow)](LICENSE-MIT.txt) [![Verificação dos notebooks](https://github.com/ricardoluizdasilva/mestrado_ai_estudos/actions/workflows/notebooks_ciencia_dados.yml/badge.svg)](https://github.com/ricardoluizdasilva/mestrado_ai_estudos/actions/workflows/notebooks_ciencia_dados.yml)

Este tutorial ensina a pensar como um cientista de dados antes de ensinar técnicas: que pergunta fazer, que dados a podem responder, como avaliar uma previsão pela decisão que ela permite e como organizar o trabalho. Cada capítulo combina explicações curtas, esquemas e gráficos gerados pelo próprio código, exemplos executáveis e exercícios com soluções.

Todo o módulo usa o mesmo caso, com **dados sintéticos** gerados dentro de cada notebook: uma rede de clínicas que quer reduzir as faltas a consultas.

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

---

## Estrutura do curso

O tutorial cresce por módulos. Os capítulos de cada módulo devem ser feitos por ordem.

### Módulo 1 – Do problema à decisão

Pasta [`modulo_1_do_problema_a_decisao`](modulo_1_do_problema_a_decisao).

| N.º | Capítulo | Conteúdos | Colab |
| --- | --- | --- | --- |
| 01 | [Dos dados à decisão](modulo_1_do_problema_a_decisao/01_Dos_Dados_a_Decisao.ipynb) | Porque ter dados não é ter respostas, *big data* e os cinco V, as quatro etapas de dados a decisão, o que é a ciência de dados e que competências junta, áreas de aplicação. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_1_do_problema_a_decisao/01_Dos_Dados_a_Decisao.ipynb) |
| 02 | [Da pergunta ao enquadramento](modulo_1_do_problema_a_decisao/02_Da_Pergunta_ao_Enquadramento.ipynb) | Perguntas descritivas, explicativas, preditivas e de decisão aplicadas aos mesmos dados; associação e causalidade (variável de confusão, paradoxo de Simpson); fuga de informação; cinco perguntas de enquadramento; da previsão à ação. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_1_do_problema_a_decisao/02_Da_Pergunta_ao_Enquadramento.ipynb) |
| 03 | [Uma boa previsão não garante uma boa decisão](modulo_1_do_problema_a_decisao/03_Previsao_nao_e_Decisao.ipynb) | Um modelo com 93% de exatidão que quase não ajuda; linha de base, matriz de confusão, sensibilidade e precisão; o limiar como decisão; custos dos erros e ponto de equilíbrio; limites de recursos; definir o sucesso antes de começar. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_1_do_problema_a_decisao/03_Previsao_nao_e_Decisao.ipynb) |
| 04 | [Dados imperfeitos e o processo de trabalho](modulo_1_do_problema_a_decisao/04_Dados_Imperfeitos_e_Processo.ipynb) | Fontes de dados; dados incompletos, ruidosos, enviesados e dependentes do contexto, cada um simulado; as seis fases do CRISP-DM; onde se gasta o tempo; ferramentas e reprodutibilidade. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_1_do_problema_a_decisao/04_Dados_Imperfeitos_e_Processo.ipynb) |
| 05 | [Projeto: enquadrar um problema](modulo_1_do_problema_a_decisao/05_Projeto_Enquadrar_um_Problema.ipynb) | Ficha de enquadramento com oito componentes, exemplo resolvido, três cenários (perdas de água, livros esgotados, bicicletas partilhadas), grelha de autoavaliação e fichas possíveis. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Ci%C3%AAncia%20de%20Dados/tutorial_ciencia_dados/modulo_1_do_problema_a_decisao/05_Projeto_Enquadrar_um_Problema.ipynb) |

### Módulos seguintes

Os próximos módulos serão acrescentados aqui, cada um na sua pasta (`modulo_2_…`, `modulo_3_…`).

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

Se ainda não programas em Python, começa pelo tutorial [Introdução ao Python](../../Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python) (os capítulos 22 a 24 chegam para acompanhar este módulo).

### Convenções dos notebooks

- Cada capítulo abre com os **objetivos** e os **pré-requisitos**.
- Os esquemas e os gráficos são desenhados pelo código das células, com as funções `tela`, `caixa` e `seta` definidas no início de cada notebook. As cores têm sempre o mesmo significado: azul para descrever, verde para explicar, violeta para prever e laranja para decidir.
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
| scikit-learn | 1.6 ou superior (capítulo 3) |
| matplotlib | 3.8 ou superior |

O Google Colab já inclui todas estas bibliotecas.

## Estrutura do repositório

```text
tutorial_ciencia_dados/
├── README.md                          ← este ficheiro
├── LICENSE.md                         ← licenças (conteúdos e código)
├── LICENSE-CC-BY-NC-SA-4.0.txt
├── LICENSE-MIT.txt
├── requirements.txt
├── ferramentas/
│   └── verificar_notebooks.py         ← executa os notebooks e procura erros
└── modulo_1_do_problema_a_decisao/
    ├── 01_Dos_Dados_a_Decisao.ipynb
    ├── 02_Da_Pergunta_ao_Enquadramento.ipynb
    ├── 03_Previsao_nao_e_Decisao.ipynb
    ├── 04_Dados_Imperfeitos_e_Processo.ipynb
    └── 05_Projeto_Enquadrar_um_Problema.ipynb
```

## Licença

- **Conteúdos** (textos, exercícios, imagens e notebooks): [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.pt). Podes partilhar e adaptar para fins não comerciais, indicando o autor e mantendo a mesma licença.
- **Código** (ficheiros `.py`, código das células e verificação automática): [MIT](LICENSE-MIT.txt).

Os detalhes e a sugestão de atribuição estão em [`LICENSE.md`](LICENSE.md).

## Autor

Desenvolvido por **RLdS** (Ricardo Luiz da Silva). Sugestões e correções são bem-vindas através de *issues* ou *pull requests*.
