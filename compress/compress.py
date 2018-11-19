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

        
    def _contains_repeats(self, vector):
        return True if self.repeat_char in vector else False
        
        
    def _convert_to_loop_vector(self, base, count):
        converted = []
        self.label_count += 1
        label = self.label_char + str(self.label_count)
        
        contains_repeats_first = self._contains_repeats(base[0])
        contains_repeats_last = self._contains_repeats(base[1])
        
        # if there is a repeat_char, then replace it with NOP
        vector_nop_first = re.sub( '{} \d'.format(self.repeat_char), self.nop_char, base[0] )
        vector_nop_last  = re.sub( '{} \d'.format(self.repeat_char), self.nop_char, base[1] )
        
        # first vector - always same
        # replace NOP or Repeat by STI
        loop_instr = '{} {}'.format(self.loop_start_char, count-1)
        if self.nop_char in base[0]:
            converted.append( re.sub(self.nop_char, loop_instr, vector_nop_first) )
        elif self.repeat_char in base[0]:    
            converted.append( re.sub('({}\d*)'.format(self.repeat_char), loop_instr, vector_nop_first) )
        
        # label
        converted.append( label )  
        
        # first vector - if it contains repeats, add with RC-1
        if self._contains_repeats(base[0]):
            # replace the RC by (RC-1), as one iteration is already covered
            # RC=1 is same as NOP
            repeat_count = int(re.match(r'IDXI(.+){V', base[0]).group(1).strip())
            if repeat_count == 2:
                converted.append( vector_nop_first )
            else:
                # replace RC by (RC-1)
                converted.append( re.sub( str(repeat_count), str(repeat_count-1), base[0] ) )
         
        # last vector - always same 
        converted.append( base[1] )
         
        ## - clipped off part/last iteration 
        
        # first vector - always same    
        # replace NOP or Repeat by JNI Label
        loop_stop_instr = '{} {}'.format(self.loop_stop_char, label)
        if self.nop_char in base[1]:
            converted.append( re.sub(self.nop_char, loop_stop_instr, vector_nop_last) )
        elif self.repeat_char in base[1]:    
            converted.append( re.sub('({}\d*)'.format(self.repeat_char), loop_stop_instr, vector_nop_last) )
         
        # first vector - if contains repeats
        if self._contains_repeats(base[0]):
            repeat_count = int(re.match(r'IDXI(.+){V', base[0]).group(1).strip())
            if repeat_count == 2:
                converted.append( vector_nop_first )
            else:
                # replace RC by (RC-1)
                converted.append( re.sub( str(repeat_count), str(repeat_count-1), base[0] ) )
                
        # last vector - always same 
        converted.append( base[1] )        
         
        return converted 
        ######
        
        # break first, add start char
        # FIX - add consideration for loop 
        if self.repeat_char in base[0]:
            raw_input('base[0]={} has repeat char'.format(base[0]))            
            vector_nop_first = re.sub('IDXI \d', self.nop_char, base[0])
            print 'vector_nop_first={}'.format(vector_nop_first)
            repeat_count = int(re.match(r'IDXI(.+){V', base[0]).group(1).strip())
            print 'repeat_count={}'.format(repeat_count)
            for _ in range(repeat_count-1):
                converted.append(vector_nop_first)
            converted.append( re.sub('NOP', '{} {}'.format(self.loop_start_char, count-2), vector_nop_first) )            
        else:
            converted.append( base[0].replace('NOP', '{} {}'.format(self.loop_start_char, count-2) ) )       
            #converted += base[1:]
        raw_input('converted={}'.format(converted))
        
        
        # label
        converted.append(label + ':')        
        #converted.append(vector_nop_last)
        raw_input('converted={}'.format(converted))
        
        # break last, add stop char
        # FIX - add consideration for loop 
        if self.repeat_char in base[1]:
            raw_input('base[1]={} has repeat char'.format(base[1])) 
            vector_nop_last = re.sub('IDXI \d', self.nop_char, base[1])
            print 'vector_nop_last={}'.format(vector_nop_last)
            repeat_count = int(re.match(r'IDXI(.+){V', base[1]).group(1).strip())
            print 'repeat_count={}'.format(repeat_count)
            for _ in range(repeat_count-1):
                converted.append(vector_nop_last)        
            converted.append( re.sub('NOP', '{} {}'.format(self.loop_stop_char, label), vector_nop_last) )
        else:   
            #converted += base[:-1]
            converted.append(base[-1].replace('NOP','{} {}'.format(self.loop_stop_char, label)))
        raw_input('converted={}'.format(converted))
        
        
        return converted
        

    def _compress_loops(self, iplines):
        """
        input - lines to compress, processed by _get_pattern()
        output - compressed lines
        """
        oplines = []
        n = len(iplines)
        i = 0
        
        depth = 2  # no of vectors to compare, default
        
        
        while i+1 < n:
            base = iplines[i:i+depth]
            ##print 'base={}'.format(base)
            c = 1
            if i+depth < n:
                for j in range(i+depth, n, depth):
                    if iplines[j:j+depth] == base:                        
                        c += 1
                        ##print 'found match: c={}'.format(c)
                    else:
                        break                
            
            if c > 2:
                ##print 'c>2, compress loop'
                oplines += self._convert_to_loop_vector(base, c)
                i += depth*c
            else:
                oplines.append(base[0])
                i += 1
        
            ##print 'i={}, oplines={}'.format(i, oplines)
        
        # add the last line
        oplines.append(iplines[i])
        return oplines
        
            
    def compress(self):
        lines = self._compress_repeats(self._get_pattern())  
        #print 'REPEAT COMPRESSED:'
        #for line in lines:
        #    print '{}'.format(line)
        
        lines = self._compress_loops(lines)
        print 'LOOP COMPRESSED:'
        for line in lines:
            print '{}'.format(line)
            
      
        
        