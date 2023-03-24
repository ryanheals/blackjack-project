import random, sys

HEARTS = chr(9829)
DIAMONDS = chr(9830) 
SPADES = chr(9824)
CLUBS = chr(9827)

BACKSIDE = "backside"

def main():
    print('''======BlackJack======
          Rules:
          -Try to get close to 21 without going over.
          -Kings, Queens, and Jacks are worth 10 points.
          -Aces are worth 1 or 11 points.
          -Cards 2 through 10 are worth their face value
          -(H) is to take another care from the dealer.
          -(S) is to stand and stop taking cards.
          -On your first play, you can (D)ouble down to increase your bet
          but must hit exactly one more time before standing.
          -In case of a tie, the bet is returned to the player.
          -The dealer stops hitting at 17''')

    money = int(input("How much money do you have?: "))
    while True: 
        if(money <= 0 ):
            print("Sorry you are broke! Thanks for playing!")
            sys.exit()
        
        print("Money:", money)
        bet = getBet(int(money))

        deck = getDeck()
        dealerHand = [deck.pop(), deck.pop()]
        playerHand = [deck.pop(), deck.pop()]

        print("Bet: ", bet)
        while True:
            displayHands(playerHand, dealerHand, False)
            print()
            if getHandValue(playerHand) > 21:
                break

            move = getMove(playerHand, money - bet)

            if move == 'D':
                additionalBet += getBet(min(bet,(money - bet)))
                bet += additionalBet
                print("Bet increased to {}".format(bet))
                print("Bet", bet)
            
            if move in ('H', 'D'):
                newCard = deck.pop()
                rank, suit = newCard
                print("You drew a {} of {}.".format(rank, suit))
                playerHand.append(newCard)
                if getHandValue(playerHand) > 21:
                    continue
            if move in ('S', 'D'):
                break
        if getHandValue(playerHand) <= 21:
            while getHandValue(dealerHand) >= 21:
                print("Dealer hits...")
                dealerHand.append(deck.pop())
                displayHands(playerHand, dealerHand, False)

                if getHandValue(dealerHand) > 21:
                    break
                input("Press Enter to Continue: ")
                print("\n\n")

        displayHands(playerHand, dealerHand, True)
        playerValue = getHandValue(playerHand)
        dealerValue = getHandValue(dealerHand)

        if dealerValue > 21:
            print("Dealer Busts! You win ${}".format(bet))
            money+=bet
        elif(playerValue > 21 ) or (playerValue < dealerValue):
            print("You lose!")
            money -= bet
        elif playerValue > dealerValue:
            print("You won {}".format(bet))
            money += bet
        elif playerValue == dealerValue:
            print("Its a tie! The bet is returned back")
        
        print("Press Enter to continue: ")
        print("\n\n")



def getBet(maxBet):
    while True:
        print("What is your bet?: ")
        bet = int(input('>' ))
        if(bet == 'QUIT'):
            print("Thanks for playing!")
            sys.exit()
        if(bet < 1):
            print("Please enter a bet that is greater than or equal to 1: ")
        if(bet >= 1 and bet <= maxBet):
            return bet
def getDeck():
    deck = []
    for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
        for rank in range(2,11):
            deck.append((str(rank), suit))
        for rank in ('J', 'Q', 'K', 'A'):
            deck.append((rank, suit))
        random.shuffle(deck)
        return deck

def getHandValue(cards):
    value = 0
    numAces = 0

    for card in cards:
        rank = card[0]
        if rank == 'A':
            numAces += 1
        elif rank in ('K','Q','J'):
            value += 10
        else:
            value += int(rank)
    value += numAces
    for i in range(numAces):
        if value + 10 <= 21:
            value += 10
    return value

def displayCards(cards):
    rows = ['', '', '', '', '']
    for i, card in enumerate(cards):
        rows[0] = ' ___  '
        if card == BACKSIDE:
            rows[1] = '|### |  '
            rows[2] = '|  ##|  '
            rows[3] = '|##  |  '
        else:
            rank, suit = card
            rows[1] += '|{}  |  '.format(rank.ljust(2))
            rows[2] += '| {}  |  '.format(suit)
            rows[3] += '|__{}|  '.format(rank.rjust(2,'_'))
    
    for row in rows:
        print(row)

def displayHands(playerHand, dealerHand, showDealerHand):
    print()
    if (showDealerHand):
        print("Dealer", getHandValue(dealerHand))
        displayCards(dealerHand)
    else:
        print("Dealer: ?")
        displayCards(([BACKSIDE] + dealerHand[1:]))

    print("Player", getHandValue(playerHand))
    displayCards(playerHand)

def getMove(playerHand, money):
    while True:
        moves = ['(H) for Hit, (S) for Stand']
        if len(playerHand) == 2 and money > 0:
            moves.append("(D) for Double Down")
        movePrompt = ", ".join(moves) + "> "
        move = input(movePrompt).upper()
        if move in ('H', 'S'):
            return move
        elif move in 'D':
            return move



if __name__ == "__main__":
    main()