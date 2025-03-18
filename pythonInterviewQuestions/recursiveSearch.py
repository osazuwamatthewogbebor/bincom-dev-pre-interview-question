def search(lst, target):
    item = str(lst[0])
    if item == str(target):
        print(f"{target} found in list.")
    else:
        if len(lst) > 1:
            lst.pop(0)
            search(lst, target)
        else:
            print(f"{target} not found in list.")


li = [1, 2, 7, 23, 24, 2, 3, 34, 33,]
search(li, 35)
