import os.path
import re
import junity.base as base


class PrettyFormatHandler(base.FormatHandler):

    class State:
        def __init__(self):
            self.test_suites = []
            self.test_suite = None

    ACCEPT = re.compile(r"^[!-] ", re.MULTILINE)

    EMPTY_LINE = re.compile(r"^\s*$")

    TEST_CASE = re.compile(r"""
                           ^
                           -\ 
                           (?P<name>[^:]+)
                           (
                           :\ 
                           (?P<verdict>\w+)
                           )?
                           $
                           """, re.VERBOSE)

    TEST_SUITE = re.compile(r"""
                            ^
                            (?P<name>[^!-].*)
                            $
                            """, re.VERBOSE)

    TEST_SUITE_ERROR = re.compile(r"""
                                  ^
                                  !\ 
                                  (?P<message>.*)
                                  $
                                  """, re.VERBOSE)

    def accept(self, path, text):
        return self.ACCEPT.search(text) is not None

    def read(self, path, text):
        state = self.State()
        for line in text.splitlines():
            self.read_line(path, line, state)
        return base.TestSuites(state.test_suites)

    def read_line(self, path, line, state):
        match = self.TEST_SUITE.match(line)
        if match:
            self.read_test_suite(path, match, state)
            return
        match = self.TEST_CASE.match(line)
        if match:
            self.read_test_case(path, match, state)
            return
        match = self.TEST_SUITE_ERROR.match(line)
        if match:
            self.read_test_suite_error(path, match, state)
            return
        if self.EMPTY_LINE.match(line):
            return
        raise base.FormatHandlerError(path, "This pretty-printed test " +
                                      "report contains a line that does " +
                                      "not follow the expected format: \"" +
                                      str(line) + "\".")

    def read_test_suite(self, path, match, state):
        name = match.group("name")
        state.test_suite = base.TestSuite(name)
        state.test_suites.append(state.test_suite)

    def read_test_suite_error(self, path, match, state):
        message = match.group("message")
        test_suite_error = base.TestSuiteError(message)
        if state.test_suite is None:
            raise base.FormatHandlerError(path, "This pretty-printed test " +
                                          "report contains a test suite " +
                                          "error outside a test suite.")
        state.test_suite.append(test_suite_error)

    def read_test_case(self, path, match, state):
        name = match.group("name")
        verdict = self.read_verdict(path, match)
        test_case = base.TestCase(name, verdict)
        if state.test_suite is None:
            raise base.FormatHandlerError(path, "This pretty-printed test " +
                                          "report contains a test case " +
                                          "outside a test suite.")
        state.test_suite.append(test_case)

    def read_verdict(self, path, match):
        verdict = match.group("verdict")
        if verdict in (None, "success", "pass"):
            return base.TestVerdict.SUCCESS
        elif verdict in ("failure", "fail"):
            return base.TestVerdict.FAILURE
        elif verdict == "error":
            return base.TestVerdict.ERROR
        raise base.FormatHandlerError(path, "This pretty-printed test " +
                                      "report contains an unexpected " +
                                      "verdict: \"" + str(verdict) + "\".")
