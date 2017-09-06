from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import STRING, BOOL, BUFFER, UINT32

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

if __name__=="__main__":
	basicUnitTest()
