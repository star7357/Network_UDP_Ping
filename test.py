import random

a = []

for i in range(10000) :
    a.append(random.random() * 2)

print(min(a), max(a))