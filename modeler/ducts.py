#!/usr/bin/python

import sys
from model import DuctModel
import numpy as np

from application import Application

if __name__ == '__main__':
    l = 300
    len_ratio = 0.7937
    alpha = np.pi / 3
    beta = np.pi / 6
    n_levels = 5
    radius = 50
    radius_ratio = 0.858374
    stem_inclination = np.pi / 2
    stem_rotation = 0
    tree_rotation = 0
    app = Application(sys.argv, 1100, 800)

    model = DuctModel(alpha, beta, l, len_ratio, radius, radius_ratio,
                      n_levels, stem_inclination, stem_rotation,
                      tree_rotation)
    app.set_model(model)

    app.exec_()
