from dataclasses import dataclass
from fractions import Fraction
from typing import Union

@dataclass
class Variable:
    value: float

@dataclass
class NumLiteral:
    value: float

@dataclass
class BinOp:
    operator: str
    left: 'AST'
    right: 'AST'

AST = NumLiteral | BinOp


class InvalidProgram(Exception):
    pass

def eval(program: AST):
    match program:
        case NumLiteral(value):
            return value
        case BinOp("+", left, right):
            return eval(left) + eval(right)
        case BinOp("-", left, right):
            return eval(left) - eval(right)
        case BinOp("*", left, right):
            return eval(left) * eval(right)
        case BinOp("/", left, right):
            return eval(left) / eval(right)
        case BinOp("=", left, right):
            x = eval(right)
            if isinstance(left, Variable) and isinstance(x,float):
                program.left.value = x
                return True
            else :
                raise InvalidProgram()
                
            
    raise InvalidProgram()


def test_eval():
    e1 = NumLiteral(2)
    e2 = NumLiteral(7)
    e3 = NumLiteral(9)
    e4 = NumLiteral(5)
    e5 = BinOp("+", e2, e3)
    e6 = BinOp("/", e5, e4)
    e7 = BinOp("*", e1, e6)
    e8 = Variable(0)
    e9 = BinOp("=",e8,e7)
    eval(e9)
    print(e8.value)

    
test_eval()
