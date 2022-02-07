lst = [None, 3, "str", []]

lst2 = []

for i in lst:
    if i != None:
        lst.extend(str(i))
print(lst2)