from py3dbp import Packer, Bin, Item
import ast

# Initialize the packer
packer = Packer()

# Define the bin
my_bin = Bin('Car', 20, 20, 20, 100000)
packer.add_bin(my_bin)

# Read the file and add items to the packer
file = open('box_dimensions.txt', 'r')
for line in file:
    parts = line.split(' [')
    # print(line)
    # print("parts 0")
    # print(parts[0])
    # print("parts 1")
    # print(parts[1])
    algo =  ast.literal_eval('['+parts[1])
    print(algo)


    dimensions =  ast.literal_eval('['+parts[1])
    packer.add_item(Item(parts[0], dimensions[0], dimensions[1], dimensions[2], 0))

# Pack the items
packer.pack()

# Print the results
for b in packer.bins:
    print(":::::::::::", b.string())

    print("FITTED ITEMS:")
    for item in b.items:
        print("====> ", item.string())

    print("UNFITTED ITEMS:")
    for item in b.unfitted_items:
        print("====> ", item.string())

    print("***************************************************")
    print("***************************************************")

# necesario para julia
# import requests

# URL_BASE = "http://localhost:8000"
# r = requests.post(URL_BASE+ "/simulations", allow_redirects=False)
# datos = r.json()

# print(datos)
