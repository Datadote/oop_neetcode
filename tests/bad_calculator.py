def add(a: int, b: int) -> int:
    return a + b

def subtract(a, b):
    return a - b

def divide(a: int, b) -> float:
    return a / b

def miss_return(a: int, b: int):
    return a / b

if __name__ == '__main__':
    print(add(3, 5))
    print(subtract(3, 4))
    print(divide('s', 4))
    