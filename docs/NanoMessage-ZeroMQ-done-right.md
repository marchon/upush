# Nanomsg: ZeroMQ done right

---
## whoami

Haïkel Guémar

Fedora Packager since 2006

Senior Software Engineer @ SysFera

---

# Nanomsg

---
## Few facts

* Written by Martin Sustrik (co-creator of ZeroMQ)

* MIT licensed

* Release 0.1 alpha (20 august 2013)

* Release 0.2 alpha (25 september 2013)

---
## A bite of history

* iMatix: a company run by Pieter Hintjens
* iMatix created AMQP as a contractor for JP Morgan
* AMQP == centralized broker
* iMatix left the AMQP standard committee due to disagreement
* In reaction to AMQP, they created AMQP

---
## ZeroMQ

* Networking library
* But acts as a concurrency framework (Actor oriented)
* Various transports: in-process, inter-process, tcp, pgm
* Various patterns (aka Protocols): fan-out, pub/sub, request/reply etc.
* Think *connected applications* fabric
* Ease creating scaling applications
* LGPLv3 

---
## Zen of Zero

Zero

* broker
* latency (best effort)
* administration
* cost
* waste

---
## A friendly fork

Sustrik wanted:

* standardize ZeroMQ network protocol
* integration with Linux kernel
* move to MIT license

No drama, few jokes and encouragements from both sides

---
## Crossroads I/O

* Technically a (compatible) fork of ZeroMQ
* It failed but Sustrik learnt a lot

---
## Nanomsg

* A reboot of ZeroMQ

---
# Why Nanomsg (and Not ZeroMQ ?)

---
## Advantages

* Aims POSIX full-compliance

* Written in C

* API for integrating new protocols and transports

* command-line tools (nanocat)

---
## Goodbye context !

    !c
    /* with zeromq */
    void *ctx = zmq_ctx_new ();
    void *s = zmq_socket (ctx, ZMQ_PUSH);
    zmq_connect (s, "tcp://192.168.0.111:5555");
    zmq_send (s, "ABC", 3, 0);
    zmq_close (s);
    zmq_ctx_destroy (ctx);
    /* with nanomsg */
    int s = nn_msg(AF_SP, NN_PUSH);
    nn_connect(s, "tcp://192.168.0.111:5555");
    nn_send(s, "ABC", 3, 0);
    nn_close(s);  /* attention, appel désormais bloquant */

---
## Performances and safety ?

* In C
* Use intrusive containers instead of STL
* Use IOCP on Windows
* Level-triggered polling
* Objects are no more tied to a thread
* Interactions are now associated to state machines
* Asynchronous DNS calls

---
## Remember, i told you so !

<img src="img/grin_small.jpg" width="60%" />

---
## Really zero-copy

    !c
    void *buf = nn_allocmsg(12, 0);
    memcpy(buf, "Hello world!", 12);
    nn_send(s, &buf, NN_MSG, 0);
    nn_recv(s, &buf, NN_MSG, 0);
    nn_freemsg(buf);

---
## nanocat

* command line tool for testing and debugging purpose
* provides many symlinks to simplify user interface
* supports msgpack


---
## Nanocat (sample)

    !bash
    # server-side
    nanocat --rep --bind tcp://127.0.0.1:8000 --format ascii --data pong
    # client side
    nanocat --req --connect tcp://127.0.0.1:8000 --format ascii --data ping

---
## Nanocat (sample)

   !bash 
   nanocat --pub --connect tcp://darthsidious --data "My liege !" --interval 10

---
# Protocol

---
## Pair Protocol

<img src="img/pair.png" class="fixdiv" />

---
## Pair Protocol (client)

    !c
    int sock = nn_socket(AF_SP, NN_PAIR);
    nn_connect(sock, url);
    nn_send(sock, "hello", 6, 0);
    char *buf = NULL;
    int result = nn_recv(sock, &buf, NN_MSG, 0);
    nn_freemsg(buf);
    nn_shutdown(sock, 0);

---
## Pair Protocol (server)

    !c
    int sock = nn_socket(AF_SP, NN_PAIR);
    nn_bind(sock, url);
    char *buf = NULL;
    int result = nn_recv(sock, &buf, NN_MSG, 0);
    nn_freemsg(buf);
    nn_send(sock, "kthxbye", 8, 0);
    nn_shutdown(sock, 0);


---
## Request/Reply Protocol

<img src="img/reqrep.png" class="fixdiv" />

---
## Request/Reply Protocol (client)

    !c
    int sz_msg = strlen(msg) + 1;
    int sock = nn_socket(AF_SP, NN_REQ);
    nn_connect(sock, url);
    int bytes = nn_send(sock, msg, sz_msg, 0);
    nn_shutdown(sock, 0);

---
## Request/Reply Protocol (server)

    !c
    int sock = nn_socket(AF_SP, NN_REP);
    nn_bind(sock, url);
    while (1) {
      char *buf = NULL;
      int bytes = nn_recv(sock, &buf, NN_MSG, 0);
      nn_freemsg(buf);
    }

---
## Pipeline Protocol

<img src="img/pipeline.png" class="fixdiv" />

---
## Pipeline Protocol (client)

    !c
    int sz_msg = strlen(msg) + 1;
    int sock = nn_socket(AF_SP, NN_PUSH);
    nn_connect(sock, url);
    int bytes = nn_send(sock, msg, sz_msg, 0);
    nn_shutdown(sock, 0);

---
## Pipeline Protocol (server)

    !c
    int sock = nn_socket(AF_SP, NN_PULL);
    nn_bind(sock, url);
    while (1) {
      char *buf = NULL;
      int bytes = nn_recv(sock, &buf, NN_MSG, 0);
      nn_freemsg(buf);
    }

---
## Survey Protocol

<img src="img/survey1.png" class="fixdiv" />

---
## Survey Protocol

<img src="img/survey2.png" class="fixdiv" />

---
## Survey Protocol

* NN_SURVEYOR
* NN_RESPONDENT

---
## Bus Protocol

<img src="img/bus1.png" class="fixdiv" />

---
## Bus Protocol

<img src="img/bus2.png" class="fixdiv" />

---
## Bus Protocol

* NN_BUS
* All nodes receive messages (except the sender !)
* scales well on a single machine or LAN

---
## A lot of bindings

Choose your weapons, cowboy !

C++, Go, Java, node.js, lua/luajit, .Net, OCaml, Perl, PHP, Python, Ruby, Rust

---
## Why keep using ZeroMQ ?

* nanomsg is very young (not production ready)
* ZeroMQ has an impressive documentation (and its own O'Reilly book)
* ZeroMQ is good *enough*
* Incompatible wire protocols (does not implement ZMTP/1.0 and 2.0)


---
# Q/A