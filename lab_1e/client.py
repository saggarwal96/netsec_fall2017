import asyncio
import playground
import logging
from playground.network.packet import PacketType
from packets import RequestCountry, Question, Answer, Result
from passthrough import *

# define client protocol
class StudentClient(asyncio.Protocol):
	def __init__(self):
		self.transport = None
		self._deserializer = PacketType.Deserializer()
		
	def connection_made(self, transport):
		print("Student Connected to Quiz Server")
		self.transport = transport
		self._state = 0
		
	def request(self, cb):
		self._cb = cb
		request = RequestCountry()
		self.transport.write(request.__serialize__())
		
	def data_received(self, data):
		self._deserializer.update(data)
		for pkt in self._deserializer.nextPackets():
			if isinstance(pkt, Question) and self._state == 0:
				self._state += 1
				print("Question Received: What is the capital of " + pkt.country + "?")
				response = Answer()
				response.capital = "tokyo"
				response.id = 1
				self.transport.write(response.__serialize__())
			elif isinstance(pkt, Result) and self._state == 1:
				self._state += 1
				print("Result Received: Answer Is " + str(pkt.passfail))
			else:
				print("Wrong Packet Received by Student")
				self.transport.close()
				
	def connection_lost(self, exc):
		self.transport = None
		print("Connection to Quiz Server Is Closed")
		self.transport.close()

# define call back
def stdInCallback():
	capital = input("Enter Capital: ")
	return capital


def basicUnitTest():
	f = StackingProtocolFactory(lambda: PassThrough1(), lambda: PassThrough2())
	ptConnector = playground.Connector(protocolStack=f)
	playground.setConnector("passthrough", ptConnector)

	loop = asyncio.get_event_loop()
	coro = playground.getConnector('passthrough').create_playground_connection(lambda: StudentClient(), '20174.1.1.1', 8000)
	
	transport, protocol = loop.run_until_complete(coro)
	protocol.request(stdInCallback)
	loop.close()


if __name__=="__main__":
	basicUnitTest()
