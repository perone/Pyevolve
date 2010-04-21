"""

:mod:`Network` -- network utility module
============================================================================

In this module you'll find all the network related implementation

.. versionadded:: 0.6
   The *Network* module.

"""
from __future__ import with_statement
import threading
import socket
import time
import sys
import Util
import cPickle

try:
    import zlib
    ZLIB_SUPPORT = True
except ImportError:
    ZLIB_SUPPORT = False

import Consts
import logging

def getMachineIP():
   """ Return all the IPs from current machine.

   Example:
      >>> Util.getMachineIP()
      ['200.12.124.181', '192.168.0.1']      

   :rtype: a python list with the string IPs

   """
   hostname = socket.gethostname()
   addresses = socket.getaddrinfo(hostname, None)
   ips = [x[4][0] for x in addresses]
   return ips

class UDPThreadBroadcastClient(threading.Thread):
   """ The Broadcast UDP client thread class.

   This class is a thread to serve as Pyevolve client on the UDP
   datagrams, it is used to send data over network lan/wan.

   Example:
      >>> s = Network.UDPThreadClient('192.168.0.2', 1500, 666)
      >>> s.setData("Test data")
      >>> s.start()
      >>> s.join()

   :param host: the hostname to bind the socket on sender (this is NOT the target host)
   :param port: the sender port (this is NOT the target port)
   :param target_port: the destination port target

   """
   def __init__(self, host, port, target_port):
      threading.Thread.__init__(self)
      self.host = host
      self.port = port
      self.targetPort = target_port
      self.data = None
      self.sentBytes = None
      self.sentBytesLock = threading.Lock()

      self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
      self.sock.bind((host, port))     

   def setData(self, data):
      """ Set the data to send

      :param data: the data to send

      """
      self.data = data

   def getData(self):
      """ Get the data to send

      :rtype: data to send

      """
      return self.data

   def close(self):
      """ Close the internal socket """
      self.sock.close()

   def getSentBytes(self):
      """ Returns the number of sent bytes. The use of this method makes sense 
      when you already have sent the data
         
      :rtype: sent bytes

      """
      sent = None
      with self.sentBytesLock:
         if self.sentBytes is None:
            Util.raiseException('Bytes sent is None')
         else: sent = self.sentBytes
      return sent

   def send(self):
      """ Broadcasts the data """
      return self.sock.sendto(self.data, (Consts.CDefBroadcastAddress, self.targetPort))
   
   def run(self):
      """ Method called when you call *.start()* of the thread """
      if self.data is None:
         Util.raiseException('You must set the data with setData method', ValueError)

      with self.sentBytesLock:
         self.sentBytes = self.send()
      self.close()

class UDPThreadUnicastClient(threading.Thread):
   """ The Unicast UDP client thread class.

   This class is a thread to serve as Pyevolve client on the UDP
   datagrams, it is used to send data over network lan/wan.

   Example:
      >>> s = Network.UDPThreadClient('192.168.0.2', 1500)
      >>> s.setData("Test data")
      >>> s.setTargetHost('192.168.0.50', 666)
      >>> s.start()
      >>> s.join()

   :param host: the hostname to bind the socket on sender (this is not the target host)
   :param port: the sender port (this is not the target port)
   :param pool_size: the size of send pool
   :param timeout: the time interval to check if the client have data to send

   """
   def __init__(self, host, port, pool_size=10, timeout=0.5):
      threading.Thread.__init__(self)
      self.host = host
      self.port = port
      self.target = []
      self.sendPool = []
      self.poolSize = pool_size
      self.sendPoolLock = threading.Lock()
      self.timeout = timeout

      self.doshutdown = False

      self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      #self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      self.sock.bind((host, port))     

   def poolLength(self):
      """ Returns the size of the pool
      
      :rtype: integer

      """
      with self.sendPoolLock:
         ret = len(self.sendPool)
      return ret

   def popPool(self):
      """ Return the last data received on the pool

      :rtype: object

      """
      with self.sendPoolLock:
         ret = self.sendPool.pop()
      return ret

   def isReady(self):
      """ Returns True when there is data on the pool or False when not
         
      :rtype: boolean
      
      """
      with self.sendPoolLock:
         ret = True if len(self.sendPool) >= 1 else False
      return ret

   def shutdown(self):
      """  Shutdown the server thread, when called, this method will stop
      the thread on the next socket timeout """
      self.doshutdown = True

   def addData(self, data):
      """ Set the data to send

      :param data: the data to send

      """
      if self.poolLength() >= self.poolSize:
         logging.warning('the send pool is full, consider increasing the pool size or decreasing the timeout !')
         return

      with self.sendPoolLock:
         self.sendPool.append(data)

   def setTargetHost(self, host, port):
      """ Set the host/port of the target, the destination

      :param host: the target host
      :param port: the target port

      .. note:: the host will be ignored when using broadcast mode
      """
      del self.target[:]
      self.target.append((host, port))

   def setMultipleTargetHost(self, address_list):
      """ Sets multiple host/port targets, the destinations
      
      :param address_list: a list with tuples (ip, port)
      """
      del self.target[:]
      self.target = address_list[:]

   def close(self):
      """ Close the internal socket """
      self.sock.close()

   def send(self, data):
      """ Send the data

      :param data: the data to send
      :rtype: bytes sent to each destination
      """
      bytes = -1
      for destination in self.target:
         bytes = self.sock.sendto(data, destination)
      return bytes
   
   def run(self):
      """ Method called when you call *.start()* of the thread """
      if len(self.target) <= 0:
         Util.raiseException('You must set the target(s) before send data', ValueError)

      while True:
         if self.doshutdown: break

         while self.isReady():
            data = self.popPool()
            self.send(data)

         time.sleep(self.timeout)
      
      self.close()

class UDPThreadServer(threading.Thread):
   """ The UDP server thread class.

   This class is a thread to serve as Pyevolve server on the UDP
   datagrams, it is used to receive data from network lan/wan.

   Example:
      >>> s = UDPThreadServer("192.168.0.2", 666, 10)
      >>> s.start()
      >>> s.shutdown()

   :param host: the host to bind the server
   :param port: the server port to bind
   :param poolSize: the size of the server pool
   :param timeout: the socket timeout

   .. note:: this thread implements a pool to keep the received data,
             the *poolSize* parameter specifies how much individuals
             we must keep on the pool until the *popPool* method 
             is called; when the pool is full, the sever will
             discard the received individuals.

   """
   def __init__(self, host, port, poolSize=10, timeout=3):
      threading.Thread.__init__(self)
      self.recvPool = []
      self.recvPoolLock = threading.Lock()
      self.bufferSize = 4096
      self.host = host
      self.port = port
      self.timeout = timeout
      self.doshutdown = False
      self.poolSize = poolSize

      self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      #self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      self.sock.bind((host, port))     
      self.sock.settimeout(self.timeout)

   def shutdown(self):
      """  Shutdown the server thread, when called, this method will stop
      the thread on the next socket timeout """
      self.doshutdown = True

   def isReady(self):
      """ Returns True when there is data on the pool or False when not
         
      :rtype: boolean
      
      """
      with self.recvPoolLock:
         ret = True if len(self.recvPool) >= 1 else False
      return ret
    
   def poolLength(self):
      """ Returns the size of the pool
      
      :rtype: integer

      """
      with self.recvPoolLock:
         ret = len(self.recvPool)
      return ret

   def popPool(self):
      """ Return the last data received on the pool

      :rtype: object

      """
      with self.recvPoolLock:
         ret = self.recvPool.pop()
      return ret

   def close(self):
      """ Closes the internal socket """
      self.sock.close()

   def setBufferSize(self, size):
      """ Sets the receive buffer size
      
      :param size: integer

      """
      self.bufferSize = size

   def getBufferSize(self):
      """ Gets the current receive buffer size

      :rtype: integer

      """
      return self.bufferSize

   def getData(self):
      """ Calls the socket *recvfrom* method and waits for the data,
      when the data is received, the method will return a tuple
      with the IP of the sender and the data received. When a timeout
      exception occurs, the method return None.
      
      :rtype: tuple (sender ip, data) or None when timeout exception

      """
      try:
         data, sender = self.sock.recvfrom(self.bufferSize)
      except socket.timeout:
         return None
      return (sender[0], data)
      
   def run(self):
      """ Called when the thread is started by the user. This method
      is the main of the thread, when called, it will enter in loop
      to wait data or shutdown when needed.
      """
      while True:
         # Get the data
         data = self.getData()
         # Shutdown called
         if self.doshutdown: break
         # The pool is full
         if self.poolLength() >= self.poolSize:
            continue
         # There is no data received
         if data == None: continue
         # It's a packet from myself
         if data[0] == self.host:
            continue
         with self.recvPoolLock:
            self.recvPool.append(data)

      self.close()

def pickleAndCompress(obj, level=9):
   """ Pickles the object and compress the dumped string with zlib
   
   :param obj: the object to be pickled
   :param level: the compression level, 9 is the best
                    and -1 is to not compress

   """
   pickled = cPickle.dumps(obj)
   if level < 0: return pickled
   else:
      if not ZLIB_SUPPORT:
         Util.raiseException('zlib not found !', ImportError)
      pickled_zlib = zlib.compress(pickled, level)
      return pickled_zlib

def unpickleAndDecompress(obj_dump, decompress=True):
   """ Decompress a zlib compressed string and unpickle the data
   
   :param obj: the object to be decompressend and unpickled
   """
   if decompress:
      if not ZLIB_SUPPORT:
         Util.raiseException('zlib not found !', ImportError)
      obj_decompress = zlib.decompress(obj_dump)
   else:
      obj_decompress = obj_dump
   return cPickle.loads(obj_decompress)

if __name__ == "__main__":
   arg = sys.argv[1]
   myself = getMachineIP()

   if arg == "server":
      s = UDPThreadServer(myself[0], 666)
      s.start()
      
      while True:
         print ".",
         time.sleep(10)
         if s.isReady():
            item = s.popPool()
            print item
         time.sleep(4)
         s.shutdown()
         break


   elif arg == "client":
      print "Binding on %s..." % myself[0]
      s = UDPThreadUnicastClient(myself[0], 1500)
      s.setData("dsfssdfsfddf")
      s.setTargetHost(myself[0], 666)
      s.start()
      s.join()
      print s.getSentBytes()
     
   print "end..."


      
