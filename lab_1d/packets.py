import asyncio
import playground
from playground.asyncio_lib.testing import TestLoopEx
from playground.network.testing import MockTransportToProtocol
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
