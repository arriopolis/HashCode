from read_input import Instance
import sys

inst = Instance(sys.argv[1])
print("Duration:", inst.D)
print("#Intersections:", inst.I)
print("#Streets:", inst.S)
print("#Cars:", inst.V)
print("Bonus:", inst.F)
