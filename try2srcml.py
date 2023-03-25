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
import ast

import expr2srcml
import xml
import stmt2srcml


# This source file contains methods that focus on converting
# a try statement node in the AST to srcML. The
# methods in this file are typically called from stmt2srcml.py
# This source file has been introduced to streamline the
# overall script and keep things organized.

def convertTry(tryStmt: ast.Try) -> str:

    """Helper method to convert try/except blocks into srcML.
    This method would be called to covert the following Python code:
        try:
            pass
        except (Exception, ValueError) as e:
            pass
    Arguments:
        stmt: the try/except block to be converted as an ast.Try object

    Returns:
        the srcML XML corresponding to the given block
    """
    XML = stmt2srcml.convertBlock(tryStmt.body)
    for handler in tryStmt.handlers:
        exception = expr2srcml.convertExprValue(handler.type) if handler.type else ""
        name = expr2srcml.convertName(ast.Name(handler.name, ast.Store())) if handler.name else ""
        body = stmt2srcml.convertBlock(handler.body)
        XML += xml.form("catch", "except" + exception + name + body)
    # should else be supported?
    XML += xml.form("else", stmt2srcml.convertBlock(tryStmt.orelse)) if len(tryStmt.orelse) > 0 else ""
    XML += xml.form("finally", stmt2srcml.convertBlock(tryStmt.finalbody)) if len(tryStmt.finalbody) > 0 else ""

    return xml.form("try","try" + XML)
