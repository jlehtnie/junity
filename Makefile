CXX ?= g++
LD := $(CXX)

ANT ?= ant
ANTFLAGS := -logfile /dev/null -quiet

BOOST_DIR := test/boost
BOOST_REPORT := $(BOOST_DIR)/ExampleTest.xml
BOOST_OBJS := $(BOOST_DIR)/ExampleTest.o
BOOST_LIBS := -lboost_unit_test_framework
BOOST_PROG := $(BOOST_DIR)/ExampleTest
BOOST_OPTS := --log_level=nothing \
              --report_format=xml \
              --report_level=detailed \
              --report_sink=$(BOOST_REPORT) \
              --result_code=no

BOOST_REPORT2 := $(BOOST_DIR)/boost_report_level.xml
BOOST_OPTS2 := --log_level=nothing \
               --report_format=xml \
               --report_sink=$(BOOST_REPORT2) \
               --result_code=no

JUNIT_DIR := test/junit
JUNIT_REPORT := $(JUNIT_DIR)/ExampleTest.xml

E := @echo
Q := @

all: test

test: $(BOOST_REPORT) $(BOOST_REPORT2) $(JUNIT_REPORT)
	$(E) "  TEST      "
	$(Q) ./test.sh

clean:
	$(E) "  CLEAN     "
	$(Q) rm -f $(BOOST_OBJS) $(BOOST_PROG) $(BOOST_REPORT) $(BOOST_REPORT2)
	$(Q) $(ANT) $(ANTFLAGS) clean

$(BOOST_REPORT): $(BOOST_PROG)
	$(E) "  GENERATE  " $@
	$(Q) $(BOOST_PROG) $(BOOST_OPTS)

$(BOOST_REPORT2): $(BOOST_PROG)
	$(E) "  GENERATE  " $@
	$(Q) $(BOOST_PROG) $(BOOST_OPTS2)

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
