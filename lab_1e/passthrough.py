from playground.network.common import *

class PassThrough1(StackingProtocol):
	def __init__(self):
		self.transport = None
		
	def connection_made(self, transport):
		print("PassThrough1: Connection Made")
		self.transport = transport
		higherTransport = StackingTransport(self.transport)
		self.higherProtocol().connection_made(higherTransport)
		
	def data_received(self, data):
		print("PassThrough1: Data Received")
		self.higherProtocol().data_received(data)
				
	def connection_lost(self, exc):
		print("PassThrough1: Connection Lost")
		self.transport = None
		self.higherProtocol().connection_lost(exc)

class PassThrough2(StackingProtocol):
	def __init__(self):
		self.transport = None
		
	def connection_made(self, transport):
		print("PassThrough2: Connection Made")
		self.transport = transport
		higherTransport = StackingTransport(self.transport)
		self.higherProtocol().connection_made(higherTransport)
		
	def data_received(self, data):
		print("PassThrough2: Data Received")
		self.higherProtocol().data_received(data)
				
	def connection_lost(self, exc):
		print("PassThrough2: Connection Lost")
		self.transport = None
		self.higherProtocol().connection_lost(exc)
