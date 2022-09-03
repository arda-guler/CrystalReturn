import math
import numpy
from pyquaternion import Quaternion

# constants
grav_const = (6.674*(10**-11)) # m^3 kg^-1 s^-2

def sign(x):
    if x >= 0:
        return 1
    else:
        return -1

# takes cartezian coords list
# gives spherical coords list
def cartesian2spherical(cart):
    
    x = cart[0]
    y = cart[1]
    z = cart[2]
    
    rho = (x**2 + y**2 + z**2)**0.5
    try:
        theta = math.degrees(math.atan(((x**2 + y**2)**0.5)/z))
    except ZeroDivisionError:
        theta = 90
    phi = math.degrees(math.atan(y/x))
    
    return [rho, theta, phi]

# takes spherical coords list
# gives cartezian coords list
def spherical2cartesian(sph):

    rho = sph[0]
    theta = math.radians(sph[1])
    phi = math.radians(sph[2])
    
    x = math.cos(theta) * math.sin(phi) * rho
    y = math.sin(theta) * math.sin(phi) * rho
    z = math.cos(phi) * rho
    
    return [x, y, z]

# cross product
def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0]]

# dot product
def dot(a, b):
    result = 0
    for a,b in zip(a,b):
        result += a*b

    return result

# get vector magnitude
def mag(vect):
    square_sum = 0
    for element in vect:
        square_sum += element**2

    return square_sum**0.5

# multiply vector with scalar
def vector_scale(vect, sca):
    result_vec = []
    for element in vect:
        result_vec.append(element * sca)
        
    return result_vec

# add vectors
def vector_add(vect1, vect2):
    for i in range(len(vect1)):
        vect1[i] = vect1[i] + vect2[i]

    return vect1

def vector_add_safe(vect1, vect2):
    result_vect = []

    if len(vect1) == len(vect2):
        for i in range(len(vect1)):
            result_vect.append(vect1[i] + vect2[i])

    else:
        return -1

    return result_vect

# rotate an orientation matrix
def rotate_matrix(orientation_matrix, rotation):
    # orientation matrix is a 3x3 matrix, rotation is a list of three angles in degrees
    orientation_matrix = numpy.array(orientation_matrix)
        
    if rotation.x:
        rotator = Quaternion(axis=orientation_matrix[0], angle=math.radians(rotation.x))
        orientation_matrix = (numpy.array([rotator.rotate(orientation_matrix[0]), rotator.rotate(orientation_matrix[1]), rotator.rotate(orientation_matrix[2])]))

    if rotation.y:
        rotator = Quaternion(axis=orientation_matrix[1], angle=math.radians(rotation.y))
        orientation_matrix = (numpy.array([rotator.rotate(orientation_matrix[0]), rotator.rotate(orientation_matrix[1]), rotator.rotate(orientation_matrix[2])]))

    if rotation.z:
        rotator = Quaternion(axis=orientation_matrix[2], angle=math.radians(rotation.z))
        orientation_matrix = (numpy.array([rotator.rotate(orientation_matrix[0]), rotator.rotate(orientation_matrix[1]), rotator.rotate(orientation_matrix[2])]))

    return orientation_matrix.tolist()

def world2cam(w_coords, cam, factor=10):
    w_coords = vector_scale(w_coords, -visual_scaling_factor)
    cam_orient = cam.get_orient()
    rel_pos = vector_add_safe(w_coords, vector_scale(cam.get_pos(), -1))
    cam_x = cam_orient[0]
    cam_y = cam_orient[1]
    cam_z = cam_orient[2]

    z_dist = dot(rel_pos, cam_z)

    # object is behind camera, assign no position
    if z_dist < 0:
        return None
    
    x_dist = dot(rel_pos, cam_x)
    y_dist = dot(rel_pos, cam_y)

    x_skew = -(x_dist/z_dist) * factor
    y_skew = -(y_dist/z_dist) * factor

    return [x_skew, y_skew]
    
