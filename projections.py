import numpy as np


def rotation_matrix_from_vectors(vec1, vec2):
    """Find the rotation matrix that aligns vec1 to vec2."""
    a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (vec2 / np.linalg.norm(vec2)).reshape(3)
    v = np.cross(a, b)
    c = np.dot(a, b)
    s = np.linalg.norm(v)
    if s < 1e-10:  # vectors are parallel
        return np.eye(3) if c > 0 else -np.eye(3)
    mat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    rotation_matrix = np.eye(3) + mat + mat.dot(mat) * ((1 - c) / (s ** 2 + 1e-10))
    return rotation_matrix


def project(position, radius, camera):
    """Project the 3D sphere with position and radius onto 2D the camara plane given by position and direction by
    using the given focal length."""
    # rotation_matrix = rotation_matrix_from_vectors(np.array([0, 0, 1]), camera.z)
    rotation_matrix = camera.get_rotation_matrix()

    # Project center
    rotated_position = rotation_matrix.dot(position - camera.position)
    z = rotated_position[2]

    # If the ball is entirely behind the plane, return None
    if z < -radius:
        return None

    if z < radius:  # FIXME If the alga is partially behind the plane, it is not calculated correctly
        return None

    # Compute the intersection point (or the center of the ball if it does not intersect the plane)
    if z >= radius:
        # If the ball is in front of the plane
        intersection_point = rotated_position
        r = radius
    else:
        # If the ball intersects the plane
        d = z
        intersection_point = rotated_position + d * camera.direction
        r = np.sqrt(radius ** 2 - d ** 2)

    # Find the x and y coordinates on the camera plane
    x = intersection_point[0] / intersection_point[2] * camera.focal_length
    y = intersection_point[1] / intersection_point[2] * camera.focal_length

    # Calculate the projected width and height
    width = 2 * ((r * camera.focal_length) / np.sqrt(intersection_point[2] ** 2 + (r) ** 2))
    height = 2 * ((r * camera.focal_length) / np.sqrt(intersection_point[2] ** 2 + (r) ** 2))

    # Translate x and y to screen coordinates
    xp = int(x) + camera.width // 2  # FIXME: ValueError: cannot convert float NaN to integer
    yp = int(y) + camera.height // 2

    return xp, yp, width, height
