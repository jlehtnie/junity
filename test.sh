#!/bin/sh

RECEIVED="temp.xml"

check()
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

check "foo" "examples/cannot-read-file.xml"
check "Makefile" "examples/unknown-file-format.xml"
check "junity/main.py" "examples/bad-file-format.xml"
check "test/boost/ExampleTest.xml" "examples/ExampleTest.xml"
check "test/boost/boost-report-level.xml" "examples/boost-report-level.xml"
check "test/boost/boost-test-log.xml" "examples/boost-test-log.xml"
check "test/junit/ExampleTest.xml" "examples/ExampleTest.xml"
check "test/titan/TitanTest.log" "examples/TitanTest.xml"
check "test/boost/ExampleTest.xml test/boost/ExampleTest.xml" \
    "examples/ExampleTest-ExampleTest.xml"
