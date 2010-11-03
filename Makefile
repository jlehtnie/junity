LD := $(CXX)

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

E := @echo
Q := @

all: test

test: $(BOOST_REPORT)
	$(E) "  TEST      "
	$(Q) ./test.sh

clean:
	rm -f $(BOOST_OBJS) $(BOOST_PROG) $(BOOST_REPORT)

$(BOOST_REPORT): $(BOOST_PROG)
	$(E) "  GENERATE  " $@
	$(Q) $(BOOST_PROG) $(BOOST_OPTS)

$(BOOST_PROG): $(BOOST_OBJS)
	$(E) "  LINK      " $@
	$(Q) $(LD) $(LDFLAGS) $(BOOST_LIBS) -o $@ $<

%.o: %.cpp
	$(E) "  COMPILE   " $@
	$(Q) $(CXX) $(CXXFLAGS) -c -o $@ $<

.PHONY: all clean test

