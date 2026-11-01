
; TP5 - Diagnostico de timer0
; Periodo nominal: 100 ms
; Motores sempre parados

dc 4
dc _ev.init, inicio
dc _ev.timer0, temporizador

inicio:
    push.s 0
    store motor.left.target
    push.s 0
    store motor.right.target

    ; Contador de diagnostico = 0
    push.s 0
    store leds.top

    ; Configurar timer0 para 100 ms
    push.s 100
    store timer.period

    stop

temporizador:
    ; Incrementar contador observavel
    load leds.top
    push.s 1
    add
    store leds.top

    ; Continuar a manter os motores parados
    push.s 0
    store motor.left.target
    push.s 0
    store motor.right.target

    stop
