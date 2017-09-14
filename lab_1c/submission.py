import asyncio
import playground
from playground.asyncio_lib.testing import TestLoopEx
from playground.network.testing import MockTransportToProtocol
from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import STRING, BOOL, BUFFER, UINT32


# define packets
class RequestCountry(PacketType):
	DEFINITION_IDENTIFIER = "lab1b.shreya.RequestCountry"
	DEFINITION_VERSION    = "1.0"

class Question(PacketType):
	DEFINITION_IDENTIFIER = "lab1b.shreya.Question"
	DEFINITION_VERSION    = "1.0"
	FIELDS = [
		("country", STRING),
		("id", UINT32)
		]

class Answer(PacketType):
	DEFINITION_IDENTIFIER = "lab1b.shreya.Answer"
	DEFINITION_VERSION    = "1.0"
	FIELDS = [
		("capital", STRING),
		("id", UINT32)
		]

class Result(PacketType):
	DEFINITION_IDENTIFIER = "lab1b.shreya.Result"
	DEFINITION_VERSION    = "1.0"
	FIELDS = [
		("passfail", BOOL),
		("id", UINT32)
		]


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


# basic unit test
def basicUnitTest():
	packet1 = RequestCountry()
	packet1Bytes = packet1.__serialize__()
	packet1a = RequestCountry.Deserialize(packet1Bytes)
	assert packet1 == packet1a

	packet2 = Question()
	packet2.country = "Japan"
	packet2.id = 1
	packet2Bytes = packet2.__serialize__()
	packet2a = Question.Deserialize(packet2Bytes)
	assert packet2 == packet2a

	packet3 = Answer()
	packet3.capital = "Tokyo"
	packet3.id = 1
	packet3Bytes = packet3.__serialize__()
	packet3a = Answer.Deserialize(packet3Bytes)
	assert packet3 == packet3a

	packet4 = Result()
	packet4.passfail = True
	packet4.id = 1
	packet4Bytes = packet4.__serialize__()
	packet4a = Result.Deserialize(packet4Bytes)
	assert packet4 == packet4a

	asyncio.set_event_loop(TestLoopEx())

	clientProtocol = StudentClient()
	serverProtocol = QuizServer()

	transportToServer = MockTransportToProtocol(myProtocol=clientProtocol)
	transportToClient = MockTransportToProtocol(myProtocol=serverProtocol)
	transportToServer.setRemoteTransport(transportToClient)
	transportToClient.setRemoteTransport(transportToServer)
	clientProtocol.connection_made(transportToServer)
	serverProtocol.connection_made(transportToClient)

	# client sends first packet
	clientProtocol.request(stdInCallback)
	
	transportToClient.close()
	transportToServer.close()
	
	print()
	
	transportToServer2 = MockTransportToProtocol(myProtocol=clientProtocol)
	transportToClient2 = MockTransportToProtocol(myProtocol=serverProtocol)
	
	transportToServer2.setRemoteTransport(transportToClient)
	transportToClient2.setRemoteTransport(transportToServer)
	
	clientProtocol.connection_made(transportToServer2)
	serverProtocol.connection_made(transportToClient2)
	
	# server receives wrong packet
	serverProtocol.data_received(packet3Bytes)
	
	print()
	
	transportToServer3 = MockTransportToProtocol(myProtocol=clientProtocol)
	transportToClient3 = MockTransportToProtocol(myProtocol=serverProtocol)
	
	transportToServer3.setRemoteTransport(transportToClient)
	transportToClient3.setRemoteTransport(transportToServer)
	
	clientProtocol.connection_made(transportToServer3)
	serverProtocol.connection_made(transportToClient3)
	
	# client receives wrong packet
	clientProtocol.data_received(packet4Bytes)
	

# main method
if __name__=="__main__":
	basicUnitTest()
