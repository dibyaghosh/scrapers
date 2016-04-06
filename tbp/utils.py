def fixCode(change_dict,coursecode):
    for og,final in change_dict.items():
        coursecode = coursecode.replace(og,final)
    return coursecode
