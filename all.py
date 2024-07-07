import os
import math

generateLABS = True
generateIRR = True
generateHDR = True

def syscall(command):
  print(command)
  os.system(command)

if generateLABS:
  LABS_DIR='labs'
  if not os.path.exists(LABS_DIR):
    os.mkdir(LABS_DIR)
  for N in range(10,51,5):
    for factor in [8/8, 7/8, 6/8, 5/8, 4/8, 3/8, 2/8, 1/8]:
      R = math.ceil(factor * N)
      syscall(f'python low-auto-correlation-binary.py {N} {R} {LABS_DIR}/low-auto-correlation-binary-sequences-{N:02}-{R:02}')

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
          syscall(f'python image-restoration-random.py {size[0]} {size[1]} {base} {pert[0]} {pert[1]} {IRR_DIR}/image-restoration-random-{base}-{pertDesc}-{size[0]}x{size[1]}-#{rep}')

if generateHDR:
  HDR_DIR='hdr'
  if not os.path.exists(HDR_DIR):
    os.mkdir(HDR_DIR)
  num_repetitions = 5
  repetitions = list(range(1, num_repetitions+1))
  for n in [50, 100, 200]:
    for m in [5*n, 10*n, 20*n]:
      for d in [2, 3, 4]:
        for r in repetitions:
          syscall(f'python high-degree-random.py {n} {m} {d} {HDR_DIR}/high-degree-random-{n}-{m}-{d}-#{r}')
 
