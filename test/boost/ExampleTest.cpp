#define BOOST_TEST_DYN_LINK
#define BOOST_TEST_MODULE ExampleTest
#include <boost/test/unit_test.hpp>

BOOST_AUTO_TEST_CASE(testSuccess)
{
    BOOST_CHECK(true);
}

BOOST_AUTO_TEST_CASE(testFailure)
{
    BOOST_CHECK(false);
}

