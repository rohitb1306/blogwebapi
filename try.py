def count_code_lines(str):
    a=str.splitlines()
    b=[]
    d=""
    for i in a:
        for j in i:
            if j!="#":
                d+=j
            else:
                break
        if(d!=""):
            b.append(d)
            d=""
    print(len(b))
input_code = """#Linear search implementation
#Takes list and a key as input and returns True or False as answer
def linear_saerch(l,key):
    for value in l:
        if key == value:
            return True #Return True is key exist
    else:
        return False #Return False if key does not exist
l = [100,200,300,400,500,600]
key = 500
result = linear_search(l,key)
print(result)
"""
count_code_lines(input_code)