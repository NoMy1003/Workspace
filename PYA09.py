with open("read.txt", "r", encoding="utf-8") as file:
    line = file.read()
    numbers = line.split()
    total = 0
    for num in numbers:
        total += int(num)
    print(total)
file.close()