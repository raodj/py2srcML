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
# a list comprehension to a corresponding srcML XML.

import ast

import expr2srcml
import XML

def convertListComp(stmt: ast.ListComp) -> str:
    """Helper method to convert an import statement to srcML XML.

    Arguments:
        stmt: The ListComp statement to be convereted to XML

    Returns:
        The srcML XML corresponding to the list comprehension statement.
    """
    # ListComp(expr elt, comprehension* generators)
    # comprehension = (expr target, expr iter, expr* ifs, int is_async)
    eltXML = expr2srcml.convertExpr(stmt.elt)
    # Convert the generators to an array in list
    genXML = convertGenerators(stmt.generators)
    # Combine the XML fragments together
    return eltXML + XML.form("operator", "=") + genXML


def convertGenerators(generators: ast.comprehension) -> str:
    """This is a refactored utility method that is used to convert generators
    associated with list comprehension or generator-expressions to srcML XML.

    Arguments:
        generators: The list of generators to be converted to XML

    Returns:
        The XML string corresponding to the list of generators.
    """
    # Convert the generators to an array in list
    genXML = ""
    for gen in generators:
        if gen.is_async != 0:
            raise Exception("Async generator not yet supported.")
        # Convert the sub-parts of the generator
        targetXML = expr2srcml.convertExpr(gen.target)
        forXML    = expr2srcml.convertExpr(gen.iter)
        ifXML = ""
        for condition in gen.ifs:
            ifXML += expr2srcml.convertExpr(condition)
        # Combine the generators into an XML
        # genXML += XML.form("block", targetXML, forXML, ifXML)
        genXML += XML.form("block", targetXML + forXML + ifXML)
    
    return genXML


def convertGenExp(stmt: ast.GeneratorExp) -> str:
    """Helper method to convert a generator expression to srcML XML.
    This method is called from expr2srcml.py script. The generator
    expression is currently handled in a manner similar to 
    list comprehension.

    Arguments:
        stmt: The generator expression to be converted to srcML XML.

    Returns:
        The srcML XML string for the given generator expression.
    """
    # GeneratorExp(expr elt, comprehension* generators)
    # comprehension = (expr target, expr iter, expr* ifs, int is_async)
    eltXML = expr2srcml.convertExpr(stmt.elt)
    # Convert the generators to an array in list
    genXML = convertGenerators(stmt.generators)
    # Combine the XML fragments together
    return eltXML + XML.form("operator", "=") + genXML


def convertDict(dict: ast.Dict) -> str:
    """Helper method to convert a dictionary initialization to corresponding
    srcML XML.

    Arguments:
        dict: The dictionary initialization list consisting of a list of
        key-value pairs.

    Returns:
        The srcML XML string for the given dictionary initialization.
    """
    # Dict(expr* keys, expr* values)
    # class Dict(expr):
    #     keys: typing.List[Optional[expr]]
    #     values: typing.List[expr]
    #
    dictXML = "["
    for (key, val) in zip(dict.keys, dict.values):
        dictXML += XML.form("expr", expr2srcml.convertExpr(key) + " = " +\
            expr2srcml.convertExpr(val))
    dictXML += "]"
    return XML.form("block", dictXML)


# End of source code
