class ISA:
    #Will handle the decoding, then send the info to the CPU
    #This decodes and is COMPLETE 
    
    def decode(self, instruction):
        
        if instruction[:6] == '000000':
            #checks for R_type instructions, then calls a function to breakdown the rest of the instructions
            return self.r_type_instruction(instruction)
        else:
            
            return self.i_or_j_type_decoder(instruction)
        
    def r_type_instruction(self, instruction):
        decoded = {'type': 'r'}
        functions = {'ADD': '100000', 'SUB': '100010', 'SLT': '101010', 'JR': '001000'}
        name_splice = {'rs': (6, 11), 'rt': (11, 16), 'rd': (16, 21), 'shamt': (21, 26)}
        for name, (start, end) in name_splice.items():
            bits = instruction[start:end]
            decoded[name] = int(bits, 2)
        for operand, bits in functions.items():
            if instruction[26:32] == bits:
             decoded['funct'] = operand
             return decoded
        else:
            raise ValueError(f"{instruction[26:32]} is not a valid funct")
        
    
    def i_or_j_type_decoder(self, instruction):
        decoded = {}
        bits_operand_type = {'001000': ('ADDI', 'i'), '000101': ('BNE', 'i'), '100011': ('LW', 'i'), '101011': ('SW', 'i'), '101111': ('CACHE', 'i'), '000010': ('J', 'j'), '000011': ('JAL', 'j')}
        name_splice = {'rs': (6, 11), 'rt': (11, 16), 'imm': (16, 32), 'tadd': (6, 32)}
        for bits, (operand, type) in bits_operand_type.items():
            if instruction[:6] == bits:
                decoded['type'] = type
                decoded['opcode'] = operand
                break
        else:
            raise ValueError(f"{instruction[:6]} is not a valid operand")
        for name, (start, end) in name_splice.items():
            if decoded['type'] == 'j' and name == 'tadd':
                decoded[name] = int(instruction[start: end], 2)
            elif decoded['type'] == 'i' and name != 'tadd':
                decoded[name] = int(instruction[start: end], 2)
        return decoded
        
        
        
            


        #rs_bits = instruction[6:11] 
        #rt_bits = instruction[11:16]
        #rd_bits = instruction[16:21]
        #shift_bits = instruction[21:26]
        
    # 3 types of instructions: 
        #R-Type 
            #6-bit opcode - is always 000000 to tell its an R-type
            #5-bit RS register
            #5-bit RT register
            #5-bit RD register
            #5-bit shift amount (shamt)
            #6-bit function code(funct)
                #OPCODE - 000000
                #Function codes
                    #ADD - 100000
                    #SUB - 100001
                    #SLT - 100010
        #I-Type
            #6-bit op code
            #6-bit source register (RS)
            #5-bit destination register (RT)
            #16-bit immediate value
            #ADDI -
            #BNE  -
            #LW   -
            #SW   - 
        #J-Type
            #6-bit opcode
            #26-bit address
            #J - 001000
            #JAL - 001001