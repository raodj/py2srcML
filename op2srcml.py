#!/usr/bin/python3

#-----------------------------------------------------------------------
#  This file is part of Python to srcML (py2srcm)
#
#  Py2srcML is free software:  you can  redistribute it and/or  modify it
#  under the terms of the GNU  General Public License  (GPL) as published
#  by  the   Free  Software Foundation, either version 3 (GPL v3), or (at
#  your option) a later version.
#
#  Py2srcML is being distributed in the hope that it will  be useful, but
#  WITHOUT  ANY  WARRANTY;  without  even  the IMPLIED WARRANTY of  MERC-
#  HANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
#  Miami University  and  our development team make no representations or
#  warranties  about the suitability  of the software, either express  or
#  implied, including but not limited to the implied warranties of merch-
#  antability, fitness  for a  particular  purpose,  or non-infringement.
#  Miami  University  and  its  affiliates  shall  not  be liable for any
#  damages suffered by the  licensee as a result of using, modifying,  or
#  distributing this software  or its derivatives.
#
#  By using or  copying  this  Software,  Licensee  agree to abide  by the 
#  intellectual property laws, and all other applicable laws of  the U.S.,
#  and the terms of the   GNU  General  Public  License  (version 3).  You  
#  should  have  received a  copy of the  GNU General Public License along
#  with Py2srcML.  If not, you  may  download  copies  of the GPL V3  from
#  <http://www.gnu.org/licenses/>.
#
# Author(s):   
#     DJ Rao               raodm@miamioh.edu
#------------------------------------------------------------------------

# This source file facilitates conversion of operators to 
# corresponding strings.  

import ast
import typing

def convertOp(op: typing.Union[ast.boolop, ast.operator, 
    ast.unaryop, ast.cmpop]) -> str:
    """This is a top-level method that can be used to convert
    any operator to corresponding python source code
    
    Arguments:
        op: The operator AST node to be converted

    Returns:
        The python source code corresponding to the node 
        or throws an exception if node is not handled.
    """
    opStr = ""
    if isinstance(op, ast.And):
        opStr = "and"
    elif isinstance(op, ast.Or):
        opStr = "or"
    elif isinstance(op, ast.operator):
        opStr = convertOperator(op)
    elif isinstance(op, ast.unaryop):
        opStr = convertUnaryOperator(op)
    elif isinstance(op, ast.cmpop):
        opStr = convertCmpOperator(op)
    else:
        raise Exception("Unhandled operator {}".format(ast.dump(op)))
    return "<operator>{}</operator>".format(opStr)

def convertCmpOperator(cop: ast.cmpop) -> str:
    """Helper method to convert comparison operators to corresponding
    operator strings.
    
    Arguments:
        op: An comparison operator node from Eq | NotEq | Lt | LtE | Gt | 
        GtE | Is | IsNot | In | NotIn

    Returns:
        The string corresponding to the node or throws an exception.
    """
    if isinstance(cop, ast.Eq):
        return "=="
    elif isinstance(cop, ast.NotEq):
        return "!="
    elif isinstance(cop, ast.Lt):
        return "&lt;"
    elif isinstance(cop, ast.LtE):
        return "&lt;="
    elif isinstance(cop, ast.Gt):
        return "&gt;"
    elif isinstance(cop, ast.GtE):
        return "&gt;="
    elif isinstance(cop, ast.Is):
        return "is"
    elif isinstance(cop, ast.IsNot):
        return "is not"
    elif isinstance(cop, ast.In):
        return "in"
    elif isinstance(cop, ast.NotIn):
        return "not in"
    else:
        raise Exception("Unhandled cmp operator {}".format(ast.dump(cop)))

def convertUnaryOperator(uop: ast.unaryop) -> str:
    """Helper method to convert unary operators to corresponding
    operator character.
    
    Arguments:
        op: An unary operator node Invert | Not | UAdd | USub

    Returns:
        The operator corresponding to the node or throws an exception.
    """
    if isinstance(uop, ast.Invert):
        return "~"
    elif isinstance(uop, ast.Not):
        return "not"
    elif isinstance(uop, ast.UAdd):
        return "+"
    elif isinstance(uop, ast.USub):
        return "-"
    else:
        raise Exception("Unhandled unary operator {}".format(ast.dump(uop)))

def convertOperator(op: ast.operator) -> str:
    """Helper method to convert binary operators to corresponding
    python source code.
    
    Arguments:
        op: An operator node from one of Add | Sub | Mult | MatMult | Div | 
        Mod | Pow | LShift | RShift | BitOr | BitXor | BitAnd | FloorDiv

    Returns:
        The operator corresponding to the node or throws an exception.
    """
    opStr = ""
    if isinstance(op, ast.Add):
        opStr = "+"
    elif isinstance(op, ast.Sub):
        opStr = "-"
    elif isinstance(op, ast.Mult):
        opStr = "*"
    elif isinstance(op, ast.MatMult):
        opStr = "@"
    elif isinstance(op, ast.Div):
        opStr = "/"
    elif isinstance(op, ast.Mod):
        opStr = "%"
    elif isinstance(op, ast.Pow):
        opStr = "**"
    elif isinstance(op, ast.LShift):
        opStr = "&lt;&lt;"
    elif isinstance(op, ast.RShift):
        opStr = "&gt;&gt;"
    elif isinstance(op, ast.BitOr):
        opStr = "|"
    elif isinstance(op, ast.BitXor):
        opStr = "^"
    elif isinstance(op, ast.BitAnd):
        opStr = "&amp;"
    elif isinstance(op, ast.FloorDiv):
        opStr = "//"
    else:
        raise Exception("Unhandled binary operator {}".format(ast.dump(op)))
    return opStr
