import os
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

@Then("the standard output should equal")
def stdout_should_equal(stdout):
    assert_equal(normalize(stdout), normalize(scc.stdout))

@Then("the return code should equal (\d+)")
def return_code_should_equal(return_code):
    assert_equal(int(return_code), scc.process.returncode)

def normalize(xml):
    tree = ElementTree.XML(xml)
    for elem in tree.iter():
        elem.text = elem.text.strip() if elem.text is not None else None
        elem.tail = elem.tail.strip() if elem.tail is not None else None
    return ElementTree.tostring(tree)
