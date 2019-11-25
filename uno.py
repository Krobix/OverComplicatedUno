import random, sys

STARTING_CARD_AMOUNT = 7

TESTING_MODE = False

debugMode = True

#####Global special objects
drawCard = None

defpl = None

debugCard = None
###########################
players = []

cardColors = ["blue",
"red",
"green",
"yellow",
]

specialCards = ["wild",
"draw4"]

class Card:
	@staticmethod
	def getRandom(owner):
		return Card(random.choice(cardColors), random.randint(1, 9), owner)
	
	def __init__(self, color, number, owner):
		self.color = color
		self.num = number
		self.owner = owner
		
	def __str__(self):
		return f"{self.owner.cards.index(self)}: {self.color} {self.num}"

drawCard = Card("DRAW", 0, None)

class Player:
	def __init__(self, ai, name):
		self.cards = [drawCard]
		if debugMode:
			self.cards.append(debugCard)
		
		self.name = name
		self.isAI = ai
		x = 0
		while x < STARTING_CARD_AMOUNT:
			self.cards.append(Card.getRandom(self))
			x += 1
			
	def chooseCardToPlaceAI(self, lastCard):
		print(f"Its {self.name}'s turn.")
		last = lastCard
		retcard = None
		for x in self.cards:
			if x.color == last.color or x.num == last.num or x.color == "wild" or x.color == "draw4":
				retcard = x
				
		if retcard != None:
			print(f"{self.name} played card {retcard}, and now has {self.cardAmount} cards.")
			self.cards.remove(retcard)
			return retcard
		else:
			self.cards.append(Card.getRandom(self))
			print(f"{self.name} does not have a valid card, and had to draw another. They now have {self.cardAmount} cards.")
			return None
			
	def doTurn(self, last):
		if self.isAI:
			return self.chooseCardToPlaceAI(last)
			
		else:
			print(f"Its now {self.name}'s turn.")
			print(f"Here are {self.name}'s cards: \n{self.getCardStrings()}")
			chosen = self.cards[int(input("Please enter the number of the card that you choose or enter 0 to draw a new card"))]
			x = chosen
			if x.color == "DEBUG" and debugMode:
				print("Debug prompt activated. Enter debug input:")
				exec(input("\n"))
				print("Starting next players turn.\n")
			elif x.color == "DRAW":
				print(f"{self.name} has chosen to draw a new card!")
				newc = Card.getRandom(self)
				self.cards.append(newc)
				print(f"{self.name} drew a new card, and it is {str(newc)}")
				print(f"{self.name} must now wait for their next turn.")
				return None
			
			elif x.color == last.color or x.num == last.num or x.color == "wild" or x.color == "draw4":
				print(f"{self.name} chose to place card {str(x)}")
				self.cards.remove(x)
				return x
				
			else:
				print("Invalid card, please try again")
				return self.doTurn(last) 
				 
	def __str__(self):
		return f"{self.name}: Is an AI: {self.isAI}\n\n Card amount: {self.cardAmount}\n\n Card list: {self.getCardStrings()}"
		
	def getCardStrings(self):
		retstr = ""
		for x in self.cards:
			retstr += str(x) + "\n"
		return retstr
			
	@property
	def cardAmount(self):
		return len(self.cards) - 1
		

def startGame():
	global players, defpl, debugCard
	defpl = Player(None, "PLACEHOLDER PLAYER")
	debugCard = Card("DEBUG", 0, defpl)
	defpl.cards.append(debugCard)
	plamount = int(input("Please enter the number of human players."))
	aiamount = int(input("Please enter the amount of AI players."))
	
	x = 0
	while x < plamount:
		players.append(Player(False, f"Human-{x}"))
		x += 1
		
	x = 0
	while x < aiamount:
		players.append(Player(True, f"Bot-{x}"))
		x += 1
	
	drawCard.owner = defpl	
	
	if TESTING_MODE:
		print(players[0].getCardStrings())
		
	last = Card.getRandom(defpl)
	defpl.cards.append(last)
	print(f"The first card is {last}!")
	while True:
		for x in players:
			temp = x.doTurn(last)
			if x.cardAmount == 2:
				print(f"{x.name} has Uno!")
			elif x.cardAmount == 1:
				print(f"{x.name} has won!")
				sys.exit()
			elif temp != None:
				last = temp
			else:
				pass
		
	


if __name__ == "__main__":
	startGame()	
