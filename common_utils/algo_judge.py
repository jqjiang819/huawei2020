def elem_cmp(list1:list,list2:list):
    if len(list1) != len(list2):
        return False
    for i,elem in enumerate(list1):
        if elem != list2[i]:
            return False
    return True

def judge1(predicts:list,targets:list):
    if len(predicts) != len(targets):
        print("Length not equal")
        return False

    for i,path in enumerate(predicts):
        if not elem_cmp(path,targets[i]):
            print("predict:{}, but expected: {}".format(path,targets[i]))
            return False

    return True

