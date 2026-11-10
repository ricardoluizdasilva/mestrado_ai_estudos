# TP6 — Odometria com Thymio (Python + Aseba)

Baseado em **TP6 – Odometria.pdf**, *Visão Computacional e Sistemas Robóticos, Lab 6*.
Sem ROS2. Projeto para Thymio-II Wireless via `thymiodirect 0.1.2` e `pyserial 3.5`.

## Estado de implementação

| Exercício | Entrega | Estado |
|---|---|---|
| 1 | Curva suave à esquerda durante ~2 s | Script de movimento preparado; **requer execução e medição reais** |
| 2 | Pose [Δx, Δy, Δθ] com régua e transferidor, extra 5 repetições | Ficha CSV e resumo média/DP; **preencher medidas reais** |
| 3 (extra) | Curva direita, 5 repetições | Script e ficha CSV; **medir** |
| 4 | Calibrar conversão `motor.left.speed` → cm/s | Experiência de retas e mínimos quadrados; **Kd desconhecido até medir** |
| 5 | Estimar odometria | Integrador RK2 em Python, testes unitários |
| 6 | Comparar com pose manual | Comparação e erros em Python, **após dados reais** |
| 7 | Atualizar pose continuamente no mundo | Integrador Python funcional a partir de logs; protótipo Aseba embarcado com `math.muldiv` e trigonometria em 16 bits, **a validar no robô** |
| 8 (extra) | Quadrado e erro final | Plano de quatro arestas/rotações e registo de velocidades; **após calibração e ensaio supervisionado** |
| 9 (extra) | Correção num canto conhecido | `corrigir_marco.py` faz correção **offline com pose do canto fornecida manualmente**; deteção automática da parede não implementada |

## Constantes geométricas do enunciado

- Raio roda `r=2.2 cm`
- Distância entre eixos `L=9.35 cm`
- Comprimento base 11.0 cm, largura 11.18 cm, altura 7.7 cm
- Cinemática diferencial: `dl=Kd_l * motor.left.speed * dt`, `dr=Kd_r * motor.right.speed * dt`
- `ds=(dr+dl)/2`, `dtheta=(dr-dl)/L`
- `x+=ds*cos(theta+dtheta/2)`, `y+=ds*sin(theta+dtheta/2)`, `theta+=dtheta`
- Coordenadas: x avança na orientação inicial, y positivo à esquerda, ângulo positivo anti-horário.

**Atenção:** `motor.left.target` define a referência; `motor.left.speed` é a leitura real. O coeficiente Kd deve ser medido no piso e robô utilizados. O raio da roda é um dado geométrico, não substitui essa calibração. As características aproximadas da API oficial não são valores experimentais.

## Instalação no Pi 5 inicial

```bash
conda activate thymio
cd /dados/projetos/mestrado_ai_estudos/robotica_visao
# extrair ou copiar a pasta TP6_Thymio para cá
cd TP6_Thymio
python -m unittest discover -s tests -v
```

No Pi 5 Ubuntu, utilizar `source ~/ambientes/thymio/bin/activate` e copiar a mesma pasta para `~/projetos/mestrado_ai_estudos/robotica_visao/TP6_Thymio`.

## Segurança e aquisição real

1. Colocar o Thymio numa superfície plana **no chão, nunca em cima de uma mesa**, com pelo menos 1 metro desimpedido; supervisionar e manter acesso à paragem física.
2. Confirmar hub D-Link, porta série estável e motores parados; um programa Aseba anteriormente carregado pode permanecer no robô — limpar comportamentos autónomos antes de começar.
3. **Sem `--execute`, o script apenas mostra o plano e não move o robô.** Limite por comando de 200 unidades e teste individual de até 3 segundos; usar sempre um `timeout` exterior adequado (p.ex. 30 s para ensaio de 2 s). O script trata SIGTERM tentando parar os motores, mas uma falha na comunicação ou SIGKILL pode impedir o comando de paragem; manter uma forma física de imobilizar/desligar o robô.
4. A rotina de encerramento foi extraída do `testar_timer_contador.py`, validado no WSL2 e no Pi Ubuntu. É baseada em internals do `thymiodirect 0.1.2` e tem de ser novamente confirmada em cada ambiente.
5. Não executar dois processos na mesma porta `ttyACM`.

### Exercício 1 — esquerda por 2 s

```bash
python scripts/executar_movimento.py --mode left --left 80 --right 120 --duration 2 --output resultados/esquerda_1.csv
# Se o plano estiver correto, colocar o robô na marca inicial e autorizar:
timeout -s TERM -k 2s 30s python -u scripts/executar_movimento.py --mode left --left 80 --right 120 --duration 2 --output resultados/esquerda_1.csv --execute
```

Medir com régua/transferidor Δx, Δy, Δθ desde uma pose inicial marcada no piso. Repetir com nomes `esquerda_2.csv` ... `esquerda_5.csv`. Preencher `modelos/medicoes_pose.csv` (coluna `log_file` = `resultados/esquerda_1.csv` etc.) e calcular:

```bash
python scripts/resumir_medicoes_manuais.py --medicoes modelos/medicoes_pose.csv
```

### Exercício 3 (extra) — direita

```bash
timeout -s TERM -k 2s 30s python -u scripts/executar_movimento.py --mode right --left 120 --right 80 --duration 2 --output resultados/direita_1.csv --execute
```

Repetir cinco vezes, medindo a pose final e preenchendo `modelos/medicoes_pose.csv`.

### Exercício 4 — calibração das velocidades reais

Para pelo menos **5 ensaios retos** com comandos diversos (por exemplo 80/80, 100/100, 120/120) e durações entre 1–3 s:

```bash
timeout -s TERM -k 2s 30s python -u scripts/executar_movimento.py --mode straight --left 100 --right 100 --duration 2 --output resultados/reta_1.csv --execute
```

Meça a distância do centro do robô ao longo da reta, incluindo a travagem observada; documente o possível erro da aproximação. Preencha `modelos/medicoes_calibracao.csv` com o caminho dos logs e a distância em cm. O script calcula `Kd` por ajuste `d = Kd * integral((v_l+v_r)/2 dt)`, com intercepto fixo zero; os desvios entre repetições ajudam a avaliar a qualidade da calibração.

```bash
python scripts/calibrar.py --medicoes modelos/medicoes_calibracao.csv --saida resultados/calibracao.json
```

**Cuidado:** o script regista a velocidade **durante o comando**, mas não integra a desaceleração após a paragem. Se a distância medida incluir o deslocamento de travagem, Kd ficará ligeiramente enviesado. Para um relatório rigoroso, medir ou modelar também esse intervalo; é uma limitação explicitada, não um valor oculto.

### Exercícios 5–6 — integração e comparação

```bash
python scripts/analisar.py --log resultados/esquerda_1.csv --calibracao resultados/calibracao.json --saida resultados/odometria_esquerda_1.csv
python scripts/analisar.py --medicoes-manuais modelos/medicoes_pose.csv --calibracao resultados/calibracao.json
```

As médias e desvios-padrão do enunciado usam `statistics.stdev` (DP amostral, n−1). As orientações são dadas em graus nas medições e em radianos internamente; o erro angular é normalizado para [-180°,180°[.

### Exercício 7 — odometria em tempo real / embarcada

- `scripts/odometria.py`: integrador de pose em tempo discreto no computador a partir de velocidades reais. O `executar_movimento.py` também regista a pose incremental quando recebe `--calibration`.
- `aseba/odometria_embarcada_template.aesl`: **protótipo** de execução periódica a cada 100 ms no Thymio, com aritmética inteira, `math.muldiv`, `math.cos` e `math.sin`. Não comanda motores. É necessário testar compilação em Aseba Studio e validar o ganho escalado e a leitura das variáveis personalizadas.
- Depois de obter `resultados/calibracao.json`:

```bash
python scripts/preparar_aseba.py --calibracao resultados/calibracao.json
```

**Não carregar diretamente um programa Aseba não testado quando o robô estiver a mover-se.** O enquadramento inicial do exercício 7 será validado com dados reais antes de avançar à execução embarcada.

### Visualização da trajetória

```bash
python scripts/plotar_trajetoria.py --trajetoria resultados/odometria_esquerda_1.csv --saida resultados/odometria_esquerda_1.png
```

### Exercício 8 (extra) — quadrado

Após calibração, inspecione primeiro o plano (sem movimento):

```bash
python scripts/executar_movimento.py --mode square --side-cm 15 --speed 110 --turn-speed 80 --calibration resultados/calibracao.json --output resultados/quadrado.csv
```

Se tempos/área forem seguros, executar com `--execute` e watchdog externo suficientemente longo para as quatro arestas e quatro rotações. Como os motores não são exatamente iguais, o quadrado deve ser **avaliado, não presumido perfeito**.

### Exercício 9 (extra) — correção por marco

Com a pose conhecida de um canto (medida manualmente), e instante de observação do marco, corrigir uma trajetória **offline**:

```bash
python scripts/corrigir_marco.py --trajetoria resultados/odometria_quadrado.csv --tempo-marco 10.0 --x-marco 15 --y-marco 15 --theta-marco-deg 90
```

Comparar os erros finais antes/depois. O enunciado pede um canto com posição conhecida; deteção sensorial automática e atualização *online* permanecem extensões a implementar.

## Organização das evidências

- `resultados/*.csv`: velocidades reais, medições, odometria e comparação.
- `resultados/calibracao.json`: **apenas valores reais medidos**.
- Fotos do chão marcado, régua e transferidor; vídeo de cada ensaio; temperatura/piso e parâmetros de controlo.
- Incluir `uname -a`, `python --version`, `pip show thymiodirect`, ligação USB, conclusão segura e logs de `journalctl`.

## Referências

- Enunciado TP6 fornecido (3 páginas).
- Thymio / Aseba API: https://wiki.thymio.org/en:thymioapi
- Aseba native functions: https://mobsya.github.io/aseba/aseba-std-natives.html

## Estado: código preparado, **não validado no robô neste TP6**

Os testes unitários do modelo geométrico passaram. Os movimentos, calibração, programa Aseba e extras dependem de medições e execução supervisionada com o Thymio real.
