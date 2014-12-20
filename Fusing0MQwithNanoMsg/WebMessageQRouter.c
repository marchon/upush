////////////////////////////////////////////////////////
/// (c) 2014. My-Classes.com
/// Basic version of fusing the ZMQ raw ROUTER (frontend) socket and NanoMsg REQ-REP (backend) sockets.
///
/// Read More at:
/// http://my-classes.com/2014/04/26/combining-zeromq-and-nanomsg-for-serving-web-requests/
///
///////////////////////////////////////////////////////
#include "czmq.h"
#include "nn.h"
#include "reqrep.h"
 
#define WORKER_SOCKET_ADDRESS "inproc://test"
 
void* nano_worker(void* args)
{
        int rc;
        int workerSock;
        char request[4096];
        char response[] = "HTTP / 1.0 200 OK\r\nContent - Type: text / plain\r\n\r\nHello World!!";
        int nResponseLen = strlen(response);
 
        workerSock = nn_socket(AF_SP, NN_REP);
        assert(workerSock >= 0);
        nn_bind(workerSock, WORKER_SOCKET_ADDRESS);
        int i = 0;
        while (1)
        {
                rc = nn_recv(workerSock, request, sizeof (request), 0);
                assert(rc >= 0);
 
                rc = nn_send(workerSock, response, nResponseLen+1, 0);
                assert(rc >= 0);
        }
}
 
int main(void)
{
        zctx_t *ctx = zctx_new();
        void *router = zsocket_new(ctx, ZMQ_ROUTER);
        zsocket_set_router_raw(router, 1);
        zsocket_set_sndhwm(router, 0);
        zsocket_set_rcvhwm(router, 0);
        int rc = zsocket_bind(router, "tcp://*:8080");
        assert(rc != -1);
 
        zthread_new(nano_worker, NULL);
 
        int sock = nn_socket(AF_SP, NN_REQ);
        assert(sock >= 0);
        assert(nn_connect(sock, WORKER_SOCKET_ADDRESS) >= 0);
 
        while (true)
        {
                //  Get HTTP request
                zframe_t *identity = zframe_recv(router);
                if (!identity) break;          //  Ctrl-C interrupt
                char *request = zstr_recv(router);
                {
                        // forward the http-request to NanoMsg
                        int bytes = nn_send(sock, request, strlen(request), 0);
                        assert(bytes >= 0);
                }
                free(request);     // free the memory
 
                // read the response from NanoMsg worker
                char* response = NULL;
                int bytes = nn_recv(sock, &response, NN_MSG, 0);
                assert(bytes >= 0);
                {
                        //  Send response to client/browser
                        zframe_send(&identity, router, ZFRAME_MORE + ZFRAME_REUSE);
                        zstr_send(router, response);
 
                        //  Close connection to browser
                        zframe_send(&identity, router, ZFRAME_MORE);
                        zmq_send(router, NULL, 0, 0);
                }
                nn_freemsg(response); // free the memory
        }
        zctx_destroy(&ctx);
        return 0;
}
