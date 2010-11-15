import junity.base as base


class JUnitFormatHandler(base.FormatHandler):

    def accept(self, path, text):
        return text.find("<testcase") != -1

    def read(self, path, text):
        document = base.parse_xml(path, text)
        test_suites = base.TestSuites()
        for element in document.getElementsByTagName("testsuite"):
            test_suites.append(self.read_test_suite(path, element))
        return test_suites

    def read_test_suite(self, path, element):
        name = element.getAttribute("name")
        test_suite = base.TestSuite(name)
        for element in element.getElementsByTagName("testcase"):
            test_suite.append(self.read_test_case(path, element))
        return test_suite

    def read_test_case(self, path, element):
        name = element.getAttribute("name")
        verdict = self.read_test_verdict(path, element)
        test_case = base.TestCase(name, verdict)
        return test_case

    def read_test_verdict(self, path, element):
        if len(element.getElementsByTagName("error")) > 0:
            verdict = base.TestVerdict.ERROR
        elif len(element.getElementsByTagName("failure")) > 0:
            verdict = base.TestVerdict.FAILURE
        else:
            verdict = base.TestVerdict.SUCCESS
        return verdict
