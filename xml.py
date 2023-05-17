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

# This is a simple source file that is used to print out XML
# formatted information.  This method essenitally centralizes XML
# generation to a few methods.  This helps primarily with debugging.
# Rather than having XML fragments generated all over source files,
# we generate XML here so that we can set a breakpoint and observe
# stack traces and troubleshoot issues.

import ast
import typing

# An alias for a large number of AST expr node classes.
# These type aliases are used in different source files.
AST_ExprNodes = typing.Union[ast.BoolOp, ast.BinOp,
    ast.UnaryOp, ast.Lambda, ast.IfExp, ast.Dict, ast.Set, 
    ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp,
    ast.Await, ast.Yield, ast.YieldFrom, ast.Compare, ast.Call,
    ast.FormattedValue, ast.JoinedStr, ast.Constant, ast.Attribute,
    ast.Subscript, ast.Starred, ast.Name, ast.List, ast.Tuple, 
    ast.Slice, ast.Num, ast.Str, ast.Expr]

# The set of AST nodes that constitute a statement in Python.
# These type aliases are used in different source files.
AST_StmtNodes = typing.Union[ast.FunctionDef, ast.AsyncFunctionDef,
    ast.ClassDef, ast.Return, ast.Delete, ast.Assign, ast.AugAssign,
    ast.AnnAssign, ast.For, ast.AsyncFor, ast.While, ast.If, 
    ast.With, ast.AsyncWith, ast.Raise, ast.Try, ast.Assert, 
    ast.Import, ast.ImportFrom, ast.Global, ast.Nonlocal, ast.Expr,
    ast.Pass, ast.Break, ast.Continue]


def form(*tagValPairs) -> str:
    xmlStr = ""
    for i in range(0, len(tagValPairs), 2):
        # Get the start tag
        stTag = tagValPairs[i]
        if (stTag != None):
            # XML tags may have attributes eg: 'literal type="string"'
            # So we just always use just the 1st word for end tag.
            endTag = stTag.split()[0]
            val = tagValPairs[i + 1]
            xmlStr += "<{}>{}</{}>".format(stTag, val, endTag)
    return xmlStr

def escape(text: str) -> str:
    """Escapes <, >, & characters from an input string
    Arguments:
        text: The input string
    Returns:
        A string with escaped characters
    """
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    # text.replace("\'", "&apos;")
    # text.replace("\"", "&quot;")
    return text

# End of source code
