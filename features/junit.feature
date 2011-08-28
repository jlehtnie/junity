Feature: JUnit

  Scenario: Test report
    When I run "make test/junit/ExampleTest.xml"
    And I run "bin/junity test/junit/ExampleTest.xml"
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
