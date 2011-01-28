import junity.base as base


class BoostFormatHandler(base.FormatHandler):

    ERROR = "This Boost test report does not follow the expected format. " \
        "Use --report_format=xml and --report_level=detailed."

    VERDICTS = {
        "aborted": base.TestVerdict.ERROR,
        "failed": base.TestVerdict.FAILURE,
        "passed": base.TestVerdict.SUCCESS
    }

    def accept(self, path, text):
        return text.find("<TestSuite") != -1

    def read(self, path, text):
        document = base.parse_xml(path, text)
        test_suites = base.TestSuites()
        for element in document.getElementsByTagName("TestSuite"):
            try:
                test_suites.append(self.read_test_suite(path, element))
            except base.FormatHandlerError, error:
                test_suites.extend(error.format())
        return test_suites

    def read_test_suite(self, path, element):
        name = element.getAttribute("name")
        test_suite = base.TestSuite(name)
        for element in element.getElementsByTagName("TestCase"):
            test_suite.append(self.read_test_case(path, element))
        if len(test_suite.children) == 0:
            raise base.FormatHandlerError(path, BoostFormatHandler.ERROR)
        return test_suite

    def read_test_case(self, path, element):
        name = element.getAttribute("name")
        verdict = self.read_test_verdict(path, element)
        test_case = base.TestCase(name, verdict)
        return test_case

    def read_test_verdict(self, path, element):
        result = element.getAttribute("result")
        verdict = BoostFormatHandler.VERDICTS.get(result)
        if verdict is None:
            raise base.FormatHandlerError(path, BoostFormatHandler.ERROR)
        return verdict
