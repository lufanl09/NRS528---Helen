# 2. Push sys.argv to the limit

import sys

# bat file created separately

# create arguments for bat file
argument1 = sys.argv[1]
argument2 = sys.argv[2]
argument3 = sys.argv[3]

argument_list = [argument1, argument2, argument3]
counter = 1

for i in argument_list:
    print("I have " + str(counter) + " " + str(i))
    counter = counter + 1
