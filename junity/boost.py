import junity.base as base


class BoostFormatHandler(base.FormatHandler):

    ERROR_MESSAGE="This Boost test report does not follow the expected " \
                  "format. Use --report_format=xml and " \
                  "--report_level=detailed."

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
            raise base.FormatHandlerError(path,
                                          BoostFormatHandler.ERROR_MESSAGE)
        return test_suite

    def read_test_case(self, path, element):
        name = element.getAttribute("name")
        verdict = self.read_test_verdict(path, element)
        test_case = base.TestCase(name, verdict)
        return test_case

    def read_test_verdict(self, path, element):
        result = element.getAttribute("result")
        if result == "passed":
            verdict = base.TestVerdict.SUCCESS
        elif result == "failed":
            verdict = base.TestVerdict.FAILURE
        elif result == "aborted":
            verdict = base.TestVerdict.ERROR
        else:
            raise base.FormatHandlerError(path,
                                          BoostFormatHandler.ERROR_MESSAGE)
        return verdict
