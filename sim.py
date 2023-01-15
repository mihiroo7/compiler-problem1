from dataclasses import dataclass
from fractions import Fraction
from typing import Union

@dataclass
class NumLiteral:
    value: Fraction
    def __init__(self, *args):
        self.value = Fraction(*args)

@dataclass
class BinOp:
    operator: str
    left: 'AST'
    right: 'AST'
    
@dataclass
class Variable:
    name : str
    
@dataclass
class Let:
    variable : Variable
    e1 : 'AST'
    e2 : 'AST'

AST = NumLiteral | BinOp | Variable | Let

Value = Fraction

class InvalidProgram(Exception):
    pass

def eval(program: AST, envi : dict):
    match program:
        case NumLiteral(value):
            return value
        case BinOp("+", left, right):
            return eval(left,envi) + eval(right,envi)
        case BinOp("-", left, right):
            return eval(left,envi) - eval(right, envi)
        case BinOp("*", left, right):
            return eval(left, envi) * eval(right, envi)
        case BinOp("/", left, right):
            return eval(left, envi) / eval(right, envi)
        case Variable(name):
            if name in envi:
                return envi[name]
            InvalidProgram()
        case Let(variable,e1,e2):
            x = eval(e1,envi)
            envi[variable.name] = eval(e2,envi | {variable.name : x})
            return envi[variable.name]
            
    raise InvalidProgram()

def test_eval():
    x = Variable("x")
    e1 = NumLiteral(5)
    e2 = BinOp("*",Variable("x"),NumLiteral(2))
    e1 = Let(x,e1,e2)
    print(eval(e1,{}))
    
test_eval()
    