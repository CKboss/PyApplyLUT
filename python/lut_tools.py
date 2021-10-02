# lut 的numpy格式到.cube格式转换工具

import numpy as np

def load_lut_file_to_input_cube(cube_path,dim=None):
    with open(cube_path,'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].strip()
            if dim is None:
                if 'LUT_3D_SIZE' in lines[i]:
                    dim = int(lines[i].split(' ')[-1])
    lines = lines[-dim*dim*dim:]
    cube = np.zeros((3,dim,dim,dim),dtype=np.float32)
    for i in range(0,dim):
        for j in range(0,dim):
            for k in range(0,dim):
                n = i * dim*dim + j * dim + k
                line = lines[n].split(' ')
                x = line
                try:
                    cube[0,i,j,k] = float(x[0])
                    cube[1,i,j,k] = float(x[1])
                    cube[2,i,j,k] = float(x[2])
                except Exception:
                    print(lines[n])
    cube = np.array(cube,dtype=np.float32)
    return cube

def npy_to_cube(cube, cube_file, cube_name=None):
    D = cube.shape[1]
    lines = list()
    if cube_name is not None:
        lines.append(f"# Preset: {cube_name}")
    lines.append(f"LUT_3D_SIZE {D}")
    lines.append("DOMAIN_MIN 0.0 0.0 0.0")
    lines.append("DOMAIN_MAX 1.0 1.0 1.0")
    for i in range(D):
        for j in range(D):
            for k in range(D):
                r,g,b = cube[:,i,j,k]
                lines.append(f"{r:.8f} {g:.8f} {b:.8f}")
    with open(cube_file,'w') as f:
        for l in lines[:-1]:
            l = l+'\n'
            f.write(l)
        f.write(lines[-1])

def cube3d_to_vec2d(cube):
    D = cube.shape[1]
    vec = list()
    for i in range(D):
        for j in range(D):
            for k in range(D):
                r,g,b = cube[:,i,j,k]
                vec.append([r,g,b])
    vec = np.array(vec)
    return vec

def cube_to_npy(cube_file):
    return load_lut_file_to_input_cube(cube_file)