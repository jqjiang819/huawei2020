
def check(path0, path1):
    f0 = open(path0, "r")
    f1 = open(path1, "r")
    lines0 = [l for l in f0.readlines() if l.strip() != ""]
    lines1 = [l for l in f1.readlines() if l.strip() != ""]
    return lines0 == lines1
