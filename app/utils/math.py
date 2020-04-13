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


def check_intersection(segment_1, segment_2):
    x1, y1 = segment_1[0].x, segment_1[0].y
    x2, y2 = segment_1[1].x, segment_1[1].y

    x3, y3 = segment_2[0].x, segment_2[0].y
    x4, y4 = segment_2[1].x, segment_2[1].y

    denominator = np.linalg.det(np.array([
        [x1-x2, x3-x4],
        [y1-y2, y3-y4]
    ]))

    t = np.linalg.det(np.array([
        [x1-x3, x3-x4],
        [y1-y3, y3-y4]
    ])) / denominator

    u = -np.linalg.det(np.array([
        [x1-x2, x1-x3],
        [y1-y2, y1-y3]
    ])) / denominator

    if 0 <= t <= 1 and 0 <= u <= 1:
        return np.array([
            x1 + t * (x2 - x1),
            y1 + t * (y2 - y1)
        ])

    return []
