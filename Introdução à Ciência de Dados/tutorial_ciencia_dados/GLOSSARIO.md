# Glossário português–inglês

O tutorial usa os termos em português. A documentação das bibliotecas, os artigos e a maior parte dos cursos usam os termos em inglês. Esta tabela faz a correspondência e indica o capítulo em que cada termo é apresentado (módulo.capítulo).

Alguns termos não têm tradução estabelecida e usam-se em inglês também em português: *pipeline*, *bagging*, *boosting*, *bootstrap*, *out-of-bag*, *biplot*, K-Means, Ridge, Lasso.

| Português | Inglês | Em poucas palavras | Capítulo |
| --- | --- | --- | --- |
| agrupamento | *clustering* | Dividir as observações em grupos de casos parecidos, sem um alvo. | [7.1](modulo_7_aprendizagem_nao_supervisionada/01_KMeans.ipynb) |
| agrupamento hierárquico | *hierarchical clustering* | Agrupamento que constrói uma árvore de fusões sucessivas, cortada depois à altura desejada. | [7.3](modulo_7_aprendizagem_nao_supervisionada/03_Agrupamento_Hierarquico.ipynb) |
| alvo | *target, label* | A coluna que o modelo aprende a prever. | [4.1](modulo_4_preparar_os_dados/01_O_que_e_Aprender_com_Dados.ipynb) |
| amostra | *sample* | A parte da população que foi observada. | [1.5](modulo_1_do_problema_a_decisao/05_Metodo_Cientifico_Amostragem_Inferencia.ipynb) |
| amostra bootstrap | *bootstrap sample* | Amostra do mesmo tamanho dos dados, tirada com reposição. | [6.7](modulo_6_modelos_supervisionados/07_Florestas_Aleatorias.ipynb) |
| anonimização | *anonymization* | Transformar os dados até ninguém poder ser identificado por nenhum meio razoável. | [8.6](modulo_8_comunicar_e_usar_com_responsabilidade/06_Privacidade_e_Dados_Pessoais.ipynb) |
| aprendizagem automática | *machine learning* | Programas que melhoram numa tarefa com a experiência, medida por um critério de desempenho. | [4.1](modulo_4_preparar_os_dados/01_O_que_e_Aprender_com_Dados.ipynb) |
| aprendizagem não supervisionada | *unsupervised learning* | Aprender a estrutura dos dados sem um alvo. | [7.1](modulo_7_aprendizagem_nao_supervisionada/01_KMeans.ipynb) |
| aprendizagem supervisionada | *supervised learning* | Aprender a prever um alvo a partir de exemplos com a resposta conhecida. | [4.1](modulo_4_preparar_os_dados/01_O_que_e_Aprender_com_Dados.ipynb) |
| árvore de decisão | *decision tree* | Modelo que prevê com uma sequência de perguntas de sim ou não. | [6.4](modulo_6_modelos_supervisionados/04_Arvores_de_Decisao.ipynb) |
| atributo | *feature* | Uma coluna usada pelo modelo para prever. | [4.1](modulo_4_preparar_os_dados/01_O_que_e_Aprender_com_Dados.ipynb) |
| atributo nominal | *nominal (categorical) feature* | Atributo cujos valores são categorias sem ordem. | [2.2](modulo_2_fontes_tipos_estruturas/02_Tipos_de_Dados.ipynb) |
| atributo ordinal | *ordinal feature* | Atributo cujos valores são categorias com ordem. | [2.2](modulo_2_fontes_tipos_estruturas/02_Tipos_de_Dados.ipynb) |
| calibração | *calibration* | As probabilidades previstas correspondem às frequências observadas. | [5.3](modulo_5_modelos_lineares/03_Regressao_Logistica.ipynb) |
| classificação | *classification* | Prever uma categoria. | [4.1](modulo_4_preparar_os_dados/01_O_que_e_Aprender_com_Dados.ipynb) |
| codificação one-hot | *one-hot encoding* | Transformar uma categoria numa coluna de 0 e 1 por cada valor possível. | [4.5](modulo_4_preparar_os_dados/05_Codificar_Categorias.ipynb) |
| coeficiente | *coefficient, weight* | O número que multiplica um atributo num modelo linear. | [5.2](modulo_5_modelos_lineares/02_Regressao_Linear_Multipla.ipynb) |
| coeficiente de determinação (R²) | *coefficient of determination, R-squared* | Parte da variação do alvo explicada pelo modelo, em comparação com prever a média. | [5.1](modulo_5_modelos_lineares/01_Regressao_Linear_Simples.ipynb) |
| coeficiente de silhueta | *silhouette coefficient* | Mede se uma observação está mais perto do seu grupo do que do grupo vizinho. | [7.2](modulo_7_aprendizagem_nao_supervisionada/02_Avaliar_sem_Rotulos.ipynb) |
| colinearidade | *collinearity, multicollinearity* | Dois ou mais atributos que trazem quase a mesma informação. | [5.2](modulo_5_modelos_lineares/02_Regressao_Linear_Multipla.ipynb) |
| componente principal | *principal component* | Direção de maior variância dos dados; uma coluna nova, combinação das originais. | [7.4](modulo_7_aprendizagem_nao_supervisionada/04_PCA.ipynb) |
| conjunto de teste | *test set* | Dados guardados para a avaliação final, usados uma só vez. | [4.2](modulo_4_preparar_os_dados/02_Treino_Teste_e_Linha_de_Base.ipynb) |
| conjunto de treino | *training set* | Dados com que o modelo aprende. | [4.2](modulo_4_preparar_os_dados/02_Treino_Teste_e_Linha_de_Base.ipynb) |
| conjunto de validação | *validation set* | Dados usados para escolher entre modelos e hiperparâmetros. | [4.2](modulo_4_preparar_os_dados/02_Treino_Teste_e_Linha_de_Base.ipynb) |
| correlação | *correlation* | Medida, entre −1 e 1, de quanto duas variáveis variam em conjunto. | [3.5](modulo_3_explorar_os_dados/05_Associacao_e_Correlacoes_Espurias.ipynb) |
| correlação espúria | *spurious correlation* | Correlação entre variáveis sem relação de causa, devida ao acaso ou a uma terceira variável. | [3.5](modulo_3_explorar_os_dados/05_Associacao_e_Correlacoes_Espurias.ipynb) |
| curva de aprendizagem | *learning curve* | O erro em função da quantidade de dados de treino. | [6.5](modulo_6_modelos_supervisionados/05_Sobreajuste_Vies_e_Variancia.ipynb) |
| curva ROC e AUC | *ROC curve, area under the curve* | Desempenho de um classificador em todos os limiares; a AUC é a área debaixo da curva. | [6.1](modulo_6_modelos_supervisionados/01_Metricas_de_Avaliacao.ipynb) |
| dado pessoal | *personal data* | Qualquer informação relativa a uma pessoa identificada ou identificável. | [8.6](modulo_8_comunicar_e_usar_com_responsabilidade/06_Privacidade_e_Dados_Pessoais.ipynb) |
| dados em falta | *missing data, missing values* | Valores que deviam existir e não foram registados. | [1.4](modulo_1_do_problema_a_decisao/04_Dados_Imperfeitos_e_Processo.ipynb) |
| dendrograma | *dendrogram* | Desenho em árvore das fusões de um agrupamento hierárquico. | [7.3](modulo_7_aprendizagem_nao_supervisionada/03_Agrupamento_Hierarquico.ipynb) |
| deriva | *drift (data drift, concept drift)* | Mudança, ao longo do tempo, dos dados ou da relação que o modelo aprendeu. | [8.4](modulo_8_comunicar_e_usar_com_responsabilidade/04_Documentar_e_Acompanhar_um_Modelo.ipynb) |
| descida do gradiente | *gradient descent* | Minimizar um erro dando pequenos passos no sentido em que ele desce mais depressa. | [5.2](modulo_5_modelos_lineares/02_Regressao_Linear_Multipla.ipynb) |
| desvio padrão | *standard deviation* | Medida da dispersão dos valores em torno da média. | [3.3](modulo_3_explorar_os_dados/03_Medidas_Descritivas.ipynb) |
| distância euclidiana | *Euclidean distance* | Distância em linha reta entre duas observações. | [6.2](modulo_6_modelos_supervisionados/02_KNN_Classificacao.ipynb) |
| engenharia de atributos | *feature engineering* | Criar atributos novos a partir dos existentes. | [4.5](modulo_4_preparar_os_dados/05_Codificar_Categorias.ipynb) |
| equidade | *fairness* | Tratamento igual de grupos de pessoas por um modelo, segundo um critério que é preciso escolher. | [8.5](modulo_8_comunicar_e_usar_com_responsabilidade/05_Equidade.ipynb) |
| erro absoluto médio (MAE) | *mean absolute error* | Média dos valores absolutos dos resíduos. | [5.1](modulo_5_modelos_lineares/01_Regressao_Linear_Simples.ipynb) |
| erro quadrático médio (MSE, RMSE) | *mean squared error, root mean squared error* | Média dos quadrados dos resíduos; a raiz (RMSE) volta à unidade do alvo. | [6.1](modulo_6_modelos_supervisionados/01_Metricas_de_Avaliacao.ipynb) |
| escala, normalização | *scaling, standardization* | Pôr os atributos em unidades comparáveis, por exemplo em desvios padrão. | [4.4](modulo_4_preparar_os_dados/04_Escalas.ipynb) |
| especificidade | *specificity, true negative rate* | Dos casos negativos, a fração corretamente identificada. | [6.1](modulo_6_modelos_supervisionados/01_Metricas_de_Avaliacao.ipynb) |
| exatidão | *accuracy* | Fração de previsões certas. | [1.3](modulo_1_do_problema_a_decisao/03_Previsao_nao_e_Decisao.ipynb) |
| extrapolação | *extrapolation* | Prever fora do intervalo de valores coberto pelos dados. | [5.1](modulo_5_modelos_lineares/01_Regressao_Linear_Simples.ipynb) |
| falso positivo, falso negativo | *false positive, false negative* | Os dois tipos de erro de um classificador: falso alarme e caso não detetado. | [6.1](modulo_6_modelos_supervisionados/01_Metricas_de_Avaliacao.ipynb) |
| ficha de dados | *datasheet* | Documento com a origem, a recolha, a qualidade e o dicionário de um conjunto de dados. | [8.4](modulo_8_comunicar_e_usar_com_responsabilidade/04_Documentar_e_Acompanhar_um_Modelo.ipynb) |
| ficha de modelo | *model card* | Documento curto com o uso previsto, os dados, o desempenho, os limites e a manutenção de um modelo. | [8.4](modulo_8_comunicar_e_usar_com_responsabilidade/04_Documentar_e_Acompanhar_um_Modelo.ipynb) |
| floresta aleatória | *random forest* | Média de muitas árvores treinadas em amostras bootstrap, com sorteio de atributos. | [6.7](modulo_6_modelos_supervisionados/07_Florestas_Aleatorias.ipynb) |
| frequências naturais | *natural frequencies* | Dizer um resultado em contagens de pessoas num grupo redondo, em vez de percentagens. | [8.1](modulo_8_comunicar_e_usar_com_responsabilidade/01_Do_Resultado_a_Mensagem.ipynb) |
| fronteira de decisão | *decision boundary* | A linha que separa as zonas em que o modelo prevê classes diferentes. | [6.2](modulo_6_modelos_supervisionados/02_KNN_Classificacao.ipynb) |
| fuga de informação | *data leakage* | Informação que não estaria disponível no momento da previsão e entra no treino. | [4.6](modulo_4_preparar_os_dados/06_Pipelines_sem_Fuga_de_Informacao.ipynb) |
| gráfico em funil | *funnel plot* | Taxa de cada grupo contra o seu tamanho, com a zona em que o acaso põe a maioria. | [8.3](modulo_8_comunicar_e_usar_com_responsabilidade/03_Comunicar_a_Incerteza.ipynb) |
| hiperparâmetro | *hyperparameter* | Escolha feita antes do treino (k, profundidade, α), que não se aprende com os dados de treino. | [6.2](modulo_6_modelos_supervisionados/02_KNN_Classificacao.ipynb) |
| igualdade de oportunidades | *equal opportunity* | Quem tem o resultado positivo tem a mesma probabilidade de ser assinalado em qualquer grupo. | [8.5](modulo_8_comunicar_e_usar_com_responsabilidade/05_Equidade.ipynb) |
| importância por permutação | *permutation importance* | Quanto piora o erro quando se baralha uma coluna. | [6.7](modulo_6_modelos_supervisionados/07_Florestas_Aleatorias.ipynb) |
| imputação | *imputation* | Preencher valores em falta com uma estimativa. | [4.3](modulo_4_preparar_os_dados/03_Valores_em_Falta_e_Imputacao.ipynb) |
| índice de Gini | *Gini impurity* | Medida da mistura de classes num grupo; zero quando o grupo é puro. | [6.4](modulo_6_modelos_supervisionados/04_Arvores_de_Decisao.ipynb) |
| índice de Rand ajustado | *adjusted Rand index (ARI)* | Concordância entre dois agrupamentos, descontado o acaso. | [7.2](modulo_7_aprendizagem_nao_supervisionada/02_Avaliar_sem_Rotulos.ipynb) |
| inércia | *inertia, within-cluster sum of squares* | Soma dos quadrados das distâncias de cada ponto ao centroide do seu grupo. | [7.1](modulo_7_aprendizagem_nao_supervisionada/01_KMeans.ipynb) |
| interação | *interaction* | O efeito de um atributo depende do valor de outro. | [5.2](modulo_5_modelos_lineares/02_Regressao_Linear_Multipla.ipynb) |
| intervalo de confiança | *confidence interval* | Intervalo de valores plausíveis para uma quantidade estimada com uma amostra. | [1.5](modulo_1_do_problema_a_decisao/05_Metodo_Cientifico_Amostragem_Inferencia.ipynb) |
| intervalo por bootstrap | *bootstrap confidence interval* | Margem de uma métrica obtida recalculando-a em reamostragens dos dados. | [8.3](modulo_8_comunicar_e_usar_com_responsabilidade/03_Comunicar_a_Incerteza.ipynb) |
| k-anonimato | *k-anonymity* | Cada pessoa é indistinguível de, pelo menos, outras k − 1 nos quase-identificadores. | [8.6](modulo_8_comunicar_e_usar_com_responsabilidade/06_Privacidade_e_Dados_Pessoais.ipynb) |
| limiar | *threshold* | Valor a partir do qual uma probabilidade passa a ser uma decisão. | [1.3](modulo_1_do_problema_a_decisao/03_Previsao_nao_e_Decisao.ipynb) |
| linha de base | *baseline* | A previsão mais simples possível, que serve de termo de comparação. | [4.2](modulo_4_preparar_os_dados/02_Treino_Teste_e_Linha_de_Base.ipynb) |
| matriz de confusão | *confusion matrix* | Tabela das previsões contra a realidade, com os acertos e os dois tipos de erro. | [1.3](modulo_1_do_problema_a_decisao/03_Previsao_nao_e_Decisao.ipynb) |
| mediana | *median* | O valor central: metade das observações fica abaixo. | [3.3](modulo_3_explorar_os_dados/03_Medidas_Descritivas.ipynb) |
| mínimos quadrados | *least squares* | Escolher os coeficientes que minimizam a soma dos quadrados dos resíduos. | [5.1](modulo_5_modelos_lineares/01_Regressao_Linear_Simples.ipynb) |
| ordenada na origem | *intercept* | A previsão de um modelo linear quando todos os atributos valem zero. | [5.1](modulo_5_modelos_lineares/01_Regressao_Linear_Simples.ipynb) |
| paragem antecipada | *early stopping* | Parar o treino quando o erro de validação deixa de melhorar. | [6.8](modulo_6_modelos_supervisionados/08_Boosting.ipynb) |
| paridade | *demographic parity* | A mesma fração de cada grupo é assinalada pelo modelo. | [8.5](modulo_8_comunicar_e_usar_com_responsabilidade/05_Equidade.ipynb) |
| perda logarítmica | *log loss, cross-entropy* | Penaliza a probabilidade dada ao que realmente aconteceu; castiga a confiança errada. | [5.3](modulo_5_modelos_lineares/03_Regressao_Logistica.ipynb) |
| população | *population* | O conjunto de todos os casos sobre os quais se quer concluir. | [1.5](modulo_1_do_problema_a_decisao/05_Metodo_Cientifico_Amostragem_Inferencia.ipynb) |
| possibilidades, razão de possibilidades | *odds, odds ratio* | Probabilidade de acontecer a dividir pela de não acontecer; a razão compara duas possibilidades. | [5.3](modulo_5_modelos_lineares/03_Regressao_Logistica.ipynb) |
| precisão | *precision* | Dos casos assinalados pelo modelo, a fração que se confirma. | [1.3](modulo_1_do_problema_a_decisao/03_Previsao_nao_e_Decisao.ipynb) |
| procura em grelha | *grid search* | Experimentar todas as combinações de uma lista de hiperparâmetros. | [6.6](modulo_6_modelos_supervisionados/06_Validacao_Cruzada.ipynb) |
| proxy | *proxy* | Coluna que transporta a informação de outra, por exemplo a distância em vez da zona. | [8.5](modulo_8_comunicar_e_usar_com_responsabilidade/05_Equidade.ipynb) |
| pseudonimização | *pseudonymization* | Trocar os identificadores diretos por códigos; os dados continuam a ser pessoais. | [8.6](modulo_8_comunicar_e_usar_com_responsabilidade/06_Privacidade_e_Dados_Pessoais.ipynb) |
| quartil, amplitude interquartil | *quartile, interquartile range (IQR)* | Os valores que dividem os dados em quatro partes; a amplitude interquartil é a distância entre o 1.º e o 3.º. | [3.3](modulo_3_explorar_os_dados/03_Medidas_Descritivas.ipynb) |
| quase-identificador | *quasi-identifier* | Coluna que sozinha não identifica, mas combinada com outras sim (data de nascimento, código postal). | [8.6](modulo_8_comunicar_e_usar_com_responsabilidade/06_Privacidade_e_Dados_Pessoais.ipynb) |
| redução de dimensão | *dimensionality reduction* | Resumir muitas colunas em poucas, perdendo o mínimo de informação. | [7.4](modulo_7_aprendizagem_nao_supervisionada/04_PCA.ipynb) |
| regressão | *regression* | Prever um número. | [4.1](modulo_4_preparar_os_dados/01_O_que_e_Aprender_com_Dados.ipynb) |
| regressão linear | *linear regression* | Prever um número com uma soma ponderada dos atributos. | [5.1](modulo_5_modelos_lineares/01_Regressao_Linear_Simples.ipynb) |
| regressão logística | *logistic regression* | Modelo de classificação: uma soma ponderada passada pela sigmoide dá uma probabilidade. | [5.3](modulo_5_modelos_lineares/03_Regressao_Logistica.ipynb) |
| regularização | *regularization* | Penalizar coeficientes grandes para o modelo não aprender acasos. | [5.4](modulo_5_modelos_lineares/04_Regularizacao.ipynb) |
| reidentificação | *re-identification* | Descobrir a quem pertence uma linha de uma tabela sem nomes, cruzando-a com outra fonte. | [8.6](modulo_8_comunicar_e_usar_com_responsabilidade/06_Privacidade_e_Dados_Pessoais.ipynb) |
| resíduo | *residual* | O valor real menos o previsto. | [5.1](modulo_5_modelos_lineares/01_Regressao_Linear_Simples.ipynb) |
| ruído | *noise* | A parte da variação que nenhum atributo explica. | [6.5](modulo_6_modelos_supervisionados/05_Sobreajuste_Vies_e_Variancia.ipynb) |
| sensibilidade | *recall, sensitivity* | Dos casos positivos que existem, a fração que o modelo deteta. | [1.3](modulo_1_do_problema_a_decisao/03_Previsao_nao_e_Decisao.ipynb) |
| série temporal | *time series* | Valores da mesma quantidade observados ao longo do tempo. | [3.6](modulo_3_explorar_os_dados/06_Series_Temporais.ipynb) |
| sobreajuste | *overfitting* | O modelo aprende particularidades do treino que não se repetem em dados novos. | [4.2](modulo_4_preparar_os_dados/02_Treino_Teste_e_Linha_de_Base.ipynb) |
| subajuste | *underfitting* | O modelo é simples de mais para captar o padrão. | [6.5](modulo_6_modelos_supervisionados/05_Sobreajuste_Vies_e_Variancia.ipynb) |
| taxa de aprendizagem | *learning rate* | O tamanho de cada passo na descida do gradiente ou no boosting. | [5.2](modulo_5_modelos_lineares/02_Regressao_Linear_Multipla.ipynb) |
| validação cruzada | *cross-validation* | Dividir os dados em K partes e usar cada uma, por turnos, para validar. | [6.6](modulo_6_modelos_supervisionados/06_Validacao_Cruzada.ipynb) |
| valor extremo | *outlier* | Observação muito afastada das restantes. | [3.3](modulo_3_explorar_os_dados/03_Medidas_Descritivas.ipynb) |
| variância | *variance* | Média dos quadrados dos desvios em relação à média; também a instabilidade de um modelo de amostra para amostra. | [3.3](modulo_3_explorar_os_dados/03_Medidas_Descritivas.ipynb) |
| variável de confusão | *confounder, confounding variable* | Terceira variável que influencia as duas que se estão a comparar. | [1.2](modulo_1_do_problema_a_decisao/02_Da_Pergunta_ao_Enquadramento.ipynb) |
| viés (de um modelo) | *bias* | Erro sistemático de um modelo demasiado simples. | [6.5](modulo_6_modelos_supervisionados/05_Sobreajuste_Vies_e_Variancia.ipynb) |
| viés de seleção | *selection bias* | A amostra não representa a população porque a forma de a recolher favorece certos casos. | [1.4](modulo_1_do_problema_a_decisao/04_Dados_Imperfeitos_e_Processo.ipynb) |
| vizinhos mais próximos (KNN) | *k-nearest neighbors* | Prever a partir das k observações mais parecidas. | [6.2](modulo_6_modelos_supervisionados/02_KNN_Classificacao.ipynb) |

## Do inglês para o português

Para quem chega aqui a partir de um termo em inglês:

| Inglês | Português |
| --- | --- |
| *accuracy* | exatidão |
| *adjusted Rand index (ARI)* | índice de Rand ajustado |
| *anonymization* | anonimização |
| *area under the curve* | curva ROC e AUC |
| *baseline* | linha de base |
| *bias* | viés (de um modelo) |
| *bootstrap confidence interval* | intervalo por bootstrap |
| *bootstrap sample* | amostra bootstrap |
| *calibration* | calibração |
| *classification* | classificação |
| *clustering* | agrupamento |
| *coefficient* | coeficiente |
| *coefficient of determination* | coeficiente de determinação (R²) |
| *collinearity* | colinearidade |
| *confidence interval* | intervalo de confiança |
| *confounder* | variável de confusão |
| *confounding variable* | variável de confusão |
| *confusion matrix* | matriz de confusão |
| *correlation* | correlação |
| *cross-entropy* | perda logarítmica |
| *cross-validation* | validação cruzada |
| *data leakage* | fuga de informação |
| *datasheet* | ficha de dados |
| *decision boundary* | fronteira de decisão |
| *decision tree* | árvore de decisão |
| *demographic parity* | paridade |
| *dendrogram* | dendrograma |
| *dimensionality reduction* | redução de dimensão |
| *drift (data drift, concept drift)* | deriva |
| *early stopping* | paragem antecipada |
| *equal opportunity* | igualdade de oportunidades |
| *Euclidean distance* | distância euclidiana |
| *extrapolation* | extrapolação |
| *fairness* | equidade |
| *false negative* | falso positivo, falso negativo |
| *false positive* | falso positivo, falso negativo |
| *feature* | atributo |
| *feature engineering* | engenharia de atributos |
| *funnel plot* | gráfico em funil |
| *Gini impurity* | índice de Gini |
| *gradient descent* | descida do gradiente |
| *grid search* | procura em grelha |
| *hierarchical clustering* | agrupamento hierárquico |
| *hyperparameter* | hiperparâmetro |
| *imputation* | imputação |
| *inertia* | inércia |
| *interaction* | interação |
| *intercept* | ordenada na origem |
| *interquartile range (IQR)* | quartil, amplitude interquartil |
| *k-anonymity* | k-anonimato |
| *k-nearest neighbors* | vizinhos mais próximos (KNN) |
| *label* | alvo |
| *learning curve* | curva de aprendizagem |
| *learning rate* | taxa de aprendizagem |
| *least squares* | mínimos quadrados |
| *linear regression* | regressão linear |
| *log loss* | perda logarítmica |
| *logistic regression* | regressão logística |
| *machine learning* | aprendizagem automática |
| *mean absolute error* | erro absoluto médio (MAE) |
| *mean squared error* | erro quadrático médio (MSE, RMSE) |
| *median* | mediana |
| *missing data* | dados em falta |
| *missing values* | dados em falta |
| *model card* | ficha de modelo |
| *multicollinearity* | colinearidade |
| *natural frequencies* | frequências naturais |
| *noise* | ruído |
| *nominal (categorical) feature* | atributo nominal |
| *odds* | possibilidades, razão de possibilidades |
| *odds ratio* | possibilidades, razão de possibilidades |
| *one-hot encoding* | codificação one-hot |
| *ordinal feature* | atributo ordinal |
| *outlier* | valor extremo |
| *overfitting* | sobreajuste |
| *permutation importance* | importância por permutação |
| *personal data* | dado pessoal |
| *population* | população |
| *precision* | precisão |
| *principal component* | componente principal |
| *proxy* | proxy |
| *pseudonymization* | pseudonimização |
| *quartile* | quartil, amplitude interquartil |
| *quasi-identifier* | quase-identificador |
| *R-squared* | coeficiente de determinação (R²) |
| *random forest* | floresta aleatória |
| *re-identification* | reidentificação |
| *recall* | sensibilidade |
| *regression* | regressão |
| *regularization* | regularização |
| *residual* | resíduo |
| *ROC curve* | curva ROC e AUC |
| *root mean squared error* | erro quadrático médio (MSE, RMSE) |
| *sample* | amostra |
| *scaling* | escala, normalização |
| *selection bias* | viés de seleção |
| *sensitivity* | sensibilidade |
| *silhouette coefficient* | coeficiente de silhueta |
| *specificity* | especificidade |
| *spurious correlation* | correlação espúria |
| *standard deviation* | desvio padrão |
| *standardization* | escala, normalização |
| *supervised learning* | aprendizagem supervisionada |
| *target* | alvo |
| *test set* | conjunto de teste |
| *threshold* | limiar |
| *time series* | série temporal |
| *training set* | conjunto de treino |
| *true negative rate* | especificidade |
| *underfitting* | subajuste |
| *unsupervised learning* | aprendizagem não supervisionada |
| *validation set* | conjunto de validação |
| *variance* | variância |
| *weight* | coeficiente |
| *within-cluster sum of squares* | inércia |
