from numpy import linspace
from random import randint
import sys

l1 = [
    "X_coordinates_left_wheel_left = ",
    "Y_coordinates_left_wheel_left = ",
    "X_coordinates_right_wheel_left = ",
    "Y_coordinates_right_wheel_left = ",
]

l2 = [
    "X_coordinates_left_wheel_right = ",
    "Y_coordinates_left_wheel_right = ",
    "X_coordinates_right_wheel_right = ",
    "Y_coordinates_right_wheel_right = ",
]

l3 = [
    "X_coordinates_left_wheel_straight = ",
    "Y_coordinates_left_wheel_straight = ",
    "X_coordinates_right_wheel_straight = ",
    "y_coordinates_right_wheel_straight = ",
]

names = {
    "leftWheelPositions.csv": l1,
    "rightWheelPositions.csv": l2,
    "straightWheelPositions.csv": l3,
}


def MovGen(n=100):
    for it in names:
        with open("./" + it, "w") as file:
            for t in names[it]:
                n1, n2 = randint(1, n//2), randint(n//2, n)
                movs = str(list(linspace(n1, n2, n).round(1)))[1:-2]
                text = t + movs
                file.write(text + "\n")


if __name__ == "__main__":
    n = int(sys.argv[1])
    MovGen(n)
