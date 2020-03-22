# Async IO

Asyncio is a concurrency library to write `concurrent code` using the `async/await` syntax. This is basically used for asynchronous programming. 
Asyncio is often a perfect fit for IO-bound and high-level structured network code.

Example: Think about a scenario where you have a page to load with different images hosted in different servers and the first image to load big. 
Now, if we do things synchronously, then loading the webpage will stuck for a long time while loading the first image (because of its size and 
also it takes time to communicate with server over the network). Instead, if we do the loading asynchronously (that is, start the image loading first
but don't sit in there for the response) then other images and elements are going to load while there is latency in I/O of loading the big image.

##### Thread: 
A Thread is the segment of a process. Every process has atleast one thread. Furthermore, a process can have multiple threads and these multiple threads 
are contained within a process and could be running simultaneously in a multi core CPU. But, on a single processing machine, threads are timesliced and
preempted (switched between) which makes them concurrent. A Thread have 3 states: `Running`, `Ready`, and `Blocked`.

* It is termed as a `lightweight process`, since it is similar to a real process but executes within the context of a process and shares the same 
resources allotted to the process by the kernel
* All the threads running within a process share the same address space including memory, file descriptors, stack and other process related attributes
* Creating new threads and communicating between them is more efficient, because threads share the same address space of the process

##### Process:
A Process is the `execution of a program`. By executing a program, you can perform necessary actions specified in the program. A `Process` can create 
other processes which are called `Child Processes`.

* Creation of each process requires separate system calls for each process
* Process execution is isolated means it does not share memory with any other process
* Process uses the IPC (Inter-Process Communication) mechanism for communication
* A Process has it's own address space, a call stack and link to any resources needed by that process

##### Concurrency: 

`Concurrency` is the ability to execute more than one task at the same time. They take advantage of CPU time-slicing feature of OS where each task run 
part of its task and then go to waiting state. When first task is in waiting state, CPU is assigned to second task to complete it’s part of task. 
The concept is similar to parallel processing, but with the possibility of many independent jobs doing different things at once rather than executing 
the same job. For example,

1. Browsing a blog on a web browser and listen to music on a media player, at the same time
2. Editing a document on a word processor, while other applications can download files from the internet, at the same time

`Concurrency` doesn’t necessarily involve multiple applications. Running multiple parts of a single application simultaneously is also termed as 
concurrency. For example,

1. A word processor formats the text and responds to keyboard events, at the same time
2. A web server, which is essentially a program running on a computer, serves thousands of requests from all over the world, at the same time

Concurrency doesn’t imply parallel execution. During concurrency, the tasks are executed in an `interleaved` manner. The OS switches between the 
tasks so frequently that it appears to the users that they are being executed parallely.

* Multi-processing: Multiple Processors/CPUs are executing concurrently. 
* Multi-tasking: Multiple tasks/processes are running concurrently on a single CPU. The OS manages these tasks.
* Multi-threading: Multiple parts (threads) of the same program running concurrently.

##### Parallelism:
Parallelism is when an application splits a task into smaller subtasks which are actually being processed in parallel in a different CPU core.

##### Coroutines:
The word `coroutine` is composed of two words: `co` (cooperative) and `routines` (functions). Coroutines are functions that are cooperative.

Usually, when a function calls a second function, the first cannot continue until the second function finishes and returns to where it was called. 
The control remains with the second function until it executes completely and only then can the control return to the first one.

Coroutines are functions where the control is transferred from one function to the other function in a way that the exit point from the first function
and the entry point to the second function are remembered – without changing the context. Thus, each function remembers where it left the execution 
and where it should resume from.

##### Asynchronous: 
An asynchronous method call is normally used for a process that needs to do work away from the current application and we don't want to wait and 
block our application awaiting the response.

#### Requirements
```
aiohttp==3.6.2
aiofiles==0.4.0
```

#### Resources:
1. [Guru99 - Difference between process and thread](https://www.guru99.com/difference-between-process-and-thread.html)
2. [Geeksforgeeks - Difference between process and thread](https://www.geeksforgeeks.org/difference-between-process-and-thread/)
3. [Java concurrency multithreading basics](https://www.callicoder.com/java-concurrency-multithreading-basics/)
4. [SO - difference between a process and a thread](https://stackoverflow.com/questions/200469/what-is-the-difference-between-a-process-and-a-thread?page=1#answer-2477945)
5. [SO - What is the difference between concurrency, parallelism and asynchronous methods?](https://stackoverflow.com/questions/4844637/what-is-the-difference-between-concurrency-parallelism-and-asynchronous-methods)
6. [Explain coroutines like im five](https://dev.to/thibmaek/explain-coroutines-like-im-five-2d9)
7. [What is a coroutine](https://www.educative.io/edpresso/what-is-a-coroutine)
8. [Geeksforgeeks - Coroutine in python](https://www.geeksforgeeks.org/coroutine-in-python/)