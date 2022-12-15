#!/bin/bash

# This is a simple shell scrip that is used to test the operation of
# py2srcml Python program on the CLCDSA (https://github.com/Kawser-nerd/CLCDSA)
# data set. Specifically, we are using the source codes in the 'AtCoder' and 
# 'CodeJamData' directories in the CLCDSA repositories.

# This script is meant to be used in the following manner:
#    1. First unzip the AtCoder and CodeJamData zip files.
#    2. Run this script via the following bash command line on a GNU machine:
#       $ ./assess_py2srcml.sh AtCoder
#
#    NOTE: The script prints a summary of number of source files successfully
#          converted to srcML format. Detailed logs are printed to a file named
#          py2srcml_log.txt

# Setup path to py2srcml.py script
PY2SRCML="../../py2srcml.py"

# This function is used to recursively assess files in a given directory
#    $1: A directory to be processed
#    Returns statistics from this method
function assessDir() {
    # Create an alias to improve readability
    local dir="$1"
    local dirStats=(0 0)
    # Process any sub-directories first
    ls -d ${dir}/*/ 2> /dev/null > /dev/null
    if [ $? -eq 0 ]; then
        for subdir in `ls -d ${dir}/*/`;
        do
            # Recursively process the files in the subdirectory
            local subDirStats=( `assessDir "${subdir}"` )
            dirStats[0]=$(( dirStats[0] + subDirStats[0] ))
            dirStats[1]=$(( dirStats[1] + subDirStats[1] ))
        done
    fi

    # Process the source files in the currect working directory
    ls -1 ${dir}/*.py > /dev/null 2> /dev/null
    if [ $? -eq 0 ]; then
        for pySrc in `ls -1 ${dir}/*.py`;
        do
            # Track the number of source files in this directory
            (( dirStats[0]++ ))
            # Process the source file and update directory stats
            echo "${pySrc}" >> py2srcml_log.txt
            "${PY2SRCML}" "${pySrc}" > /dev/null 2>> py2srcml_log.txt
            if [ $? -eq 0 ]; then
                (( dirStats[1]++ ))
            fi
        done
    fi
    # Print the statistics for this directory
    >&2 echo -e "${dirStats[0]}\t${dirStats[1]}\t${dir}"
    # Return the stats back to the caller
    echo -e "${dirStats[0]}\t${dirStats[1]}\t${dir}"
    return 0
}

# The main function
#   $*: The main function 
function main() {
    echo -e "#Files\t#Pass\tDir"
    for dir in $*;
    do
        local ret=`assessDir "${dir}"`
    done
}

# Start the main function
main $*

# End of script
