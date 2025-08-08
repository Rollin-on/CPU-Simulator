CPU Simulator 
-------------
The purpose of this program is to showcase the complex communications within the CPU itself. As well as to give an example of the different portions within the CPU that allow for the complex compuations we ask of our systems on a daily basis. 

------------- 
isa.py

isa.py's purpose is two fold. First it is designed to list and specify the operations that will be available to the CPU to execute. Additionally, this file works as a decoder for the CPU. Having two functions the ISA file is capable of decoding three kinds of 32 bit instructions r, i, and j. Using binary manipulation and spicing each portion of the binary instruction is sectioned out and placed into a dictionary in order of its corresponding instruction format. One of the functions is for 'r' type the other handles 'i' and 'j' type instructions. Finally the decoded instruction is sent back to CPU

-------------
ram.py

Holds memory addresses and instructions within a dictionary. Using key value pairs to simulate the memory addressing done on a real CPU. Two functions are also held here. One function is a searching function, holding a memory address which is then used in dictionary indexing to receive its corresponding set of instructions. These instructions are returned to the memory bus to furthur communicate. The second function is designed to update data, or an instruction at a specified memory address. 

-------------
memorybus.py

The function of this file is to operate as a messenger between the cpu file and the ram. Two functions exist here. The first receives data from the ram memory at the address specified by the CPU's program counter then sends it back to the cpu.py The second file held within this portion of the program works to send data from the cpu.py to the ram in order to update memory in ram. 

------------- 
cpu.py

This file is the backbone that ties the rest of the files together. Over all the responsibility of the CPU is to Fetch, Decode, and Execute the instructions it receives. In order to do so the CPU is initiated with a series of 31 registers, whos values are held and maintained via a dictionary within the dunder method. Also held in this dunder method is a function dispatch table, as well as a pointer counter (PC), of which is designed to call the appropriate operand function to compute the instructions. The file begins with the fetch function, requesting data from the memory bus, of which in turn requests instructions stored within ram. After the binary string of instructions have been received by the fetch function they are then ran through a decoder function which utilizes the ISA's specialty of decoding to receive a dictionary of values corresponding to the instruction format required of the instruction type i.e ('r', 'i', 'j'). From there the instructions are formatted with two helper functions to simplify the process of calling and updating registers during execution. One last helper function is available and used to translate a integer into its binary string representation. Finally the execute function is called using the formatted instructions received from the helper functions. The operation being held in the instruction is tested in an if statement against our function dispatch table. If there is a match, the corresponding function appropriate to the operand given is ran along with the rest of the values held by the dictionary holding the instructions. After the completion of the operand function the execute function ticks the PC by 4 completing the first instruction and cuing the fetch function to continue onto the next memory address. The PC is simulated ticking forward in 4s as in mips 32 bit architecture instructions are beld every 32 btis. That being said there are 8 bits in a byte, and each instruction is 4 bytes long. So incrementing in ram was done this way as well to simulate memory addressing in 32 bit mips architecture. PC is not incremented by 4 only in the following cases; 'J', 'JAL', 'BNE', 'JR'. The program continues as long as there are instructions written into ram prior to the program running. 


-------------
main.py

Handles the initialization of the fetch() function and creates a domino affect to allow the rest of the program to continue as long as the instructions received from RAM are not '' an empty string.
