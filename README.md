JUnity
======

JUnity converts and merges test reports into a single JUnit test report.


Testing
-------

Testing of JUnity involves generation of Boost and JUnit test reports.

Boost test reports require C++ compiler and Boost Test Library. The compiler
must be able to access the Boost headers and the linker the Boost libraries.
If they are in non-standard locations and GCC is in use, the environment
variables `CPLUS_INCLUDE_PATH` and `LIBRARY_PATH` can be used.

JUnit test reports require Java, Ant and JUnit. The JUnit JAR must be in the
`CLASSPATH` environment variable.

License
-------

See `LICENSE`.

