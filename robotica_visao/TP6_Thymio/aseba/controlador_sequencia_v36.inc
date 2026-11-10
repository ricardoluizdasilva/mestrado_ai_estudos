# V3.6 - Um avanço e uma rotação, modo físico
# 0=pronto, 1=reta, 2=estabilizar reta
# 3=rodar, 4=estabilizar rotação
# 5=concluído, 6=falha

motor.left.target = 0
motor.right.target = 0

if seq_state == 0 then
    if seq_request == 1 and seq_arm == 1 then
        seq_request = 0
        seq_arm = 0
        seq_ticks = 0
        seq_line_ticks = 0
        seq_turn_ticks = 0
        seq_progress = 0
        seq_heading_b = 0
        seq_angle_b = 0
        seq_wait = 0
        seq_fault = 0
        seq_state = 1
    end

elseif seq_state == 1 then
    seq_ticks = seq_ticks + 1
    seq_line_ticks = seq_line_ticks + 1

    seq_progress = seq_progress + (odo_dl_01mm + odo_dr_01mm) * 5
    seq_heading_b = seq_heading_b + odo_dtheta_b

    seq_correction = (0 - seq_heading_b) / 182
    if seq_correction > 8 then
        seq_correction = 8
    end
    if seq_correction < -8 then
        seq_correction = -8
    end

    if seq_line_ticks >= 60 then
        seq_fault = 2
        seq_state = 6
    elseif seq_heading_b > 2730 or seq_heading_b < -2730 then
        seq_fault = 3
        seq_state = 6
    elseif seq_progress >= 9700 then
        seq_state = 2
        seq_wait = 0
    else
        if seq_progress >= 7000 then
            motor.left.target = 40 - seq_correction
            motor.right.target = 40 + seq_correction
        else
            motor.left.target = 80 - seq_correction
            motor.right.target = 80 + seq_correction
        end
    end

elseif seq_state == 2 then
    seq_ticks = seq_ticks + 1
    seq_wait = seq_wait + 1
    if seq_wait >= 8 then
        seq_wait = 0
        seq_angle_b = 0
        seq_state = 3
    end

elseif seq_state == 3 then
    seq_ticks = seq_ticks + 1
    seq_turn_ticks = seq_turn_ticks + 1
    seq_angle_b = seq_angle_b + odo_dtheta_b

    if seq_turn_ticks >= 100 then
        seq_fault = 4
        seq_state = 6
    elseif seq_angle_b < -1000 then
        seq_fault = 5
        seq_state = 6
    elseif seq_angle_b >= 16111 then
        seq_state = 4
        seq_wait = 0
    elseif seq_angle_b >= 11833 then
        motor.left.target = -30
        motor.right.target = 30
    else
        motor.left.target = -60
        motor.right.target = 60
    end

elseif seq_state == 4 then
    seq_ticks = seq_ticks + 1
    seq_wait = seq_wait + 1
    if seq_wait >= 8 then
        seq_state = 5
    end
end

# Obstáculo frontal ou pedido de interrupção.
if seq_state >= 1 and seq_state <= 4 then
    if seq_abort == 1 then
        seq_fault = 6
        seq_state = 6
    elseif prox.horizontal[0] > 3000 or prox.horizontal[1] > 3000 or prox.horizontal[2] > 3000 or prox.horizontal[3] > 3000 or prox.horizontal[4] > 3000 then
        seq_fault = 1
        seq_state = 6
    end
end

if seq_ticks >= 160 and seq_state != 5 then
    seq_fault = 7
    seq_state = 6
end

if seq_state == 5 or seq_state == 6 then
    motor.left.target = 0
    motor.right.target = 0
end

if seq_state != seq_last_state then
    if seq_history_n < 6 then
        seq_history[seq_history_n] = seq_state
        seq_history_n = seq_history_n + 1
    end
    seq_last_state = seq_state
end
