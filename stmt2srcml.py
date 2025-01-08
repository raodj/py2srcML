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
# a statement node in the AST to srcML.  The statement node has
# several subclasses and is involved.  Hence, they have been
# placed in a separate source file to keep things organized.

import ast
import typing

import expr2srcml
import func2srcml
import loops2srcml
import import2srcml
import op2srcml
import if2srcml
import XML
import class2srcml
import try2srcml

# The set of AST nodes that constitute a statement in Python.
AST_StmtNodes = typing.Union[ast.FunctionDef, ast.AsyncFunctionDef,
    ast.ClassDef, ast.Return, ast.Delete, ast.Assign, ast.AugAssign,
    ast.AnnAssign, ast.For, ast.AsyncFor, ast.While, ast.If, 
    ast.With, ast.AsyncWith, ast.Raise, ast.Try, ast.Assert, 
    ast.Import, ast.ImportFrom, ast.Global, ast.Nonlocal, ast.Expr,
    ast.Pass, ast.Break, ast.Continue]

def convertBlock(block: AST_StmtNodes) -> str:
    """Helper method to convert a block of code such as body of
    an if-statement, else-statement, for-loop etc. to srcML
    
    Arguments:
        block: Any AST node for an statement can be passed-in.

    Returns:
        The srcML XML corresponding to the body.
    """
    blockXML  = "<block>:<block_content>"
    for stmt in block:
        # print(ast.dump(stmt))
        blockXML += convertStmt(stmt)
    blockXML += "</block_content></block>"
    return blockXML


def convertAssignment(stmt: ast.Assign) -> str:
    """Helper method to convert assignments of the form 'i = i + 1' to
    corresponding srcML XML.
    
    Arguments:
        stmt: The assignment statement to be converted to srcML

    Returns:
        The srcML XML corresponding to the given assignment statement
    """
    if len(stmt.targets) > 1: 
        raise Exception("Unhandled many targets {}".format(ast.dump(stmt)))
    rhsXML = XML.form("operator", "=") + expr2srcml.convertExpr(stmt.value)
    lhsXML = expr2srcml.convertExpr(stmt.targets[0])
    return XML.form("expr_stmt", lhsXML + rhsXML)


def convertAugAssignment(stmt: ast.AugAssign) -> str:
    """Helper method to convert augumented assignments of the form 
    'i += 1' to corresponding srcML XML.
    
    Arguments:
        stmt: The augumented assignment statement to be converted to srcML

    Returns:
        The srcML XML corresponding to the given statement
    """
    # Get the XML for the target expression
    lhsXML = expr2srcml.convertExpr(stmt.target)
    opXML  = op2srcml.convertOp(stmt.op)
    rhsXML = expr2srcml.convertExpr(stmt.value)
    return XML.form("expr_stmt", lhsXML + opXML + rhsXML)

def convertDeclaration(stmt: typing.Union[ast.Nonlocal,ast.Global]) -> str:
    """Helper method to convert non-local and global variable declarations
    of the form 'global x' to corresponding srcML XML.

    Arguments:
        stmt: The declaration statement to be converted

    Returns:
        The srcML XML corresponding to the given statement
    """

    if isinstance(stmt, ast.Global):
        specifier = "global"
    else:
        specifier = "nonlocal"

    globalXML = "<decl_stmt>"
    for i in range(len(stmt.names)):
        if i == 0:
            globalXML += f"<decl><type><specifier>{specifier}</specifier></type>" \
                         f"{expr2srcml.convertName(ast.Name(stmt.names[i]))}</decl><operator>,</operator>"
        else:
            globalXML += f"<decl><type ref=\"prev\"/>{expr2srcml.convertName(ast.Name(stmt.names[i]))}</decl>" \
                         f"<operator>,</operator>"
    # removes trailing comma
    globalXML = globalXML[:-22] + "</decl_stmt>"
    return globalXML


def convertStmt(stmt: AST_StmtNodes) -> str:
    """
    This is a top-level method that can be used to convert any type of
    python statement to corresponding srcML XML.

    Arguments:
        stmt: The python statement to converted to XML
    Returns:
        The XML fragment corresponding to the python statement.
    """
    if isinstance(stmt, ast.FunctionDef):
        return func2srcml.convertFuncDef(stmt)
    elif isinstance(stmt, ast.AsyncFunctionDef):
        raise Exception("Unhandled async func def {}".format(ast.dump(stmt)))
    elif isinstance(stmt, ast.ClassDef):
        return class2srcml.convertClassDef(stmt)
    elif isinstance(stmt, ast.Return):
        retXML = expr2srcml.convertExpr(stmt.value) if stmt.value else ""
        return "<return>return{}</return>".format(retXML)
    elif isinstance(stmt, ast.Delete):
        raise Exception("Unhandled delete {}".format(ast.dump(stmt)))
    elif isinstance(stmt, ast.Assign):
        return convertAssignment(stmt)
    elif isinstance(stmt, ast.AugAssign):
        return convertAugAssignment(stmt)
    elif isinstance(stmt, ast.AnnAssign):
        raise Exception("Unhandled ann assign {}".format(ast.dump(stmt)))
    elif isinstance(stmt, ast.For):
        return loops2srcml.convertForLoop(stmt)
    elif isinstance(stmt, ast.AsyncFor):
        raise Exception("Unhandled async for loop {}".format(ast.dump(stmt)))
    elif isinstance(stmt, ast.While):
        return loops2srcml.convertWhileLoop(stmt)
    elif isinstance(stmt, ast.If):
        return if2srcml.convertIf(stmt)
    elif isinstance(stmt, ast.With):
        raise Exception("Unhandled with {}".format(ast.dump(stmt)))
    elif isinstance(stmt, ast.AsyncWith):
        raise Exception("Unhandled async with {}".format(ast.dump(stmt)))
    elif isinstance(stmt, ast.Raise):
        raiseXML = "<throw>raise"
        raiseXML += expr2srcml.convertExpr(stmt.exc)
        if stmt.cause is not None:
            raiseXML += "<name>from</name>"
            raiseXML += expr2srcml.convertExpr(stmt.cause)
        raiseXML += "</throw>"
        return raiseXML
    elif isinstance(stmt, ast.Try):
        return try2srcml.convertTry(stmt)
    elif isinstance(stmt, ast.Assert):
        assertXML = "<assert>"
        assertXML += expr2srcml.convertExpr(stmt.test)
        if stmt.msg is not None:
            assertXML += "<operator>,</operator>"
            assertXML += expr2srcml.convertExpr(stmt.msg)
        assertXML += "</assert>"
        return assertXML
    elif isinstance(stmt, ast.Import):
        return import2srcml.convertImport(stmt)
    elif isinstance(stmt, ast.ImportFrom):
        return import2srcml.convertImportFrom(stmt)
    elif isinstance(stmt, ast.Global):
        return convertDeclaration(stmt)
    elif isinstance(stmt, ast.Nonlocal):
        return convertDeclaration(stmt)
    elif isinstance(stmt, ast.Expr):
        exprXML = expr2srcml.convertExpr(stmt)
        return "<expr_stmt>{}</expr_stmt>".format(exprXML)
    elif isinstance(stmt, ast.Pass):
        return "<empty_stmt>pass</empty_stmt>"
    elif isinstance(stmt, ast.Break):
        return "<break>break</break>"
    elif isinstance(stmt, ast.Continue):
        return "<continue>continue</continue>"
    else:
        raise Exception("Unhandled statement {}".format(ast.dump(stmt)))
    return None
