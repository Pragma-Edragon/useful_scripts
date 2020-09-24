import time

start = str(round(time.time(), 2)).replace('.', '')
end = str(round(time.time(), 2)).replace('.', '')

ftime = ':'.join(list(''.join(i) for i in zip(str(end)[4::2], str(end)[5::2])))
s_time = ':'.join(list(''.join(i) for i in zip(str(start)[4::2], str(start)[5::2])))

print(ftime.split(':'))
print(s_time.split(':'))

res = []
for list1, list2 in zip(ftime.split(':'), s_time.split(':')):
    print(str(int(list1) - int(list2)))

print(res)
