# 包装
import cv2
from pathlib2 import Path
import numpy as np
from typing import Union

import ApplyLUT

class PyApplyLUT(object):

    def __init__(self,lut_file: Path=None,lut_dim=None, lut_cube: np.ndarray=None) -> None:

        super().__init__()
        if lut_file is not None and lut_dim is None and lut_cube is None:
            self.alut = ApplyLUT.ApplyLUT(lut_file.as_posix())
        elif lut_dim is not None and lut_cube is not None and lut_file is None:
            c,d1,d2, d3 = lut_cube.shape
            assert c==3,'Cube\' channle should equal to 3.'
            assert lut_dim==d1 and lut_dim==d2 and lut_dim==d3,f"Cube dim should euqal to lut_dim: {lut_dim}"
            lut_cube = lut_cube.reshape(3,-1)
            lut_cube = lut_cube.transpose()
            self.alut = ApplyLUT.ApplyLUT(lut_dim,lut_cube)
        else:
            raise NotImplementedError

    def load_imseq_from_file(self, image_path: Path):
        img = cv2.imread(image_path.as_posix())
        return self.load_imgseq_from_npy(img)

    def load_imgseq_from_npy(self, img: np.ndarray):
        H,W,C = img.shape
        imgseq = np.reshape(img,(H*W,C))
        imgseq = imgseq.astype(np.float64)
        if imgseq.max() > 1: imgseq = imgseq/255
        return imgseq,H,W,C

    def apply_lut(self, img: Union[Path,np.ndarray] ):
        '''
        img should be image path or the image in [H,W,3] normal to 0~1
        return the image apply with lut and its value normal to 0~1
        '''
        if isinstance(img,Path):
            imgseq,H,W,C = self.load_imseq_from_file(img)
        elif isinstance(img, np.ndarray):
            imgseq,H,W,C = self.load_imgseq_from_npy(img)
        nimg = self.alut.apply_lut_1d(imgseq)
        nimg = np.reshape(nimg,(H,W,C))
        return nimg

if __name__=='__main__':
    pass