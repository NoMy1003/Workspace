n = int(input())
round = 1
while(n != 9999):
    if round == 1:
        tmp_min = n
    else:
        if n < tmp_min and n != 9999:
            tmp_min = n
    round += 1
    n = int(input())
print(tmp_min)