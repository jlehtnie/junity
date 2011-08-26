Feature: Boost

  Scenario: Test report
    When I run "make test/boost/ExampleTest.xml"
    And I run "bin/junity test/boost/ExampleTest.xml"
    Then the standard output should equal
      """
      <testsuites>
        <testsuite name="ExampleTest">
          <testcase name="testSuccess" />
          <testcase name="testFailure">
            <failure />
          </testcase>
          <testcase name="testError">
            <error />
          </testcase>
        </testsuite>
      </testsuites>
      """
    And the return code should equal 0

  Scenario: Report level other than detailed
    When I run "make test/boost/boost-report-level.xml"
    And I run "bin/junity test/boost/boost-report-level.xml"
    Then the standard output should equal
      """
      <testsuites>
        <testsuite name="boost-report-level.xml">
          <error message="This Boost test report does not follow
            the expected format. Use --report_format=xml and
            --report_level=detailed." />
        </testsuite>
      </testsuites>
      """
    And the return code should equal 0

  Scenario: Test log
    When I run "make test/boost/boost-test-log.xml"
    And I run "bin/junity test/boost/boost-test-log.xml"
    Then the standard output should equal
      """
      <testsuites>
        <testsuite name="boost-test-log.xml">
          <error message="This Boost test report does not follow
            the expected format. Use --report_format=xml and
            --report_level=detailed." />
        </testsuite>
      </testsuites>
      """
    And the return code should equal 0
