#!/usr/bin/env python3
"""Подаёт простую команду скорости на RMC1 или RMC2 и затем останавливает его."""

import argparse
import time

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--robot", choices=("RMC1", "RMC2"), required=True)
    parser.add_argument("--x", type=float, default=0.0, help="Скорость вперёд, м/с")
    parser.add_argument("--y", type=float, default=0.0, help="Боковая скорость RMC1, м/с")
    parser.add_argument("--yaw", type=float, default=0.0, help="Угловая скорость, рад/с")
    parser.add_argument("--seconds", type=float, default=1.0)
    args = parser.parse_args()

    if args.seconds <= 0:
        parser.error("--seconds должен быть больше нуля")
    if args.robot == "RMC2" and args.y != 0:
        parser.error("RMC2 не поддерживает боковое движение: используйте --y 0")

    rclpy.init()
    node = Node("mvch_basic_move")
    publisher = node.create_publisher(Twist, f"/{args.robot}/cmd_vel", 10)
    command = Twist()
    command.linear.x = args.x
    command.linear.y = args.y
    command.angular.z = args.yaw

    print(f"{args.robot}: cmd_vel x={args.x}, y={args.y}, yaw={args.yaw}")
    started = time.monotonic()
    try:
        while time.monotonic() - started < args.seconds:
            publisher.publish(command)
            rclpy.spin_once(node, timeout_sec=0.05)
    finally:
        stop = Twist()
        for _ in range(5):
            publisher.publish(stop)
            rclpy.spin_once(node, timeout_sec=0.05)
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()

