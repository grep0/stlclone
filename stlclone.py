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
    p.add_argument('-gap', type=float, default=-1, help='Gap between bounding boxes for auto placement (set this or -dx and -dy)')
    p.add_argument('-o', type=str, help='Output file')
    p.add_argument('-i', type=str, required=True, help='Input file')
    p.add_argument('-ascii', action='store_true', help='Ascii output')
    return p

def main(argv):
    args = _argparser().parse_args(argv[1:])
    in_file = args.i
    if args.o:
        out_file = args.o
    else:
        out_file = in_file + '_out.stl'
        print('output is going to', out_file)
    nx,ny,dx,dy = args.nx,args.ny,args.dx,args.dy
    mesh = stl.Mesh.from_file(in_file)
    if args.gap>=0:
        bbox_size = mesh.max_ - mesh.min_
        if dx==0:
            dx = bbox_size[stl.Dimension.X] + args.gap
        if dy==0:
            dy = bbox_size[stl.Dimension.Y] + args.gap
        print('Auto delta:',(dx,dy))
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
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
