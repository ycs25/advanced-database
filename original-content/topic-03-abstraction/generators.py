def count_up():
    numbers = []
    for i in range(0,100):
        numbers.append(i+1)
    return numbers

print(count_up())

def count_up_generator(n):
    for i in range(0,n):
        yield i+1
    
x = count_up_generator(100)
print(next(x))
print(next(x))
print(next(x))
print(next(x))

x = count_up_generator(4)
print(list(x))
