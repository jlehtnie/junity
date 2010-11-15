import os.path
import re
import junity.base as base


class TitanFormatHandler(base.FormatHandler):

    VERDICT = re.compile(r"""
                          Test\ case\ 
                          (?P<testcase>[^\ ]+)\ 
                          finished.\ 
                          Verdict:\ 
                          (?P<verdict>[a-z]+)
                          """, re.VERBOSE)
    
    def accept(self, path, text):
        return text.find("TESTCASE") != -1

    def read(self, path, text):
        test_suite = base.TestSuite(os.path.basename(path))
        matches = TitanFormatHandler.VERDICT.findall(text)
        for match in matches:
            test_suite.append(self.read_test_case(path, match))
        if len(test_suite.children) == 0:
            raise base.FormatHandlerError(path, "This TITAN log file appears "
                                                "to contain no test cases.")
        return base.TestSuites([ test_suite ])

    def read_test_case(self, path, match):
        name = match[0]
        verdict = match[1]
        if verdict == "none":
            verdict = base.TestVerdict.FAILURE
        elif verdict == "pass":
            verdict = base.TestVerdict.SUCCESS
        elif verdict == "inconc":
            verdict = base.TestVerdict.ERROR
        elif verdict == "fail":
            verdict = base.TestVerdict.FAILURE
        else:
            verdict = base.TestVerdict.ERROR
        test_case = base.TestCase(name, verdict)
        return test_case
