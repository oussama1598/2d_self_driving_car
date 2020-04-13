import numpy as np


def rotate_vector(vector, angle):
    rotation_matrix = np.array(
        [[np.cos(angle), -np.sin(angle)],
         [np.sin(angle), np.cos(angle)]]
    )

    return vector.dot(rotation_matrix)


def rotate_vector_around_a_point(vector, point, angle):
    vector_copy = rotate_vector(point.copy(), angle)

    return vector_copy + vector


def limit_abs(value, limit):
    return np.sign(value) * min(np.abs(value), limit)


def rotate_90_counter_clock_wise(vector):
    return np.array([
        vector[1],
        vector[0]
    ])


def normalize(vector):
    return vector / np.linalg.norm(vector)
