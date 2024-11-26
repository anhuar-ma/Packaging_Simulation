from py3dbp import Packer, Bin, Item, Painter
import time
import ast

import re
from decimal import Decimal

start = time.time()

'''

This example can be used to compare the fix_point function with and without the fix_point function.

'''

# init packing function
packer = Packer()

# Evergreen Real Container (20ft Steel Dry Cargo Container)
# Unit cm/kg
# box = Bin(
#     partno='example0',
#     WHD=(30,10,20),
#     max_weight=28080,
#     corner=0,
#     put_type=1
# )

# packer.addBin(box)

# dyson DC34 (20.5 * 11.5 * 32.2 ,1.33kg)
# 64 pcs per case ,  82 * 46 * 170 (85.12)
# for i in range(5):
#     packer.addItem(Item(
#         partno='Dyson DC34 Animal{}'.format(str(i+1)),
#         name='Dyson',
#         typeof='cube',
#         WHD=(170, 82, 46),
#         weight=85.12,
#         level=1,
#         loadbear=100,
#         updown=True,
#         color='#FF0000')
#     )

# # washing machine (85 * 60 *60 ,10 kG)
# # 1 pcs per case, 85 * 60 *60 (10)
# for i in range(10):
#     packer.addItem(Item(
#         partno='wash{}'.format(str(i+1)),
#         name='wash',
#         typeof='cube',
#         WHD=(85, 60, 60),
#         weight=10,
#         level=1,
#         loadbear=100,
#         updown=True,
#         color='#FFFF37'
#     ))

# # 42U standard cabinet (60 * 80 * 200 , 80 kg)
# # one per box, 60 * 80 * 200 (80)
# for i in range(5):
#     packer.addItem(Item(
#         partno='Cabinet{}'.format(str(i+1)),
#         name='cabint',
#         typeof='cube',
#         WHD=(60, 80, 200),
#         weight=80,
#         level=1,
#         loadbear=100,
#         updown=True,
#         color='#842B00')
#     )

# # Server (70 * 100 * 30 , 20 kg)
# # one per box , 70 * 100 * 30 (20)
# for i in range(10):
#     packer.addItem(Item(
#         partno='Server{}'.format(str(i+1)),
#         name='server',
#         typeof='cube',
#         WHD=(70, 100, 30),
#         weight=20,
#         level=1,
#         loadbear=100,
#         updown=True,
#         color='#0000E3')
#     )

# for i in range(6):
#     packer.addItem(Item(
#         partno='Server{}'.format(str(i+1)),
#         name='server',
#         typeof='cube',
#         WHD=(5, 5, 5),
#         weight=20,
#         level=1,
#         loadbear=100,
#         updown=True,
#         color='#0000E3')
#     )

#Read the file and add ems to the packer
file = open('box_dimensions.txt', 'r')
for line in file:
    parts = line.split(' [')
    print(line)
    print("-------------")
    print("Parts")
    # print(parts)
    print("parts 0")
    print(parts[0])

    parts2 = parts[0].split(' ')

    print(parts2[0])
    # print("parts 1")
    # print(parts[1])


    dimensions =  ast.literal_eval('['+parts[1])

    print("Dimensions")
    print(dimensions)

    print("-------------")

    if(parts2[0] == "Contenedor"):
        print("Algo"*20)
        box = Bin(
            partno='{}'.format(str(parts2[1])),
            WHD=(dimensions[0],dimensions[2],dimensions[1]),
            max_weight=28080,
            corner=0,
            put_type=1
        )
        packer.addBin(box)

    else:
        packer.addItem(Item(
            partno='{}'.format(str(parts[0])),
            name='server',
            typeof='cube',
            WHD=(dimensions[0], dimensions[2], dimensions[1]),
            weight=1,
            level=1,
            loadbear=100,
            updown=True,
            color='#0000E3')
        )





# calculate packing
packer.pack(

    bigger_first=True,
    distribute_items=False,
    fix_point=True, # Try switching fix_point=True/False to compare the results
    check_stable=False,
    support_surface_ratio=0.75,
    number_of_decimals=0
)

# print result
for box in packer.bins:

    volume = box.width * box.height * box.depth
    print(":::::::::::", box.string())

    print("FITTED ITEMS:")
    volume_t = 0
    volume_f = 0
    unfitted_name = ''

    # '''
    for item in box.items:
        print("partno : ",item.partno)
        print("type : ",item.name)
        print("color : ",item.color)
        #position is (x,y,z)
        print("position : ",item.position)
        print("rotation type : ",item.rotation_type)
        print("W*H*D : ",str(item.width) +'*'+ str(item.height) +'*'+ str(item.depth))
        print("volume : ",float(item.width) * float(item.height) * float(item.depth))
        print("weight : ",float(item.weight))
        volume_t += float(item.width) * float(item.height) * float(item.depth)
        print("***************************************************")
    print("***************************************************")
    # '''
    print("UNFITTED ITEMS:")
    for item in box.unfitted_items:
        print("partno : ",item.partno)
        print("type : ",item.name)
        print("color : ",item.color)
        print("W*H*D : ",str(item.width) +'*'+ str(item.height) +'*'+ str(item.depth))
        print("volume : ",float(item.width) * float(item.height) * float(item.depth))
        print("weight : ",float(item.weight))
        volume_f += float(item.width) * float(item.height) * float(item.depth)
        unfitted_name += '{},'.format(item.partno)
        print("***************************************************")
    print("***************************************************")
    print('space utilization : {}%'.format(round(volume_t / float(volume) * 100 ,2)))
    print('residual volumn : ', float(volume) - volume_t )
    print('unpack item : ',unfitted_name)
    print('unpack item volumn : ',volume_f)
    print("gravity distribution : ",box.gravity)
    # '''
    stop = time.time()
    print('used time : ',stop - start)

    # draw results
    painter = Painter(box)
    fig = painter.plotBoxAndItems(
        title=box.partno,
        alpha=0.2,
        write_num=True,
        fontsize=10
    )




fig.show()

#write the ordered positions in the txt
with open('box_positions.txt', 'w') as file:
    for box in packer.bins:
        for item in box.items:
            # Extract just the numbers as floats
            numbers = [int(d) for d in item.position]
            file.write( "{0} [{1}, {2}, {3}] {4}\n".format(item.partno,numbers[0],numbers[1],numbers[2],item.rotation_type) )



