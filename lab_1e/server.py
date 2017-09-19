import asyncio
import playground
import logging
from playground.network.packet import PacketType
from packets import RequestCountry, Question, Answer, Result
from passthrough import *

# define server protocol
class QuizServer(asyncio.Protocol):
	def __init__(self):
		self.transport = None
		self._deserializer = PacketType.Deserializer()
		
	def connection_made(self, transport):
		print("Quiz Server Connected to Student")
		self.transport = transport
		self._state = 0
		
	def data_received(self, data):
		self._deserializer.update(data)
		for pkt in self._deserializer.nextPackets():
			if isinstance(pkt, RequestCountry) and self._state == 0:
				self._state += 1
				print("Country Requested By Student")
				response = Question()
				response.country = "Japan"
				response.id = 1
				self.transport.write(response.__serialize__())
			elif isinstance(pkt, Answer) and self._state == 1:
				self._state += 1
				print("Answer Received: " + pkt.capital)
				response = Result()
				if pkt.capital.lower() == "tokyo":
					response.passfail = True
				else:
					response.passfail = False
				response.id = 1
				self.transport.write(response.__serialize__())
			else:
				print("Wrong Packet Received by Quiz Server")
				self.transport.close()
				
	def connection_lost(self, exc):
		print("Connection to Student Is Closed")
		self.transport = None
		self.transport.close()
				
		
def basicUnitTest():				

	f = StackingProtocolFactory(lambda: PassThrough1(), lambda: PassThrough2())
	ptConnector = playground.Connector(protocolStack=f)
	playground.setConnector("passthrough", ptConnector)

	loop = asyncio.get_event_loop()
	loop.set_debug(enabled=True)
	coro = playground.getConnector('passthrough').create_playground_server(lambda: QuizServer(), 8000)
	server = loop.run_until_complete(coro)

	try:
		loop.run_forever()
	except KeyboardInterrupt:
		pass

	server.close()
	loop.run_until_complete(server.wait_closed())
	loop.close()
	
if __name__=="__main__":
	basicUnitTest()
