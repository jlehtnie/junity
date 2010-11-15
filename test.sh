#!/bin/sh

RECEIVED="temp.xml"

check_file()
{
    ARGS=$1
    EXPECTED=$2

    bin/junity -o $RECEIVED $ARGS

    diff $RECEIVED $EXPECTED > /dev/null 2>&1
    if [ $? == 0 ]
    then
        echo "pass"
    else
        echo "fail"
    fi

    rm -f $RECEIVED
}

check_stdout()
{
    ARGS=$1
    EXPECTED=$2

    bin/junity $ARGS > $RECEIVED

    diff $RECEIVED $EXPECTED > /dev/null 2>&1
    if [ $? == 0 ]
    then
        echo "pass"
    else
        echo "fail"
    fi

    rm -f $RECEIVED
}

check_stdout "foo" "examples/cannot-read-file.xml"
check_stdout "Makefile" "examples/unknown-file-format.xml"
check_stdout "junity/junit.py" "examples/bad-file-format.xml"
check_stdout "test/boost/ExampleTest.xml" "examples/ExampleTest.xml"
check_stdout "test/boost/boost-report-level.xml" \
    "examples/boost-report-level.xml"
check_stdout "test/boost/boost-test-log.xml" "examples/boost-test-log.xml"
check_stdout "test/junit/ExampleTest.xml" "examples/ExampleTest.xml"
check_stdout "test/titan/TitanTest.log" "examples/TitanTest.xml"
check_stdout "test/boost/ExampleTest.xml test/boost/ExampleTest.xml" \
    "examples/ExampleTest-ExampleTest.xml"
check_file "test/boost/ExampleTest.xml" "examples/ExampleTest.xml"

