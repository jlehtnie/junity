import getopt
import os.path
import sys
import junity.base as base
from junity.boost import BoostFormatHandler
from junity.junit import JUnitFormatHandler
from junity.pretty import PrettyFormatHandler
from junity.titan import TitanFormatHandler


def die(path, message):
    sys.exit(os.path.basename(path) + ": " + message)


def handle(path, handlers):
    text = read(path)
    if text is None:
        raise base.FormatHandlerError(path, "This file cannot be read.")
    return handle_text(path, handlers, text)


def handle_text(path, handlers, text):
    for handler in handlers:
        if handler.accept(path, text):
            return handler.read(path, text)
    raise base.FormatHandlerError(path, "This file has unknown format.")


def main():
    output = None
    pretty = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], "o:p")
        for opt, arg in opts:
            if opt == "-o":
                output = arg
            if opt == "-p":
                pretty = True
    except getopt.GetoptError:
        usage()

    if len(args) == 0 and output is None:
        usage()
    
    handlers = [ BoostFormatHandler(),
                 JUnitFormatHandler(),
                 TitanFormatHandler(),
                 PrettyFormatHandler() ]

    test_suites = read_output(output, handlers)
    for arg in args:
        try:
            test_suites.extend(handle(arg, handlers))
        except base.FormatHandlerError, error:
            test_suites.extend(error.format())
    write_output(output, test_suites, pretty)


def read(path):
    try:
        with open(path, "r") as infile:
            return infile.read()
    except:
        return None


def read_output(path, handlers):
    test_suites = base.TestSuites()
    if path is not None and os.path.exists(path):
        try:
            test_suites.extend(handle(path, handlers))
        except base.FormatHandlerError, error:
            die(path, "cannot read file")
    return test_suites


def write(path, text):
    try:
        with open(path, "w") as outfile:
            outfile.write(text)
    except:
        die(path, "cannot write file")


def write_output(path, test_suites, pretty):
    text = test_suites.to_pretty() if pretty else test_suites.to_xml()
    if path is not None:
        write(path, text + "\n")
    else:
        print text


def usage():
    sys.exit("Usage: junity [-o FILE] [-p] [FILE ...]")
