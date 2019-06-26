#### What is an asynchronous framework ? 
A different programming paradigm that offers high concurrency with low overhead for context switching.

##### Traditional Sequential Models
* Code is evaluated sequentially from top to bottom
* Sequential code evaluation, while very readable can cause waste of compute time
* What happens when your code makes a blocking request ( SQL query, HTTP request ) ? What are the implications of the GIL here ? 
    * Solutions - Multiprocessing, gevent, tornado, twisted, threading .. 
* Sequential execution and effects on the stack 
* Variable scoping and context
    -> DEMO: example1.py 

##### Event Driven Frameworks 
* The crontab is an example of an event driven framework 
* How would you implement it as a python program ? 

#### Async Primitives
* Generators / Co-routines

    -> DEMO: example2.py,  ( Yield ) 
    -> DEMO: example3.py, example4.py, example5.py

    * Yield's work both ways!

* Can a generator / co-routine live on the stack ? 
    "The generator can be resumed at any time, from any function, because its stack frame is not actually on the stack: it is on the heap. 
     Its position in the call hierarchy is not fixed, and it need not obey the first-in, last-out order of execution that regular functions do. 
     It is liberated, floating free like a cloud."

* Sockets 
    * Interprocess communication is generally done through sockets.
    * "Everything is a file"
    * OS level hooks for events can trigger code execution

    -> DEMO: example6.py 

#### Putting it together
* What happens when you depart from the async paradigm ? 
    -> DEMO: example 8.py, async_request.py ( Performance )

    time seq 1 10 | xargs -I{} -P10 curl localhost:1234

* Am I in callback hell ? Co-routines to the rescue!
    -> DEMO example 9.py

    * Exception handling 

