from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template

class ClasificadorAgent(Agent):
    class ClasificadorBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=90000)
            if msg:
                print("desde dentro", msg.body)
                
    async def setup(self):
        b = self.ClasificadorBehaviour()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)