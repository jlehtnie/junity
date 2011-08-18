import os.path
import re
from . import base


class Titan(object):

    VERDICT = re.compile(r"""
        Test\ case\ 
        (?P<testcase>[^\ ]+)\ 
        finished.\ 
        Verdict:\ 
        (?P<verdict>[a-z]+)
        """, re.VERBOSE)

    VERDICTS = {
        'fail': base.TestVerdict.FAILURE,
        'none': base.TestVerdict.FAILURE,
        'pass': base.TestVerdict.SUCCESS
    }


class TitanFormatHandler(base.FormatHandler):

    def accept(self, path, text):
        return text.find("TESTCASE") != -1

    def read(self, path, text):
        test_suite = base.TestSuite(os.path.basename(path))
        matches = Titan.VERDICT.findall(text)
        for match in matches:
            test_suite.append(self.read_test_case(path, match))
        if len(test_suite.children) == 0:
            raise TitanFormatHandlerError(path)
        return base.TestSuites([ test_suite ])

    def read_test_case(self, path, match):
        name = match[0]
        verdict = Titan.VERDICTS.get(match[1], base.TestVerdict.ERROR)
        test_case = base.TestCase(name, verdict)
        return test_case


class TitanFormatHandlerError(base.FormatHandlerError):

    MESSAGE = "This TITAN log file appears to contain no test cases."

    def __init__(self, path):
        base.FormatHandlerError.__init__(self, path,
            TitanFormatHandlerError.MESSAGE)
