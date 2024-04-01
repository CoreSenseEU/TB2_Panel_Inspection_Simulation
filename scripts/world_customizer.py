"""
Random world generator
"""
from __future__ import annotations
import argparse
import math
from pathlib import Path
import random
from jinja2 import Environment, FileSystemLoader

__authors__ = "David Ho, Pedro Arias Perez"
__license__ = "BSD-3-Clause"


def distance(point1: tuple[float, float], point2: tuple[float, float]) -> float:
    """
    Calculate the euclidean distance between 2 points
    """
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


# def randomize_drone_pose(id: int, upper: int, lower: int) -> dict[str, list]:
#     """
#     Generate a random drone position within a [lower, upper] range
#     """
#     if upper < lower:
#         raise ValueError
#     x = round(random.uniform(lower, upper), 2)
#     y = round(random.uniform(lower, upper), 2)
#     yaw = round(random.uniform(0, 2 * math.pi), 2)

#     drone = {
#         "name": f'"drone{id}"',
#         "xyz": [x, y, 0],
#         "rpy": [0, 0, yaw],
#     }
#     return drone

def generate_drone_row(num_drones: int) -> list[dict[str, list]]:
    """
    Generate a row of drones
    """
    drones = []
    x, y = 0, 0
    yaw = 0.0
    for i in range(num_drones):
        drone = {
            "name": f'"drone{i}"',
            "xyz": [x, y, 0],
            "rpy": [0, 0, yaw],
        }
        drones.append(drone)
        y = y + 2.0
    return drones


def generate_panel_rows(num_rows: int, num_panels: int) -> dict[str, list[float]]:
    """
    Given drone coordinates, generate random panels outside the grid

    drone_coords = (x, y)
    min_distance = minimum distance away from drone
    """

    panels = {}
    x = 20  # Initial x position
    y = 0  # Initial y position
    for i in range(num_rows):
        for j in range(num_panels):
            displacement = 3.5
            panels[f"panel{j+i*num_panels}"] = [x, y +
                                                displacement, 0.45, 0, 0.60, 3.14]
            y = y + displacement
        x = x + 3.5
        y = 0
    return panels


def generate_world(world_name: str, num_panels: int, num_rows: int, num_drones: int) -> None:
    """Generate world"""
    assets_path = Path(__file__).parents[1].joinpath(
        'assets')
    environment = Environment(loader=FileSystemLoader(
        assets_path.joinpath("templates")))

    json_template = environment.get_template("drone.json.jinja")
    sdf_template = environment.get_template("world.sdf.jinja")
    # initial_grid_size = 10

    world_name = f"{world_name}"
    drones = generate_drone_row(num_drones)

    obstacles = generate_panel_rows(num_rows=num_rows,
                                    num_panels=num_panels)

    json_output = json_template.render(
        world_name=world_name, drones=drones)
    sdf_output = sdf_template.render(
        world_name=world_name, models=obstacles)

    # if visualize:
    #     visualize_world(world_name, {'drone': drone_xy},
    #                     obstacles)

    json_path = assets_path.joinpath(f"worlds/{world_name}.json")
    sdf_path = assets_path.joinpath(f"worlds/{world_name}.sdf")

    # Write the JSON string to the file
    with open(json_path, "w", encoding='utf-8') as json_file:
        json_file.write(json_output)

    # Write the XML string to the file
    with open(sdf_path, "w", encoding='utf-8') as sdf_file:
        sdf_file.write(sdf_output)

    print(f"World {world_name} has been saved")


def main():
    """
    entrypoint
    """
    parser = argparse.ArgumentParser(
        description='Generate a randomize world as a json file')
    parser.add_argument('number_of_drones', metavar='drones', type=int,
                        help='number of drones to generate')
    parser.add_argument('number_of_panels', metavar='panels', type=int,
                        help='number of panels to generate')
    parser.add_argument('number_of_rows', metavar='rows', type=int,
                        help='number of rows of panels to generate')
    parser.add_argument('-name', '--world_name', metavar='name', type=str, nargs='?',
                        default='solar_field', help='generic name of generated world')
    args = parser.parse_args()

    num_drones = args.number_of_drones    # Number of Drones
    num_obj = args.number_of_panels    # Number of panels
    num_rows = args.number_of_rows    # Number of rows
    world_name = args.world_name

    print(num_rows)

    generate_world(world_name, num_obj, num_rows, num_drones)


if __name__ == '__main__':
    main()
