import random
import sys

def printImage(image):
  numRows = len(image)
  numColumns = len(image[0])
  for r in range(numRows):
    print(''.join( str(x) for x in image[r]))

def generateTopleft(numRows, numColumns):
  '''
  top-left floor(w/2)-by-floor(h/2) matrix of 1s.
  '''
  image = [ [0] * numColumns for r in range(numRows) ]
  for r in range(numRows // 2):
    for c in range(numColumns // 2):
      image[r][c] = 1
  return image

def generateCenter(numRows, numColumns):
  '''
  border of size floor(w/4) and floor(h/4) around a centered block of 1s.
  '''
  image = [ [0] * numColumns for r in range(numRows) ]
  left = numColumns // 4
  top = numRows // 4
  for r in range(numRows // 4, numRows - numRows // 4):
    for c in range(numColumns // 4, numColumns - numColumns // 4):
      image[r][c] = 1
  return image

def generateCross(numRows, numColumns):
  '''
  centered cross
  '''
  image = [ [0] * numColumns for r in range(numRows) ]
  w = numRows // 5
  h = numColumns // 5
  for r in range(2*w, numRows - 2*w):
    for c in range(h, numColumns - h):
      image[r][c] = 1
  for r in range(w, numRows - w):
    for c in range(2*h, numColumns - 2*h):
      image[r][c] = 1
  return image

def generateDiamond(numRows, numColumns):
  '''
  A centered diamond.
  '''
  image = [ [0] * numColumns for r in range(numRows) ]
  for r in range(numRows):
    for c in range(numColumns):
      dx = abs(r - numRows // 2)
      dy = abs(c - numColumns // 2)
      if dx + numRows/numColumns * dy <= numRows / 2.2:
        image[r][c] = 1
  return image

def generateBall(numRows, numColumns):
  '''
  A ball.
  '''
  image = [ [0] * numColumns for r in range(numRows) ]
  squaredRadius = (min(numRows, numColumns) / 2.2)**2
  for r in range(numRows):
    for c in range(numColumns):
      dx = c - numColumns // 2
      dy = r - numRows // 2
      if dx**2 + dy**2 > squaredRadius:
        continue
      image[r][c] = 1
  return image

def generatePacman(numRows, numColumns):
  '''
  A pacman.
  '''
  image = [ [0] * numColumns for r in range(numRows) ]
  squaredRadius = (min(numRows, numColumns) / 2.2)**2
  for r in range(numRows):
    for c in range(numColumns):
      dx = c - numColumns // 2
      dy = r - numRows // 2
      if dx**2 + dy**2 > squaredRadius:
        continue
      if dx > 0 and abs(dy)/dx < 0.5:
        continue
      image[r][c] = 1
  return image

def blurImage(baseImage, perturbationType, perturbationProbability):
  if perturbationType == 'all':
    probabilities = [perturbationProbability, perturbationProbability]
  elif perturbationType == 'ones':
    probabilities = [0, perturbationProbability]
  elif perturbationType == 'zeros':
    probabilities = [perturbationProbability, 0]
  else:
    probabilities = [0, 0]
  numRows = len(baseImage)
  numColumns = len(baseImage[0])
  image = [ baseImage[r][:] for r in range(numRows) ]
  for r in range(numRows):
    for c in range(numColumns):
      if random.random() < probabilities[image[r][c]]:
        image[r][c] = 1 - image[r][c]
  return image

def add(coefficients, factor, product, prefix=[]):
  if product:
    r,c,n = product[0]
    if n == '+':
      add(coefficients, factor, product[1:], prefix + [(r,c)])
    else:
      add(coefficients, factor, product[1:], prefix)
      add(coefficients, -factor, product[1:], prefix + [(r,c)])
  else:
    prefix = tuple(set(prefix))
    coefficients[prefix] = coefficients.get(prefix, 0.0) + factor

def write(baseImage, blurredImage, base, perturbation, outFilePrefix):
  numRows = len(baseImage)
  numColumns = len(baseImage[0])
  rows = list(range(numRows))
  columns = list(range(numColumns))

  coefficients = {}
  # Linear penality: 25 * (pixel - x_rc)^2
  for r in rows:
    for c in columns:
      if blurredImage[r][c]:
        add(coefficients, 25, [(r,c,'-'),(r,c,'-')]) # (1-x_rc)(1-x_rc)
      else:
        add(coefficients, 25, [(r,c,'+')]) # x_rc
  # Patch penalty
  for r in range(numRows-1):
    for c in range(numColumns-1):
      add(coefficients, 10, [(r,c,'-'),(r,c+1,'-'),(r+1,c,'-'),(r+1,c+1,'-')]) # 10*(1-x11)*(1-x12)*(1-x21)*(1-x22)
      add(coefficients, 10, [(r,c,'+'),(r,c+1,'+'),(r+1,c,'+'),(r+1,c+1,'+')])
      add(coefficients, 20, [(r,c,'-'),(r,c+1,'-'),(r+1,c,'-'),(r+1,c+1,'+')])
      add(coefficients, 20, [(r,c,'-'),(r,c+1,'-'),(r+1,c,'+'),(r+1,c+1,'-')])
      add(coefficients, 20, [(r,c,'-'),(r,c+1,'+'),(r+1,c,'-'),(r+1,c+1,'-')])
      add(coefficients, 20, [(r,c,'+'),(r,c+1,'-'),(r+1,c,'-'),(r+1,c+1,'-')])
      add(coefficients, 20, [(r,c,'+'),(r,c+1,'+'),(r+1,c,'+'),(r+1,c+1,'-')])
      add(coefficients, 20, [(r,c,'+'),(r,c+1,'+'),(r+1,c,'-'),(r+1,c+1,'+')])
      add(coefficients, 20, [(r,c,'+'),(r,c+1,'-'),(r+1,c,'+'),(r+1,c+1,'+')])
      add(coefficients, 20, [(r,c,'-'),(r,c+1,'+'),(r+1,c,'+'),(r+1,c+1,'+')])
      add(coefficients, 30, [(r,c,'+'),(r,c+1,'+'),(r+1,c,'-'),(r+1,c+1,'-')])
      add(coefficients, 30, [(r,c,'-'),(r,c+1,'-'),(r+1,c,'+'),(r+1,c+1,'+')])
      add(coefficients, 30, [(r,c,'+'),(r,c+1,'-'),(r+1,c,'+'),(r+1,c+1,'-')])
      add(coefficients, 30, [(r,c,'-'),(r,c+1,'+'),(r+1,c,'-'),(r+1,c+1,'+')])
      add(coefficients, 40, [(r,c,'+'),(r,c+1,'-'),(r+1,c,'-'),(r+1,c+1,'+')])
      add(coefficients, 40, [(r,c,'-'),(r,c+1,'+'),(r+1,c,'+'),(r+1,c+1,'-')]) # 40*(1-x11)*x12*x12*(1-x22)

  # Compute objective value of base image.
  baseImageObj = 0.0
  for product,coef in coefficients.items():
    for term in product:
      if not baseImage[term[0]][term[1]]:
        coef = 0.0
        break
    baseImageObj += coef

  pixelToVar = { (r,c):f'x_{r+1:02}_{c+1:02}' for r in range(numRows) for c in range(numColumns) }

  outFile = open(outFilePrefix + '.pip', 'w')
  outFile.write(f'\\ Image restoration problem\n')
  outFile.write(f'\\ Tries to recover a base image (consisting of 0s and 1s) from a randomly perturbed one.\n')
  outFile.write(f'\\ Base: {base}\n')
  outFile.write(f'\\ Perturbation: {perturbation}\n')
  outFile.write('\\\n')
  outFile.write(f'\\ Base image (with objective value {baseImageObj}):\n')
  outFile.write(f'\\ +' + ''.join( '-' for _ in range(numColumns) ) + '+\n'  )
  for r in range(numRows):
    outFile.write(f'\\ |' + ''.join( str(x) for x in baseImage[r] ) + '|\n')
  outFile.write(f'\\ +' + ''.join( '-' for _ in range(numColumns) ) + '+\n'  )
  outFile.write('\\\n')
  outFile.write(f'\\ Blurred image:\n')
  outFile.write(f'\\ +' + ''.join( '-' for _ in range(numColumns) ) + '+\n'  )
  for r in range(numRows):
    outFile.write(f'\\ |' + ''.join( str(x) for x in blurredImage[r] ) + '|\n')
  outFile.write(f'\\ +' + ''.join( '-' for _ in range(numColumns) ) + '+\n'  )
  outFile.write('\\\n')
  outFile.write('minimize\n')
  outFile.write('  obj: penalties\n')
  outFile.write('subject to\n')
  outFile.write('  objcons: ')
  count = 0
  for product,coef in coefficients.items():
    if len(product) == 0 or coef == 0.0:
      continue
    if coef > 0.0:
      outFile.write(f' +{coef}')
    else:
      outFile.write(f' {coef}')
    for term in product:
      outFile.write(' ' + pixelToVar[term])
    count = (count + 1) % 10
    if count == 0:
      outFile.write('\n    ')
  abscoef = coefficients.get((), 0.0)
  outFile.write(f' - penalties <= {-abscoef}\n')
  outFile.write('bounds\n')
  for r in rows:
    for c in columns:
      outFile.write(f'  0 <= {pixelToVar[(r,c)]} <= 1\n')
  outFile.write('  -inf <= penalties <= inf\n')
  outFile.write('binary\n')
  count = 0
  for r in rows:
    for c in columns:
      outFile.write(f' {pixelToVar[(r,c)]}')
      count = (count + 1) % 10
      if count == 0:
        outFile.write('\n  ')
  outFile.write('\nend\n')
  outFile.close()

  outFile = open(outFilePrefix + '.sol', 'w')
  outFile.write(f'objective value: {baseImageObj}\n')
  for r in rows:
    for c in columns:
      if baseImage[r][c]:
        outFile.write(f'{pixelToVar[(r,c)]} 1 (obj: 0)\n')
  outFile.write(f'penalties {baseImageObj} (obj: 1)\n')
  outFile.close()

if __name__ == '__main__':
  try:
    numRows = int(sys.argv[1])
    numColumns = int(sys.argv[2])
    baseType = sys.argv[3]
    perturbationType = sys.argv[4]
    perturbationProbability = float(sys.argv[5])
    outFilePrefix = sys.argv[6]
  except:
    print(f'Usage: {sys.argv[0]} #ROWS #COLUMNS BASE-TYPE PERTURBATION PROBABILITY OUTFILEPREFIX')
    print('BASE-TYPE must be in {"topleft", "center", "cross", "diamond", "ball", "pacman"}')
    print('PERTURBATION must be in {"all", "ones", "zeros"}')
    print('PROBABILITY must be in [0,1]')
    print('Creates the multilinear model in OUTFILEPREFIX.pip')
    print('and a solution that represents the base image in OUTFILEPREFIX.sol')
    sys.exit(1)

  baseImage = None
  if baseType == 'topleft':
    baseImage = generateTopleft(numRows, numColumns)
  elif baseType == 'center':
    baseImage = generateCenter(numRows, numColumns)
  elif baseType == 'cross':
    baseImage = generateCross(numRows, numColumns)
  elif baseType == 'diamond':
    baseImage = generateDiamond(numRows, numColumns)
  elif baseType == 'ball':
    baseImage = generateBall(numRows, numColumns)
  elif baseType == 'pacman':
    baseImage = generatePacman(numRows, numColumns)
  else:
    print(f'Unrecognized BASE-TYPE <{baseType}>.')
    sys.exit(1)

  print('Original image:')
  printImage(baseImage)

  blurredImage = blurImage(baseImage, perturbationType, perturbationProbability)

  print('\nBlurred image:')
  printImage(blurredImage)

  base = baseType
  perturbation = f'{perturbationType} with probability {perturbationProbability}'
  write(baseImage, blurredImage, base, perturbation, outFilePrefix)

