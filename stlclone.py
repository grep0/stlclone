#!/usr/bin/python3
import argparse
import sys

import numpy as np
import stl

def _argparser():
    p = argparse.ArgumentParser(description='Tool for cloning objects in STL')
    p.add_argument('-nx', type=int, default=1, help='Number of clones in X direction')
    p.add_argument('-ny', type=int, default=1, help='Number of clones in Y direction')
    p.add_argument('-dx', type=float, default=0, help='Delta in X direction')
    p.add_argument('-dy', type=float, default=0, help='Delta in Y direction')
    p.add_argument('-o', type=str, help='Output file')
    p.add_argument('-i', type=str, help='Input file')
    p.add_argument('-ascii', action='store_true', help='Ascii output')
    return p

def main(argv):
    args = _argparser().parse_args(argv[1:])
    in_file = args.i
    out_file = args.o or in_file + '_out.stl'
    nx,ny,dx,dy = args.nx,args.ny,args.dx,args.dy
    if nx>1 and dx==0:
        print('error: nx>1 and dx=0')
        return 1
    if ny>1 and dy==0:
        print('error: ny>1 and dy=0')
        return 1
    mesh = stl.Mesh.from_file(in_file)
    nt = mesh.data.shape[0]  # number of triangles
    print("Original mesh size:", nt)
    data_repl = np.tile(mesh.data, nx*ny)
    deltas_x = np.tile(np.arange(nx, dtype=np.float32)*dx, ny)
    deltas_x = np.repeat(deltas_x, nt*3).reshape((-1,3))
    deltas_y = np.repeat(np.arange(ny, dtype=np.float32)*dy, nx)
    deltas_y = np.repeat(deltas_y, nt*3).reshape((-1,3))
    data_repl['vectors'][:, :, stl.Dimension.X] += deltas_x
    data_repl['vectors'][:, :, stl.Dimension.Y] += deltas_y
    mesh_repl = stl.Mesh(data_repl)
    print("Replicated mesh size:", mesh_repl.data.shape[0])
    mesh_repl.save(out_file, mode=stl.Mode.ASCII if args.ascii else stl.Mode.BINARY)

if __name__ == "__main__":
    main(sys.argv)
