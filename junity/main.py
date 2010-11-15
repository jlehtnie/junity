import getopt
import os.path
import sys
import junity.base as base
import junity.boost as boost
import junity.junit as junit
import junity.titan as titan


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

    try:
        opts, args = getopt.getopt(sys.argv[1:], "o:")
        for opt, arg in opts:
            if opt == "-o":
                output = arg
    except getopt.GetoptError:
        usage()

    if len(args) == 0:
        usage()
    
    handlers = [ boost.BoostFormatHandler(),
                 junit.JUnitFormatHandler(),
                 titan.TitanFormatHandler() ]

    test_suites = read_output(output, handlers)
    for arg in args:
        try:
            test_suites.extend(handle(arg, handlers))
        except base.FormatHandlerError, error:
            test_suites.extend(error.format())
    write_output(output, test_suites)


def read(path):
    infile = None
    try:
        infile = open(path, "r")
        return infile.read()
    except:
        return None
    finally:
        if infile is not None:
            infile.close()


def read_output(path, handlers):
    if not path or not os.path.exists(path):
        return base.TestSuites()
    return handle(path, handlers)


def write(path, text):
    outfile = None
    try:
        outfile = open(path, "w")
        outfile.write(text)
    except:
        die("")
    finally:
        if outfile is not None:
            outfile.close()


def write_output(path, test_suites):
    text = test_suites.to_xml()
    if path is not None:
        write(path, text + "\n")
    else:
        print text


def usage():
    sys.exit("Usage: junity.py [-o FILE] FILE [FILE ...]")
