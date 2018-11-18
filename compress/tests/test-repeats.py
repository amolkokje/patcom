import sys
sys.path.append('..')

from compress import Compress


files = [
    #'pat-0.pat', 
    #'pat-1.pat', 
    #'pat-2.pat',
    'pat-3.pat',
    'pat-4.pat'
]

print files

for file in files:
    print '----------------' + file + '----------------'
    comp = Compress(file)
    comp.compress()
