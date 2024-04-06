# d1 is a strict dict which contains details of the object stored in database
# d2 is update dict which contains none and not none fields, not none fields should reflect in d1


def merge_dicts(d1, d2):
    result = {}
    for k in d1.keys():
        print(k)
        if isinstance (d1[k], dict):
            if (k not in d2.keys()) or (type(d1[k]) != type(d2[k])):
                result[k] = d1[k]
            else :
                result[k] = merge_dicts(d1[k] , d2[k])
        else:
            if (k in d2.keys()) and (d2[k] is not None):
                result[k] = d2[k]
            else:
                result[k] = d1[k]
    
    return result