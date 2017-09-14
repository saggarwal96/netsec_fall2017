import asyncio
import playground
from playground.network.packet import PacketType
from packets import RequestCountry, Question, Answer, Result


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
				response.capital = self._cb()
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


# define call back
def stdInCallback():
	capital = input("Enter Capital: ")
	return capital

def test():
	loop = asyncio.get_event_loop()
	coro = playground.getConnector().create_playground_connection(lambda: StudentClient(), '20174.1.1.1', 8000)
	#coro = loop.create_connection(lambda: StudentClient(), '127.0.0.1', 8000)
	loop.run_until_complete(coro)
	#loop.run_forever()
	loop.close()


if __name__=="__main__":
	test()
