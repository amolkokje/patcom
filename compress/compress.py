import re, string

# TODO:
# - sub-class: abstract base for compressor, inherited repeat, loop
#       - input: lines, output: compressed lines
# - proper space for instructions
# - pip install -- add dependent modules or patcom!
# - add function doc
# - clean up code
# - add proper exceptions 
# 

class Compress:
    def __init__(self, iplines, repeat_char='IDXI', nop_char='NOP', loop_start_char='STI', loop_stop_char='JNI'):
        self.iplines = iplines
        self.repeat_char = repeat_char
        self.nop_char = nop_char
        self.loop_start_char = loop_start_char
        self.loop_stop_char = loop_stop_char
        
        self.label_char = 'L'
        self.label_count = 0
        
    def _get_vectors(self):
        """
        removes all the comments, and unwanted spaces from the input lines
        """
                    
        vectors = []        
        for line in self.iplines:
            # remove all spaces, and new lines
            line = line.replace(' ','').replace('\r','').replace('\n','')
            # if line is not a comment
            if not re.match(r'^#', line):
                vectors.append(line)
        return vectors
        
   
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
        # currently only works for the depth of 2
        
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
        converted.append( label + ':' )  
        
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
        
            
    def compress(self, algo='all'):
        #print 'algo={}'.format(algo)
        if algo == 'all' or algo == 'repeats' or algo == 'loops':
            vectors = self._get_vectors()
            #print vectors
            if algo == 'all':
                return self._compress_loops( self._compress_repeats(vectors) )
            elif algo == 'repeats':
                return self._compress_repeats(vectors)
            elif algo == 'loops':
                return self._compress_loops(vectors)
        else:
            # TODO - Create InputErrorException
            raise RunTimeError('Invalid algo selection!')
      
        
        