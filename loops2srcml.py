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

def convertForLoop(stmt: ast.For) -> str:
    """Helper method to convert a for-loop to srcML XML.  Currently,
    we don't handle the for-else construct because the corresponding
    srcML is unspecified.
    """
    forXML = "<for>for <control><init><decl>" +\
        expr2srcml.convertExpr(stmt.target) + " <range>in " +\
        expr2srcml.convertExpr(stmt.iter) +\
        "</range></decl></init></control>"
    forXML += stmt2srcml.convertBlock(stmt.body)
    if len(stmt.orelse) > 0:
        raise Exception("Unhandled for-else {}".format(ast.dump(stmt)))
    forXML += "</for>"
    return forXML


def convertWhileLoop(stmt: ast.While) -> str:
    """Helper method to convert a while-loop to srcML XML.  Currently,
    we don't handle the while-else construct because the corresponding
    srcML is unspecified.
    """
    whileXML = "<while>while <condition>" +\
        expr2srcml.convertExpr(stmt.test) + "</condition>"
    whileXML += stmt2srcml.convertBlock(stmt.body)
    if len(stmt.orelse) > 0:
        raise Exception("Unhandled while-else {}".format(ast.dump(stmt)))
    whileXML += "</while>"
    return whileXML

# End of source code
