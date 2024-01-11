# hintStr_w_p.txtからどれほど違うヒントを生成しているか
# 調べてallSameHint.txtに出力する

NUMBER = 200
WRITE_FILE_NAME = "diff_count.txt"

def get_file_name(w, p):
    return "result/hintStr___" + str(w) + "_" + str(p) + ".txt"

def get_diff_count(file_name, number = NUMBER):
    with open(file_name, "r") as f:
        diff_data = list(map(str, f.readlines()[number-1].split()))
    return int(diff_data[1])


def write_diff(w, p, diff, file_name=WRITE_FILE_NAME):
    s = str(w) + " " + str(p) + " " + str(diff) + "\n"
    with open(file_name, "a") as f:
        f.write(s)

def main():
    for w in range(3, 9):
        for p in range(2, w+1):
            file_name = get_file_name(w, p)
            try:
                diff = get_diff_count(file_name)
                print(diff)
                write_diff(w, p, diff)
            except:
                print("error:", file_name)

if __name__ == "__main__":
    main()