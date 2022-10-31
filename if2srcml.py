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

""" If to srcML conversion

This source file contains methods that focus on converting
an if or if-exp statement nodes in the AST to srcML.  The
methods in this file are typically called from stmt2srcml.py
This source file has been introduced to streamline the 
overall script and keep things organized.
"""

import ast

import stmt2srcml
import expr2srcml
import xml

def convertIf(ifStmt: ast.If, isElseIf: bool = False) -> str:
    """This method converts if-elif-else block to corresponding
    srcML XML.  This method works recursively. In recursive
    calls the isElseIF flag should be set to True.

    Arguments:
        ifStmt: The AST node corresponding to the if or elif
        statement to be converted to srcML.
        isElseIF: This flag should be True when this method is
        recursively called to process elif blocks.

    Returns:
        The srcML fragment corresponding to the statement (includes body).
    """
    condXML   = xml.form("condition", expr2srcml.convertExpr(ifStmt.test))
    ifBodyXML = stmt2srcml.convertBlock(ifStmt.body)
    if not isElseIf:
        ifXML = "<if_stmt><if>if " + condXML + ifBodyXML + "</if>"
    else:
        ifXML = "<if type=\"elseif\">elif " + condXML + ifBodyXML + "</if>"
    # Handle any elif statement(s)
    if len(ifStmt.orelse) > 0:
        if isinstance(ifStmt.orelse[0], ast.If):
            ifXML += convertIf(ifStmt.orelse[0], True)
        else:
            ifXML += "<else>else <block>:<block_content>"
            for expr in ifStmt.orelse:
                ifXML += stmt2srcml.convertStmt(expr)
            ifXML += "</block_content></block></else>"
    # Finish and return the XML for the if-elif-else statement
    if not isElseIf:
        ifXML += "</if_stmt>"
    return ifXML


def convertIfExp(ifExp: ast.IfExp) -> str:
    """This method converts ternary-type if-else statement to 
    corresponding srcML XML. For example: "if True 1 else 0"

    Arguments:
        ifExp: The AST node corresponding to the if-exp
        statement to be converted to srcML.

    Returns:
        The srcML fragment corresponding to the statement.
    """
    # Convert the condition 
    condXML = xml.form("condition", expr2srcml.convertExpr(ifExp.test))
    # Convert the expression for the 'true' case
    trueXML = xml.form("then", expr2srcml.convertExpr(ifExp.body))
    # Convert the expression for the 'false' case
    falseXML = xml.form("else", expr2srcml.convertExpr(ifExp.orelse))
    # Return the full ternary XML back
    return xml.form("ternary", condXML + trueXML + falseXML)
