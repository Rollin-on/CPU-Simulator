from cpu import CPU
from memorybus import memory_bus
from ram import RAM
from isa import ISA



def main():

    ram = RAM()
    memorybus = memory_bus(ram)
    isa = ISA()
    cpu = CPU(memorybus, isa)
    while True: 
        instruction = cpu.fetch()
        if not instruction: 
            print("End of Instructions")
            break
        decoded = cpu.decoder(instruction)
        formatted = cpu.format(decoded)
        answer = cpu.execute(formatted)


if __name__ == "__main__":
    main()