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

import ast
import sys
import typing

import srcMLFormats
import stmt2srcml

def convertModule(module: ast.Module) -> None:
    """Helper method to generate srcML for a given module. A module
    consists of many functions.
    """
    print(stmt2srcml.convertBlock(module.body))

    # print("<block>:<block_content>")
    # Process each statement in the module 
    # for stmt in module.body:
    #     print(stmt2srcml.convertStmt(stmt))
    # Finish the XML for the module
    # print("</block_content></block>")

def convert(pySrcPath: str) -> None:
    """Top-level method that performs the generation of srcML from a 
    given Python source file.
    
    Arguments:
        pySrcPath: Path to the python source file to be processed
    """
    # Open the specified source file.
    srcFile = open(pySrcPath, "r")
    if not srcFile.readable():
        raise IOError("Unable to read from {}".format(pySrcPath))
    # Now that the file is valid, let's parse it with Python's ast
    srcAST: ast.Module = ast.parse(srcFile.read())
    # Now, let's process the body of the top-level module
    print(srcMLFormats.START_UNIT.format(pySrcPath))
    convertModule(srcAST)
    print(srcMLFormats.END_UNIT.format(pySrcPath))

def main():
    """The main function that starts the process of XML generation
    by calling suitable helper methods.
    
    It uses command line arguments. Each command-line argument
    is assumed to be a python program to be converted to
    srcML.
    """
    # If we don't have command-line arguments, then report an error
    if len(sys.argv) < 2:
        print("Specify python source file as command-line argument.")
    else:
        # Process each source file specified as command-line argument
        for pySrcPath in sys.argv[1:]:
            # print("Converting {}".format(pySrcPath))
            convert(pySrcPath)

# The top-level script.
if __name__ == "__main__":
    main()
