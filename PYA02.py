num = int(input())
if num % 3 == 0:
    if num % 5 == 0:
        print(f"{num} is a multiple of 3 and 5.")
    else:
        print(f"{num} is a multiple of 3.")
elif num % 5 == 0:
    print(f"{num} is a multiple of 5.")
else:
    print(f"{num} is not a multiple of 3 or 5.")