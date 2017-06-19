import sys
import Const

temp = ['a','b']

# mod1.py
def sum(a, b):
    return a+b

def safe_sum(a, b):
    if type(a) != type(b):
        print("더할수 있는 것이 아닙니다.")
        return
    else:
        result = sum(a, b)
    return result

if __name__ == "__main__":
    # print(safe_sum('a', 1))
    # print(safe_sum(1, 4))
    # print(sum(10, 10.4))

    # print(sys.argv[1])
    print(temp[0])
    print(temp[1])

    item = {}
    item['a'] = 1
    item['b'] = 2

    print(item)

    item = {}

    print(item)