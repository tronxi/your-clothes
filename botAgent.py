from spacyBot import Bot
from spade import agent

class BotAgent(agent.Agent):
    async def setup(self):
        self.bot = Bot()