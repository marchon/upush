from collections import defaultdict
import random
 
from nanomsg import NanoMsgAPIError
from nanomsg import Socket
from nanomsg import SURVEYOR
from nanomsg import SURVEYOR_DEADLINE
 
class ServiceDiscovery(object):
 
    def __init__(self, port, deadline=5000):
        self.socket = Socket(SURVEYOR)
        self.port = port
        self.deadline = deadline
        self.services = defaultdict(set)
 
    def bind(self):
        self.socket.bind('tcp://172.30.42.174:%s' % self.port)
        self.socket.set_int_option(SURVEYOR, SURVEYOR_DEADLINE, self.deadline)
 
    def discover(self):
        if not self.socket.is_open():
            return self.services
 
        self.services = defaultdict(set)
        self.socket.send('service query')
 
        while True:
            try:
                response = self.socket.recv()
            except NanoMsgAPIError:
                break
 
            service, address = response.split('|')
            self.services[service].add(address)
 
        return self.services
 
    def resolve(self, service):
        providers = self.services[service]
 
        if not providers:
            return None
 
        return random.choice(tuple(providers))
 
    def close(self):
        self.socket.close()
