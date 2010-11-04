#!/usr/bin/env python


import os.path
import re
import sys
import xml.dom.minidom


class TestVerdict(object):
    SUCCESS = 0
    FAILURE = 1
    ERROR = 2


class TestCase(object):

    def __init__(self, name, verdict):
        self.name = name
        self.verdict = verdict

    def to_xml(self):
        x = ""
        x += "<testcase name=\"" + self.name + "\""
        if self.verdict == TestVerdict.ERROR:
            x += "><error /></testcase>"
        elif self.verdict == TestVerdict.FAILURE:
            x += "><failure /></testcase>"
        else:
            x += " />"
        return x

    def __str__(self):
        return self.to_xml()


class TestSuiteError(object):

    def __init__(self, message):
        self.message = message

    def to_xml(self):
        x = ""
        x += "<error message=\"" + self.message + "\" />"
        return x

    def __str__(self):
        return self.to_xml()


class TestSuite(object):

    def __init__(self, name):
        self.name = name
        self.children = [] # TestCase or TestSuiteError

    def append(self, child):
        self.children.append(child)

    def to_xml(self):
        x = ""
        x += "<testsuite name=\"" + self.name + "\">"
        for child in self.children:
            x += child.to_xml()
        x += "</testsuite>"
        return x

    def __str__(self):
        return self.to_xml()


class TestSuites(object):

    def __init__(self, test_suites = None):
        self.test_suites = [] if test_suites is None else test_suites

    def append(self, test_suite):
        self.test_suites.append(test_suite)

    def extend(self, test_suites):
        self.test_suites.extend(test_suites.test_suites)

    def to_xml(self):
        x = ""
        x += "<testsuites>"
        for test_suite in self.test_suites:
            x += test_suite.to_xml()
        x += "</testsuites>"
        return x

    def __str__(self):
        return self.to_xml()


class FormatHandler(object):

    def accept(self, path, text):
        raise NotImplementedError

    def read(self, path, text):
        raise NotImplementedError


class BoostFormatHandler(FormatHandler):

    def accept(self, path, text):
        return text.find("<TestSuite") != -1

    def read(self, path, text):
        document = parse_xml(path, text)
        test_suites = TestSuites()
        for element in document.getElementsByTagName("TestSuite"):
            try:
                test_suites.append(self.read_test_suite(path, element))
            except FormatHandlerError, error:
                test_suites.extend(error.format())
        return test_suites

    def read_test_suite(self, path, element):
        name = element.getAttribute("name")
        test_suite = TestSuite(name)
        for element in element.getElementsByTagName("TestCase"):
            test_suite.append(self.read_test_case(path, element))
        if len(test_suite.children) == 0:
            raise FormatHandlerError(path, "This Boost test suite appears "
                                           "to contain no test cases. Is "
                                           "--report_level=detailed used "
                                           "alongside --report_format=xml?")
        return test_suite

    def read_test_case(self, path, element):
        name = element.getAttribute("name")
        verdict = self.read_test_verdict(path, element)
        test_case = TestCase(name, verdict)
        return test_case

    def read_test_verdict(self, path, element):
        result = element.getAttribute("result")
        if result == "passed":
            verdict = TestVerdict.SUCCESS
        elif result == "failed":
            verdict = TestVerdict.FAILURE
        else:
            verdict = TestVerdict.ERROR
        return verdict


class JUnitFormatHandler(FormatHandler):

    def accept(self, path, text):
        return text.find("<testcase") != -1

    def read(self, path, text):
        document = parse_xml(path, text)
        test_suites = TestSuites()
        for element in document.getElementsByTagName("testsuite"):
            test_suites.append(self.read_test_suite(path, element))
        return test_suites

    def read_test_suite(self, path, element):
        name = element.getAttribute("name")
        test_suite = TestSuite(name)
        for element in element.getElementsByTagName("testcase"):
            test_suite.append(self.read_test_case(path, element))
        return test_suite

    def read_test_case(self, path, element):
        name = element.getAttribute("name")
        verdict = self.read_test_verdict(path, element)
        test_case = TestCase(name, verdict)
        return test_case

    def read_test_verdict(self, path, element):
        if len(element.getElementsByTagName("error")) > 0:
            verdict = TestVerdict.ERROR
        elif len(element.getElementsByTagName("failure")) > 0:
            verdict = TestVerdict.FAILURE
        else:
            verdict = TestVerdict.SUCCESS
        return verdict


class TitanFormatHandler(FormatHandler):

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
        test_suite = TestSuite(os.path.basename(path))
        matches = TitanFormatHandler.VERDICT.findall(text)
        for match in matches:
            test_suite.append(self.read_test_case(path, match))
        if len(test_suite.children) == 0:
            raise FormatHandlerError(path, "This TITAN log file appears to "
                                           "contain no test cases.")
        return TestSuites([ test_suite ])

    def read_test_case(self, path, match):
        name = match[0]
        verdict = match[1]
        if verdict == "none":
            verdict = TestVerdict.FAILURE
        elif verdict == "pass":
            verdict = TestVerdict.SUCCESS
        elif verdict == "inconc":
            verdict = TestVerdict.ERROR
        elif verdict == "fail":
            verdict = TestVerdict.FAILURE
        else:
            verdict = TestVerdict.ERROR
        test_case = TestCase(name, verdict)
        return test_case


HANDLERS = [ BoostFormatHandler(),
             JUnitFormatHandler(),
             TitanFormatHandler() ]


class FormatHandlerError(Exception):

    def __init__(self, path, message):
        self.test_suite = TestSuite(os.path.basename(path))
        self.test_suite.append(TestSuiteError(message))

    def format(self):
        return TestSuites([ self.test_suite ])


def parse_xml(path, text):
    try:
        return xml.dom.minidom.parseString(text)
    except:
        raise FormatHandlerError(path, "This XML file is not well-formed.")


def handle(path):
    try:
        text = open(path).read()
    except:
        raise FormatHandlerError(path, "This file cannot be read.")

    for handler in HANDLERS:
        if handler.accept(path, text):
            return handler.read(path, text)

    raise FormatHandlerError(path, "This file has unknown format.")


def main():
    if len(sys.argv) < 2:
        usage()

    test_suites = TestSuites()
    for arg in sys.argv[1:]:
        try:
            test_suites.extend(handle(arg))
        except FormatHandlerError, error:
            test_suites.extend(error.format())
    print test_suites


def usage():
    sys.exit("Usage: junity.py FILE [FILE ...]")


if __name__ == "__main__":
    main()
