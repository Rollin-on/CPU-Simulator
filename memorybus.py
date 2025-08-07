

class memory_bus:
    #What will the memory buses job be here?
        #To communicate between the CPU and RAM
    #How will it look? Will the memory bus facilitate the main functions for the RAM? or will it include a function call to the RAM?
    def __init__(self, ram):
        self.ram = ram 
    
    def read(self, address):
        return self.ram.retrieve(address)
    
    def save_to_ram(self, key, value):
        self.ram.update(key, value)