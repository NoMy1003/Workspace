num1 = []
num2 = []
print("Create tuple1:")
while True:
    num = int(input())
    if num == -9999:
        break
    else:
        num1.append(num)
print("Create tuple2:")
while True:
    num = int(input())
    if num == -9999:
        break
    else:
        num2.append(num)

print(f"Combined tuple before sorting: {tuple(num1 + num2)}")
print(f"Combined list after sorting: {sorted(num1 + num2)}")