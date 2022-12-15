# Benchmarking Py2SrcML

This folder contains source code used by the CLCDSA project. We use
the same subset of source code for benchmarking the py2srcml script.
The objective is to see if the program is able to convert python
programs to srcML.  **Note that this script only tests if the
conversion works but does not validate that the generated srcML is
correct.**

The assess_py2srcml.sh is a simple shell scrip that is used to test
the operation of py2srcml Python program on the CLCDSA
(https://github.com/Kawser-nerd/CLCDSA) data set. Specifically, we are
using the source codes in the 'AtCoder' and 'CodeJamData' directories
in the CLCDSA repositories.

This script is meant to be used in the following manner:
   1. First unzip the AtCoder and CodeJamData zip files.
   2. Run this script via the following bash command line on a GNU machine:
      > $ ./assess_py2srcml.sh AtCoder

## NOTE on operation of the above command

The script prints a summary of number of source files successfully
converted to srcML format. Detailed logs are printed to a file named
py2srcml_log.txt
