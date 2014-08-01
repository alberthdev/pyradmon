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

Usage
------
Sound excited? Let's make it work!

First, move the dummymp directory out of PyRadmon, as necessary.
If you are using PyRadmon, you can just use the copy in the PyRadmon 
library directly.

Your program needs to be structured like this:

    for/while loop:
    ....[queue functions to run]
    
    [queue functions to run out-of-loop if necessary]
    
    [process queue loop] OR [process queue block]

Here's a simple example. (Taken partly from `__init__.py`.)
Read the comments!

```python
    import logging
    import random
    
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
        
        dummymp.run(test, [])
        dummymp.run(test, [])
        dummymp.run(test, [])
        
        # Set some configuration options...
        
        # Set the number of processes DummyMP can use, max
        dummymp.set_max_processes(2)
        
        # Set the priority mode, or how much consideration DummyMP
        # should have regarding other processes and their CPU usage
        # when spawning processes
        dummymp.set_priority_mode(dummymp.DUMMYMP_NUCLEAR)
        
        # Now actually run the functions - block until done!
        process_until_done()
        
        # Get the return values from your function calls
        print get_returns()
        
        # Reset state!
        print "Resetting..."
        reset()
        
        # Queue again...
        run(test, [])
        run(test, [])
        run(test, [])
        
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
        reset()
        
        # This time, let's demo stopping a running process!
        
        # Set the number of processes DummyMP can use to 1
        set_max_processes(1)
        
        # Queue again...
        run(test, [])
        run(test, [])
        run(test, [])
        
        # We run this once to start one process.
        process_process()
        
        # Wait two seconds...
        time.sleep(2)
        
        # ...and reset!
        # This should produce a single log message, the only message
        # that came out of the function process. Note that returns are
        # lost after a reset. Run killall() instead if you want to
        # preserve any returns! (Functions that haven't finished running
        # will not have any returns.)
        reset()
        
        # This shouldn't do anything.
        process_until_done()
```
