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
    
@dataclass
class IfElse:
    condition : 'AST'
    whentrue : 'AST'
    whenfalse : 'AST'

AST = NumLiteral | BinOp | Variable | IfElse


    

    

class InvalidProgram(Exception):
    pass

def eval(program: AST):
    match program:
        case NumLiteral(value) | Variable(value) :
            return float(value)
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
            print(type(x))
            if isinstance(left, Variable) and (isinstance(x,float)):
                if isinstance(x,NumLiteral): x=x.value
                program.left.value = x
                print("equal assignment completed")
                return 1.0
            else :
                raise InvalidProgram()
        case BinOp(">", left, right) | BinOp("<", left, right) | BinOp("==", left, right):
            x = eval(right)
            y = eval(left)
            if isinstance(x,Variable):
                x= x.value
            if isinstance(y,Variable):
                y= y.value
            print("condition completed")
            match program.operator :
                case ">":
                    return float(int(x>y))
                case "<":
                    return float(int(x<y))
                case "==":
                    return float(int(x==y))
        case IfElse(condition,whentrue, whenfalse):
            x= eval(condition)
            if x==0:
                eval(program.whenfalse)
                return 
            else:
                eval(program.whentrue)
                return 
            
    raise InvalidProgram()


def test_eval():
    a = Variable(0)
    e2 = BinOp("=",a,NumLiteral(2))
    e3 = BinOp("=",a,NumLiteral(1))
    e1 = IfElse(BinOp("<",NumLiteral(1),NumLiteral(2)),e2,e3)
    eval(e1)
    print(a.value)
    
test_eval()
