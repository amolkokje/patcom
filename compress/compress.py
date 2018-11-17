import re, string

class Compress:
    def __init__(self, input_pattern_file, repeat_char='IDXI', nop_char='NOP', loop_start_char='STI', loop_stop_char='JNI'):
        self.input_pattern_file = input_pattern_file
        self.repeat_char = repeat_char
        self.nop_char = nop_char
        self.loop_start_char = loop_start_char
        self.loop_stop_char = loop_stop_char
        
        self.label_char = 'L'
        self.label_count = 0
        
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
        """
        input - lines to compress, processed by _get_pattern()
        output - compressed lines
        """
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

        
    def _convert_to_loop_vector(self, base, count):
        converted = []
        self.label_count += 1
        label = self.label_char + str(self.label_count) + ':'
        
        # break first, add start char
        # FIX - add consideration for loop 
        if self.repeat_char in base[0]:
            vector_nop = re.sub( self.repeat_char, self.nop_char, re.sub('\d','',base[0]) )
            converted.append( re.sub('NOP', '{} {}'.format(self.loop_start_char, count), vector_nop) )
            for _ in range(count-1):
                converted.append(vector_nop)
        else:
            converted.append(base[0].replace('NOP','{} {}'.format(self.loop_start_char, count)))        
            #converted += base[1:]
        
        # label
        converted.append(label)
        converted += base[1:]
        
        # break last, add stop char
        # FIX - add consideration for loop 
        if self.repeat_char in base[-1]:
            vector_nop = re.sub( self.repeat_char, self.nop_char, re.sub('\d','',base[-1]) )
            for _ in range(count-1):
                converted.append(vector_nop)        
            converted.append( re.sub('NOP', '{} {}'.format(self.loop_stop_char, count), vector_nop) )
        else:   
            #converted += base[:-1]
            converted.append(base[-1].replace('NOP','{} {}'.format(self.loop_stop_char, label)))
        
        return converted
        

    def _compress_loops(self, iplines):
        """
        input - lines to compress, processed by _get_pattern()
        output - compressed lines
        """
        oplines = []
        n = len(iplines)
        i = 0
        
        depth = 2  # no of vectors to compare
        
        
        while i+1 < n:
            base = iplines[i:i+depth]
            #print 'base={}'.format(base)
            c = 1
            if i+depth < n:
                for j in range(i+2, n, depth):
                    if iplines[j:j+depth] == base:
                        c += 1
                    else:
                        break
                i += 1        
            
            # FIX - count has to be greater than 2 atleast to see any benefits
            if c > 3:
                oplines += self._convert_to_loop_vector(base, c)
                i += depth*c
            else:
                oplines += base
                i += depth
        
        return oplines
        
            
    def compress(self):
        lines = self._compress_repeats(self._get_pattern())  
        print 'REPEAT COMPRESSED:'
        for line in lines:
            print 'r={}'.format(line)
        
        lines = self._compress_loops(lines)
        print 'LOOP COMPRESSED:'
        for line in lines:
            print 'l={}'.format(line)
            
      
        
        