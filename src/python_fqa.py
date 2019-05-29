from pyquaternion import Quaternion
import numpy as np

my_quat = Quaternion(axis=[1, 0, 0], angle=3.14159)
print(my_quat)
my_quat2 = Quaternion(1, 0, 0, 3.14159)
print(my_quat2)
my_quat3 = Quaternion(scalar=3.14159, vector=(1, 0, 0))
print(my_quat3.normalised)
print()


#Uses the factored quaternion algorithm to estimate the orientation of a mobile body based
#on a gravity and magnetic field measurement.
#accel must be a 3-vector. In the presence of no mag vector only calculate pitch and roll
class Direction:
    def __init__(self, vec):
        #TODO: type checking
        assert(len(vec) == 3, "Direction must be a 3-vector")
        self.kappa, self.lambd = self._normalize(vec)

    def _normalize(self, vec):
        lambd = 0 if abs(vec[2]) < np.finfo(np.float64).eps else vec[2]
        squared_mag = (lambd * lambd) + (vec[0] * vec[0]) + (vec[1] * vec[1])
        scale = 1/np.sqrt(squared_mag)
        lambd = lambd * scale
        kappa = [vec[0]*scale, vec[1]*scale]
        return kappa, lambd

#Calculates sine and cosines of theta/2 given sin_theta, cos_theta
def halfAngles(sin_theta, cos_theta):
    assert sin_theta <= 1, "sin_theta must be below 1!"
    assert sin_theta >= -1, "sin_theta must be above -1!"
    assert cos_theta <= 1, "cos_theta must be below 1!"
    assert cos_theta >= -1, "cos_theta must be above -1!"
    sign = lambda x:(1, -1)[x < 0]
    sin_half_theta = sign(sin_theta) * np.sqrt((1-cos_theta)/2)
    cos_half_theta = np.sqrt((1 + cos_theta) /2)
    return sin_half_theta, cos_half_theta


#Calculates the elevation quaternion given measured directions
def elevation(accel):
    assert(isinstance(accel, Direction))
    sin_theta = accel.kappa[0]
    cos_theta = np.sqrt(1 - sin_theta*sin_theta)
    sin_half, cos_half = halfAngles(sin_theta, cos_theta)
    #now we return the quaternion representing the elevation (to be normalized before applied in a rotation sequence)
    return Quaternion(0, sin_half, 0, cos_half), cos_theta

def roll(g, cos_theta):
    assert(isinstance(g, Direction))
    assert(isinstance(cos_theta, np.float64))
    if cos_theta == 0:
        sin_phi = 0.0
        cos_phi = 1.0
    else:
        sin_phi = -g.kappa[1] / cos_theta
        cos_phi = -g.lambd / cos_theta
    sin_half_phi, cos_half_phi = halfAngles(sin_phi, cos_phi)
    return Quaternion(sin_half_phi, 0, 0, cos_half_phi)

def fqa(accel, mag=None):
    assert(len(accel) == 3)
    if mag is not None and len(mag) != 3:
        raise Exception("Mag must be a 3-vector if supplied")
    #We should now normalize g and M as directions
    g = Direction(accel)
    q_pitch, cos_theta = elevation(g)
    q_roll = roll(g, cos_theta)
    print(q_pitch)
    print(q_roll)

