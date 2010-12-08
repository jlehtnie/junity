CXX ?= g++
LD := $(CXX)

TEST_DIR = test

ANT_BUILDFILE := $(TEST_DIR)/build.xml

ANT ?= ant
ANTFLAGS := -buildfile $(ANT_BUILDFILE) -logfile /dev/null -quiet

BOOST_DIR := $(TEST_DIR)/boost
BOOST_REPORT := $(BOOST_DIR)/ExampleTest.xml
BOOST_OBJS := $(BOOST_DIR)/ExampleTest.o
BOOST_LIBS := -lboost_unit_test_framework
BOOST_PROG := $(BOOST_DIR)/ExampleTest
BOOST_OPTS := --log_level=nothing \
              --report_format=xml \
              --report_level=detailed \
              --report_sink=$(BOOST_REPORT) \
              --result_code=no

BOOST_REPORT2 := $(BOOST_DIR)/boost-report-level.xml
BOOST_OPTS2 := --log_level=nothing \
               --report_format=xml \
               --report_sink=$(BOOST_REPORT2) \
               --result_code=no

BOOST_REPORT3 := $(BOOST_DIR)/boost-test-log.xml
BOOST_OPTS3 := --log_level=all \
               --log_format=xml \
               --log_sink=$(BOOST_REPORT3) \
               --result_code=no

JUNIT_DIR := $(TEST_DIR)/junit
JUNIT_REPORT := $(JUNIT_DIR)/ExampleTest.xml

E := @echo
Q := @

all: test

clean:
	$(E) "  CLEAN     "
	$(Q) rm -fr build 
	$(Q) find . -name *.pyc | xargs rm -f
	$(Q) rm -f $(BOOST_OBJS) $(BOOST_PROG) $(BOOST_REPORT) $(BOOST_REPORT2)
	$(Q) $(ANT) $(ANTFLAGS) clean

test: $(BOOST_REPORT) $(BOOST_REPORT2) $(BOOST_REPORT3) $(JUNIT_REPORT)
	$(E) "  TEST      "
	$(Q) $(TEST_DIR)/suite.sh

$(BOOST_REPORT): $(BOOST_PROG)
	$(E) "  GENERATE  " $@
	$(Q) $(BOOST_PROG) $(BOOST_OPTS)

$(BOOST_REPORT2): $(BOOST_PROG)
	$(E) "  GENERATE  " $@
	$(Q) $(BOOST_PROG) $(BOOST_OPTS2)

$(BOOST_REPORT3): $(BOOST_PROG)
	$(E) "  GENERATE  " $@
	$(Q) $(BOOST_PROG) $(BOOST_OPTS3) > /dev/null 2>&1

$(BOOST_PROG): $(BOOST_OBJS)
	$(E) "  LINK      " $@
	$(Q) $(LD) $(LDFLAGS) $(BOOST_LIBS) -o $@ $<

%.o: %.cpp
	$(E) "  COMPILE   " $@
	$(Q) $(CXX) $(CXXFLAGS) -c -o $@ $<

$(JUNIT_REPORT):
	$(E) "  GENERATE  " $@
	$(Q) $(ANT) $(ANTFLAGS) test

.PHONY: all clean test
