import numpy as np 

def chirp_mass(r):
    return (r.mass1 * r.mass2)**(3./5) / (r.mass1 + r.mass2)**(1./5)

def spin_tilt1(r):
    a1 = spin_mag1(r)
    return np.arccos(r.spin1z / a1)

def spin_tilt2(r):
    a2 = spin_mag2(r)
    return np.arccos(r.spin2z / a2)

def spin_mag1(r):
    return np.sqrt(r.spin1x**2+r.spin1y**2+r.spin1z**2)

def spin_mag2(r):
    return np.sqrt(r.spin2x**2+r.spin2y**2+r.spin2z**2)

# FIXME: The *injected* range for mc in 2 -- 7 ish.
# The posteriors go way beyond this -- this leads to everything concentrated in
# a bin
RANGES = {
    #"mc": (0.87, 27), # 1+1 -> 30+30
    "mc": (1, 10), # 1+1 -> 30+30
    "q": (0, 1),
    "tilt1": (0, np.pi),
    "tilt2": (0, np.pi),
    "a1": (0, 1),
    "a2": (0, 1),
    "theta_jn": (0, np.pi),
    "distance": (1, 1000),
    "ra": (0, 2*np.pi),
    "dec": (-np.pi/2, np.pi/2)
}

GET_PARAM = {
    "mc": lambda r: r.mchirp,
    "q": lambda r: r.mass2 / r.mass1,
    "tilt1": spin_tilt1,
    "tilt2": spin_tilt2,
    "a1": spin_mag1,
    "a2": spin_mag2,
    "theta_jn": lambda r: r.inclination, # FIXME: NOT RIGHT
    "distance": lambda r: r.distance,
    "ra": lambda r: r.longitude,
    "dec": lambda r: r.latitude
}
