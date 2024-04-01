#!/bin/python3

"""
mission.py
"""

from time import sleep
import threading
import argparse
import rclpy
from as2_python_api.drone_interface import DroneInterface


def drone_run(drone_interface: DroneInterface, _id: int):
    """ Run the mission """

    speed = 0.5
    takeoff_height = 1.0

    sleep_time = 2.0

    print("Start mission")

    ##### ARM OFFBOARD #####
    print("Arm")
    drone_interface.offboard()
    sleep(sleep_time)
    print("Offboard")
    drone_interface.arm()
    sleep(sleep_time)

    ##### TAKE OFF #####
    print("Take Off")
    drone_interface.takeoff(takeoff_height, speed=1.0)
    print("Take Off done")
    sleep(sleep_time)

    ##### GO TO #####
    # print(f"Go to with path facing {goal}")
    drone_interface.go_to.go_to_point_with_yaw(
        [0, 0, 5.0], speed=speed, angle=3.14, frame_id=f"panel_{_id}")
    print("Go to done")
    sleep(sleep_time)
    drone_interface.point_gimbal.point_gimbal(
        _x=0.0, _y=0.0, _z=0.0, frame_id=f"panel_{_id}")

    ##### LAND #####
    # print("Landing")
    # drone_interface.land(speed=0.5)
    # print("Land done")

    # drone_interface.disarm()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Execute mission for n drones')

    parser.add_argument('number_of_drones', metavar='drones', type=int,
                        help='number of drones to generate')

    args = parser.parse_args()

    num_drones = args.number_of_drones    # Number of Drones

    rclpy.init()

    threads = []

    for i in range(num_drones):
        uav = DroneInterface(f"drone{i}", verbose=False, use_sim_time=True)
        uav.load_module('point_gimbal')
        thread = threading.Thread(target=drone_run, args=(uav, 10*i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    while True:
        pass

    uav.shutdown()
    rclpy.shutdown()

    print("Clean exit")
    exit(0)
