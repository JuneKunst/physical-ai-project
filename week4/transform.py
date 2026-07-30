import numpy as np


def rotation_matrix_2d(theta_deg):
    theta = np.deg2rad(theta_deg)
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)

    return np.array(
        [
            [cos_theta, -sin_theta],
            [sin_theta, cos_theta],
        ],
        dtype=float,
    )


def scale_matrix_2d(sx, sy):
    return np.array(
        [
            [sx, 0.0],
            [0.0, sy],
        ],
        dtype=float,
    )


def translate_2d(point, tx, ty):
    point = np.asarray(point, dtype=float)
    return point + np.array([tx, ty], dtype=float)


def pixel_to_world(point, image_size, scale=0.01, angle_deg=0.0):
    width, height = image_size

    centered = translate_2d(point, -width / 2, -height / 2)
    scaled = scale_matrix_2d(scale, scale) @ centered
    return rotation_matrix_2d(angle_deg) @ scaled
