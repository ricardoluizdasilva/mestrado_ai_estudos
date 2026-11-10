# TP6 - Controlador linear embarcado V3.4
# Estado: 0=pronto, 1=avancar, 2=estabilizar,
# 3=concluido, 4=abortado
# Modo: 0=simulacao, 1=movimento real

if lin_state == 0 then
    motor.left.target = 0
    motor.right.target = 0

    if lin_request == 1 then
        lin_request = 0
        lin_active_mode = lin_mode
        lin_ticks = 0
        lin_progress_001mm = 0
        lin_stop_001mm = 0
        lin_settle_ticks = 0
        lin_state = 1
    end
end

if lin_state == 1 then
    lin_ticks = lin_ticks + 1

    if lin_active_mode == 0 then
        # Simulacao: 0,25 cm por ciclo
        lin_progress_001mm = lin_progress_001mm + 250
    else
        # Incrementos das duas rodas em unidades de 0,1 mm.
        # Distancia media em unidades de 0,01 mm.
        lin_increment_001mm = odo_dl_01mm + odo_dr_01mm
        lin_increment_001mm = lin_increment_001mm * 5
        lin_progress_001mm = lin_progress_001mm + lin_increment_001mm
    end

    if lin_abort == 1 or lin_ticks >= 60 then
        lin_state = 4
    elseif lin_active_mode != 0 and lin_active_mode != 1 then
        lin_state = 4
    elseif lin_progress_001mm < -100 then
        lin_state = 4
    elseif lin_progress_001mm >= 9500 then
        lin_stop_001mm = lin_progress_001mm
        lin_settle_ticks = 0
        lin_state = 2
    end

    if lin_state == 1 and lin_active_mode == 1 then
        if lin_progress_001mm >= 7000 then
            motor.left.target = 40
            motor.right.target = 40
        else
            motor.left.target = 80
            motor.right.target = 80
        end
    else
        motor.left.target = 0
        motor.right.target = 0
    end
end

if lin_state == 2 then
    motor.left.target = 0
    motor.right.target = 0
    lin_settle_ticks = lin_settle_ticks + 1

    if lin_abort == 1 then
        lin_state = 4
    elseif lin_settle_ticks >= 8 then
        lin_state = 3
    end
end

if lin_state == 3 or lin_state == 4 then
    motor.left.target = 0
    motor.right.target = 0
end
