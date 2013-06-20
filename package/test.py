class Test:
    def method(self, x, y):
        return x * y

def func():
    a = Test()
    out = a.method(1, 2)
    return out
