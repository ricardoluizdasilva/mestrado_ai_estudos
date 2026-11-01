
; TP5 - Watchdog de motores
; Intervalo: 100 ms
; Expiracao nominal: 500 ms
; Teste experimental com rodas suspensas

; _userdata+0 = heartbeat
; _userdata+1 = heartbeat anterior
; _userdata+2 = contador sem heartbeat
; _userdata+3 = autorizacao
; _userdata+4 = comando motor esquerdo
; _userdata+5 = comando motor direito

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

    ; Heartbeat novo
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


; Aplicar comandos apenas com autorizacao valida

aplicar:
    load _userdata+3
    push.s 1
    jump.if.not eq, parar

; Limitar motor esquerdo a [-20, 20]

limitar_esquerdo:
    load _userdata+4
    push.s 200
    jump.if.not le, esquerdo_alto

    load _userdata+4
    push.s -200
    jump.if.not ge, esquerdo_baixo

    jump aplicar_esquerdo

esquerdo_alto:
    push.s 200
    store _userdata+4
    jump aplicar_esquerdo

esquerdo_baixo:
    push.s -200
    store _userdata+4

aplicar_esquerdo:
    load _userdata+4
    store motor.left.target

; Limitar motor direito a [-20, 20]

limitar_direito:
    load _userdata+5
    push.s 200
    jump.if.not le, direito_alto

    load _userdata+5
    push.s -200
    jump.if.not ge, direito_baixo

    jump aplicar_direito

direito_alto:
    push.s 200
    store _userdata+5
    jump aplicar_direito

direito_baixo:
    push.s -200
    store _userdata+5

aplicar_direito:
    load _userdata+5
    store motor.right.target
    jump diagnostico

; Paragem quando a autorizacao expira

parar:
    push.s 0
    store motor.left.target

    push.s 0
    store motor.right.target

    jump diagnostico

diagnostico:
    ; Expor autorizacao para diagnostico
    load _userdata+3
    store leds.top+1

    stop
