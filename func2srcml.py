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
import stmt2srcml
import xml


def convertParams(args: ast.arguments) -> str:
    """Helper method to process a list of parmaeters (to either a 
    function defintion or a lambda) and returns a srcML XML.

    Arguments:
        args: The arguments to be converted to a srcML XML

    Returns:
        A string with the srcML XML
    """
    # Process parameters to the function into an list of XML entries
    prmListXML = ""
    for prm in args.args:
        prmType = xml.form("type", expr2srcml.convertName(prm.annotation))\
            if prm.annotation else ""
        prmDecl = xml.form("decl",  prmType + xml.form("name", prm.arg))
        prmListXML += xml.form("parameter", prmDecl)
        prmListXML += ", "
    # Remove trailing ", " and create parameter list.
    prmListXML = "(" + prmListXML[:-2] + ")"
    # Return the parameter list
    return prmListXML


def convertFuncDef(fnDef: ast.FunctionDef) -> str:
    """Helper method that is called from stmt2srcml.convertStmt() method.
    This method is called to convert a function definition to corresponding
    XML.  This method would be called to covert the following Python code:
        
        def testing(a: int, b: str) -> str:
            a = a + 1
            return str + "*"

    Arguments:
        fnDef: The function definition to be coverted to XML

    Returns:
        The function definition to be converted to source ML
    """
    # Get return type if specified as hint. Otherwise it will be ""
    retTypeXML = xml.form("type", expr2srcml.convertExpr(fnDef.returns))\
        if fnDef.returns else ""
    # Get the name of the function
    fnName = fnDef.name
    # Process parameters to the function into an list of XML entries
    prmListXML = convertParams(fnDef.args)
    # Next convert the function body to corresponding XML
    fnBody = stmt2srcml.convertBlock(fnDef.body)
    # Make the sequence of elements for your function.
    fnXML = xml.form("name", fnName, "parameter_list", prmListXML) + fnBody
    # Return the fully formed XML for the function defintion
    return xml.form("function", retTypeXML + fnXML) +\
        " <!-- {} -->".format(fnName)


def convertArg(arg: xml.AST_ExprNodes) -> str:
    """This is a helper method used in convertFuncCall to process
    each argument to a function call. 

    Arguments:
        arg: The argument to be processed.  This parameter can 
        either be an ast.Expr ndoe or ast.Str depending on the
        version of the AST package being used.
    """
    # Use helper methods to get XML.
    argXML = expr2srcml.convertExpr(arg) if isinstance(arg, ast.Expr) else\
            expr2srcml.convertExprValue(arg)
    # For some reason each argument does not come out as an ast.Expr
    # node. So we streamline it by explicitly adding "<expr>" here
    # as needed.
    if not argXML.startswith("<expr>"):
        argXML = xml.form("expr", argXML)
    return argXML


def convertFuncCall(call: ast.Call) -> str:
    """Prints the srcML XML corresponding to the given function call.

    Arguments:
        call: The function call node for which XML is to be printed.
    """
    # First figure out the name of function being called.
    # The call.func can be slightly different objects.

    fnName:str = expr2srcml.convertExprValue(call.func)

    if not fnName:
        raise Exception("Invalid function call {}".format(ast.dump(call)))
    # Start the starting XML-node for function calls
    fnXML = "<call>{}<argument_list>(".format(fnName)

    # Next figure out the arguments to the function call.
    for arg in call.args:
        fnXML += xml.form("argument", convertArg(arg))

    # Handle named arguments in function calls. Eg: print("0",end="")
    if call.keywords:
        for kw in call.keywords:
            fnXML += xml.form("argument", xml.form("name", kw.arg) +\
                expr2srcml.convertExpr(kw.value))

    # Add the ending XML-node for the function call.
    # fnXML += ")</argument_list></call> <!-- {} -->".format(fnName)
    fnXML += ")</argument_list></call>"
    return fnXML


def convertLambda(lmda: ast.Lambda) -> str:
    """Helper method to convert a lambda to corresponding srcML XML.
    Arguments:
        lmda: The lambda to be converted to XML
    Returns:
        The string with the XML corresponding to the lambda
    """
    # Convert all the parameters to the lambda to srcML XML
    paramXML = convertParams(lmda.args)
    # Convert the body of the lambda to srcML XML
    lmdaBody = "<block>: <block_content>" + expr2srcml.convertExpr(lmda.body) +\
        "</block_content></block>"
    # Return the lambda XML
    return xml.form("lambda", paramXML + lmdaBody)

# End of source code
