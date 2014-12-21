# Nanomsg: ZeroMQ done right

---
# What is Nanomsg
# How does it relate to 0MQ
# How do I use Nanomsg

# What do I need to know to get started?

## nanomessage will change the way you think about sockets / connections
and message routing.

What nanomsg calles a socket is a communications pipeline that is establishes a connection that can communicate with the core in a protocol agnostic way.

The "Socket" might be a TCP connection, a IPC connection or a INPROC connection.
 You can use the defined message channels to route messages between different communications systems.

Each base class has two channels
### one side to speak to either a transport or protocol-specific
derived class
### the other side communicates directly with the core

each of the baseclasses exposes two interfaces.

nn_sockbase, nn_epbase and nn_pipebase

are used to communicate with the derived classes
(i.e. specific transports and protocols).

These same base classes are used in the core to internally route messages
nn_sock, nn_ep and nn_pipe are used for internal communication inside the core.


The structure of Nanomsg

Transports (the way that data is moved to creators or from consumers of messages)
----
inproc
ipc
tcp



Connections to the Core of Nanomsg are made with Transports

##These Transports can connect to the core via 2 internal communications layers

Transport consists endpoint objects (there's a base class nn_ep in the core to derive all endpoints from) and pipe objects (derive it from nn_pipebase core object).
Pipe is an object that consumes and produces messages. It may correspond to e.g. TCP connection, but you are free to implement it in any way you like (reading/writing data to file, console, whatever).


## endpoints are defined by either *bind* or *connect*
### bind is for receiving messages
### connect is for sending messages


Endpoint is what is created when nn_bind or nn_connect is called. It isn't necessarily a connection. For example, when you bind socket to a TCP port, endpoint "tcp://eth0:5555" is created, but there's no connection yet.

## nn_ep (subclassed from nn_epbase)

## nn_pipe (subclassed from nn_pipebase)


#  Transport tests

#  Protocol Summary

  * (pair)

   ![Pair Protocol](http://www.bravenewgeek.com/wp-content/uploads/2014/06/pair.png "Pair")

   * One-to-one protocol. Socket for communication with exactly
        one peer. Each party can send messages at any time. If the
        peer is not available or send buffer is full subsequent
        to 'send' will block until it's possible to send the
        message.


  * (pubsub)

   ![Pair Protocol](http://www.bravenewgeek.com/wp-content/uploads/2014/06/pubsub.png "Pair")

     * PUBLISH
        * Publish/subscribe protocol. This socket is used to
    distribute messages to multiple destinations. Receive
    operation is not defined.
     * SUBSCRIBE
       * Publish/subscribe protocol. Receives messages from the
    publisher. Only messages that the socket is subscribed to are
    received. When the socket is created there are no
    subscriptions and thus no messages will be received. Send
    operation is not defined on this socket
  * (reqrep)

  ![Pair Protocol](http://www.bravenewgeek.com/wp-content/uploads/2014/06/reqrep.png "Pair")

    * REQUEST
      * Request/reply protocol. Used to implement the
      stateless worker that receives requests and sends replies.
    * REPLY
      * Request/reply protocol. Used to implement the client
      application that sends requests and receives replies.
  * (pipeline)

  ![Pair Protocol](http://www.bravenewgeek.com/wp-content/uploads/2014/06/pipeline.png)

  PIPELINE provides unidirectional dataflow which is useful for creating load-balanced processing pipelines. A producer node submits work that is distributed among consumer nodes.

    * Push
      * This socket is used to send messages to
      a cluster of load-balanced nodes. Receive operation is not
      implemented on this socket type.
    * Pull
      * This socket is used to receive a message from a
      cluster of nodes. Send operation is not implemented on this
      socket type.


  * (bus)  (Many-to-Many Communication)

      ![Bus Protocol](  http://www.bravenewgeek.com/wp-content/uploads/2014/06/bus.png)

      BUS allows messages sent from each peer to be delivered to every other peer in the group.


  * (survey) (Ask Group a Question)

  ![Bus Protocol]( http://www.bravenewgeek.com/wp-content/uploads/2014/06/survey.png)

  The last scalability protocol, and the one in which I will further examine by implementing a use case with, is SURVEY. The SURVEY pattern is similar to PUBSUB in that a message from one node is broadcasted to the entire group, but where it differs is that each node in the group responds to the message. This opens up a wide variety of applications because it allows you to quickly and easily query the state of a large number of systems in one go. The survey respondents must respond within a time window configured by the surveyor.



#  Feature tests.
  * (block)
  * (term)
  * (timeo)
  * (iovec)
  * (msg)
  * (prio)
  * (poll)
  * (device)
  * (emfile)
  * (domain)
  * (trie)
  * (list)
  * (hash)
  * (symbol)
  * (separation)
  * (zerocopy)
  * (shutdown)
  * (cmsg)
