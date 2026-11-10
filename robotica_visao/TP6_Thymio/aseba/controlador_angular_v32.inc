# Controlador angular - executar no fim de timer0
# Estados: 0=pronto, 1=rotacao, 2=paragem,
# 3=concluido, 4=timeout/abortado.
# Modo 0=simulacao; modo 1=movimento real.

if ctl_state == 0 then
    motor.left.target = 0
    motor.right.target = 0

    if ctl_request == 1 then
        ctl_request = 0
        ctl_active_mode = ctl_mode
        ctl_ticks = 0
        ctl_angle_b = 0
        ctl_stop_angle_b = 0
        ctl_state = 1
    end
end

if ctl_state == 1 then
    ctl_ticks = ctl_ticks + 1

    if ctl_active_mode == 0 then
        # Incremento artificial: aproximadamente 2,81 graus/ciclo
        ctl_angle_b = ctl_ticks * 512
    else
        ctl_angle_b = odo_theta_b
    end

    if ctl_abort == 1 or ctl_ticks >= 50 then
        ctl_state = 4
        motor.left.target = 0
        motor.right.target = 0
    elseif ctl_active_mode == 1 and odo_turns != 0 then
        ctl_state = 4
        motor.left.target = 0
        motor.right.target = 0
    elseif ctl_angle_b >= 6736 then
        # Paragem antecipada, aproximadamente 37 graus
        ctl_stop_angle_b = ctl_angle_b
        ctl_state = 2
        ctl_settle_ticks = 0
        motor.left.target = 0
        motor.right.target = 0
    elseif ctl_active_mode == 0 then
        # Nunca movimentar os motores no modo simulacao
        motor.left.target = 0
        motor.right.target = 0
    elseif ctl_angle_b >= 3641 then
        # Desacelerar depois de aproximadamente 20 graus
        motor.left.target = -30
        motor.right.target = 30
    else
        motor.left.target = -60
        motor.right.target = 60
    end
end

if ctl_state == 2 then
    motor.left.target = 0
    motor.right.target = 0
    ctl_settle_ticks = ctl_settle_ticks + 1
    if ctl_settle_ticks >= 8 then
        ctl_state = 3
    end
end

if ctl_state == 3 or ctl_state == 4 then
    motor.left.target = 0
    motor.right.target = 0
end
