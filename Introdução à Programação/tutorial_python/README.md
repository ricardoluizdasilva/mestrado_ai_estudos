# Introdução ao Python

**Curso de introdução à programação com Python, em notebooks Jupyter e em português europeu.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![Notebooks](https://img.shields.io/badge/notebooks-43-orange) ![Idioma](https://img.shields.io/badge/idioma-português%20(PT)-green) [![Licença: CC BY-NC-SA 4.0](https://img.shields.io/badge/licen%C3%A7a-CC%20BY--NC--SA%204.0-lightgrey)](LICENSE.md) [![Código: MIT](https://img.shields.io/badge/c%C3%B3digo-MIT-yellow)](LICENSE-MIT.txt) [![Verificação dos notebooks](https://github.com/ricardoluizdasilva/mestrado_ai_estudos/actions/workflows/notebooks.yml/badge.svg)](https://github.com/ricardoluizdasilva/mestrado_ai_estudos/actions/workflows/notebooks.yml)

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
- Manipular dados numéricos com **NumPy** e tabelas com **pandas**, e comunicá-los com gráficos (**matplotlib**, **seaborn** e **plotly**).
- No nível avançado: preparar dados reais e criar, avaliar e interpretar modelos com **scikit-learn**.

---

## Estrutura do curso

O curso está organizado em **dois níveis**, a que se junta um nível dedicado à inteligência artificial.

### Nível 1 – Introdução

Pasta [`nivel_1_introducao`](nivel_1_introducao). São 26 capítulos, da lógica de programação à visualização de dados e ao Python intermédio. Os capítulos devem ser feitos por ordem, porque cada um usa conceitos dos anteriores.

#### Fundamentos (capítulos 0 a 3)

| N.º | Capítulo | Conteúdos | Colab |
| --- | --- | --- | --- |
| 00 | [Introdução à lógica de programação](nivel_1_introducao/00_Logica_Programacao.ipynb) | Algoritmos, fluxogramas e pseudocódigo, entrada/processamento/saída, operadores e tabelas de verdade, variáveis e tipos, estruturas de controlo, vetores e funções. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_1_introducao/00_Logica_Programacao.ipynb) |
| 01 | [O que é Python?](nivel_1_introducao/01_O_que_e_Python.ipynb) | História da linguagem, linguagens compiladas e interpretadas, níveis de linguagem e o Zen of Python. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_1_introducao/01_O_que_e_Python.ipynb) |
| 02 | [Primeiros passos](nivel_1_introducao/02_Primeiros_Passos.ipynb) | O Python como calculadora, operadores aritméticos, precedência e a função `print()`. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_1_introducao/02_Primeiros_Passos.ipynb) |
| 03 | [Boas práticas de programação](nivel_1_introducao/03_Boas_Praticas.ipynb) | Sintaxe, identificadores, indentação, comentários e docstrings, instruções e guia de estilo PEP 8. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_1_introducao/03_Boas_Praticas.ipynb) |

#### Tipos de dados e operadores (capítulos 4 a 9)

| N.º | Capítulo | Conteúdos | Colab |
| --- | --- | --- | --- |
| 04 | [Variáveis](nivel_1_introducao/04_Variaveis.ipynb) | Atribuição simples e múltipla, nomes válidos, tipos dinâmicos, `type()` e variáveis globais. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_1_introducao/04_Variaveis.ipynb) |
| 05 | [Números](nivel_1_introducao/05_Numeros.ipynb) | `int`, `float` e `complex`, conversões, precisão dos decimais e bases (binário, octal, hexadecimal). | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_1_introducao/05_Numeros.ipynb) |
| 06 | [Strings](nivel_1_introducao/06_Strings.ipynb) | Unicode, índices e fatias, imutabilidade, métodos de strings e caracteres de escape. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_1_introducao/06_Strings.ipynb) |
| 07 | [Entrada e saída de dados](nivel_1_introducao/07_Entrada_Saida.ipynb) | `print()` e `input()`, conversão e validação da entrada. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_1_introducao/07_Entrada_Saida.ipynb) |
| 08 | [Operadores](nivel_1_introducao/08_Operadores.ipynb) | Aritméticos, atribuição, comparação, lógicos, valores verdadeiros/falsos, pertença, identidade e bitwise. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_1_introducao/08_Operadores.ipynb) |
| 09 | [Formatação da saída de dados](nivel_1_introducao/09_Formatacao_Saida.ipynb) | `sep` e `end`, `format()`, operador `%` e f-strings com especificações de formato. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_1_introducao/09_Formatacao_Saida.ipynb) |

#### Controlo de fluxo (capítulos 10 e 11)

| N.º | Capítulo | Conteúdos | Colab |
| --- | --- | --- | --- |
| 10 | [Estruturas de decisão](nivel_1_introducao/10_Estruturas_Decisao.ipynb) | `if`/`elif`/`else`, condições compostas e aninhadas, expressão condicional e `match/case`. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_1_introducao/10_Estruturas_Decisao.ipynb) |
| 11 | [Ciclos](nivel_1_introducao/11_Ciclos.ipynb) | `for`, `range()`, `enumerate()`, `while`, `break`/`continue`/`pass`, `for…else` e ciclos aninhados. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_1_introducao/11_Ciclos.ipynb) |

#### Estruturas de dados (capítulos 12 a 15)

| N.º | Capítulo | Conteúdos | Colab |
| --- | --- | --- | --- |
| 12 | [Listas](nivel_1_introducao/12_Listas.ipynb) | Indexação e slicing, métodos, ordenação, listas aninhadas, cópia vs. referência e list comprehensions. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_1_introducao/12_Listas.ipynb) |
| 13 | [Tuplos](nivel_1_introducao/13_Tuplos.ipynb) | Imutabilidade, tuplo de um elemento, desempacotamento e conversões. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_1_introducao/13_Tuplos.ipynb) |
| 14 | [Dicionários](nivel_1_introducao/14_Dicionarios.ipynb) | Acesso por chave, `get()`, percorrer, atualizar e juntar, ordenar, comprehensions e cópias. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_1_introducao/14_Dicionarios.ipynb) |
| 15 | [Conjuntos e síntese das estruturas de dados](nivel_1_introducao/15_Conjuntos.ipynb) | Operações de conjuntos, comprehensions de conjuntos e comparação entre listas, tuplos, dicionários e conjuntos (incluindo os métodos de cada um). | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_1_introducao/15_Conjuntos.ipynb) |

#### Programas robustos e organizados (capítulos 16 a 21)

| N.º | Capítulo | Conteúdos | Colab |
| --- | --- | --- | --- |
| 16 | [Tratamento de exceções](nivel_1_introducao/16_Excecoes.ipynb) | Exceções mais comuns, `try`/`except`/`else`/`finally`, `raise`, como ler um *traceback* e exceções próprias. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_1_introducao/16_Excecoes.ipynb) |
| 17 | [Ficheiros](nivel_1_introducao/17_Ficheiros.ipynb) | Modos de abertura, `with`, leitura e escrita, codificação UTF-8, cursor (`seek`/`tell`) e modo binário. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_1_introducao/17_Ficheiros.ipynb) |
| 18 | [Funções](nivel_1_introducao/18_Funcoes.ipynb) | Parâmetros e valores por omissão, argumentos nomeados, âmbito, `*args`/`**kwargs`, recursão e memoização. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_1_introducao/18_Funcoes.ipynb) |
| 19 | [Expressões lambda](nivel_1_introducao/19_Lambda.ipynb) | Funções anónimas com `map()`, `filter()`, `sorted()`, `min()`/`max()` e funções que criam funções. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_1_introducao/19_Lambda.ipynb) |
| 20 | [Classes e objetos](nivel_1_introducao/20_Classes_Objetos.ipynb) | Classes, `__init__` e `self`, métodos, `__str__`, atributos de classe, herança, composição, encapsulamento (`_`, `__` e `@property`), classes abstratas (`abc`) e `dataclasses`. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_1_introducao/20_Classes_Objetos.ipynb) |
| 21 | [Módulos e pacotes](nivel_1_introducao/21_Modulos_Pacotes.ipynb) | Importar, criar módulos e pacotes, `if __name__ == "__main__"`, biblioteca padrão e bibliotecas externas. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_1_introducao/21_Modulos_Pacotes.ipynb) |

#### Introdução à análise de dados (capítulos 22 a 24)

| N.º | Capítulo | Conteúdos | Colab |
| --- | --- | --- | --- |
| 22 | [NumPy](nivel_1_introducao/22_NumPy.ipynb) | Arrays, tipos, indexação e máscaras, vistas e cópias, broadcasting, eixos, estatística e álgebra linear (opcional). | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_1_introducao/22_NumPy.ipynb) |
| 23 | [Pandas básico](nivel_1_introducao/23_Pandas_Basico.ipynb) | Series e DataFrames, seleção com `loc`/`iloc`, filtros, colunas, tipos, agregações, valores em falta e CSV. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_1_introducao/23_Pandas_Basico.ipynb) |
| 23 · Ficha | [Ficha de estudo – Pandas (Quiz 1)](nivel_1_introducao/23_Pandas_Ficha_Estudo_Quiz_01.ipynb) | Revisão para o quiz: `read_csv`, `loc`/`iloc`, filtros com `isin`, atribuição segura com `loc`, `describe`, contagens e `merge`, com a grelha das 16 perguntas. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_1_introducao/23_Pandas_Ficha_Estudo_Quiz_01.ipynb) |
| 24 | [Visualização de dados](nivel_1_introducao/24_Visualizacao_Dados.ipynb) | Escolher o gráfico certo, matplotlib, `.plot()` do pandas, seaborn (distribuições, relações, correlações), gráficos interativos com plotly, séries temporais, áreas empilhadas, barras de erro, `jointplot`, hexágonos e densidade 2D, e boas práticas. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_1_introducao/24_Visualizacao_Dados.ipynb) |

#### Python intermédio (capítulo 25)

| N.º | Capítulo | Conteúdos | Colab |
| --- | --- | --- | --- |
| 25 | [Python intermédio](nivel_1_introducao/25_Python_Intermedio.ipynb) | Iteradores (`iter`/`next`), geradores e `yield`, `zip`/`any`/`all`, decoradores com `functools.wraps`, gestores de contexto (`with`, `__enter__`/`__exit__`, `contextlib`) e anotações de tipo, com a ligação ao `DataLoader` e ao `torch.no_grad()` do PyTorch. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_1_introducao/25_Python_Intermedio.ipynb) |

### Nível 2 – Avançado

Pasta [`nivel_2_avancado`](nivel_2_avancado). São 5 módulos e dois anexos, para quem concluiu o nível 1. Os módulos de scikit-learn pressupõem noções básicas de estatística (média, desvio padrão, probabilidade). Cada módulo é autónomo, gera os seus próprios dados sintéticos e inclui exercícios resolvidos e um projeto final.

| Módulo | Tema | Conteúdos | Colab |
| --- | --- | --- | --- |
| 1 | [Pandas na prática – dos ficheiros às decisões](nivel_2_avancado/N2_01_Pandas_Intermedio.ipynb) | Projeto CRISP-DM: importação de CSV, Excel e web, diagnóstico, limpeza e validação, junções, reformatação, agregação, datas, gráficos e exportação. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_2_avancado/N2_01_Pandas_Intermedio.ipynb) |
| 2 | [Pandas avançado](nivel_2_avancado/N2_02_Pandas_Avancado.ipynb) | Parquet e Arrow, SQLite, fusos horários, contratos de dados, testes, janelas temporais, desempenho e preparação para modelos. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_2_avancado/N2_02_Pandas_Avancado.ipynb) |
| 3 | [Scikit-learn: fundamentos e regressão](nivel_2_avancado/N2_03_ScikitLearn_Fundamentos.ipynb) | API do scikit-learn, regressão linear simples e múltipla, métricas, pipelines, validação cruzada, regularização e afinação. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_2_avancado/N2_03_ScikitLearn_Fundamentos.ipynb) |
| 4 | [Scikit-learn: classificação e seleção de modelos](nivel_2_avancado/N2_04_ScikitLearn_Classificacao.ipynb) | Matriz de confusão e métricas, modelos de classificação, curvas ROC/PR, limiar de decisão e seleção de modelos. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_2_avancado/N2_04_ScikitLearn_Classificacao.ipynb) |
| 5 | [Scikit-learn: aprofundamento e aplicações](nivel_2_avancado/N2_05_ScikitLearn_Aplicacoes.ipynb) | Ensembles, calibração, importância por permutação, validação por grupos e no tempo, clustering, PCA e gravação de modelos. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_2_avancado/N2_05_ScikitLearn_Aplicacoes.ipynb) |
| Anexo A1 | [Linha de comando, concorrência, redes e outras ferramentas](nivel_2_avancado/N2_A1_Anexo_Linha_Comando_Concorrencia.ipynb) | `sys.argv`, `argparse`, `logging`, threads, sockets, `requests`, Beautiful Soup, `sqlite3` e `unittest`. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_2_avancado/N2_A1_Anexo_Linha_Comando_Concorrencia.ipynb) |
| Anexo A2 | [Do notebook ao projeto](nivel_2_avancado/N2_A2_Anexo_Notebook_Projeto.ipynb) | Instalar o Python, executar ficheiros `.py`, ambientes virtuais (`venv`), `pip`, `requirements.txt` e `pyproject.toml`, estrutura `src/`/`tests/`, testes com `pytest`, `ruff` (linter e formatador), Git e GitHub. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_2_avancado/N2_A2_Anexo_Notebook_Projeto.ipynb) |

### Nível IA – Python para inteligência artificial

Pasta [`nivel_3_ia`](nivel_3_ia). Módulos orientados para a inteligência artificial, que partem da teoria (estatística, matemática) e chegam às bibliotecas usadas na prática.

| Módulo | Tema | Conteúdos | Colab |
| --- | --- | --- | --- |
| 1 | [Estatística descritiva com Python](nivel_3_ia/N3_01_Estatistica_Descritiva_Python.ipynb) | Os exercícios 1 a 12 da disciplina de Fundamentos de Estatística resolvidos em Python puro: tabelas de frequências, classes pela regra de Sturges, medidas de localização, dispersão, assimetria e curtose, outliers, histogramas e diagramas de extremos e quartis, e verificação automática contra as soluções oficiais. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_3_ia/N3_01_Estatistica_Descritiva_Python.ipynb) |
| 2 | [Estatística descritiva com NumPy, pandas e SciPy](nivel_3_ia/N3_02_Estatistica_Descritiva_Bibliotecas.ipynb) | Resolução completa dos mesmos 12 exercícios com as bibliotecas, alínea a alínea, comparada com o módulo 1: `ddof` e métodos de quantis (Weibull, linear, equivalências no Excel), tabelas com pandas e `np.histogram`, `groupby`, interpolação na ogiva, assimetria e curtose por momentos com SciPy, gráficos com seaborn, e refatoração num módulo com classes de dados testado com `unittest`. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_3_ia/N3_02_Estatistica_Descritiva_Bibliotecas.ipynb) |
| 2 · Caso real | [Estatística descritiva dos pinguins de Palmer](nivel_3_ia/N3_02_Caso_Real_Pinguins.ipynb) | A análise completa num conjunto de dados real (344 pinguins de três espécies, dados em domínio público), com o módulo `estatistica.py` e as convenções da disciplina: tipos de variáveis, valores em falta, tabelas de frequências, de contingência e de classes, localização, dispersão, forma e *outliers*, comparação por espécie e sexo, e um relatório gerado a partir dos cálculos. Mostra como a distribuição global pode esconder grupos. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_3_ia/N3_02_Caso_Real_Pinguins.ipynb) |
| 3 | [Do dado ao conhecimento: o processo KDD](nivel_3_ia/N3_03_Processo_KDD.ipynb) | Caso de estudo de ponta a ponta (prever o abandono de clientes) com as seis fases do KDD: seleção de três fontes (CSV, SQLite, JSON de uma API) e janelas temporais, limpeza com registo de decisões, transformação (agregação RFM, normalização, codificação), redução (correlação, informação mútua, `SelectKBest`, PCA), mineração (classificação e k-médias), avaliação (*lift*, importância, paradoxo de Simpson) e fugas de informação. Inclui o módulo reutilizável `kdd.py`. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_3_ia/N3_03_Processo_KDD.ipynb) |
| 3 · Modelo | [Modelo do processo KDD](nivel_3_ia/N3_03_Modelo_KDD.ipynb) | Notebook-modelo para aplicar o processo KDD aos teus dados: perguntas por fase, células `# ADAPTAR` e funções do `kdd.py`. Corre de ponta a ponta com um exemplo do scikit-learn. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_3_ia/N3_03_Modelo_KDD.ipynb) |
| 4 | [Redes neuronais de raiz, com NumPy](nivel_3_ia/N3_04_Redes_Neuronais_NumPy.ipynb) | Do neurónio à retropropagação, sem bibliotecas de *deep learning*: o neurónio como regressão logística e o problema do XOR, funções de ativação, entropia cruzada e descida do gradiente (taxa de aprendizagem), rede com uma camada escondida, retropropagação com verificação por diferenças finitas, mini-lotes com um gerador, curvas de aprendizagem, sobreajuste, L2 e paragem antecipada, comparação com o `MLPClassifier` e o que o PyTorch automatiza. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_3_ia/N3_04_Redes_Neuronais_NumPy.ipynb) |
| 5 | [PyTorch: fundamentos](nivel_3_ia/N3_05_PyTorch_Fundamentos.ipynb) | Tensores e conversão com NumPy, *autograd* (conferido com a retropropagação do N3_04), `nn.Module` e `nn.Sequential`, perdas e otimizadores (SGD, *momentum*, Adam), `Dataset` e `DataLoader`, ciclo de treino com `train`/`eval` e `torch.no_grad()`, *dropout*, paragem antecipada, guardar e carregar modelos, e o caso do abandono de clientes (N3_03) com uma rede neuronal comparada com modelos clássicos. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_3_ia/N3_05_PyTorch_Fundamentos.ipynb) |
| 6 | [Visão computacional com redes convolucionais](nivel_3_ia/N3_06_Visao_Computacional_CNN.ipynb) | Imagens como tensores (N, C, A, L), convolução à mão e com `nn.Conv2d` (filtros de Sobel numa fotografia), *padding*, *stride* e *max pooling*, uma CNN para os dígitos 8×8 do scikit-learn, classificação multiclasse com *softmax* e `CrossEntropyLoss`, matriz de confusão e erros, filtros e mapas de ativação, robustez a deslocações (CNN contra rede densa) e *data augmentation*. Parte opcional com o Fashion-MNIST. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_3_ia/N3_06_Visao_Computacional_CNN.ipynb) |
| 7 | [Texto e linguagem natural](nivel_3_ia/N3_07_Texto_NLP.ipynb) | Análise de sentimento de avaliações de clientes em português: tokenização e *stopwords* (o caso do «não»), *bag-of-words* à mão e com `CountVectorizer`, n-gramas, TF-IDF à mão e com `TfidfVectorizer`, regressão logística com interpretação dos pesos, *embeddings* treinados com PyTorch (`nn.EmbeddingBag`, semelhança do cosseno) e, opcionalmente, *transformers* pré-treinados da Hugging Face. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_3_ia/N3_07_Texto_NLP.ipynb) |
| 8 | [Otimização combinatória: formar grupos de projeto](nivel_3_ia/N3_08_Otimizacao_Grupos.ipynb) | Caso de estudo completo, do enunciado ao relatório: dividir alunos em grupos de 3 a 5 minimizando o pior grupo (objetivo *minimax*). Formulação e complexidade (NP-difícil), contagem do espaço de soluções, pesquisa exaustiva com poda (*branch and bound*), construção gulosa, vizinhança focada e avaliação incremental, subida de colina com reinícios, recozimento simulado e pesquisa tabu, comparação com o mesmo orçamento e apresentação de resultados (avaliações, iterações e tempo de CPU). | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_3_ia/N3_08_Otimizacao_Grupos.ipynb) |
| 9 | [Aprender a otimizar](nivel_3_ia/N3_09_Aprender_a_Otimizar.ipynb) | O mesmo problema dos grupos, agora com aprendizagem: método da entropia cruzada (e o modelo de afinidades que aprende), algoritmo genético com cruzamento por grupos e versão memética, e uma rede neuronal treinada por imitação das escolhas da pesquisa tabu, testada em dados nunca vistos e com grupo de controlo. Comparação por avaliações e por tempo de CPU e síntese: quando compensa aprender. | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricardoluizdasilva/mestrado_ai_estudos/blob/main/Introdu%C3%A7%C3%A3o%20%C3%A0%20Programa%C3%A7%C3%A3o/tutorial_python/nivel_3_ia/N3_09_Aprender_a_Otimizar.ipynb) |

---

## Fichas de consulta rápida

Pasta [`consulta_rapida`](consulta_rapida). São resumos em PDF (A4 na horizontal), para imprimir ou ter abertos ao lado do notebook. Cada bloco indica o capítulo e a secção onde o tema é explicado, e cada ficha inclui um bloco com os erros mais frequentes.

| Ficha | Conteúdos | Capítulos |
| --- | --- | --- |
| [Python essencial](consulta_rapida/Consulta_Rapida_Python.pdf) | 4 páginas: bases (variáveis, strings, entrada e saída, operadores, decisões, ciclos); estruturas de dados e os métodos de cada uma; funções, exceções (incluindo exceções próprias e *tracebacks*) e ficheiros; classes, encapsulamento, classes abstratas, módulos e armadilhas frequentes. | 4 a 21 |
| [NumPy](consulta_rapida/Consulta_Rapida_NumPy.pdf) | 2 páginas: criar, selecionar e remodelar arrays; operações vetorizadas, broadcasting, eixos, valores especiais, álgebra linear e armadilhas. | 22 |
| [Pandas](consulta_rapida/Consulta_Rapida_Pandas.pdf) | 3 páginas: fundamentos (ler, inspecionar, selecionar, filtrar); transformar e resumir (colunas, ordenação, ausentes, tipos, texto, datas, `groupby`); combinar, exportar e armadilhas. | 23 · N2_01 · N2_02 |
| [Visualização de dados](consulta_rapida/Consulta_Rapida_Visualizacao.pdf) | 2 páginas: que gráfico usar, matplotlib e gráficos com pandas; seaborn, plotly express e boas práticas. | 24 |
| [Scikit-learn](consulta_rapida/Consulta_Rapida_ScikitLearn.pdf) | 3 páginas: fluxo, separação, pré-processamento e pipelines; modelos, métricas e afinação; probabilidades, aplicações e armadilhas. | N2_03 · N2_04 · N2_05 |
| [Python intermédio](consulta_rapida/Consulta_Rapida_Python_Intermedio.pdf) | 2 páginas: iteradores, geradores e `yield`, `itertools`, lista ou gerador; `zip`/`any`/`all`, decoradores, gestores de contexto e anotações de tipo. | 25 |
| [Do notebook ao projeto](consulta_rapida/Consulta_Rapida_Notebook_Projeto.pdf) | 2 páginas: executar código, ambientes virtuais (Windows e macOS/Linux), `pip` e `requirements.txt`, estrutura de um projeto; `pytest`, `ruff`, Git e GitHub, e armadilhas. | A2 |
| [Processo KDD](consulta_rapida/Consulta_Rapida_Processo_KDD.pdf) | 2 páginas: as seis fases, seleção, limpeza e transformação com o `kdd.py`; redução, mineração, avaliação e fugas de informação. | N3_03 |
| [Redes neuronais e PyTorch](consulta_rapida/Consulta_Rapida_Redes_Neuronais_PyTorch.pdf) | 2 páginas: neurónio, ativações, perda, descida do gradiente, formas das matrizes, retropropagação e treino com NumPy; tensores, *autograd*, `nn.Module`, perdas, otimizadores, `DataLoader`, ciclo de treino e armadilhas do PyTorch. | N3_04 · N3_05 |
| [Visão e texto](consulta_rapida/Consulta_Rapida_Visao_Texto.pdf) | 2 páginas: convolução, *padding*, *stride*, *pooling*, uma CNN, avaliação e *data augmentation*; tokenização e *stopwords*, *bag-of-words*, n-gramas, TF-IDF, classificação, *embeddings* e *transformers*. | N3_06 · N3_07 |

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
cd "mestrado_ai_estudos/Introdução à Programação/tutorial_python"
python -m pip install -r requirements.txt
```

Para os módulos N3_05 a N3_07 instala também o PyTorch. A versão só para CPU é mais leve: `python -m pip install torch --index-url https://download.pytorch.org/whl/cpu`.

Depois abre a pasta no Jupyter (`jupyter lab`) ou no VS Code (com a extensão Jupyter) e escolhe um kernel **Python 3.10 ou superior**.

### Convenções dos notebooks

- 🧪 **Experimenta:** células vazias para alterares e testares os exemplos.
- ⚠️ **Erros de propósito:** as células que começam por `# ⚠️ Esta célula gera um erro de propósito` mostram erros intencionais. Lê a mensagem e continua.
- 💡 **Soluções:** os exercícios têm uma solução escondida num bloco «Ver uma solução possível». Tenta primeiro sozinho!
- Alguns capítulos usam `input()`: escreve a resposta na caixa que aparece e carrega em `Enter`.
- ✅ **Verifica o que aprendeste:** cada capítulo termina com uma lista de verificação. Se houver um ponto de que não tenhas a certeza, volta à secção correspondente.
- Os notebooks dos níveis 1 e 2 são guardados **sem saídas**: os resultados aparecem quando executas as células. Os do nível IA guardam as saídas de uma execução de referência, porque alguns exemplos demoram a correr.

### Verificação automática

Sempre que o tutorial é alterado, o GitHub executa todos os notebooks (fluxo [`notebooks.yml`](../../.github/workflows/notebooks.yml)) e o selo no início desta página mostra o resultado. A verificação também corre no dia 1 de cada mês, para detetar alterações nas bibliotecas. Os erros de propósito (⚠️) não contam.

Para fazer a mesma verificação no teu computador, a partir desta pasta:

```bash
python ferramentas/verificar_notebooks.py                     # todos os notebooks
python ferramentas/verificar_notebooks.py nivel_1_introducao  # só uma pasta
```

Os notebooks são executados numa cópia temporária, por isso os originais e a pasta de trabalho não são alterados.

---

## Requisitos

| Componente | Versão |
| --- | --- |
| Python | 3.10 ou superior (o `match/case` do capítulo 10 exige 3.10) |
| NumPy | 2.x |
| pandas | 2.2 ou superior (testado também com 3.0) |
| scikit-learn | 1.6 ou superior (nível avançado) |
| matplotlib | 3.x |
| seaborn | 0.13 ou superior |
| plotly | 5.x ou superior |
| PyTorch | 2.x (módulos N3_05 a N3_07; já vem no Colab) |
| torchvision | só para a parte opcional do N3_06 (Fashion-MNIST); já vem no Colab |
| transformers | só para a parte opcional do N3_07 (Hugging Face); já vem no Colab |
| pytest e ruff | versões recentes (anexo A2; o notebook instala-as) |

O Google Colab já inclui todas estas bibliotecas.

## Estrutura do repositório

```text
tutorial_python/
├── README.md                 ← este ficheiro
├── LICENSE.md                ← licenças (conteúdos e código)
├── LICENSE-*.txt             ← textos completos das licenças CC BY-NC-SA 4.0 e MIT
├── requirements.txt          ← bibliotecas usadas nos notebooks
├── consulta_rapida/          ← fichas de consulta rápida em PDF
├── ferramentas/              ← verificação automática dos notebooks
├── nivel_1_introducao/       ← capítulos 0 a 25
├── nivel_2_avancado/         ← módulos 1 a 5 e anexos A1 e A2
└── nivel_3_ia/               ← Python para inteligência artificial
    └── dados/                ← conjuntos de dados reais usados nos módulos
```

## Licença

- **Conteúdos** (textos, exercícios, imagens, notebooks e fichas em PDF): [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.pt). Podes partilhar e adaptar para fins não comerciais, indicando o autor e mantendo a mesma licença.
- **Código** (ficheiros `.py`, código das células e verificação automática): [MIT](LICENSE-MIT.txt).

Os detalhes, a sugestão de atribuição e as exceções (dados de terceiros) estão em [`LICENSE.md`](LICENSE.md).

## Autor

Desenvolvido por **RLdS** (Ricardo Luiz da Silva). Sugestões e correções são bem-vindas através de *issues* ou *pull requests*.
