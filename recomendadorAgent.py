from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template

class RecomendadorAgent(Agent):
    class RecomendadorBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=90000)
            if msg:
                print("Recomendador con mensaje", msg.body)
                
    async def setup(self):
        b = self.RecomendadorBehaviour()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)