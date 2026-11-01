
; TP5 - Watchdog logico Aseba
; Temporizador: 100 ms
; Expiracao nominal: 5 ciclos = 500 ms
; TESTE SEM MOVIMENTO DOS MOTORES

; Memoria reservada:
; _userdata+0 = heartbeat recebido
; _userdata+1 = heartbeat anterior
; _userdata+2 = contador de ciclos sem alteracao
; _userdata+3 = autorizacao logica (0 ou 1)

dc 4
dc _ev.init, inicio
dc _ev.timer0, temporizador

inicio:
    ; Motores sempre parados
    push.s 0
    store motor.left.target
    push.s 0
    store motor.right.target

    ; Inicializar as quatro variaveis
    push.s 0
    store _userdata
    push.s 0
    store _userdata+1
    push.s 0
    store _userdata+2
    push.s 0
    store _userdata+3

    ; Timer0 = 100 ms
    push.s 100
    store timer.period

    stop

temporizador:
    ; Comparar heartbeat recebido com anterior
    load _userdata
    load _userdata+1
    jump.if.not ne, sem_novo_sinal

    ; Novo heartbeat recebido
    load _userdata
    store _userdata+1

    ; Reiniciar contador
    push.s 0
    store _userdata+2

    ; Ativar autorizacao logica
    push.s 1
    store _userdata+3

    jump atualizar

sem_novo_sinal:
    ; Incrementar o contador de ausencia de sinal
    load _userdata+2
    push.s 1
    add
    store _userdata+2

    ; Se contador >= 5, expirar autorizacao
    load _userdata+2
    push.s 5
    jump.if.not lt, expirado

    jump atualizar

expirado:
    push.s 0
    store _userdata+3

atualizar:
    ; Indicadores de diagnostico:
    ; leds.top[0] = contador (limitado a 32)
    ; leds.top[1] = autorizacao (0 ou 1)

    load _userdata+2
    push.s 32
    jump.if.not lt, limitar_contador
    jump guardar_contador

limitar_contador:
    push.s 32
    jump guardar_valor_limitado

guardar_contador:
    load _userdata+2

guardar_valor_limitado:
    store leds.top

    load _userdata+3
    store leds.top+1

    ; Nunca permitir movimento neste teste
    push.s 0
    store motor.left.target
    push.s 0
    store motor.right.target

    stop
