import os
import re
import shlex
import subprocess

from freshen import *
from xml.etree import ElementTree


@When("I run \"([^\"]+)\"")
def run_command(command):
    args = shlex.split(command)
    scc.process = subprocess.Popen(args, stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    scc.stdout, scc.stderr = scc.process.communicate()

@Then("the standard error should equal")
def stderr_should_equal(stderr):
    assert_equal(normalize_text(stderr), normalize_text(scc.stderr))

@Then("the standard output should equal")
def stdout_should_equal(stdout):
    assert_equal(normalize_xml(stdout), normalize_xml(scc.stdout))

@Then("the return code should equal (\d+)")
def return_code_should_equal(return_code):
    assert_equal(int(return_code), scc.process.returncode)

@Then("the return code should not equal (\d+)")
def return_code_should_not_equal(return_code):
    assert_not_equal(int(return_code), scc.process.returncode)

def normalize_text(text):
    return text.strip()

def normalize_xml(xml):
    tree = ElementTree.XML(xml)
    for elem in tree.iter():
        elem.text = strip(elem.text) if elem.text is not None else None
        elem.tail = strip(elem.tail) if elem.tail is not None else None
        attrib = {}
        for name, value in elem.items():
            attrib[name] = strip(value)
        elem.attrib = attrib
    return ElementTree.tostring(tree)

def strip(text):
    return re.sub('\s+', ' ', text, 0, re.MULTILINE).strip()
