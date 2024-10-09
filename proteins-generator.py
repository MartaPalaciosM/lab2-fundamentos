import numpy as np
import random
import string
import sys

letters = np.array(list(chr(ord('A') + i) for i in range(8)))
#print(letters)


f=open('proteins.csv', 'w+')

f.write("structureId,sequence\n")

print(sys.argv[1])

linesno=int(sys.argv[1])
count = 0

for i in range (linesno):
   chars = ''.join([random.choice(letters) for j in range(random.randrange(1, 256, 8))])
#   print(chars)
   f.write(str(i+1))
   f.write(",") 
   if (random.randrange(1, 8, 1) ==   i % 8):
      count =  count +1
      f.write("ABCD")
      if (count % 2 ==   0):
#         print(i, count, "CDEFGH")
         f.write("CDEFGH")
      if (count % 4 ==   0):
#         print(i, count, "ABCD")
         f.write("ABCD")
   f.write(chars)
   f.write("\n")



