from unittest import TestCase

from mock import MagicMock
from pyevolve import Network

class UDPThreadServerTestCase(TestCase):
    def setUp(self):
        self.server = Network.UDPThreadServer("localhost", 777)
        self.plain_data = ("living is not enough one must have sunshine freedom"
                            "and a little flower")
        self.data = format(len(self.plain_data), "#06x") + self.plain_data
        self.chunk_size = 8
        
    def test_get_data_packs(self):                
        def recv_effect(size):
            buf = self.data[:self.chunk_size]
            self.data = self.data[self.chunk_size:]
            return (buf, ("Butterfly", ))
    
        self.server.sock = MagicMock()
        self.server.sock.recvfrom = MagicMock(side_effect = recv_effect)        
        
        ret = self.server.getData()
        self.assertEqual(ret, ("Butterfly", self.plain_data))
        
class UDPThreadUnicastClientTestCase(TestCase):
    def setUp(self):
        self.client = Network.UDPThreadUnicastClient("localhost", 777)
        self.plain_data = ("living is not enough one must have sunshine freedom"
                            "and a little flower")
        self.client.target = 4*[None]
        self.chunk_size = 8

    def test_send_data_packs(self):
        def sendto_effect(data, dest):
            buf = data[:self.chunk_size]
            return len(buf)
    
        self.client.sock = MagicMock()
        self.client.sock.sendto = MagicMock(side_effect = sendto_effect)
    
        ret = self.client.send(self.plain_data)        
        self.assertEqual(ret, len(self.plain_data) + 6)