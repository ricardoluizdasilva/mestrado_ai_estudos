# Dados do projeto

## `bank-additional-full.csv`

Registos de campanhas de telemarketing de um banco português, de maio de 2008 a novembro de 2010, para a venda de depósitos a prazo: 41 188 linhas (uma por chamada) e 21 colunas, separadas por ponto e vírgula.

| | |
| --- | --- |
| **Nome** | *Bank Marketing* (versão com indicadores sociais e económicos) |
| **Autores** | S. Moro, P. Cortez e P. Rita |
| **Fonte** | UCI Machine Learning Repository, https://doi.org/10.24432/C5K306 |
| **Licença** | [Creative Commons Atribuição 4.0 Internacional (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/deed.pt) |
| **Alterações** | Nenhuma. O ficheiro é o original; as transformações são feitas em código, nos notebooks. |
| **SHA-256** | `74adfc578bf77a7ff4bb1ba4a9f8709d9e3c6907342959c2c8416847e0afb4d8` |

Citação pedida pelos autores:

> S. Moro, P. Cortez e P. Rita (2014). A Data-Driven Approach to Predict the Success of Bank Telemarketing. *Decision Support Systems*, 62, 22–31. https://doi.org/10.1016/j.dss.2014.03.001

## Notas de utilização

- O dicionário de dados, em português, está na parte 1 do projeto.
- Os valores em falta aparecem como `unknown` (colunas de texto) e como `999` (coluna `pdays`).
- A coluna `duration` só é conhecida depois da chamada e não deve entrar em modelos de previsão.
- O ficheiro não tem ano nem identificador de cliente. As linhas estão ordenadas por data.
- Segundo a documentação original, alguns atributos foram retirados por motivos de privacidade. Mesmo assim, o ficheiro deve ser tratado como dados pessoais (ver a parte 3 do projeto).
