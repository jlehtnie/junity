JUnity
======

JUnity converts and merges test reports into a single JUnit test report. At
the moment JUnity has rudimentary support for Boost, JUnit and TITAN test
report formats.


Usage
-----

Given one or more input files, JUnity tries to interpret them as test reports
and produces a combined test report to standard output:

    junity results1.log results2.log results3.log > results.xml

JUnity is designed for continuous integration scripts. For reliability,
operational failures (such as unreadable input files) do not cause program
termination but are reported as test errors in the combined test report.

JUnity is primarily targeted towards the Hudson continuous integration server.


### Options

- `-o FILE`: Write combined test report to a file. If the file does not exist,
  JUnity will create it. If the file exists, JUnity interprets it as a test
  report.

- `-p`: Pretty-print the combined test report in a human-readable format
  instead of the JUnit test report format.


### Boost

JUnity reads Boost test reports in the XML format. Give the following command
line arguments to the executable:

    --report_format=xml
    --report_level=detailed


### TITAN

JUnity reads TITAN log files. The log message type `TESTCASE` must be active.


Installation
------------

Install the program with `setup.py`:

    python setup.py install


Development
-----------

To run the program from the repository, add the root of the working tree to
the `$PYTHONPATH` environment variable.

Run the regression test suite with `Makefile`:

    make test

The regression test suite generates Boost and JUnit test reports.

Boost test reports require C++ compiler and Boost Test Library. The compiler
must be able to access the Boost headers and the linker and the executable
the Boost libraries. If they are in non-standard locations and GCC is in use,
the environment variables `CPLUS_INCLUDE_PATH` and `LIBRARY_PATH` can be used.
Additionally, on GNU/Linux `LD_LIBRARY_PATH` and on Mac OS X
`DYLD_LIBRARY_PATH` should be set to `$LIBRARY_PATH`.

JUnit test reports require Java, Ant and JUnit. The JUnit JAR must be in the
`CLASSPATH` environment variable.

License
-------

See `LICENSE`.
