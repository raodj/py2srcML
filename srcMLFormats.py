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

# This file just contains some of the fixed format strings that are
# used to generate srcML from a given Python string.

START_UNIT:str = '<unit xmlns="http://www.srcML.org/srcML/src" '\
                   'xmlns:py="http://www.srcML.org/srcML/cpp" '\
                   'revision="1.0.0" language="Python3" '\
                   'filename="{}">'

END_UNIT:str = '</unit>  <!-- {} -->';

# End of source code
