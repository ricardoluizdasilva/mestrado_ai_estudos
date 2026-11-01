# Thymio Wireless — módulo partilhado WSL2 / Raspberry Pi 5

## Conteúdo

- `thymio_shutdown.py`: função `encerrar(th, node_id)` extraída **sem alterações** do `testar_timer_contador.py` validado no WSL2 e usada na adaptação testada no Pi 5 Ubuntu.
- `test_sensores_modular.py`: teste seguro de aquisição dos sete sensores de proximidade a 5 Hz, parametrizado. Não comanda movimento; a rotina de encerramento envia velocidade 0 preventivamente.

Requer `thymiodirect==0.1.2`, `pyserial==3.5`, Python com suporte a `asyncio` usado nos ensaios. Depende de atributos internos da biblioteca; não constitui API pública estável.

## Instalação no Pi 5 Ubuntu

Na raiz do repositório `~/projetos/mestrado_ai_estudos`:

```bash
mkdir -p robotica_visao/testes_wireless/comum
cp thymio_modular/thymio_shutdown.py robotica_visao/testes_wireless/comum/
cp thymio_modular/test_sensores_modular.py robotica_visao/testes_wireless/comum/
source ~/ambientes/thymio/bin/activate
python -m py_compile robotica_visao/testes_wireless/comum/*.py
```

## Testar

```bash
cd ~/projetos/mestrado_ai_estudos/robotica_visao/testes_wireless/comum
mkdir -p ../diagnostico/teste_modular
inicio=$(date --iso-8601=seconds)
timeout -s TERM -k 2s 30s python -u test_sensores_modular.py \
  --duration 10 --output ../diagnostico/teste_modular/sensores_10s.csv \
  > ../diagnostico/teste_modular/execucao_10s.log 2>&1
estado=$?
echo "Codigo de saida: $estado"
cat ../diagnostico/teste_modular/execucao_10s.log
sudo journalctl -k --since "$inicio" --no-pager | grep -Ei 'EMI|disabled by hub|USB disconnect|ttyACM' || true
```

O esperado é ~50 amostras, encerramento de threads e tarefas, `Ciclo asyncio fechado corretamente`, código 0 e ausência de desconexões. `timeout` é proteção contra bloqueio na descoberta; código 124 é insucesso no encerramento. A ausência de avisos não prova estabilidade ilimitada.

## Sincronizar com GitHub — executar no Pi 5 Ubuntu

Na raiz do repositório:

```bash
git status --short
git add robotica_visao/testes_wireless/comum/thymio_shutdown.py \
        robotica_visao/testes_wireless/comum/test_sensores_modular.py \
        robotica_visao/testes_wireless/comum/README.md
# Acrescentar seletivamente logs e CSV pequenos e úteis, após rever conteúdo.
git diff --cached --stat
git diff --cached --check
git commit -m 'Adicionar encerramento Thymio partilhado e teste de sensores'
git push origin main
```

Não executar `git add .`: preserva capturas anteriores e evita enviar binários, dados grandes, arquivos de debug ou credenciais. Se ocorrerem alterações remotas, resolver antes de fazer push.

## Pi 5 original (Raspberry Pi OS)

Quando estiver ligado, transferir fisicamente o mesmo hub e dongle, mantendo a configuração estável. No repositório `/dados/projetos/mestrado_ai_estudos`, verificar `git status` antes de `git pull --ff-only`, pois existem alterações locais não sincronizadas. Se houver conflitos, não apagar nem sobrescrever: fazer cópia/commit local ou resolver conscientemente. Para testar:

```bash
cd /dados/projetos/mestrado_ai_estudos/robotica_visao/testes_wireless/comum
conda activate thymio
mkdir -p ../diagnostico/teste_hub_pi_os
inicio=$(date --iso-8601=seconds)
timeout -s TERM -k 2s 30s python -u test_sensores_modular.py \
  --duration 10 --output ../diagnostico/teste_hub_pi_os/sensores_10s.csv \
  > ../diagnostico/teste_hub_pi_os/execucao_10s.log 2>&1
status=$?
echo "Codigo de saida: $status"
cat ../diagnostico/teste_hub_pi_os/execucao_10s.log
sudo journalctl -k --since "$inicio" --no-pager | grep -Ei 'EMI|disabled by hub|USB disconnect|ttyACM' || true
```

Comparar primeiro 10 s e depois várias repetições e 60 s. Se ocorrerem `SerialException` ou desconexões, interromper os ensaios.
