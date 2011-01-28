assert_equal()
{
    TITLE=$1
    FILE1=$2
    FILE2=$3

    echo -n "$TITLE: "
    diff $FILE1 $FILE2 > /dev/null 2>&1
    if [ $? == 0 ]
    then
        echo "pass"
    else
        echo "fail"
    fi
}

test_stderr()
{
    TITLE=$1
    COMMAND=$2
    MESSAGE=$3

    RECEIVED="lib0.tmp"
    EXPECTED="lib1.tmp"

    echo "$MESSAGE" > $EXPECTED
    $COMMAND 2> $RECEIVED
    assert_equal "$TITLE" "$RECEIVED" "$EXPECTED"
    rm -f $EXPECTED $RECEIVED
}

test_stdout()
{
    TITLE=$1
    COMMAND=$2
    EXPECTED=$3

    RECEIVED="lib2.tmp"

    $COMMAND > $RECEIVED
    assert_equal "$TITLE" "$RECEIVED" "$EXPECTED"
    rm -f $RECEIVED
}
