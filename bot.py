import discord
import os
import json
import numpy as np

class Card:
   
    async def display(self, message, dealer=False):
        myarrayofcards = ["","A","2","3","4","5","6", "7", "8","9", "10", "J", "Q", "K"]
        myarrayofsuits = ["H","D","S","C"]
        todisplay = ""
        if dealer:
            todisplay = f'Dealer: {myarrayofcards[int(self.number)]}{myarrayofsuits[int(self.suite)]}'
        else:
            todisplay = f'{myarrayofcards[int(self.number)]}{myarrayofsuits[int(self.suite)]}'
        await message.reply(todisplay)

    def __init__(self,number,suite) -> None:
         # 2-10 obvious, 1=A, 11=J, 12=Q, 13=K
    # 0 = heart, 1 = diamond, 2 = spade, 3 = club
        self.number = number
        self.suite = suite
    def getName():
        pass

class Deck:
    
    def __init__(self, unititalized = False) -> None:
        self.mydeckarray = []
        if unititalized:
            return
        for number in range(1, 14):
            for suite in range(0, 4):
                self.mydeckarray.append(Card(number,suite))
    def shuffle(self) -> None:
        np.random.shuffle(self.mydeckarray)
    async def deal(self, message = 0) -> Card:
        if self.numberOfCards() == 0:
            self.__init__()
            self.shuffle()
            if message != 0:
                await message.reply("NEW DECK!")
        mycard = self.mydeckarray[0]
        self.mydeckarray.pop(0)
        return mycard
    def numberOfCards(self) -> int:
        return len(self.mydeckarray)
    def toString(self)->str:
        arraystring = ""
        for card in self.mydeckarray:
            arraystring += f'{card.number},{card.suite},'
        return arraystring[:-1]
    def fromString(self, mystr:str) -> None:
        self.mydeckarray = []
        mylist = mystr.split(',')
        j = -1
        if len(mystr) == 0:
            self = Deck()
            return
        for i in range(0, len(mylist)):
            j += 1
            if j % 2 == 1:
                continue
            
            self.mydeckarray.append(Card(mylist[i], mylist[i+1]))
            i += 1
            if len(mylist) - i == 1:
                break
class Hand:
    def __init__(self) -> None:
        self.myhandarray = []
    def addCard(self,newCard):
        self.myhandarray.append(newCard)
    def calcPoints(self)->int:
        points = 0
        for card in self.myhandarray:
            if 1 < int(card.number) < 11:
                points += int(card.number)
            if 10 < int(card.number) < 14:
                points += 10
        for card in self.myhandarray:
            if int(card.number) == 1:
                if 21 - points >= 11:
                    points += 11
                else: 
                    points += 1           
        return points 
    async def display(self, message, dealer=False, reveal = True):
        if reveal:
            for card in self.myhandarray:
                await card.display(message, dealer)
        else:
            i = 0
            for card in self.myhandarray:
                if i == 0:
                    if dealer:
                        await message.reply("Dealer: ##")
                    else:
                        await message.reply("##")
                else:
                    await card.display(message, dealer)
                i += 1
        
    def toString(self)->str:
        mystring = ""
        for card in self.myhandarray:
            mystring += f'{card.number},{card.suite},'
        return mystring[:-1]
    def fromString(self, mystring:str) -> None:
        mylist = mystring.split(",")
        j = -1
        for i in range(0, len(mylist)):
            j += 1
            if j % 2 == 1:
                continue
            
            self.addCard(Card(mylist[i], mylist[i+1]))
            if len(mylist) - i == 1:
                break

    
client = discord.Client()

@client.event
async def on_ready():
    f = open('data.json',)
    data = json.load(f)
    f.close()
    if 'Deck' not in data:
        mydeck = Deck()
        mydeck.shuffle()
        data['Deck'] = mydeck.toString()
    if 'DealerHand' not in data:
        myhand = Hand()
        deck = Deck()
        deck.shuffle()
        print(deck.numberOfCards())
        myhand.addCard(await deck.deal())
        myhand.addCard(await deck.deal())
        data['DealerHand'] = myhand.toString()
        data['Deck'] = deck.toString()
    f = open("data.json","w")
    json.dump(data, f)
    f.close()
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    if message.content.startswith('$BlackJack'):
        f = open('data.json')
        data = json.load(f)
        f.close()
        mycommand = message.content.removeprefix("$BlackJack ")
        if message.author.name not in data:
            # create a new hand and display it
            deck = Deck(True)
            deck.fromString(data['Deck'])
            playerhand = Hand()
            playerhand.addCard(await deck.deal(message))
            playerhand.addCard(await deck.deal(message))
            await playerhand.display(message)
            data[message.author.name] = playerhand.toString()
            data["Deck"] = deck.toString()
            if playerhand.calcPoints() == 21:
                await message.reply("You win!")
                data.pop(message.author.name)
            f = open('data.json', "w")
            json.dump(data, f)
            f.close()
        elif mycommand.startswith('Hit') and message.author.name in data:
            deck = Deck(True)
            deck.fromString(data['Deck'])
            playerhand = Hand()
            playerhand.fromString(data[message.author.name])
            playerhand.addCard(await deck.deal(message))
            await playerhand.display(message)
            data[message.author.name] = playerhand.toString()
            if playerhand.calcPoints() > 21:
                await message.reply("Bust")
                data.pop(message.author.name)
            if playerhand.calcPoints() == 21:
                await message.reply("You win!")
                data.pop(message.author.name)
            dealerhand = Hand()
            dealerhand.fromString(data['DealerHand'])
            if dealerhand.calcPoints() < 17:
                await message.reply("The Dealer Hits")
                dealerhand.addCard(await deck.deal(message))
            else:
                await message.reply("The Dealer Stands")
            if dealerhand.calcPoints() > 21:
                await message.reply("The Dealer Busts")
                await message.reply("You win!")
                data.pop(message.author.name)
                await dealerhand.display(message, dealer = True)
                dealerhand = Hand()
               
                dealerhand.addCard(await deck.deal(message))
                dealerhand.addCard(await deck.deal(message))

            data['DealerHand']=dealerhand.toString()
            data['Deck'] = deck.toString()
            f = open('data.json', "w")
            json.dump(data, f)
            f.close()
        elif mycommand.startswith('Stand') and message.author.name in data:
            deck = Deck()
            deck.fromString(data['Deck'])
            playerhand = Hand()
            playerhand.fromString(data[message.author.name])
            score = playerhand.calcPoints()
            await message.reply(f'You got a score of {score}')
            dealerhand = Hand()
            dealerhand.fromString(data['DealerHand'])
            while(dealerhand.calcPoints() < 17):
                await message.reply("The Dealer Hits.")
                dealerhand.addCard(await deck.deal(message))
            if dealerhand.calcPoints() > 21:
                await message.reply("The Dealer Busts")
                await message.reply("You win!")

            else:
                await message.reply("The Dealer Stands")
            if dealerhand.calcPoints() > score and dealerhand.calcPoints() <= 21:
                await message.reply(f'The Dealer had a score of {dealerhand.calcPoints()}, and won!')
            elif dealerhand.calcPoints() <= 21:
                await message.reply(f'The Dealer had a score of {dealerhand.calcPoints()}, therefore you won!')
            await dealerhand.display(message, True)
            dealerhand = Hand()
            dealerhand.addCard(await deck.deal(message))
            dealerhand.addCard(await deck.deal(message))
            data['DealerHand'] = dealerhand.toString()

            data['Deck'] = deck.toString()
            data[message.author.name]
            data.pop(message.author.name)
            f = open('data.json', "w")
            json.dump(data, f)
            f.close()
        elif mycommand.startswith('Dealer'):
            dealerhand = Hand()
            dealerhand.fromString(data['DealerHand'])
            await dealerhand.display(message, dealer=True, reveal = False)
        elif message.author.name in data:
            playerhand = Hand()
            playerhand.fromString(data[message.author.name])
            await playerhand.display(message)

            

client.run(os.getenv('TOKEN'))
