input_str = input()
total = 0
for i in range(len(input_str)):
    print(f"ASCII code for '{input_str[i]}' is {ord(input_str[i])}.")
    total += ord(input_str[i])
print(total)