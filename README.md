# py2srcML

py2srcML is a program that takes python source code and labels it with srcML style XML tags

To learn more about srcML, visit their website: [srcML.org](http://www.srcml.org/)

### How it works
---
The [ast](https://docs.python.org/3/library/ast.html) module from The Python Standard Library is used to generate an abstract syntax tree of the orginial code. 
At this point, any source code with invalid synatx will cause the program to throw an error.
Each node of the syntax tree is translated into srcML style XML through helper methods.

### Running the script
---
The script is written in Python3 and Python3 must be installed for the script to run.

The script can be called as an executeable or through the python interpreter. 
In both cases, the filepath of python source code must be passed as an argument.

`./py2srcml.py tests/simple.py `

`python3 py2srcml.py tests/simple.py`


To learn more about testing the program on directories of code, see the [README](/benchmarks/clcdsa/README.md) in /benchmarks.
