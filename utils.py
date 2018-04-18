
def replaceLess(str, old, new):
    while True:
        l = len(str)
        str = str.replace(old, new)
        if l == len(str):
            break
    return str

if __name__ == "__main__":
    print(replaceLess("c:///User/hyj///xx//a.txt", "//", "/"))
    print(replaceLess("c:/u/x/y/z.txt", "//", "/"))
