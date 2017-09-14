import asyncio
import playground
from playground.asyncio_lib.testing import TestLoopEx
from playground.network.testing import MockTransportToProtocol
from playground.network.packet import PacketType
from packets import RequestCountry, Question, Answer, Result
from server import QuizServer
from client import StudentClient, stdInCallback

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
