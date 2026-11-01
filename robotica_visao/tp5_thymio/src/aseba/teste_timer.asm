; TP5 - Teste inicial do temporizador Aseba
; Programa sem comandos de movimento

dc 4
dc _ev.init, inicio
dc _ev.timer0, temporizador

inicio:
    push.s 0
    store motor.left.target

    push.s 0
    store motor.right.target

    ; Configurar timer.period[0] = 100 ms
    push.s 100
    store timer.period

    stop

temporizador:
    ; Manter ambos os motores parados
    push.s 0
    store motor.left.target

    push.s 0
    store motor.right.target

    stop