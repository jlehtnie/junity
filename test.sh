#!/bin/sh

RECEIVED="temp.xml"

assert_equal()
{
    FILE1=$1
    FILE2=$2

    diff $FILE1 $FILE2 > /dev/null 2>&1
    if [ $? == 0 ]
    then
        echo "pass"
    else
        echo "fail"
    fi
}

assert_file_equal1()
{
    ARGS=$1
    EXPECTED=$2

    write_to_file $ARGS
    assert_equal $RECEIVED $EXPECTED
    tear_down
}

assert_file_equal2()
{
    ARGS1=$1
    ARGS2=$2
    EXPECTED=$3

    write_to_file $ARGS1
    write_to_file $ARGS2
    assert_equal $RECEIVED $EXPECTED
    tear_down
}

assert_stdout_equal()
{
    ARGS=$1
    EXPECTED=$2

    direct_to_file $ARGS
    assert_equal $RECEIVED $EXPECTED
    tear_down
}

direct_to_file()
{
    ARGS=$*
    
    bin/junity $ARGS > $RECEIVED
}

tear_down()
{
    rm -f $RECEIVED
}

write_to_file()
{
    ARGS=$*
    
    bin/junity -o $RECEIVED $ARGS
}

assert_stdout_equal "foo" "examples/cannot-read-file.xml"
assert_stdout_equal "Makefile" "examples/unknown-file-format.xml"
assert_stdout_equal "junity/junit.py" "examples/bad-file-format.xml"
assert_stdout_equal "test/boost/ExampleTest.xml" "examples/ExampleTest.xml"
assert_stdout_equal "test/boost/boost-report-level.xml" \
    "examples/boost-report-level.xml"
assert_stdout_equal "test/boost/boost-test-log.xml" \
    "examples/boost-test-log.xml"
assert_stdout_equal "test/junit/ExampleTest.xml" "examples/ExampleTest.xml"
assert_stdout_equal "test/titan/TitanTest.log" "examples/TitanTest.xml"
assert_stdout_equal "test/boost/ExampleTest.xml test/boost/ExampleTest.xml" \
    "examples/ExampleTest-ExampleTest.xml"
assert_file_equal1 "test/boost/ExampleTest.xml" "examples/ExampleTest.xml"
assert_file_equal2 "test/boost/ExampleTest.xml" "test/boost/ExampleTest.xml" \
    "examples/ExampleTest-ExampleTest.xml"

