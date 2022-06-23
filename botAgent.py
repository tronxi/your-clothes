from spacyBot import Bot
from spade import agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message

class BotAgent(agent.Agent):
    async def setup(self):
        self.bot = Bot()

class CallClasificator(OneShotBehaviour):

    async def run(self):
        msg = Message(to="test-dasi-ucm@yax.im")
        msg.set_metadata("performative", "inform")
        await self.send(msg)

class CallRecomendador(OneShotBehaviour):
    def __init__(self, color, season, type): 
        self.color = color
        self.season = season
        self.type = type
        super().__init__()

    async def run(self):
        msg = Message(to="recomendador-dasi-ucm-clothes@yax.im")
        msg.body = self.color + "," + self.season + "," + self.type
        msg.set_metadata("performative", "inform")
        await self.send(msg)