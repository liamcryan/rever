from rever import rever


@rever()
def f():
    return "hi liam"

a = f()

print(a)