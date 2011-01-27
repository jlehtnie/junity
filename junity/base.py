import os.path
import xml.dom.minidom


class TestVerdict(object):
    SUCCESS = 0
    FAILURE = 1
    ERROR = 2


class TestCase(object):

    def __init__(self, name, verdict):
        self.name = name
        self.verdict = verdict

    def to_pretty(self):
        p = ""
        p += "- " + self.name
        if self.verdict == TestVerdict.ERROR:
            p += ": error"
        if self.verdict == TestVerdict.FAILURE:
            p += ": failure"
        p += "\n"
        return p

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

    def to_pretty(self):
        p = ""
        p += "- Error: " + self.message + "\n"
        return p

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

    def to_pretty(self):
        p = ""
        p += self.name + "\n"
        for child in self.children:
            p += child.to_pretty()
        return p

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

    def to_pretty(self):
        p = ""
        for test_suite in self.test_suites:
            p += test_suite.to_pretty() + "\n"
        return p.rstrip()

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


def get_children_by_tag_name(element, name):
    return filter(lambda x: x.parentNode is element,
        element.getElementsByTagName(name))
