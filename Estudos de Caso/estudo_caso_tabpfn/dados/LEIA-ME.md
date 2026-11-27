# Dados do estudo de caso

Esta pasta contém a base por município usada nas fases 3 a 6 do estudo. Foi construída pelo notebook [`02_Recolha_Base_Municipios_IBGE_TSE.ipynb`](../fase_0_preliminar/02_Recolha_Base_Municipios_IBGE_TSE.ipynb), que pode ser executado de novo para a reproduzir.

## Ficheiros

| Ficheiro | Conteúdo |
| --- | --- |
| `base_municipios_eleicoes2026_censo2022.csv` | Uma linha por município do Brasil: 5 571 linhas e 61 colunas |
| `base_municipios_dicionario.csv` | Uma linha por variável: origem, descrição, unidade, filtros aplicados e período |

Os dois ficheiros usam `;` como separador e codificação UTF-8 com BOM. Os códigos de município têm de ser lidos como texto, para não perderem os zeros à esquerda:

```python
import pandas as pd

base = pd.read_csv(
    "base_municipios_eleicoes2026_censo2022.csv",
    sep=";", encoding="utf-8-sig",
    dtype={"id_municipio_ibge": str, "id_municipio_tse": str, "id_uf": str},
)
```

## Fontes

| Fonte | O que fornece | Endereço |
| --- | --- | --- |
| TSE – Resultados 2026, «Detalhe da apuração por município e zona» | Eleitores aptos, comparecimento, abstenções, votos brancos e nulos, nas duas voltas | <https://dadosabertos.tse.jus.br/dataset/resultados-2026> |
| TSE – Eleitorado 2026, «Perfil do eleitorado» | Eleitores por género, faixa etária, escolaridade e estado civil; biometria | <https://dadosabertos.tse.jus.br/dataset/eleitorado-2026> |
| IBGE – Censo Demográfico 2022, tabelas SIDRA 10295, 10281, 10297, 10268 e 10296 | Rendimento domiciliar per capita, rendimento do trabalho, nível de ocupação, classes de rendimento | <https://sidra.ibge.gov.br/tabela/10295> |
| IBGE – API de localidades | Nomes dos municípios, estado, região e regiões intermédia e imediata | <https://servicodados.ibge.gov.br/api/v1/localidades/municipios> |
| Tabela de códigos TSE–IBGE | Correspondência entre o código do TSE (5 dígitos) e o do IBGE (7 dígitos) | <https://github.com/betafcc/Municipios-Brasileiros-TSE> |

Os dados do TSE foram descarregados em 26 de novembro de 2026. O ficheiro do perfil do eleitorado tem data de geração de 14 de julho de 2026.

## Como a base foi construída

- **Resultados eleitorais:** filtrados para o cargo de Presidente, sem o voto no exterior (`ZZ`), com as zonas eleitorais somadas por município. A taxa de abstenção é calculada depois da soma.
- **Perfil do eleitorado:** agregado por município e convertido em percentagens do eleitorado. A variável `pct_voto_facultativo` junta os eleitores de 16 e 17 anos, os de 70 ou mais e os analfabetos, sem contar ninguém duas vezes.
- **Censo:** uma variável por tabela, com as classificações no total, exceto no nível de ocupação, que é o do grupo de 14 anos ou mais.
- **Junção:** pelo código de município do TSE, depois de convertido a partir do código do IBGE.

## Verificações feitas

- Sem códigos de município duplicados, do IBGE ou do TSE.
- Em todos os municípios e nas duas voltas, os eleitores aptos são iguais à soma de comparecimento e abstenções.
- Os grupos de idade, os níveis de escolaridade e as classes de rendimento somam 100.
- Totais nacionais sem o exterior: 157 828 968 eleitores aptos na 1.ª volta, abstenção de 20,84 % na 1.ª volta e de 18,99 % na 2.ª.
- Os valores extremos do rendimento do trabalho coincidem com os divulgados pelo IBGE.

## Limitações a ter em conta

- **Um município sem dados do Censo.** Boa Esperança do Norte (MT) foi criado depois do Censo 2022: tem dados eleitorais, mas não tem os indicadores socioeconómicos. Para modelar ficam 5 570 municípios.
- **Correspondência manual.** Esse mesmo município não constava da tabela de códigos; o seu código do TSE (`73709`) foi acrescentado à mão, depois de confirmado no ficheiro de resultados.
- **Desfasamento temporal.** Os indicadores do Censo são de 2022 e as eleições de 2026.
- **Estimativas por amostra.** As tabelas de rendimento do Censo são resultados preliminares da amostra, com maior erro nos municípios pequenos.
- **Dados agregados.** A base descreve municípios, não pessoas. Não permite concluir como votou nenhum grupo de eleitores.
- **Coluna constante.** `pop_classes_rdpc_sm_total` vale sempre 100 e deve ser retirada antes de modelar.
- **Eleitores aptos entre voltas.** O número de aptos de um município pode diferir ligeiramente entre a 1.ª e a 2.ª volta, por causa das transferências temporárias de eleitores.

## Licenças

- Os dados do TSE são publicados no Portal de Dados Abertos com a licença Creative Commons Atribuição. Ao reutilizar esta base, cite o TSE como fonte dos dados eleitorais.
- Os dados do IBGE devem ser citados com a indicação da fonte (IBGE, Censo Demográfico 2022).
- A tabela de códigos é mantida por um particular no GitHub e não é uma fonte oficial.

Esta base é uma agregação desses dados e mantém as condições das fontes originais, e não a licença dos conteúdos do estudo.
