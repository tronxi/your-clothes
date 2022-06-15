from botAgent import BotAgent
from spade import quit_spade

if __name__ == "__main__":
    botAgent = BotAgent("bot-dasi-ucm-clothes@yax.im", "1234")
    future = botAgent.start()
    future.result()
    print("Buenas, como te llamas?")
    while True:
        try:
            userInput = input()
            bot_input = botAgent.bot.response(userInput)
            print(bot_input)
            
        except(KeyboardInterrupt, EOFError, SystemExit):
            botAgent.stop()
            quit_spade()