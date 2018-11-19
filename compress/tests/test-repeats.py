import sys
sys.path.append('..')

from compress import Compress


files = [
    'pat-0.pat', 
    #'pat-1.pat', 
    #'pat-2.pat',
    #'pat-3.pat',
    #'pat-4.pat',
    'pat-5.pat',
    'pat-6.pat',
    'pat-7.pat',
    'pat-8.pat'
]

print files

for file in files:
    print '\n\n----------------' + file + '----------------'
    with open(file, 'r') as fh:        
        comp = Compress(fh.readlines())        
        print 'COMPRESSED:'
        for line in comp.compress():
            print line
       