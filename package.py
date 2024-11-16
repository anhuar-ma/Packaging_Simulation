from py3dbp import Packer, Bin, Item

packer = Packer()
#widht, height, depth, weight
packer.add_bin(Bin('Car',10,10,20,10))
# packer.add_bin(Bin('Car',))


packer.add_item(Item('Box', 5,5,5, 0))
packer.add_item(Item('Box', 5,5,5, 0))
packer.add_item(Item('Box', 5,5,5, 0))
packer.add_item(Item('Box', 5,5,5, 0))
packer.add_item(Item('Box', 5,5,5, 0))
packer.add_item(Item('Box', 5,5,5, 0))
packer.add_item(Item('Box', 5,5,5, 0))
packer.add_item(Item('Box', 5,5,5, 0))


packer.pack()

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
