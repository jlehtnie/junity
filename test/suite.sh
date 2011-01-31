#!/bin/sh

source lib.sh

JUNITY="../bin/junity"

test_stdout \
    "File that cannot be read results in a test suite error        " \
    "$JUNITY foo" \
    "../examples/cannot-read-file.xml"

test_stdout \
    "Unknown file format results in a test suite error             " \
    "$JUNITY ../Makefile" \
    "../examples/unknown-file-format.xml"

test_stdout \
    "Bad file format results in a test suite error                 " \
    "$JUNITY ../junity/junit.py" \
    "../examples/bad-file-format.xml"

test_stdout \
    "Test suite errors in input files are preserved                " \
    "$JUNITY ../examples/cannot-read-file.xml" \
    "../examples/cannot-read-file.xml"

test_stdout \
    "Boost test report is a supported input format                 " \
    "$JUNITY boost/ExampleTest.xml" \
    "../examples/ExampleTest.xml"

test_stdout \
    "Boost test report level must be detailed                      " \
    "$JUNITY boost/boost-report-level.xml" \
    "../examples/boost-report-level.xml"

test_stdout \
    "Boost test log results in a test suite error                  " \
    "$JUNITY boost/boost-test-log.xml" \
    "../examples/boost-test-log.xml"

test_stdout \
    "JUnit test report is a supported input format                 " \
    "$JUNITY junit/ExampleTest.xml" \
    "../examples/ExampleTest.xml"

test_stdout \
    "TITAN log file is a supported input format                    " \
    "$JUNITY titan/TitanTest.log" \
    "../examples/TitanTest.xml"

test_stdout \
    "Multiple test reports result in a combined test report        " \
    "$JUNITY boost/ExampleTest.xml boost/ExampleTest.xml" \
    "../examples/ExampleTest-ExampleTest.xml"

test_stdout \
    "Pretty-print is a supported output format                     " \
    "$JUNITY -p ../examples/ExampleTest.xml" \
    "../examples/ExampleTest.txt"

test_stdout \
    "Pretty-print is a supported input format                      " \
    "$JUNITY ../examples/ExampleTest.txt" \
    "../examples/ExampleTest.xml"

test_stdout \
    "Test suite errors can be written to pretty-print              " \
    "$JUNITY -p foo" \
    "../examples/cannot-read-file.txt"

test_stdout \
    "Test suite errors can be read from pretty-print               " \
    "$JUNITY ../examples/cannot-read-file.txt" \
    "../examples/cannot-read-file.xml"

test_stdout \
    "Multiple test reports can be read from pretty-print           " \
    "$JUNITY ../examples/ExampleTest-ExampleTest.txt" \
    "../examples/ExampleTest-ExampleTest.xml"

test_stdout \
    "Multiple test reports can be written to pretty-print          " \
    "$JUNITY -p boost/ExampleTest.xml boost/ExampleTest.xml" \
    "../examples/ExampleTest-ExampleTest.txt"

READONLY_FILE="../examples/cannot-write-file.xml"
chmod u-w $READONLY_FILE

test_stderr \
    "File that cannot be written results in program termination    " \
    "$JUNITY -o $READONLY_FILE ../examples/ExampleTest.xml" \
    "`basename $READONLY_FILE`: cannot write file"

chmod u+w $READONLY_FILE

TEMP_FILE="suite.tmp"
$JUNITY -o $TEMP_FILE boost/ExampleTest.xml junit/ExampleTest.xml

test_stdout \
    "Output can be directed to an output file                      " \
    "cat $TEMP_FILE" \
    "../examples/ExampleTest-ExampleTest.xml"

cp -f junit/ExampleTest.xml $TEMP_FILE
$JUNITY -o $TEMP_FILE boost/ExampleTest.xml

test_stdout \
    "Input is appended to the output file                          " \
    "cat $TEMP_FILE" \
    "../examples/ExampleTest-ExampleTest.xml"

cp -f boost/ExampleTest.xml $TEMP_FILE
$JUNITY -o $TEMP_FILE

test_stdout \
    "Output file is converted to JUnit test report format          " \
    "cat $TEMP_FILE" \
    "../examples/ExampleTest.xml"

echo "<testsuite" > $TEMP_FILE

test_stderr \
    "Bad file format in output file results in program termination " \
    "$JUNITY -o $TEMP_FILE" \
    "`basename $TEMP_FILE`: cannot read file"

rm -f $TEMP_FILE
