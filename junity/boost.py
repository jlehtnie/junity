from . import base


class Boost(object):

    VERDICTS = {
        'aborted': base.TestVerdict.ERROR,
        'failed': base.TestVerdict.FAILURE,
        'passed': base.TestVerdict.SUCCESS
    }


class BoostFormatHandler(base.FormatHandler):

    def accept(self, path, text):
        return text.find("<TestSuite") != -1

    def read(self, path, text):
        document = base.parse_xml(path, text)
        test_suites = base.TestSuites()
        for element in document.getElementsByTagName('TestSuite'):
            try:
                test_suites.append(self.read_test_suite(path, element))
            except base.FormatHandlerError, error:
                test_suites.extend(error.format())
        return test_suites

    def read_test_suite(self, path, element):
        name = element.getAttribute('name')
        test_suite = base.TestSuite(name)
        for element in element.getElementsByTagName('TestCase'):
            test_suite.append(self.read_test_case(path, element))
        if len(test_suite.children) == 0:
            raise BoostFormatHandlerError(path)
        return test_suite

    def read_test_case(self, path, element):
        name = element.getAttribute('name')
        verdict = self.read_test_verdict(path, element)
        test_case = base.TestCase(name, verdict)
        return test_case

    def read_test_verdict(self, path, element):
        result = element.getAttribute('result')
        verdict = Boost.VERDICTS.get(result)
        if verdict is None:
            raise BoostFormatHandlerError(path)
        return verdict


class BoostFormatHandlerError(base.FormatHandlerError):

    MESSAGE = "This Boost test report does not follow the expected format. " \
        "Use --report_format=xml and --report_level=detailed."

    def __init__(self, path):
        base.FormatHandlerError.__init__(self, path,
            BoostFormatHandlerError.MESSAGE)
