; TP5 v11 - Watchdog e bloqueio de obstaculos EMBARCADOS no Thymio.
; Timer0 100 ms; heartbeat ausente 5 ciclos -> parar.
; Proximidade: 0..4 frente, 5..6 tras; bloqueio >= 2200.
; O bloqueio impede tambem rotacao cujo motor avance para um obstaculo.
; Limite de cada motor: -200 a +200.
; Memoria _userdata +0..+5 inalterada (protocolo Python v10).
;
; +0 heartbeat, +1 anterior, +2 contador, +3 autorizado,
; +4 pedido esquerdo, +5 pedido direito.
;
dc 4
dc _ev.init, inicio
dc _ev.timer0, temporizador

inicio:
    push.s 0
    store motor.left.target
    push.s 0
    store motor.right.target
    push.s 0
    store _userdata
    push.s 0
    store _userdata+1
    push.s 5
    store _userdata+2
    push.s 0
    store _userdata+3
    push.s 0
    store _userdata+4
    push.s 0
    store _userdata+5
    push.s 100
    store timer.period
    stop

temporizador:
    load _userdata
    load _userdata+1
    jump.if.not ne, sem_sinal
    load _userdata
    store _userdata+1
    push.s 0
    store _userdata+2
    push.s 1
    store _userdata+3
    jump aplicar

sem_sinal:
    load _userdata+2
    push.s 1
    add
    store _userdata+2
    load _userdata+2
    push.s 5
    jump.if.not lt, expirado
    jump aplicar

expirado:
    push.s 0
    store _userdata+3
    push.s 0
    store _userdata+4
    push.s 0
    store _userdata+5

aplicar:
    load _userdata+3
    push.s 1
    jump.if.not eq, parar

; Limites independentes, sem tocar nos valores de proximidade.
limitar_esquerdo:
    load _userdata+4
    push.s 200
    jump.if.not le, esquerdo_alto
    load _userdata+4
    push.s -200
    jump.if.not ge, esquerdo_baixo
    jump limitar_direito
esquerdo_alto:
    push.s 200
    store _userdata+4
    jump limitar_direito
esquerdo_baixo:
    push.s -200
    store _userdata+4

limitar_direito:
    load _userdata+5
    push.s 200
    jump.if.not le, direito_alto
    load _userdata+5
    push.s -200
    jump.if.not ge, direito_baixo
    jump verificar_frente
direito_alto:
    push.s 200
    store _userdata+5
    jump verificar_frente
direito_baixo:
    push.s -200
    store _userdata+5

; Se obstaculo frontal e ALGUM motor positivo, parar ambos.
verificar_frente:
    load prox.horizontal
    push.s 2200
    jump.if.not lt, risco_frente
    load prox.horizontal+1
    push.s 2200
    jump.if.not lt, risco_frente
    load prox.horizontal+2
    push.s 2200
    jump.if.not lt, risco_frente
    load prox.horizontal+3
    push.s 2200
    jump.if.not lt, risco_frente
    load prox.horizontal+4
    push.s 2200
    jump.if.not lt, risco_frente
    jump verificar_tras

risco_frente:
    load _userdata+4
    push.s 0
    jump.if.not le, parar
    load _userdata+5
    push.s 0
    jump.if.not le, parar
    jump verificar_tras

; Se obstaculo traseiro e ALGUM motor negativo, parar ambos.
verificar_tras:
    load prox.horizontal+5
    push.s 2200
    jump.if.not lt, risco_tras
    load prox.horizontal+6
    push.s 2200
    jump.if.not lt, risco_tras
    jump aplicar_motores

risco_tras:
    load _userdata+4
    push.s 0
    jump.if.not ge, parar
    load _userdata+5
    push.s 0
    jump.if.not ge, parar

aplicar_motores:
    push.s 10
    store leds.top
    load _userdata+4
    store motor.left.target
    load _userdata+5
    store motor.right.target
    jump diagnostico

parar:
    push.s 20
    store leds.top
    push.s 0
    store motor.left.target
    push.s 0
    store motor.right.target

diagnostico:
    load _userdata+3
    store leds.top+1
    stop
