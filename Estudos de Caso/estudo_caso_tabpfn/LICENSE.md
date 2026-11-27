# Licença

© 2026 Ricardo Luiz da Silva (RLdS)

Este estudo usa duas licenças, uma para os conteúdos e outra para o código. Os dados e os modelos de terceiros mantêm as suas próprias licenças.

## Conteúdos: CC BY-NC-SA 4.0

Os textos, as explicações e os notebooks no seu conjunto estão licenciados sob a licença [Creative Commons Atribuição-NãoComercial-CompartilhaIgual 4.0 Internacional (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.pt). O texto completo está em [`LICENSE-CC-BY-NC-SA-4.0.txt`](LICENSE-CC-BY-NC-SA-4.0.txt).

Podes copiar, partilhar e adaptar estes materiais, desde que:

- **Atribuição:** indiques o autor (Ricardo Luiz da Silva, RLdS), incluas uma ligação para a licença e assinales se fizeste alterações;
- **Não comercial:** não os uses para fins comerciais;
- **Compartilha igual:** distribuas as adaptações com a mesma licença.

Sugestão de atribuição:

> «Estudo de caso: modelos fundacionais para dados tabulares (TabPFN)», de Ricardo Luiz da Silva (RLdS), https://github.com/ricardoluizdasilva/mestrado_ai_estudos, licenciado sob CC BY-NC-SA 4.0.

## Código: MIT

O código-fonte está licenciado sob a [licença MIT](LICENSE-MIT.txt). Isto inclui o código das células dos notebooks e os ficheiros `.py` que venham a ser acrescentados.

## Conteúdos de terceiros

- **Dados do TSE.** Os resultados e o perfil do eleitorado das eleições de 2026 vêm do Portal de Dados Abertos do Tribunal Superior Eleitoral, publicados com a licença Creative Commons Atribuição. A base em `dados/` é uma obra derivada: agrega esses dados por município.
- **Dados do IBGE.** Os indicadores do Censo Demográfico 2022 e a divisão territorial vêm do IBGE (sistema SIDRA e API de localidades). Devem ser citados com a indicação da fonte.
- **Tabela de códigos.** A correspondência entre os códigos de município do TSE e do IBGE vem do repositório público `betafcc/Municipios-Brasileiros-TSE`. As condições de utilização são as indicadas nesse repositório.
- **Conjuntos do OpenML.** Os conjuntos de dados usados nas fases de classificação são descarregados do OpenML durante a execução e não são distribuídos aqui. Cada um tem a licença indicada na respetiva página.
- **TabPFN.** O código do pacote `tabpfn` é distribuído pela Prior Labs com a licença Apache 2.0. Os pesos do TabPFN v2 têm uma licença aberta com requisito de atribuição; os pesos das versões 2.5 e posteriores têm **licença não comercial**. Este repositório não distribui pesos de modelos.
- As restantes bibliotecas (LightGBM, scikit-learn, NumPy, pandas, SciPy, matplotlib) não são distribuídas com o estudo e têm as suas próprias licenças.

Os detalhes sobre os dados estão em [`dados/LEIA-ME.md`](dados/LEIA-ME.md).
