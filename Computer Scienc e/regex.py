import re
pattern = re.compile('^[A-Za-z\s]*?[A-Za-z]{2}[0-9]\s?[0-9][a-zA-Z]{2}+$')
print(pattern.search('CT45PY'))
print(pattern.search('CT4 5PY'))

print(pattern.search('Crossacres CT4 5PY'))
print(pattern.search('Crossacres House CT4 5PY'))
print(pattern.search('Crossacres House Waltham CT4 5PY'))

