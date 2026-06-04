total = 0
for i in range(5):
    num = input()
    if num == "A":
        total += 1
    elif num == "J":
        total += 11
    elif num == "Q":
        total += 12
    elif num == "K":
        total += 13
    else:
        total += int(num)
print(total)

