from botAgent import BotAgent
from spade import quit_spade
from spade.template import Template
from clasificadorAgent import ClasificadorAgent
from botAgent import CallClasificator, CallRecomendador
from recomendadorAgent import RecomendadorAgent
import os

if __name__ == "__main__":
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    
    botAgent = BotAgent("bot-dasi-ucm-clothes@yax.im", "1234")
    future = botAgent.start()
    future.result()

    clasificadorAgent = ClasificadorAgent("test-dasi-ucm@yax.im", "1234")
    clasificadorAgentFuture = clasificadorAgent.start()
    clasificadorAgentFuture.result()

    RecomendadorAgent = RecomendadorAgent("recomendador-dasi-ucm-clothes@yax.im", "1234")
    recomendadorAgentFuture = RecomendadorAgent.start()
    recomendadorAgentFuture.result()

    template = Template()
    template.set_metadata("performative", "inform")
    print("Buenas, como te llamas?")
    while True:
        try:
            userInput = input()
            message, name, color, season, type, new, recommender = botAgent.bot.response(userInput)
            print(message)
            if new:
                behaviour = CallClasificator()
                botAgent.add_behaviour(behaviour, template)
            if recommender:
                behaviour = CallRecomendador(color, season, type)
                botAgent.add_behaviour(behaviour, template)
        except(KeyboardInterrupt, EOFError, SystemExit):
            botAgent.stop()
            quit_spade()