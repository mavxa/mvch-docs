#!/usr/bin/env python3
"""Поднимает или опускает лифт RMC2 через штатный ROS-топик."""

import argparse
import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64, String


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("state", choices=("up", "down"))
    parser.add_argument("--wait", type=float, default=6.0, help="Сколько ждать статус, с")
    args = parser.parse_args()

    rclpy.init()
    node = Node("mvch_basic_lift")
    publisher = node.create_publisher(Float64, "/RMC2/lift", 10)
    statuses = []
    node.create_subscription(String, "/RMC2/lift_status", lambda msg: statuses.append(msg.data), 10)

    height = 0.1 if args.state == "up" else 0.0
    print(f"RMC2 lift: {args.state}, команда {height}")
    for _ in range(5):
        publisher.publish(Float64(data=height))
        rclpy.spin_once(node, timeout_sec=0.1)

    deadline = time.monotonic() + args.wait
    while time.monotonic() < deadline and not statuses:
        rclpy.spin_once(node, timeout_sec=0.1)

    if statuses:
        print(f"Статус: {statuses[-1]}")
    else:
        print("Нового lift_status нет. Это возможно, если лифт уже был в нужном положении.")

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()

