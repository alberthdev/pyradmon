DummyMP Library
================

Introduction
-------------
DummyMP is a really smart but simple ("for dummies") library for
running functions in parallel.

Features include:
 * Dead-simple API
 * Intelligent queuing of tasks based on CPU usage and configuration
 * Multiprocess logging (with standard logging module) - you can log 
   from your function without blowing up anything!
 * Access to function returns
 * Options controlling overall task priority
 * Option for limiting the number of CPUs used by DummyMP
 * Ability to terminate all processes at once
 * Ability to reset DummyMP state (for a "fresh start")

Requirements
-------------
You need the following:
 * Python 2.6+ (but not 3.x... yet)
   * Python 2.6+ is a MUST - the important multiprocessing module only
     exists from Python 2.6 and onward!
 * psutil 2.x+ - https://github.com/giampaolo/psutil

Usage
------
Sounds exciting? Let's make it work!

First, move the dummymp directory out of PyRadmon, as necessary.
If you are using PyRadmon, you can just use the copy in the PyRadmon 
library directly.

Your program needs to be structured like this:

    for/while loop:
    ....[queue functions to run]
    
    [queue functions to run out-of-loop if necessary]
    
    [process queue loop] OR [process queue block]

Somewhat confused? Basically, in plain English:
  1. Add the functions you want to run, with their arguments. The syntax
     is very similar to running an actual function - just slightly
     different. This does NOT run the function immediately, but instead
     queues it for execution.
  2. Run DummyMP's processing function(s). By "processing", we mean the
     functions to actually execute your functions in a new process, and
     communicate with your process to faciliate logging, store function
     value returns, and clean up finished processes.

Here's a simple example. (Taken partly from `__init__.py`.)
Read the comments!

```python
    import logging
    import random
    import time
    
    import dummymp
    # OR: from pyradmon import dummymp
    
    # Just a test function.
    def test():
        for i in xrange(0, 10000000):
            pass
        logging.info("Hi there from logging!")
        num = random.randint(2,7)
        logging.info("Sleeping for %i secs..." % num)
        time.sleep(num)
        if num > 5:
            logging.info("Returning the random number %i!" % num)
        logging.info("Bye bye from logging!")
        if num > 5:
            return num
    
    if __name__ == "__main__":
        # This is optional, but running this before processing may help
        # speed things up.
        dummymp.getCPUAvail()
        
        # Now queue! This is similar to calling the function.
        # 
        # Running the function:
        #   my_func(my_arg1, my_arg2)
        # Queuing the function with DummyMP:
        #   dummymp.run(my_func, [my_arg1, my_arg2])
        # 
        # dummymp.run() does not return anything.
        # 
        # If you are expecting your function to return something, use
        # dummymp.get_returns(). This returns a dictionary with your
        # function's return values - see below for more details.
        # 
        # Note: while queuing, it may be a good idea to run
        # dummymp.process_process() inbetween calls, e.g.
        #  dummymp.run(test, [])
        #  dummymp.process_process()
        #  dummymp.run(test, [])
        #  dummymp.process_process()
        # 
        # This is what is used in PyRadmon. It doesn't save a lot - we
        # tested and determind that it saves 0.1-1.5 seconds based on
        # light to moderate workloads - but if your workload increases
        # significantly, this may help!
        
        dummymp.run(test, [])
        dummymp.run(test, [])
        dummymp.run(test, [])
        
        # Set some configuration options...
        
        # Set the number of processes
        # (or CPUs, 1 process = 1 processor/CPU) DummyMP can use, max
        dummymp.set_max_processes(2)
        
        # Set the priority mode, or how much consideration DummyMP
        # should have regarding other processes and their CPU usage
        # when spawning processes.
        # Available modes:
        #   dummymp.DUMMYMP_GENEROUS
        #   dummymp.DUMMYMP_NORMAL
        #   dummymp.DUMMYMP_AGGRESSIVE
        #   dummymp.DUMMYMP_EXTREME
        #   dummymp.DUMMYMP_NUCLEAR
        # For more details, see ./pyradmon.py --help or
        # the help text for set_priority_mode(mode) in source file
        # dummymp/interface.py.
        dummymp.set_priority_mode(dummymp.DUMMYMP_NUCLEAR)
        
        # Now actually run the functions - block until done!
        dummymp.process_until_done()
        
        # Get the return values from your function calls.
        # This returns a dict, with keys being the zero-indexed order
        # in which you called each function.
        # So dummymp.get_returns()[0] for the first run call,
        # dummymp.get_returns()[1] for the second run call, etc.
        print dummymp.get_returns()
        
        # Reset state!
        print "Resetting..."
        dummymp.reset()
        
        # Queue again...
        dummymp.run(test, [])
        dummymp.run(test, [])
        dummymp.run(test, [])
        
        # You can also use a loop to run and process the functions!
        # When all processes are done, dummymp.process_process() will
        # return True. Otherwise, it returns False.
        while not dummymp.process_process():
            # Process the inter-process queue - this processes/handles
            # any logging messages, function returns, or process
            # completions.
            dummymp.process_queue()
            time.sleep(0.001)
        
        # Let's reset again!
        print "Resetting once more..."
        dummymp.reset()
        
        # This time, let's demo stopping a running process!
        
        # Set the number of processes DummyMP can use to 1
        dummymp.set_max_processes(1)
        
        # Queue again...
        dummymp.run(test, [])
        dummymp.run(test, [])
        dummymp.run(test, [])
        
        # We run this once to start one process.
        dummymp.process_process()
        
        # Wait two seconds...
        time.sleep(2)
        
        # ...and reset!
        # This should produce a single log message, the only message
        # that came out of the function process. Note that returns are
        # lost after a reset. Run killall() instead if you want to
        # preserve any returns! (Functions that haven't finished running
        # will not have any returns.)
        dummymp.reset()
        
        # This shouldn't do anything.
        dummymp.process_until_done()
```
