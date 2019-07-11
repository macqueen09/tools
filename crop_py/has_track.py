# -*- coding: utf-8 -*-

import cv2
import numpy as np
import sys
import time
import random

from croplib import *
sys.path.append('/home/makaili/openposeori/build/python/openpose')
import pyopenpose as op

class item():
    def _init_(self):
        self.data = np.array([])
        self.num_fream = 0


def f2p_list(afream,datum):
    datum.cvInputData = afream
    opWrapper.emplaceAndPop([datum])
    person_list = datum.poseKeypoints
    return person_list

