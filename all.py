import os
import math

generateLABS = True
generateIRR = False

if generateLABS:
  LABS_DIR='labs'
  if not os.path.exists(LABS_DIR):
    os.mkdir(LABS_DIR)
  for N in range(15,61,5):
    for factor in [8/8, 7/8, 6/8, 5/8, 4/8, 3/8, 2/8, 1/8]:
      R = math.ceil(factor * N)
      os.system(f'python low-auto-correlation-binary.py {N} {R} {LABS_DIR}/low-auto-correlation-binary-sequences-{N:02}-{R:02}')

if generateIRR:
  IRR_DIR='irr'
  if not os.path.exists(IRR_DIR):
    os.mkdir(IRR_DIR)
  for size in [ (10,10), (10,15), (15,15), (15,20), (20,20), (20,25), (25,25) ]:
    for base in ['topleft', 'center', 'cross']: #, 'diamond', 'ball', 'pacman']:
      for pert in [None, ('all', 0.05), ('zeros', 0.50)]:
        if pert is None:
          repetitions = [1]
          pert = ('all', 0.0)
          pertDesc = 'none'
        else:
          repetitions = [1, 2]
          pertDesc = f'{pert[0]}{pert[1]}'
        for rep in repetitions:
          os.system(f'python random-image-restoration.py {size[0]} {size[1]} {base} {pert[0]} {pert[1]} {IRR_DIR}/image-restoration-random-{base}-{pertDesc}-{size[0]}x{size[1]}-#{rep}')
 
