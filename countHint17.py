def get_file_name(w, p):
    return "result/hintStr___" + str(w) + "_" + str(p) + ".txt"


def getHint17Number(file_name):
    count = 0
    with open(file_name, "r") as f:
        count = len(f.readlines())
    return count


min_count = 2 ** 32
for w in range(3, 9):
    for p in range(2, w+1):
        file_name = get_file_name(w, p)
        try:
            count = getHint17Number(file_name)
            min_count = min(min_count, count)
            print(file_name, count)
        except:
            print("error:", file_name)

print("min count of hint 17:", min_count)