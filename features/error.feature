Feature: Error handling

  Scenario: Cannot read file
    When I run "bin/junity foo"
    Then the standard output should equal
      """
      <testsuites>
        <testsuite name="foo">
          <error message="This file cannot be read." />
        </testsuite>
      </testsuites>
      """
    And the return code should equal 0

  Scenario: Unknown file format
    When I run "bin/junity Makefile"
    Then the standard output should equal
      """
      <testsuites>
        <testsuite name="Makefile">
          <error message="This file has unknown format." />
        </testsuite>
      </testsuites>
      """
    And the return code should equal 0

  Scenario: Bad file format
    When I run "bin/junity junity/junit.py"
    Then the standard output should equal
      """
      <testsuites>
        <testsuite name="junit.py">
          <error message="This XML file is not well-formed." />
        </testsuite>
      </testsuites>
      """
    And the return code should equal 0
