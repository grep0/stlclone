# stlclone
Simple command line tool to make an STL file containing multiple copies of a given file.
Useful if you want to print multiple copies of some part.

### Install prerequisites:
 * numpy
 * numpy-stl: ```pip3 install numpy-stl```
 
### Example:
```
$ ./stlclone.py -i Bunny.stl -o Bunny_2x3.stl -nx 2 -ny 3 -gap 15
```
Input: [Bunny.stl](Bunny.stl)
Output: [Bunny_2x3.stl](Bunny_2x3.stl)


```
usage: stlclone.py [-h] [-nx NX] [-ny NY] [-dx DX] [-dy DY] [-gap GAP] [-o O]
                   -i I [-ascii]

Tool for cloning objects in STL

optional arguments:
  -h, --help  show this help message and exit
  -nx NX      Number of clones in X direction
  -ny NY      Number of clones in Y direction
  -dx DX      Delta in X direction
  -dy DY      Delta in Y direction
  -gap GAP    Gap between bounding boxes for auto placement (set this or -dx
              and -dy)
  -o O        Output file
  -i I        Input file
  -ascii      Ascii output
```
