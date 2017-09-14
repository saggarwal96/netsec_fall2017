import asyncio
import playground
from playground.network.packet import PacketType
from packets import RequestCountry, Question, Answer, Result


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
		
		
def test():				
	loop = asyncio.get_event_loop()
	coro = playground.getConnector().create_playground_server(lambda: QuizServer(), 8000)
	#coro = loop.create_server(QuizServer, '127.0.0.1', 8000)
	server = loop.run_until_complete(coro)

	print('Serving on {}'.format(server.sockets[0].getsockname()))
	try:
		loop.run_forever()
	except KeyboardInterrupt:
		pass

	server.close()
	loop.run_until_complete(server.wait_closed())
	loop.close()
	
if __name__=="__main__":
	test()
