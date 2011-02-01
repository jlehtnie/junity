import os.path
import re
import junity.base as base


class Pretty(object):

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

    VERDICTS = {
        'fail': base.TestVerdict.FAILURE,
        'failure': base.TestVerdict.FAILURE,
        'pass': base.TestVerdict.SUCCESS,
        'success': base.TestVerdict.SUCCESS,
        None: base.TestVerdict.SUCCESS
    }


class PrettyFormatHandler(base.FormatHandler):

    class State:
        def __init__(self):
            self.test_suites = []
            self.test_suite = None

    def accept(self, path, text):
        return Pretty.ACCEPT.search(text) is not None

    def read(self, path, text):
        state = PrettyFormatHandler.State()
        for line in text.splitlines():
            self.read_line(path, line, state)
        return base.TestSuites(state.test_suites)

    def read_line(self, path, line, state):
        match = Pretty.TEST_SUITE.match(line)
        if match:
            self.read_test_suite(path, match, state)
            return
        match = Pretty.TEST_CASE.match(line)
        if match:
            self.read_test_case(path, match, state)
            return
        match = Pretty.TEST_SUITE_ERROR.match(line)
        if match:
            self.read_test_suite_error(path, match, state)
            return
        if Pretty.EMPTY_LINE.match(line):
            return
        raise PrettyFormatHandlerError(path, "This pretty-printed test " +
            "report contains a line that does now follow the expected " +
            "format: \"" + str(line) + "\".")

    def read_test_suite(self, path, match, state):
        name = match.group('name')
        state.test_suite = base.TestSuite(name)
        state.test_suites.append(state.test_suite)

    def read_test_suite_error(self, path, match, state):
        message = match.group('message')
        test_suite_error = base.TestSuiteError(message)
        if state.test_suite is None:
            raise PrettyFormatHandlerError(path, "This pretty-printed test " +
                "report contains a test suite error outside a test suite.")
        state.test_suite.append(test_suite_error)

    def read_test_case(self, path, match, state):
        name = match.group('name')
        verdict = self.read_verdict(path, match)
        test_case = base.TestCase(name, verdict)
        if state.test_suite is None:
            raise PrettyFormatHandlerError(path, "This pretty-printed test " +
                "report contains a test case outside a test suite.")
        state.test_suite.append(test_case)

    def read_verdict(self, path, match):
        verdict = match.group('verdict')
        return Pretty.VERDICTS.get(verdict, base.TestVerdict.ERROR)


class PrettyFormatHandlerError(base.FormatHandlerError):

    def __init__(self, path, message):
        base.FormatHandlerError.__init__(self, path, message)
