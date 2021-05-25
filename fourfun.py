# 4 function calculator example

import sys
from ppc import *

#build a parser
def dofactor(result, *args, **kwargs):
      if result[1] == "*":
            return [result[0] * result[2]]
      else:
            return [result[0] // result[2]]

def doexpr(result, *args, **kwargs):
      if result[1] == "+":
            return [result[0] + result[2]]
      else:
            return [result[0] - result[2]]


skip_ws = terminal(" ").any().discard()

digit = terminal("0") \
      | terminal("1") \
      | terminal("2") \
      | terminal("3") \
      | terminal("4") \
      | terminal("5") \
      | terminal("6") \
      | terminal("7") \
      | terminal("8") \
      | terminal("9")

number = digit.some().bind(lambda result, *args, **kwargs: [int("".join(result))]) + skip_ws

openp = terminal("(") + skip_ws
closep = terminal(")") + skip_ws

plus = terminal("+") + skip_ws
minus = terminal("-") + skip_ws
times = terminal("*") + skip_ws
over = terminal("/") + skip_ws

expr = forward()

subexpr = (openp + expr + closep).bind(lambda result, *args, **kwargs: result[1:-1])

term = number | subexpr

factor = forward()
factor._def = (term + (times | over) + factor).bind(dofactor) | term

expr._def = (expr + (plus | minus) + factor).bind(doexpr) | factor

#repl
if __name__ == '__main__':
      print("4 function calculator example")
      print("supported operations: + - * / ( )")
      print("submit a blank line or press ^C to exit")
      while True:
            print("? ", end="", flush=True)
            try:
                  line = sys.stdin.readline()
            except KeyboardInterrupt as e:
                  exit()
            if not len(line.strip()):
                exit()
            p = expr.parse(line)
            if p.error:
                  print("bad input: syntax error")
            else:
                  print(p.result[0])