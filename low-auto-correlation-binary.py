import sys
from collections import defaultdict

def generate(N, R, outFilePrefix, factor=1):
  coefficients = defaultdict(lambda: 0)
  for i in range(1, N - R + 2):
    for d in range(1, R):
      inner = defaultdict(lambda: 0)
      for j in range(i, i + R - d):
        inner[(j,j+d)] += 4
        inner[(j,)] += -2
        inner[(j+d,)] += -2
        inner[()] += 1
      squared = defaultdict(lambda: 0)
      for term1,coef1 in inner.items():
        for term2,coef2 in inner.items():
          term = tuple(sorted(set(term1).union(set(term2))))
          coef = coef1 * coef2
          squared[term] += coef
      for term,coef in squared.items():
        if coef != 0:
          coefficients[term] += coef
  coefficients = { key: value for key,value in coefficients.items() if value != 0 }
  sys.stderr.write(f'Polynomial for N = {N} and R = {R} has {len(coefficients)} monomials.\n')
  sys.stderr.flush()

  outFile = open(outFilePrefix + '.pip', 'w')
  outFile.write('\\ Low auto-correlation binary sequence problem\n')
  outFile.write('\\ Determines the ground state for the Bernasconi model.\n')
  outFile.write(f'\\ Parameters: N = {N}, R = {R}\n')
  outFile.write('minimize\n  obj: objvar\nsubject to\n  objcons: ')
  sortedTerms = sorted(coefficients.keys(), key=lambda term: (len(term), term) )
  count = 0
  for term in sortedTerms:
    if term == ():
      continue
    coef = coefficients[term] * factor
    if coef > 0:
      outFile.write(f' + {coef}')
    else:
      outFile.write(f' - {-coef}')
    for i in term:
      outFile.write(f' x#{i}')
    count += 1
    if count % 16 == 0:
      outFile.write('\n')
  outFile.write(f' - objvar <= {-coefficients[()]}\n')
  outFile.write('bounds\n  objvar free\n')
  for i in range(1,N+1):
    outFile.write(f'  x#{i} <= 1\n')
  outFile.write('binary\n')
  outFile.write(' ' + ' '.join(f' x#{i}' for i in range(1,N+1)))
  outFile.write('\nend\n')

if __name__ == '__main__':
  try:
    N = int(sys.argv[1])
    R = int(sys.argv[2])
    outFilePrefix = sys.argv[3]
  except:
    print(f'Usage: {sys.argv[0]} N R OUTFILEPREFIX')
    print('Creates OUTFILEPREFIX.pip')
    sys.exit(1)

  generate(N, R, outFilePrefix)
