import cv2
import numpy as np
from pathlib2 import Path

import sys
#
sys.path.append("Q:/WorkSpace/bfood/lut-master/build/Debug")
from python.PyApplyLUT import PyApplyLUT
from python.lut_tools import cube_to_npy

INPUT_IMG = Path(r".\test\1.jpg")
LUT_FILE = Path(r".\test\1.cube")

img = cv2.imread(INPUT_IMG.as_posix())
img = img / 255

# apply lut 

# method 1 load from .cube file
alut = PyApplyLUT(lut_file=LUT_FILE)
new_img = alut.apply_lut(img)
new_img = new_img * 255
cv2.imwrite("./test/new_img_1.jpg",new_img)

# method 2 load from npy file
cubenpy = cube_to_npy(LUT_FILE)
alut = PyApplyLUT(lut_dim=32, lut_cube=cubenpy)
new_img = alut.apply_lut(img)
new_img = new_img * 255
cv2.imwrite("./test/new_img_2.jpg",new_img)