from glob import glob

file_path = glob("*.py")
count = 0
for file_name in file_path:
    if file_name == "count_line.py":
        continue
    with open(file_name, "r") as fp:
        line = len(fp.readlines())
        print(file_name,':', line)
        count += line

print(count)