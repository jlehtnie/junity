import os.path
import sys
import junity.base as base
import junity.boost as boost
import junity.junit as junit
import junity.titan as titan


def handle(path, handlers):
    try:
        text = open(path).read()
    except:
        raise base.FormatHandlerError(path, "This file cannot be read.")

    for handler in handlers:
        if handler.accept(path, text):
            return handler.read(path, text)

    raise base.FormatHandlerError(path, "This file has unknown format.")


def main():
    if len(sys.argv) < 2:
        usage()

    handlers = [ boost.BoostFormatHandler(),
                 junit.JUnitFormatHandler(),
                 titan.TitanFormatHandler() ]

    test_suites = base.TestSuites()
    for arg in sys.argv[1:]:
        try:
            test_suites.extend(handle(arg, handlers))
        except base.FormatHandlerError, error:
            test_suites.extend(error.format())
    print test_suites


def usage():
    sys.exit("Usage: junity.py FILE [FILE ...]")
