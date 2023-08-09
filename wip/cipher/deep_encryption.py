def a(x):
    r_dict = globals().copy()
    r_dict.update(locals())
    s = """
def b(x):
    print(x)
b(x)
"""
    exec(s, r_dict)


def foo(x):
    s = """
def b(x):
    print(x)
"""
    exec(s, globals())
    b(x)
    del globals()["b"]


s = "Hello, world!"

a(s)

foo(s)
