Feature: TITAN

  Scenario: Test report
    When I run "bin/junity test/titan/TitanTest.log"
    Then the standard output should equal
      """
      <testsuites>
        <testsuite name="TitanTest.log">
          <testcase name="testNone">
            <failure />
          </testcase>
          <testcase name="testPass" />
          <testcase name="testInconc">
            <error />
          </testcase>
          <testcase name="testFail">
            <failure />
          </testcase>
          <testcase name="testError">
            <error />
          </testcase>
        </testsuite>
      </testsuites>
      """
    And the return code should equal 0
