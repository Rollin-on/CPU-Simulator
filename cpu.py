class CPU:
    def __init__(self, memorybus, isa):
        self.pc = 0 #Program Pointer
        #Instantiate a dictionary of registers (these all are general for simplicity)
        self.registers = {'R0': 0, 'R1': 1, 'R2': 2, 'R3': 0, 'R4': 5, 'R5': 0, 'R6': 0, 'R7': 3, 'R8': 0, 'R9': 15, 'R10': 0, 'R11': 80, 'R12': 100, 'R13': 5, 'R14': 5, 'R15': 5, 'R16': 2, 'R17': 0, 'R18': 18, 'R19': 9, 'R20': 0, 'R21': 0, 'R22': 0, 'R23': 0, 'R24': 0, 'R25': 0, 'R26': 0, 'R27': 0, 'R28': 0, 'R29': 0, 'R30': 0, 'R31': 0}
        self.memorybus = memorybus
        self.isa = isa
        #Function Dispatch Table
        self.operations = {"ADD": self.add, "SUB" : self.sub, "SLT": self.slt, "ADDI": self.addi, "BNE": self.bne, "LW": self.lw, "SW": self.sw, "J": self.j, "JAL": self.jal, "JR": self.jr}



    #Formats register number into R(-) formatt like self.registers
    def number_to_name(self, number):
        return f"R{number}"
    
    def int_to_bin(self, int):
        if int == 0:
           return "0"
        else:
            remainder = int % 2
            return (self.int_to_bin(int // 2) + str(remainder))
        
    #Fetches instruction using memory bus
    def fetch(self):
        instruction = self.memorybus.read(self.pc)
        print(f"this is from the fetch function {instruction}")
        print(f"Here is the current memory address {self.pc}")
        return instruction
        
    
    #Decodes the binary code using the ISA and gives us a dictionary of key value pairs, parts of the instructions are labelled and the number associated is the value
    def decoder(self, instruction):
        return self.isa.decode(instruction)
    
    #Formatted the register numbers from int into strings EX 1 with R"-" to R1 for the rt rs, rd as neccessary 
    def format(self, decoded):
        if decoded['type'] == 'r':
            decoded['rs'] = self.number_to_name(decoded['rs'])
            decoded['rt'] = self.number_to_name(decoded['rt'])
            decoded['rd'] = self.number_to_name(decoded['rd'])
            print(f"R type instruction is formatted! {decoded}")
            return decoded
        elif decoded['type'] == 'i':
            decoded['rt'] = self.number_to_name(decoded['rt'])
            decoded['rs'] = self.number_to_name(decoded['rs'])
            print(f"I type instruction is formatted! {decoded}")
            return decoded
        elif decoded['type'] == 'j':
            print(f"J type formatted! {decoded}")
            return decoded
        else:
            raise Exception("Type Error")

    #Here we extract the opcode or funct dependent of the type of instruction. 
    #Reference the dispatch table above, then call the neccessary function
    def execute(self, formatted):
        operand = formatted.get('opcode') or formatted.get('funct')
        if operand in self.operations:
            self.operations[operand](formatted)
            if operand not in ['J', 'JAL', 'BNE', 'JR']:
                self.pc += 4
                print("Action Completed")
                
                
        else:
            raise Exception(f"Unknown operation {operand}")
                    
    #Completes logic rt + rs = rd. Total is updated to rd's register in self.registers
    def add(self, formatted):
        rt = formatted['rt']
        rs = formatted['rs']
        rd = formatted['rd']
        self.registers[rd] = self.registers[rt] + self.registers[rs]
        print(f"{formatted['rd']} has been updated to {self.registers[rd]}")
        print(self.registers)
        return self.registers[rd]
        
        
        
        
    #Executes the Subtraction. rt is subtracted from rs then rd is updated.
    def sub(self, formatted):
        rt = formatted['rt']
        rs = formatted['rs']
        rd = formatted['rd']
        self.registers[rd] = self.registers[rs] - self.registers[rt]
        
        print(f"{formatted['rd']} has been updated to {self.registers[rd]}")
        print(self.registers)
        return self.registers[rd]
    
    #Preforms mapping to rs rt and rd to give it a variable such as "R0" in order to call upon its value later
    #Preforms the logic of if the value in RS is smaller than the value in RT set RD to 1, if its not set the value of RD to 0. 
    def slt(self, formatted):
        rt = formatted['rt']
        rs = formatted['rs']
        rd = formatted['rd']
        
        if self.registers[rs] < self.registers[rt]:
            self.registers[rd] = 1
            print(f"{formatted['rd']} has been updated to {self.registers[rd]}")
            print(self.registers)
        else:
            self.registers[rd] = 0 
            print(f"{formatted[rd]} has been updated to {self.registers[rd]}")
            print(self.registers)
        
    #I type
    #ADDI logic preforms addition between the immediate value and a registers value then stores the answer in another register. rt = rs + immediate
    def addi(self, formatted):
        rt = formatted['rt']
        rs = formatted['rs']
        imm = formatted['imm']
        self.registers[rt] = self.registers[rs] + imm
        print(self.registers)
    
    #Completes the logic of rs + imm. Then uses that number as an address and retrieves the 'word' or in my case the 32 bit number there then stored it in rt
    def lw (self, formatted):
        rs = formatted['rs']
        rt = formatted['rt']
        imm = formatted['imm']
        new_word = self.memorybus.read(self.registers[rs] + imm)
        self.registers[rt] = int(new_word, 2)
        print(self.registers)

    #SW logic  rs + offset (imm) = ram address, number to save . I need to save the number to lets say register 80
    def sw(self, formatted):
        rs = formatted['rs']
        rt = formatted['rt']
        imm = formatted['imm']
        address = self.registers[rs] + imm
        number = self.int_to_bin(self.registers[rt]).zfill(32)
        self.memorybus.save_to_ram(address, number)
        print(self.registers)

            #BNE LOGIC - if rs and rt are the same 
                            #PC counter goes up by 4 and we move to the next instruction. 
                        #else:
                            #PC counter + 4 + imm
            
    def bne(self, formatted): #Does not move pointer counter by 4
        rs = formatted['rs']
        rt = formatted['rt']
        imm = formatted['imm']
        new_pc = self.pc + 4 + (imm * 4)
        if self.registers[rs] == self.registers[rt]:
            self.pc += 4
            print("Action completed")
        elif 0 <= new_pc:
            self.pc = new_pc
        else:
            raise Exception("Not a valid memory address")
        print(self.registers)
    #J type Simulating adding two 0s then adding the top four of pc.
    def j(self, formatted): 
        self.pc = formatted['tadd'] * 4
        print("Jump activated")
        return self.pc
    #Save currrent PC + 4 into R31 then jump to specific instruction
    def jal(self, formatted): 
        self.registers['R31'] = self.pc + 4
        self.pc = formatted['tadd'] * 4
        return self.pc
    
    def jr(self, formatted):
         self.pc = self.registers['R31']
         return self.pc
