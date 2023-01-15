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
    
@dataclass
class Boolean:
    value : bool
    
@dataclass
class IfEl:
    exp: 'AST'
    ifstate : 'AST'
    elsestate : 'AST'

AST = NumLiteral | BinOp | Variable | Let | Boolean

Value = Fraction

class InvalidProgram(Exception):
    pass

def eval(program: AST, envi : dict):
    match program:
        case NumLiteral(value) | Boolean(value):
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
        case BinOp("<",left,right):
            x = eval(left,envi)
            y = eval(right,envi)
            return x<y
        case BinOp(">",left,right):
            x = eval(left,envi)
            y = eval(right,envi)
            return x>y
        case BinOp("==",left,right):
            x = eval(left,envi)
            y = eval(right,envi)
            return x<y
        case IfEl(exp,ifstate,elsestate):
            if(eval(exp,envi)):
                return eval(ifstate,envi)
            else:
                return eval(elsestate,envi)
            
            
    raise InvalidProgram()

def test_eval():
    x = Variable("x")
    e1 = NumLiteral(5)
    e2 = BinOp("*",Variable("x"),NumLiteral(2))
    e3 = Let(x,e1,e2)
    e4 = BinOp("<",NumLiteral(4),NumLiteral(3))
    e5 = BinOp("*",Variable("x"),NumLiteral(3))
    e6 = Let(x,e1,e5)
    e7 = IfEl(e4,e3,e6)
    print(eval(e7,{}))
    
test_eval()
    