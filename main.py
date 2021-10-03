import numpy as np
import discord
import os
class Card:
   
    async def display(self, message):
        myarrayofcards = ["","A","2","3","4","5","6", "7", "8","9", "10", "J", "Q", "K"]
        myarrayofsuits = ["H","D","S","C"]
        todisplay = myarrayofcards[self.number] + myarrayofsuits[self.suite]
        await message.reply(todisplay)

    def __init__(self,number,suite) -> None:
         # 2-10 obvious, 1=A, 11=J, 12=Q, 13=K
    # 0 = heart, 1 = diamond, 2 = spade, 3 = club
        self.number = number
        self.suite = suite
    def getName():
        pass

class Deck:
    
    def __init__(self) -> None:
        self.mydeckarray = []
        for number in range(1, 14):
            for suite in range(0, 4):
                self.mydeckarray.append(Card(number,suite))
    def shuffle(self) -> None:
        np.random.shuffle(self.mydeckarray)
    def deal(self) -> Card:
        mycard = self.mydeckarray[0]
        self.mydeckarray.pop(0)
        return mycard
    def numberOfCards(self) -> int:
        return len(self.mydeckarray)

class Hand:
    def __init__(self) -> None:
        self.myhandarray = []
    def addCard(self,newCard):
        self.myhandarray.append(newCard)
    def calcPoints(self)->int:
        points = 0
        for card in self.myhandarray:
            if 1 < card.number < 11:
                points += card.number
            if 10 < card.number < 14:
                points += 10
        for card in self.myhandarray:
            if card.number == 1:
                if 21 - points > 11:
                    points += 11
                else: 
                    points += 1           
        return points 

def blackjack():
    mydeck = Deck()
    mydeck.shuffle()
    
    playerhand = Hand()
    playerhand.addCard(mydeck.deal())
    playerhand.addCard(mydeck.deal())
    dealerhand = Hand()
    dealerhand.addCard(mydeck.deal())
    dealerhand.addCard(mydeck.deal())
    endgame = False
    while(not endgame):
        endgame = playround(playerhand, dealerhand, mydeck)
        myprint(endgame)
    if dealerhand.calcPoints() < playerhand.calcPoints() < 22:
        myprint("You won!")
        displayGameState(playerhand, dealerhand, True)
    else: 
        myprint("You lost!")
        displayGameState(playerhand, dealerhand, True)
    


def playround(playerhand: Hand, dealerhand: Hand, mydeck: Deck, message):
    displayGameState(playerhand, dealerhand)
    message.reply("Stand or Hit?");
    x = myinput()
    if x == "Stand":
        return True
    if x == "Hit":
        playerhand.addCard(mydeck.deal())
    if playerhand.calcPoints() > 21:
        myprint("Bust.")
        return True 
    if dealerhand.calcPoints() >= 17:
        myprint("The Dealer Stands")
    if dealerhand.calcPoints() <= 16:
        dealerhand.addCard(mydeck.deal())
        myprint("The Dealer Hits")
    return False
    

    


def myprint(a):
    print(a)

def myinput():
    return input()

async def displayGameState(playerhand,dealerhand,message, endgame = False):
    message.reply("PlayerHand")
    for card in playerhand.myhandarray:
        await card.display(message)
    await message.reply("DealerHand")
    if not endgame:
        await dealerhand.myhandarray[0].display(message)
        i = 0
        for card in dealerhand.myhandarray:
            if i != 0:
                await message.reply("##")
            i += 1
    else:
        for card in dealerhand.myhandarray:
            await card.display(message)


client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
mydeck = Deck()
mydeck.shuffle()
playerhand = Hand()
playerhand.addCard(mydeck.deal())
playerhand.addCard(mydeck.deal())
dealerhand = Hand()
dealerhand.addCard(mydeck.deal())
dealerhand.addCard(mydeck.deal())
gamestarted = False 


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("$BlackJack"):
        if gamestarted:
            mydeck = Deck()
            mydeck.shuffle()
            playerhand = Hand()
            playerhand.addCard(mydeck.deal())
            playerhand.addCard(mydeck.deal())
            dealerhand = Hand()
            dealerhand.addCard(mydeck.deal())
            dealerhand.addCard(mydeck.deal())
            gamestarted = True
            displayGameState(playerhand,dealerhand,message,endgame=False)
            """
            while(not endgame):
                endgame = await playround(playerhand, dealerhand, mydeck, message)
                myprint(endgame)
            if dealerhand.calcPoints() < playerhand.calcPoints() < 22:
                await message.reply("You won!")
                await displayGameState(playerhand, dealerhand, message, True)
            else: 
                await message.reply("You lost!")
                await displayGameState(playerhand, dealerhand, message, True)
            """
    if message.content.startswith("Hit"):
        if gamestarted == True:
            playerhand.addCard(mydeck.deal())
        if playerhand.calcPoints() > 21:
            await message.reply("Bust.")
        if dealerhand.calcPoints() >= 17:
            message.reply("The Dealer Stands")
        if dealerhand.calcPoints() <= 16:
            dealerhand.addCard(mydeck.deal())
            message.reply("The Dealer Hits")
        if dealerhand.calcPoints() < playerhand.calcPoints() < 22:
            message.reply("You won!")
            await displayGameState(playerhand, dealerhand, message, True)
        else: 
            message.reply("You lost!")
            await displayGameState(playerhand, dealerhand, message, True)
    if message.content.startswith("Stand"):
        if dealerhand.calcPoints() >= 17:
            message.reply("The Dealer Stands")
        if dealerhand.calcPoints() <= 16:
            dealerhand.addCard(mydeck.deal())
            message.reply("The Dealer Hits")
        if dealerhand.calcPoints() < playerhand.calcPoints() < 22:
            message.reply("You won!")
            await displayGameState(playerhand, dealerhand, message, True)
        else: 
            message.reply("You lost!")
            await displayGameState(playerhand, dealerhand, message, True)

client.run(os.getenv('TOKEN'))