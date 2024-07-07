from numpy.random import geometric
import random
import sys

def generate(n, numMonomials, minDegree, outFilePrefix):
  coefficients = {}
  while len(coefficients) < numMonomials:
    d = n + 1
    while d > n:
      d = geometric(0.5) - 1 + minDegree
    monomial = frozenset(random.sample(range(1, n+1), d))
    coefficients[monomial] = random.randrange(-10, 10+1)

  outFile = open(f'{outFilePrefix}.pip', 'w')
  outFile.write(f'\\ Random high-degree instance\n')
  outFile.write(f'\\ Number of variables: {n}\n')
  outFile.write(f'\\ Number of coefficients: {numMonomials}\n')
  outFile.write('\\\n')
  outFile.write('minimize\n')
  outFile.write('  obj: objvar\n')
  outFile.write('subject to\n')
  outFile.write('  objcons: ')
  count = 0
  for product,coef in coefficients.items():
    if len(product) <= 0 or coef == 0:
      continue
    if coef > 0.0:
      outFile.write(f' +{coef}')
    else:
      outFile.write(f' {coef}')
    for term in product:
      outFile.write(f' x_{term}')
    count = (count + 1) % 10
    if count == 0:
      outFile.write('\n    ')
  outFile.write(f' - objvar <= 0\n')
  outFile.write('bounds\n')
  for i in range(1, n+1):
    outFile.write(f'  0 <= x_{i}\n')
  outFile.write('  -inf <= objvar <= inf\n')
  outFile.write('binary\n')
  count = 0
  for i in range(1, n+1):
    outFile.write(f' x_{i}')
    count = (count + 1) % 10
    if count == 0:
      outFile.write('\n  ')
  outFile.write('\nend\n')
  outFile.close()

if __name__ == '__main__':
  try:
    numVariables = int(sys.argv[1])
    numMonomials = int(sys.argv[2])
    minDegree = int(sys.argv[3])
    outFilePrefix = sys.argv[4]
  except:
    print(f'Usage: {sys.argv[0]} #VARS #MONOMIALS MINDEGREE OUTFILEPREFIX')
    print('Creates a random multilinear model in OUTFILEPREFIX.pip with #VARS variables')
    print('and #MONOMIALS monomials. Each monomial has degree d >= MINDEGREE with probability ~2^(MINDEGREE-d-1).')
    sys.exit(1)

  generate(numVariables, numMonomials, minDegree, outFilePrefix)

