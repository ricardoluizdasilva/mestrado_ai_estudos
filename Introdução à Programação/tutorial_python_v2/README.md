# Introdução ao Python

**Curso de introdução à programação com Python, em notebooks Jupyter e em português europeu.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![Notebooks](https://img.shields.io/badge/notebooks-30-orange) ![Idioma](https://img.shields.io/badge/idioma-português%20(PT)-green)

Este tutorial acompanha quem nunca programou desde a lógica de programação até à análise de dados e à aprendizagem automática. Cada capítulo combina explicações curtas, exemplos executáveis, células para experimentar e exercícios com soluções.

Os notebooks funcionam no **Google Colab** (sem instalar nada), no **Jupyter** e no **VS Code**. Cada notebook tem um botão «Abrir no Colab».

---

## Para quem é

- Quem quer aprender a programar do zero, sem conhecimentos prévios.
- Estudantes e profissionais que precisam de Python para trabalhar com dados.
- Formadores que procuram materiais prontos a usar em aula.

## O que vais aprender

- Pensar de forma algorítmica e escrever programas estruturados e legíveis.
- Usar os tipos de dados, as estruturas de controlo e as estruturas de dados do Python.
- Tratar erros, trabalhar com ficheiros e organizar código em funções, classes, módulos e pacotes.
- Manipular dados numéricos com **NumPy** e tabelas com **pandas**.
- No nível avançado: preparar dados reais e criar, avaliar e interpretar modelos com **scikit-learn**.

---

## Estrutura do curso

O curso está organizado em **dois níveis**.

### Nível 1 – Introdução

Pasta [`nivel_1_introducao`](nivel_1_introducao). São 24 capítulos, da lógica de programação ao pandas básico. Os capítulos devem ser feitos por ordem, porque cada um usa conceitos dos anteriores.

#### Fundamentos (capítulos 0 a 3)

| N.º | Capítulo | Conteúdos | Colab |
| --- | --- | --- | --- |
| 00 | [Introdução à lógica de programação](nivel_1_introducao/RLdS_00_Logica_Programacao.ipynb) | Algoritmos, fluxogramas e pseudocódigo, entrada/processamento/saída, operadores e tabelas de verdade, variáveis e tipos, estruturas de controlo, vetores e funções. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python_v2/nivel_1_introducao/RLdS_00_Logica_Programacao.ipynb) |
| 01 | [O que é Python?](nivel_1_introducao/RLdS_01_O_que_e_Python.ipynb) | História da linguagem, linguagens compiladas e interpretadas, níveis de linguagem e o Zen of Python. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python_v2/nivel_1_introducao/RLdS_01_O_que_e_Python.ipynb) |
| 02 | [Primeiros passos](nivel_1_introducao/RLdS_02_Primeiros_Passos.ipynb) | O Python como calculadora, operadores aritméticos, precedência e a função `print()`. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python_v2/nivel_1_introducao/RLdS_02_Primeiros_Passos.ipynb) |
| 03 | [Boas práticas de programação](nivel_1_introducao/RLdS_03_Boas_Praticas.ipynb) | Sintaxe, identificadores, indentação, comentários e docstrings, instruções e guia de estilo PEP 8. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python_v2/nivel_1_introducao/RLdS_03_Boas_Praticas.ipynb) |

#### Tipos de dados e operadores (capítulos 4 a 9)

| N.º | Capítulo | Conteúdos | Colab |
| --- | --- | --- | --- |
| 04 | [Variáveis](nivel_1_introducao/RLdS_04_Variaveis.ipynb) | Atribuição simples e múltipla, nomes válidos, tipos dinâmicos, `type()` e variáveis globais. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python_v2/nivel_1_introducao/RLdS_04_Variaveis.ipynb) |
| 05 | [Números](nivel_1_introducao/RLdS_05_Numeros.ipynb) | `int`, `float` e `complex`, conversões, precisão dos decimais e bases (binário, octal, hexadecimal). | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python_v2/nivel_1_introducao/RLdS_05_Numeros.ipynb) |
| 06 | [Strings](nivel_1_introducao/RLdS_06_Strings.ipynb) | Unicode, índices e fatias, imutabilidade, métodos de strings e caracteres de escape. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python_v2/nivel_1_introducao/RLdS_06_Strings.ipynb) |
| 07 | [Entrada e saída de dados](nivel_1_introducao/RLdS_07_Entrada_Saida.ipynb) | `print()` e `input()`, conversão e validação da entrada. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python_v2/nivel_1_introducao/RLdS_07_Entrada_Saida.ipynb) |
| 08 | [Operadores](nivel_1_introducao/RLdS_08_Operadores.ipynb) | Aritméticos, atribuição, comparação, lógicos, valores verdadeiros/falsos, pertença, identidade e bitwise. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python_v2/nivel_1_introducao/RLdS_08_Operadores.ipynb) |
| 09 | [Formatação da saída de dados](nivel_1_introducao/RLdS_09_Formatacao_Saida.ipynb) | `sep` e `end`, `format()`, operador `%` e f-strings com especificações de formato. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python_v2/nivel_1_introducao/RLdS_09_Formatacao_Saida.ipynb) |

#### Controlo de fluxo (capítulos 10 e 11)

| N.º | Capítulo | Conteúdos | Colab |
| --- | --- | --- | --- |
| 10 | [Estruturas de decisão](nivel_1_introducao/RLdS_10_Estruturas_Decisao.ipynb) | `if`/`elif`/`else`, condições compostas e aninhadas, expressão condicional e `match/case`. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python_v2/nivel_1_introducao/RLdS_10_Estruturas_Decisao.ipynb) |
| 11 | [Ciclos](nivel_1_introducao/RLdS_11_Ciclos.ipynb) | `for`, `range()`, `enumerate()`, `while`, `break`/`continue`, `for…else` e ciclos aninhados. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python_v2/nivel_1_introducao/RLdS_11_Ciclos.ipynb) |

#### Estruturas de dados (capítulos 12 a 15)

| N.º | Capítulo | Conteúdos | Colab |
| --- | --- | --- | --- |
| 12 | [Listas](nivel_1_introducao/RLdS_12_Listas.ipynb) | Indexação e slicing, métodos, ordenação, listas aninhadas, cópia vs. referência e list comprehensions. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python_v2/nivel_1_introducao/RLdS_12_Listas.ipynb) |
| 13 | [Tuplos](nivel_1_introducao/RLdS_13_Tuplos.ipynb) | Imutabilidade, tuplo de um elemento, desempacotamento e conversões. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python_v2/nivel_1_introducao/RLdS_13_Tuplos.ipynb) |
| 14 | [Dicionários](nivel_1_introducao/RLdS_14_Dicionarios.ipynb) | Acesso por chave, `get()`, percorrer, atualizar e juntar, ordenar, comprehensions e cópias. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python_v2/nivel_1_introducao/RLdS_14_Dicionarios.ipynb) |
| 15 | [Conjuntos e síntese das estruturas de dados](nivel_1_introducao/RLdS_15_Conjuntos.ipynb) | Operações de conjuntos e comparação entre listas, tuplos, dicionários e conjuntos. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python_v2/nivel_1_introducao/RLdS_15_Conjuntos.ipynb) |

#### Programas robustos e organizados (capítulos 16 a 21)

| N.º | Capítulo | Conteúdos | Colab |
| --- | --- | --- | --- |
| 16 | [Tratamento de exceções](nivel_1_introducao/RLdS_16_Excecoes.ipynb) | Exceções mais comuns, `try`/`except`/`else`/`finally` e `raise`. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python_v2/nivel_1_introducao/RLdS_16_Excecoes.ipynb) |
| 17 | [Ficheiros](nivel_1_introducao/RLdS_17_Ficheiros.ipynb) | Modos de abertura, `with`, leitura e escrita, codificação UTF-8, cursor (`seek`/`tell`) e modo binário. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python_v2/nivel_1_introducao/RLdS_17_Ficheiros.ipynb) |
| 18 | [Funções](nivel_1_introducao/RLdS_18_Funcoes.ipynb) | Parâmetros e valores por omissão, argumentos nomeados, âmbito, `*args`/`**kwargs`, recursão e memoização. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python_v2/nivel_1_introducao/RLdS_18_Funcoes.ipynb) |
| 19 | [Expressões lambda](nivel_1_introducao/RLdS_19_Lambda.ipynb) | Funções anónimas com `map()`, `filter()`, `sorted()`, `min()`/`max()` e funções que criam funções. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python_v2/nivel_1_introducao/RLdS_19_Lambda.ipynb) |
| 20 | [Classes e objetos](nivel_1_introducao/RLdS_20_Classes_Objetos.ipynb) | Classes, `__init__` e `self`, métodos, `__str__`, atributos de classe, herança, composição e `dataclasses`. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python_v2/nivel_1_introducao/RLdS_20_Classes_Objetos.ipynb) |
| 21 | [Módulos e pacotes](nivel_1_introducao/RLdS_21_Modulos_Pacotes.ipynb) | Importar, criar módulos e pacotes, `if __name__ == "__main__"`, biblioteca padrão e bibliotecas externas. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python_v2/nivel_1_introducao/RLdS_21_Modulos_Pacotes.ipynb) |

#### Introdução à análise de dados (capítulos 22 e 23)

| N.º | Capítulo | Conteúdos | Colab |
| --- | --- | --- | --- |
| 22 | [NumPy](nivel_1_introducao/RLdS_22_NumPy.ipynb) | Arrays, tipos, indexação e máscaras, vistas e cópias, broadcasting, eixos, estatística e álgebra linear (opcional). | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python_v2/nivel_1_introducao/RLdS_22_NumPy.ipynb) |
| 23 | [Pandas básico](nivel_1_introducao/RLdS_23_Pandas_Basico.ipynb) | Series e DataFrames, seleção com `loc`/`iloc`, filtros, colunas, tipos, agregações, valores em falta e CSV. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python_v2/nivel_1_introducao/RLdS_23_Pandas_Basico.ipynb) |

### Nível 2 – Avançado

Pasta [`nivel_2_avancado`](nivel_2_avancado). São 5 módulos e um anexo, para quem concluiu o nível 1. Os módulos de scikit-learn pressupõem noções básicas de estatística (média, desvio padrão, probabilidade). Cada módulo é autónomo, gera os seus próprios dados sintéticos e inclui exercícios resolvidos e um projeto final.

| Módulo | Tema | Conteúdos | Colab |
| --- | --- | --- | --- |
| 1 | [Pandas na prática – dos ficheiros às decisões](nivel_2_avancado/RLdS_N2_01_Pandas_Intermedio.ipynb) | Projeto CRISP-DM: importação de CSV, Excel e web, diagnóstico, limpeza e validação, junções, reformatação, agregação, datas, gráficos e exportação. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python_v2/nivel_2_avancado/RLdS_N2_01_Pandas_Intermedio.ipynb) |
| 2 | [Pandas avançado](nivel_2_avancado/RLdS_N2_02_Pandas_Avancado.ipynb) | Parquet e Arrow, SQLite, fusos horários, contratos de dados, testes, janelas temporais, desempenho e preparação para modelos. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python_v2/nivel_2_avancado/RLdS_N2_02_Pandas_Avancado.ipynb) |
| 3 | [Scikit-learn: fundamentos e regressão](nivel_2_avancado/RLdS_N2_03_ScikitLearn_Fundamentos.ipynb) | API do scikit-learn, regressão linear simples e múltipla, métricas, pipelines, validação cruzada, regularização e afinação. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python_v2/nivel_2_avancado/RLdS_N2_03_ScikitLearn_Fundamentos.ipynb) |
| 4 | [Scikit-learn: classificação e seleção de modelos](nivel_2_avancado/RLdS_N2_04_ScikitLearn_Classificacao.ipynb) | Matriz de confusão e métricas, modelos de classificação, curvas ROC/PR, limiar de decisão e seleção de modelos. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python_v2/nivel_2_avancado/RLdS_N2_04_ScikitLearn_Classificacao.ipynb) |
| 5 | [Scikit-learn: aprofundamento e aplicações](nivel_2_avancado/RLdS_N2_05_ScikitLearn_Aplicacoes.ipynb) | Ensembles, calibração, importância por permutação, validação por grupos e no tempo, clustering, PCA e gravação de modelos. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python_v2/nivel_2_avancado/RLdS_N2_05_ScikitLearn_Aplicacoes.ipynb) |
| Anexo | [Linha de comando, concorrência, redes e outras ferramentas](nivel_2_avancado/RLdS_N2_A1_Anexo_Linha_Comando_Concorrencia.ipynb) | `sys.argv`, `argparse`, `logging`, threads, sockets, `requests`, Beautiful Soup, `sqlite3` e `unittest`. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python_v2/nivel_2_avancado/RLdS_N2_A1_Anexo_Linha_Comando_Concorrencia.ipynb) |

---

## Como usar

### No Google Colab (recomendado para começar)

1. Carrega no botão **«Abrir no Colab»** do capítulo que queres estudar.
2. Para guardar as tuas alterações, usa **Ficheiro → Guardar uma cópia no Drive**.
3. Executa as células por ordem, com `Shift + Enter`.

> Os ficheiros que os notebooks criam ficam em `/content` e são apagados quando a sessão termina. Descarrega-os pelo painel de ficheiros (📁) se os quiseres guardar.

### No computador (Jupyter ou VS Code)

```bash
git clone https://github.com/ricardoluizdasilva/mestrado_ai_estudos.git
cd "mestrado_ai_estudos/Introdução à Programação/tutorial_python_v2"
python -m pip install numpy pandas matplotlib scikit-learn openpyxl pyarrow requests beautifulsoup4
```

Depois abre a pasta no Jupyter (`jupyter lab`) ou no VS Code (com a extensão Jupyter) e escolhe um kernel **Python 3.10 ou superior**.

### Convenções dos notebooks

- 🧪 **Experimenta:** células vazias para alterares e testares os exemplos.
- ⚠️ **Erros de propósito:** as células que começam por `# ⚠️ Esta célula gera um erro de propósito` mostram erros intencionais. Lê a mensagem e continua.
- 💡 **Soluções:** os exercícios têm uma solução escondida num bloco «Ver uma solução possível». Tenta primeiro sozinho!
- Alguns capítulos usam `input()`: escreve a resposta na caixa que aparece e carrega em `Enter`.

---

## Requisitos

| Componente | Versão |
| --- | --- |
| Python | 3.10 ou superior (o `match/case` do capítulo 10 exige 3.10) |
| NumPy | 2.x |
| pandas | 2.2 ou superior (testado também com 3.0) |
| scikit-learn | 1.6 ou superior (nível avançado) |
| matplotlib | 3.x |

O Google Colab já inclui todas estas bibliotecas.

## Estrutura do repositório

```text
tutorial_python_v2/
├── README.md                 ← este ficheiro
├── LEIA-ME_ALTERACOES.md     ← registo de alterações da revisão de 2026
├── nivel_1_introducao/       ← capítulos 0 a 23
└── nivel_2_avancado/         ← módulos 1 a 5 e anexo
```

## Autor

Desenvolvido por **RLdS** (Ricardo Luiz da Silva). Sugestões e correções são bem-vindas através de *issues* ou *pull requests*.

