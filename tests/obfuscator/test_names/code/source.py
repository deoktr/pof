# source to be obfuscated for testing
import tutu
import tata as poo
from huhu import coco as poo
import ah, be, ce
from foo import (
  coo,
  boo,
)
from foo import (
  coo as jk,
  boo as lm,
)
from foo import (
  cil,
  bal as mp,
)

class A:
    def __init__(self, x=12):
        print(x)
        self.a = x
        self.bbb = "toto"

    def toto(self, a=1, b=None):
        self.a = 2
        print(self.a)

    @classmethod
    def toto(self, a=1, b=None, x=17):
        self.a = 2
        print(self.a)

a = A()
a.toto()
print(getattr(a, "bbb"))
print("bbb")
print(a.__dict__["a"])
print("a")
x = a.__dict__["a"]
print(a)
print("a")
print(tutu.titi())
