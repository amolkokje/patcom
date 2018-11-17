import re

class Compress:
    def __init__(self, input_pattern_file, repeat_char='IDXI', nop_char='NOP'):
        self.input_pattern_file = input_pattern_file
        self.repeat_char = repeat_char
        self.nop_char = nop_char
        
        
    def _get_pattern(self):
        iplines = []
        with open(self.input_pattern_file, 'r') as fh:
            for line in fh.readlines():
                # remove all spaces, and new lines
                line = line.replace(' ','').replace('\r','').replace('\n','')
                # if line is not a comment
                if not re.match(r'^#', line):
                    iplines.append(line)
        return iplines
        
   
    def _convert_to_repeat_vector(self, ipvector, count):
        # replace 'NOP' with 'REPEAT <Count>'
        return ipvector.replace(self.nop_char, '{} {}'.format(self.repeat_char, count))
        
        
    def _compress_repeats(self, iplines):
        oplines = []
        n = len(iplines)
        i = 0
        
        while i < n:
            if i+1 < n and iplines[i+1] == iplines[i]:
                j = i+2
                c = 2
                while j < n:
                    if iplines[j] == iplines[i]:
                        c += 1 
                        j += 1
                    else:
                        break
                
                oplines.append(self._convert_to_repeat_vector(iplines[i], c))                
                i += c
                        
            else:
                oplines.append(iplines[i])
                i += 1
        return oplines        
            
    def compress(self):
        return self._compress_repeats(self._get_pattern())        
      
        
        