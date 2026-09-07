# Базовые примеры

Это короткие учебные скрипты для проверки отдельных ROS-интерфейсов. Они не являются готовым решением конкурсного модуля и не заменяют аварийный стоп симулятора.

Перед запуском:

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
```

Примеры:

```bash
# Только показать маршрут по сетке 6x6
python3 basic/grid_route.py 0 14 --blocked 8 9

# RMC1 едет вперёд 1 секунду; после этого скрипт отправит stop
python3 basic/move_rmc.py --robot RMC1 --x 0.15 --seconds 1

# Поворот RMC2 на месте
python3 basic/move_rmc.py --robot RMC2 --yaw 0.3 --seconds 1

# Статус положения и лидара
python3 basic/watch_robot.py --robot RMC1

# Управление лифтом RMC2
python3 basic/lift_rmc2.py up
python3 basic/lift_rmc2.py down

# Остановить оба ровера
python3 basic/stop_all.py
```

У RMC1 доступно боковое движение (`linear.y`), у RMC2 оно принудительно запрещено в примере. До движения всегда проверьте имена топиков через `ros2 topic list` и оставьте окно симулятора доступным для ручного STOP.
