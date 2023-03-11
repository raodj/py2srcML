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

# This source file contains methods that focus on converting
# an expression node in the AST to srcML.  The Expr node has
# several subclasses and is involved.  Hence, they have been
# placed in a separate source file to keep things organized.

import ast
import typing

import op2srcml
import func2srcml
import comp2srcml
import if2srcml
import xml

def convertAttribute(attrib: ast.Attribute) -> str:
    """Helper method to convert an attribute to srcML XML

    Arguments:
        attrib: The attribute to be converted to XML
    Returns:
        The XML corresponding to the attribute.
    """
    attribXML = xml.form("name", convertExpr(attrib.value),
        "operator", ".", "name", attrib.attr)
    return xml.form("name", attribXML)

def convertName(node: typing.Union[ast.Name, ast.Expr]) -> str:
    """Helper method to just return the string for a given identifier

    Arguments:
        node: An ast.Name or ast.Expr node from where the name of a
        identifier (variable, function, etc.) is returned.
    """
    if isinstance(node, ast.Name):
        return xml.form("name", node.id)
    elif isinstance(node, ast.Expr):
        return convertExpr(node)
    elif isinstance(node, ast.Attribute):
        return convertAttribute(node)
    else:
        raise Exception("Uhandled name node {}", ast.dump(node))


def convertConstant(const: ast.Constant) -> str:
    """Helper method to convert literals to srcML XML
    Arguments:
        const: An ast.Constant node containing the literal
    Returns:
        Returns the srcML XML fragment for the literal
    """
    if isinstance(const.value, str):
        return xml.form("literal type=\"string\"", "\"" + const.value + "\"")
    elif isinstance(const.value, bool):
        return xml.form("literal type=\"boolean\"", "\"" + str(const.value) + "\"")
    elif isinstance(const.value, float) or isinstance(const.value, int):
        return xml.form("literal type=\"number\"", str(const.value))
    elif isinstance(const.value, complex):
        return xml.form("literal type=\"complex\"", "\"" + str(const.value) + "\"")
    elif const.value is None:
        return xml.form("literal type=\"none\"", "\"" + str(const.value) + "\"")
    else:
        raise Exception("Unhandled Constant {}".format(ast.dump(const)))


def convertBoolOper(binOp: ast.BoolOp) -> str:
    """Converts boolean operators in the from "True and False"
    Arguments:
        binOp: The binary operator 
    Returns:
        Returns the srcML XML fragment for the boolean operator
    """
    # For get XML the operator itself.
    operXML = op2srcml.convertOp(binOp.op)
    # Next convert the value expressions and process them
    valXML = convertExpr(binOp.values[0])
    for val in binOp.values[1:]:
        valXML += operXML
        valXML += convertExpr(val)
    # Return the formatted XML
    return xml.form("expr", valXML)


def convertBinOper(binOp: ast.BinOp) -> str:
    """Converts binary operators in the from 1 + 2
    """
    # First obtain the XML for the left and right hand side expressions.
    lhsXML = convertExpr(binOp.left)
    rhsXML = convertExpr(binOp.right)
    # Get the operator itself.
    operXML = op2srcml.convertOp(binOp.op)
    # Return the formatted XML
    return xml.form("expr", lhsXML + operXML + rhsXML)


def convertCompare(comp: ast.Compare) -> str:
    """Helper method to convert a comparison operator.
    """
    exprXML = ""
    # First obtain the XML for the left and right hand side expressions.
    lhsXML = convertExpr(comp.left)
    for i in range(0, len(comp.ops)):
        # Add the "and" operator to successive expresions
        if i > 0:
            exprXML += xml.form("operator", "and")
        # Convert the operators into a suitable subexpressions
        operXML = op2srcml.convertOp(comp.ops[i])
        rhsXML = convertExpr(comp.comparators[i])
        # Combine them into the running expression
        exprXML += lhsXML + operXML + rhsXML
        # Prep for the next set of operators
        lhsXML = rhsXML
    # Return the formatted XML
    return xml.form("expr", exprXML)


def convertTuple(tup: ast.Tuple) -> str:
    # Converts "[k, v]" to "<index>[<expr><name>k</name></expr>
    # <operator>,</operator> <name>v</name>]</index>"
    elemXML = ""
    for entry in tup.elts:
        # Add the ',' separator that may be needed
        elemXML += xml.form("operator", ",") if elemXML else ""
        elemXML += convertExpr(entry)
    # Return the overall index expression
    elemXML = "[" + elemXML + "]"
    return xml.form("index", elemXML)


def convertList(lst: ast.List) -> str:
    """Method to convert a list of the form [1, 2, 3] to srcML XML

    Arguments:
        lst: The list to be converted to XML

    Returns
        The XML corresponding to the list
    """
    lstXML = ""
    for entry in lst.elts:
        # Add the ',' separator that may be needed
        lstXML += xml.form("operator", ",") if lstXML else ""
        lstXML += convertExpr(entry)
    # Return the overall index expression
    lstXML = "[" + lstXML + "]"
    return xml.form("block", lstXML) 


def convertSlice(slice: ast.Slice) -> str:
    """Helper method to convert a slice to a suitable srcML XML.
    For example, expressions of the form "[1:]", "[2:3]", and "[:2]"

    Arguemnts:
        slice: The slice to be converted to XML

    Returns:
        The XML string 
    """
    # Convert each individual components of the slice to corresponding XML
    colXML   = xml.form("operator", ":")
    lowXML   = convertExpr(slice.lower) if slice.lower else ""
    hiXML    = convertExpr(slice.upper) if slice.upper else ""
    stepXML  = colXML + convertExpr(slice.step)  if slice.step  else ""
    # Return the combined XML back
    return xml.form("index", "[" + lowXML + colXML + hiXML + stepXML + "]")


def convertSubscript(sub: ast.Subscript) -> str:
    """Helper method to convert a subscript expression of the form
    s[1:2] to corresponding srcML

    Arguments:
        sub: The subcript expression to be converted to srcML XML

    Returns:
        Returns a string corresponding to the XML
    """
    if isinstance(sub.slice, ast.Slice):
        return convertExpr(sub.value) + convertSlice(sub.slice)
    elif isinstance(sub.slice, ast.Constant):
        return convertExpr(sub.value) + convertExprValue(sub.slice)
    else:
        raise Exception("Unhandled subscript {}".format(ast.dump(sub)))


def convertUnaryOp(uop: ast.UnaryOp) -> str:
    """Helper method to convert an unary operator in the form "-a"
    to corresponding srcML XML.

    Arguments:
        uop: The unary operator to be converted to XML

    Returns:
        The srcML XML corresponding to the unary operator.
    """
    return op2srcml.convertOp(uop.op) + convertExpr(uop.operand);


def convertExprValue(exprVal: xml.AST_ExprNodes) -> str:
    """"The top-level method for processing an expression AST node. 
    Expressions are most diverse nodes in the AST.

    Arguments:
        expr: The expression node to be processed.
    Returns:
        An optional string value or None.
    """
    # The XML string corresponding to the 
    exprXML = ""
    if isinstance(exprVal, ast.BoolOp):
        exprXML = convertBoolOper(exprVal)
    # elif isinstance(expr.value, ast.NamedExpr):
    #    raise Exception("Unhandled NamedExpr {}".format(ast.dump(exprVal)));
    elif isinstance(exprVal, ast.BinOp):
        exprXML = convertBinOper(exprVal)
    elif isinstance(exprVal, ast.UnaryOp):
        exprXML = convertUnaryOp(exprVal)
    elif isinstance(exprVal, ast.Lambda):
        exprXML = func2srcml.convertLambda(exprVal)
    elif isinstance(exprVal, ast.IfExp):
        exprXML = if2srcml.convertIfExp(exprVal)
    elif isinstance(exprVal, ast.Dict):
        exprXML = comp2srcml.convertDict(exprVal)
    elif isinstance(exprVal, ast.Set):
        raise Exception("Unhandled Set {}".format(ast.dump(exprVal)));
    elif isinstance(exprVal, ast.ListComp):
        exprXML = comp2srcml.convertListComp(exprVal)
    elif isinstance(exprVal, ast.SetComp):
        raise Exception("Unhandled SetComp {}".format(ast.dump(exprVal)));
    elif isinstance(exprVal, ast.DictComp):
        raise Exception("Unhandled DictComp {}".format(ast.dump(exprVal)));
    elif isinstance(exprVal, ast.GeneratorExp):
        exprXML = comp2srcml.convertGenExp(exprVal)
    elif isinstance(exprVal, ast.Await):
        raise Exception("Unhandled Await {}".format(ast.dump(exprVal)));
    elif isinstance(exprVal, ast.Yield):
        raise Exception("Unhandled Yield {}".format(ast.dump(exprVal)));
    elif isinstance(exprVal, ast.YieldFrom):
        raise Exception("Unhandled YieldFrom {}".format(ast.dump(exprVal)));
    elif isinstance(exprVal, ast.Compare):
        exprXML = convertCompare(exprVal)
    elif isinstance(exprVal, ast.Call):
        exprXML = func2srcml.convertFuncCall(exprVal)
    elif isinstance(exprVal, ast.FormattedValue):
        raise Exception("Unhandled FormattedValue {}".format(ast.dump(exprVal)));
    elif isinstance(exprVal, ast.JoinedStr):
        raise Exception("Unhandled JoinedStr {}".format(ast.dump(exprVal)));
    elif isinstance(exprVal, ast.Constant):
        exprXML = convertConstant(exprVal)
    elif isinstance(exprVal, ast.Attribute):
        return convertAttribute(exprVal)
    elif isinstance(exprVal, ast.Subscript):
        exprXML = convertSubscript(exprVal)
    elif isinstance(exprVal, ast.Starred):
        raise Exception("Unhandled Starred {}".format(ast.dump(exprVal)));
    elif isinstance(exprVal, ast.Name):
        exprXML = convertName(exprVal)
    elif isinstance(exprVal, ast.List):
        exprXML = convertList(exprVal)
    elif isinstance(exprVal, ast.Tuple):
        exprXML = convertTuple(exprVal)
    elif isinstance(exprVal, ast.Slice):
        raise Exception("Unhandled Slice {}".format(ast.dump(exprVal)));
    elif isinstance(exprVal, ast.NameConstant):
        const: ast.NameConstant = exprVal
        return str(const.value)
    else:
        raise Exception("Unhandled expression {}".format(ast.dump(exprVal)));

    # Return the formatted string.
    return exprXML


def convertExpr(expr: xml.AST_ExprNodes) -> str:
    """"The top-level method for processing subnode of an expression AST node. 
    Expressions are most diverse nodes in the AST.

    Arguments:
        expr: The expression node to be processed.
    Returns:
        An optional string value or None.
    """
    # Use helper method to handle different cases better
    if isinstance(expr, ast.Expr):
        exprXML = convertExprValue(expr.value);
        return xml.form("expr", exprXML)
    else:
        return convertExprValue(expr)

# End of source code
