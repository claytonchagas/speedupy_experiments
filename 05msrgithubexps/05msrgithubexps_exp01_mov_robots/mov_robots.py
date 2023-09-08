import numpy as np
import random, sys,time
from collections import deque
import numpy as np
import random

from pathlib import Path

sys.path.append(str(Path(__file__).parent / "speedupy"))

from intpy import initialize_intpy, deterministic

suitDict = {"S": 0, "H": 1, "C": 2, "D": 3}

# Helper functions for matrix representation of cards

# Gets index of first occuring card in a hand (row-wise)


@deterministic
def getFirstCard(matrix, shp):
    for i in range(shp[0]):
        for j in range(shp[1]):
            if matrix[i][j] == 1:
                return (i, j)


# Gets all indexes of same value for same-value melds


@deterministic
def getSameValue(matrix, index):
    j = index[1]
    result = []
    for i in range(4):
        if i != index[0] and matrix[i][j] == 1:
            result.append((i, j))
    return result


# Entity classes


class Card:
    def __init__(self, val, st):
        self.value = val  # actual number on card
        self.suit = st
        self.points = val  # point value of card
        if val == -1:  # joker cards have no points
            self.points = 0
        elif val == 1 or val > 10:  # ace and face cards
            self.points = 10

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        strVal = ["A"] + [str(x) for x in range(2, 11)] + ["J", "Q", "K"]
        if self.value != -1:
            return self.suit + strVal[self.value - 1]
        else:
            return self.suit  # will return "JK1" or "JK2" for joker cards

    def __eq__(self, object) -> bool:
        if not isinstance(object, Card):
            return False
        return self.value == object.value and self.suit == object.suit

    def __ne__(self, object) -> bool:
        return not self.__eq__(object)

    def __hash__(self) -> int:
        return hash(str(self))


class Deck:
    def __init__(self):
        self.cards = []
        # each card is represented by a letter for suit + number for value. A is 1, J, Q, K are 11, 12, 13 respectively
        for s in suitDict.keys():
            for v in range(1, 14):
                self.cards.append(Card(v, s))
        self.cards.append(Card(-1, "JK1"))
        self.cards.append(Card(-1, "JK2"))
        self.joker = None

    def __repr__(self) -> str:
        return "Deck()"

    def __str__(self) -> str:
        output = "Deck: "
        for card in self.cards:
            output += str(card) + "    "
        return output

    def shuffle(self, seed):
        if seed:
            random.seed(seed)
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()  # direction doesn't matter so pop from end

    def returnToDeck(self, card):
        self.cards.append(card)


class DiscardPile:
    def __init__(self):
        self.cards = deque()  # acts as a stack

    def __repr__(self) -> str:
        return "DiscardPile()"

    def __str__(self) -> str:
        output = "Discard Pile: "
        for card in self.cards:
            output += str(card) + "    "
        return output

    def draw(self):
        return self.cards.pop()

    def discard(self, card):
        self.cards.append(card)


class Hand:
    def __init__(self):
        self.cards = []
        self.cardMatrix = np.zeros((4, 13))
        self.compMatrix = np.zeros((4, 13))  # used for checking if game is complete
        self.jokers = 0
        self.rummyJokerVal = -1

    def __repr__(self) -> str:
        return "Hand()"

    def __str__(self) -> str:
        output = ""
        for card in self.cards:
            output += str(card) + "    "
        return output

    def setJoker(self, jokerVal):
        if jokerVal == -1:  # joker card is rummy joker drawn at start of round
            return
        for i in range(4):
            self.cardMatrix[i][jokerVal - 1] = -1
            self.compMatrix[i][jokerVal - 1] = -1
        self.rummyJokerVal = jokerVal

    def draw(self, card):
        self.cards.append(card)
        if card.value != -1 and card.value != self.rummyJokerVal:
            self.cardMatrix[suitDict[card.suit]][card.value - 1] = 1
        else:
            self.jokers += 1

    # def discard(self, val):
    #     for index, card in enumerate(self.cards):
    #         if card.value == val:
    #             if val != -1:
    #                 self.cardMatrix[suitDict[card.suit]][card.value-1] = 0
    #             else:
    #                 self.jokers -= 1
    #             return self.cards.pop(index)
    #     return "error"

    def discard(self, index):
        if self.cards[index].value != -1:
            self.cardMatrix[suitDict[self.cards[index].suit]][
                self.cards[index].value - 1
            ] = 0
        else:
            self.jokers -= 1
        return self.cards.pop(index)

    def checkMelds(
        self, matrix=None, jkr=None, pureFlag=0, straightCount=0
    ):  # only checks for win state for now, returns bool if game is won
        # TODO: implement pure and straight checks
        try:
            if matrix == None:
                matrix = self.cardMatrix.copy()
        except:
            pass
        try:
            if jkr == None:
                jkr = self.jokers
        except:
            pass
        # Recursive function
        # find first 1 in matrix, check all melds (including chances+jokers, reduce num of jokers in this case) using this card
        # for each meld, recursive call checkMelds with new matrix, without the cards in the meld being considered
        # if no chances => return false, backtrack one step
        # base case => matrix is all 0s, return true
        # end of recursion case => if all melds lead to false, return false

        # Base case:
        if (matrix == self.compMatrix).all():
            if straightCount > 1 and pureFlag:
                print(
                    "Note: Additional jokers in hand may be excluded in following melds"
                )
                return True
            else:
                return False

        # Recursive case
        # search for straight melds on right side only, prevents overlap
        shp = np.shape(matrix)
        i, j = getFirstCard(matrix, shp)
        if j == 12:  # king
            right1 = right2 = right3 = (False, (i, j))
        elif j == 11:  # queen
            right1 = (bool(matrix[i][j + 1] == 1), (i, j + 1))
            right2 = (bool(matrix[i][0] == 1), (i, 0))
            right3 = (False, (i, j))
        elif j == 10:  # jack:
            right1 = (bool(matrix[i][j + 1] == 1), (i, j + 1))
            right2 = (bool(matrix[i][j + 2] == 1), (i, j + 2))
            right3 = (bool(matrix[i][0] == 1), (i, 0))
        else:
            right1 = (bool(matrix[i][j + 1] == 1), (i, j + 1))
            right2 = (bool(matrix[i][j + 2] == 1), (i, j + 2))
            right3 = (bool(matrix[i][j + 3] == 1), (i, j + 3))

        melds = []
        # no elif anywhere in case the other card needs to be used for something; considers all cases

        # straight melds
        # pure highest in order so it's considered first if possible
        if right1[0] and right2[0]:
            if right3[0]:
                melds.append(
                    [[(i, j), right1[1], right2[1], right3[1]], 1, 1]
                )  # priority 1
            melds.append([[(i, j), right1[1], right2[1]], 1, 1])  # priority 2
            if jkr:
                melds.append(
                    [[(i, j), right1[1], right2[1], "JKR"], 0, 1]
                )  # priority 3
        if right1[0] and jkr:
            if right3[0]:
                melds.append(
                    [[(i, j), right1[1], "JKR", right3[1]], 0, 1]
                )  # priority 4
            melds.append([[(i, j), right1[1], "JKR"], 0, 1])  # priority 5
        if right2[0] and jkr:
            if right3[0]:
                melds.append(
                    [[(i, j), "JKR", right2[1], right3[1]], 0, 1]
                )  # priority 6
            melds.append([[(i, j), "JKR", right2[1]], 0, 1])  # priority 7
        if jkr > 1:
            if right3[0]:
                melds.append([[(i, j), "JKR", "JKR", right3[1]], 0, 1])  # priority 8
            melds.append([[(i, j), "JKR", "JKR"], 0, 1])  # priority 9

        # same value melds
        j_vals = getSameValue(matrix, (i, j))
        if len(j_vals) == 3:
            melds.append(
                [[(i, j), j_vals[0], j_vals[1], j_vals[2]], 0, 0]
            )  # priority 10
            melds.append([[(i, j), j_vals[0], j_vals[1]], 0, 0])  # priority 11
            melds.append([[(i, j), j_vals[2], j_vals[1]], 0, 0])  # priority 12
            melds.append([[(i, j), j_vals[0], j_vals[2]], 0, 0])  # priority 13
            if jkr:
                melds.append(
                    [[(i, j), "JKR", j_vals[1], j_vals[2]], 0, 0]
                )  # priority 14
                melds.append(
                    [[(i, j), j_vals[0], "JKR", j_vals[2]], 0, 0]
                )  # priority 15
                melds.append(
                    [[(i, j), j_vals[0], j_vals[1], "JKR"], 0, 0]
                )  # priority 16
            if jkr > 1:
                melds.append([[(i, j), j_vals[0], "JKR", "JKR"], 0, 0])  # priority 17
                melds.append([[(i, j), j_vals[1], "JKR", "JKR"], 0, 0])  # priority 18
                melds.append([[(i, j), j_vals[2], "JKR", "JKR"], 0, 0])  # priority 19
        elif len(j_vals) == 2:
            melds.append([[(i, j), j_vals[0], j_vals[1]], 0, 0])  # priority 10
            if jkr:
                melds.append(
                    [[(i, j), j_vals[0], j_vals[1], "JKR"], 0, 0]
                )  # priority 11
                melds.append([[(i, j), "JKR", j_vals[1]], 0, 0])  # priority 12
                melds.append([[(i, j), j_vals[0], "JKR"], 0, 0])  # priority 13
        elif len(j_vals) == 1 and jkr:
            melds.append([[(i, j), j_vals[0], "JKR"], 0, 0])  # priority 10

        # print(melds)  # for debugging purposes only

        for (
            item
        ) in melds:  # if no melds, following block is skipped and it returns false
            meld = item[0]
            matrixCopy = matrix.copy()
            jkrCopy = jkr
            pureCopy = pureFlag
            straightCopy = straightCount
            if item[1]:
                pureCopy += 1
            if item[2]:
                straightCopy += 1
            for index in meld:
                if index == "JKR":
                    jkrCopy -= 1
                else:
                    matrixCopy[index[0]][index[1]] = 0
            if self.checkMelds(
                matrixCopy, jkrCopy, pureCopy, straightCopy
            ):  # recursive call
                print(meld)
                return True  # dfs match found
        return False  # no match in this dfs branch, backtracks one step

    def calculatePoints(self, matrix=None, jkr=None, pureFlag=0, pts=0, fullHand=None):
        try:
            if matrix == None:
                matrix = self.cardMatrix.copy()
        except:
            pass
        try:
            if jkr == None:
                jkr = self.jokers
        except:
            pass
        try:
            if fullHand == None:
                fullHand = 0
                for s in suitDict.keys():
                    i = suitDict[s]
                    for j in range(13):
                        if matrix[i][j] == 1:
                            fullHand += Card(j + 1, s).points
        except:
            pass

        # Recursive function
        # set "fullHand" to full points of hand if none
        # find first 1 in matrix, check all melds (including chances+jokers, reduce num of jokers in this case) using this card
        # to melds, always add just the card itself, in which case you increment "pts" by the card's points (this condition accounts for when card is left alone)
        # set min_temp to fullHand
        # for each meld, recursive call calculatePoints with new matrix, without the cards in the meld being considered
        # if value returned is less than min_temp, replace min_temp. Else, continue.
        # on evaluating all options, return min_temp
        # base case -> if matrix is all 0s: if pureFlag is 1, return pts. Else, return minpts.

        # Base case:
        if (matrix == self.compMatrix).all():
            if pureFlag:
                return pts
            else:
                return fullHand

        # Recursive case
        # search for straight melds on right side only, prevents overlap
        shp = np.shape(matrix)
        i, j = getFirstCard(matrix, shp)
        if j == 12:  # king
            right1 = right2 = right3 = (False, (i, j))
        elif j == 11:  # queen
            right1 = (bool(matrix[i][j + 1] == 1), (i, j + 1))
            right2 = (bool(matrix[i][0] == 1), (i, 0))
            right3 = (False, (i, j))
        elif j == 10:  # jack:
            right1 = (bool(matrix[i][j + 1] == 1), (i, j + 1))
            right2 = (bool(matrix[i][j + 2] == 1), (i, j + 2))
            right3 = (bool(matrix[i][0] == 1), (i, 0))
        else:
            right1 = (bool(matrix[i][j + 1] == 1), (i, j + 1))
            right2 = (bool(matrix[i][j + 2] == 1), (i, j + 2))
            right3 = (bool(matrix[i][j + 3] == 1), (i, j + 3))

        melds = []
        # no elif anywhere in case the other card needs to be used for something; considers all cases

        # straight melds
        # pure highest in order so it's considered first if possible
        if right1[0] and right2[0]:
            if right3[0]:
                melds.append(
                    [[(i, j), right1[1], right2[1], right3[1]], 1]
                )  # priority 1
            melds.append([[(i, j), right1[1], right2[1]], 1])  # priority 2
            if jkr:
                melds.append([[(i, j), right1[1], right2[1], "JKR"], 0])  # priority 3
        if right1[0] and jkr:
            if right3[0]:
                melds.append([[(i, j), right1[1], "JKR", right3[1]], 0])  # priority 4
            melds.append([[(i, j), right1[1], "JKR"], 0])  # priority 5
        if right2[0] and jkr:
            if right3[0]:
                melds.append([[(i, j), "JKR", right2[1], right3[1]], 0])  # priority 6
            melds.append([[(i, j), "JKR", right2[1]], 0])  # priority 7
        if jkr > 1:
            if right3[0]:
                melds.append([[(i, j), "JKR", "JKR", right3[1]], 0])  # priority 8
            melds.append([[(i, j), "JKR", "JKR"], 0])  # priority 9

        # same value melds
        j_vals = getSameValue(matrix, (i, j))
        if len(j_vals) == 3:
            melds.append([[(i, j), j_vals[0], j_vals[1], j_vals[2]], 0])  # priority 10
            melds.append([[(i, j), j_vals[0], j_vals[1]], 0])  # priority 11
            melds.append([[(i, j), j_vals[2], j_vals[1]], 0])  # priority 12
            melds.append([[(i, j), j_vals[0], j_vals[2]], 0])  # priority 13
            if jkr:
                melds.append([[(i, j), "JKR", j_vals[1], j_vals[2]], 0])  # priority 14
                melds.append([[(i, j), j_vals[0], "JKR", j_vals[2]], 0])  # priority 15
                melds.append([[(i, j), j_vals[0], j_vals[1], "JKR"], 0])  # priority 16
            if jkr > 1:
                melds.append([[(i, j), j_vals[0], "JKR", "JKR"], 0])  # priority 17
                melds.append([[(i, j), j_vals[1], "JKR", "JKR"], 0])  # priority 18
                melds.append([[(i, j), j_vals[2], "JKR", "JKR"], 0])  # priority 19
        elif len(j_vals) == 2:
            melds.append([[(i, j), j_vals[0], j_vals[1]], 0])  # priority 10
            if jkr:
                melds.append([[(i, j), j_vals[0], j_vals[1], "JKR"], 0])  # priority 11
                melds.append([[(i, j), "JKR", j_vals[1]], 0])  # priority 12
                melds.append([[(i, j), j_vals[0], "JKR"], 0])  # priority 13
        elif len(j_vals) == 1 and jkr:
            melds.append([[(i, j), j_vals[0], "JKR"], 0])  # priority 10

        # print(melds)  # for debugging purposes only
        melds.append(
            [[(i, j)], 0]
        )  # case where card is added to points and not considered for future melds
        min_temp = fullHand

        for item in melds:
            meld = item[0]
            matrixCopy = matrix.copy()
            jkrCopy = jkr
            pureCopy = pureFlag
            ptsCopy = pts
            if item[1]:
                pureCopy += 1
            if len(meld) == 1:
                for s in suitDict.keys():
                    if suitDict[s] == meld[0][0]:
                        ptsCopy += Card(meld[0][1] + 1, s).points
            for index in meld:
                if index == "JKR":
                    jkrCopy -= 1
                else:
                    matrixCopy[index[0]][index[1]] = 0
            min_temp = min(
                min_temp,
                self.calculatePoints(matrixCopy, jkrCopy, pureCopy, ptsCopy, fullHand),
            )  # recursive call
        return min_temp


float_formatter = "{:.0f}".format
np.set_printoptions(formatter={"float_kind": float_formatter})


def saveToDB(dataList, filename):
    resultStr = ",".join([str(x) for x in dataList]) + "\n"
    with open(filename, "a") as fileobj:
        fileobj.write(resultStr)


def resetDB(filename):
    with open(filename, "w") as fileobj:
        fileobj.write("winner,starter,turns,pts\n")


class GameMgr:
    def __init__(self, seed=None, gameMode="pvp", verbose=1):
        self.verbose = verbose
        self.deck = Deck()
        self.discardPile = DiscardPile()
        # self.Player1 = Player()
        # self.Player2 = Player()
        # initializes game state
        if gameMode == "avb":
            self.Players = [AdvancedAgent(), BasicAgent()]
        elif gameMode == "bva":
            self.Players = [BasicAgent(), AdvancedAgent()]
        elif gameMode == "ava":
            self.Players = [AdvancedAgent(), AdvancedAgent()]
        elif gameMode == "bvb":
            self.Players = [BasicAgent(), BasicAgent()]
        elif gameMode == "pvb":
            self.Players = [Player(), BasicAgent()]
        elif gameMode == "pva":
            self.Players = [Player(), AdvancedAgent()]
        else:
            self.Players = [Player(), Player()]

        self.DealGame(seed)

        if self.verbose:
            print("Hand 1:", self.Players[0].hand)
            print()
            print("Hand 2:", self.Players[1].hand)
            print()
            print(self.discardPile)
            print()
            print(self.deck)
            print("Joker:", self.deck.joker)
            print("Length of deck:", len(self.deck.cards))
            print()

        self.PlayPvP()

    def DealGame(self, seed):
        # initializes game state
        self.deck.shuffle(seed)
        self.deck.joker = self.deck.draw()
        for player in self.Players:
            player.hand.setJoker(self.deck.joker.value)
            if player.isObserving():
                player.initializeHeatmap(self.deck.joker.value)
            for _ in range(13):
                player.hand.draw(self.deck.draw())
            player.calculateMeldsAndChances()
        self.discardPile.discard(self.deck.draw())

    def PlayPvP(self):
        CurrentPlayer = random.randint(0, 1)
        starter = CurrentPlayer
        self.turn = 0
        while True:
            if self.Play(CurrentPlayer):
                break
            self.turn += 1
            if self.Players[CurrentPlayer].hand.checkMelds() == True:
                print(
                    "Player",
                    CurrentPlayer + 1,
                    "wins! (Player",
                    starter + 1,
                    "started)",
                )
                pts = self.Players[1 - CurrentPlayer].hand.calculatePoints()
                print("Player", CurrentPlayer + 1, "wins", pts, "points.")
                print("\n")
                saveToDB(
                    [CurrentPlayer + 1, starter + 1, self.turn, pts], "resultData.csv"
                )
                break
            CurrentPlayer = 1 - CurrentPlayer  # switches between 0 and 1
            if self.verbose:
                print("Turns completed:", self.turn)
                print("\n\n")

    def Play(self, CurrentPlayer):  # return true at any point to quit the game
        if self.verbose:
            print(int(CurrentPlayer + 1), "'s turn:")
            print("Hand:", self.Players[CurrentPlayer].hand)
            print(self.discardPile)
            print()
            print("Joker:", self.deck.joker)
            print()
            print(
                "Where do you want to?\nEnter \n'D' to draw from Deck \n'P' to draw from discard pile"
            )

        openCard = self.discardPile.cards[-1]
        while True:
            try:
                loc = self.Players[CurrentPlayer].getPickupChoice(openCard)
                if self.verbose:
                    print(loc)
                if loc == "D":
                    if not len(self.deck.cards):
                        print("Deck exhausted, it's a draw.")
                        return True
                    if self.Players[1 - CurrentPlayer].isObserving:
                        self.Players[1 - CurrentPlayer].opponentPickChoice(
                            openCard, False
                        )
                        # print(self.Players[1-CurrentPlayer].heatmap)
                    self.Players[CurrentPlayer].hand.draw(
                        self.deck.draw()
                    )  # assumes the agent does not pick up and discard the open card, remember to test later
                elif loc == "P":
                    if self.Players[1 - CurrentPlayer].isObserving:
                        self.Players[1 - CurrentPlayer].opponentPickChoice(
                            openCard, True
                        )
                        # print(self.Players[1-CurrentPlayer].heatmap)
                    self.Players[CurrentPlayer].hand.draw(self.discardPile.draw())
                else:
                    raise ValueError
                break
            except ValueError:
                print("Error - incorrect input, try again:")
                continue
        self.Players[CurrentPlayer].calculateMeldsAndChances()
        if self.verbose:
            print(
                "index: ",
                "".join(
                    [
                        str(x) + "     "
                        for x in range(0, len(self.Players[CurrentPlayer].hand.cards))
                    ]
                ),
            )
            print("Hand:", self.Players[CurrentPlayer].hand)
            print("Enter index of card to disard:")
        while True:
            try:
                ind = int(self.Players[CurrentPlayer].getDiscardChoice())
                if self.verbose:
                    print(ind)
                self.discardPile.discard(self.Players[CurrentPlayer].hand.discard(ind))
                self.Players[CurrentPlayer].calculateMeldsAndChances()
                self.Players[CurrentPlayer].discardHistory.append(
                    self.discardPile.cards[-1]
                )
                if self.Players[1 - CurrentPlayer].isObserving:
                    self.Players[1 - CurrentPlayer].opponentDiscards(
                        self.discardPile.cards[-1]
                    )
                    # print(self.Players[1-CurrentPlayer].heatmap)
                break
            except:
                print("Error - invalid choice, try again:", ind)
                continue
        if self.verbose:
            print("Hand:", self.Players[CurrentPlayer].hand)


class Player:  # by default, it's a real user. Agents inherit from this class.
    def __init__(self):
        self.hand = Hand()
        self.melds = []
        self.chances = []
        self.discardHistory = []
        # self.heatmap = []

    def getPickupChoice(self, openCard):
        # print("Top of discard pile:", openCard)
        return input()

    def getDiscardChoice(self):
        return input()

    def calculateMeldsAndChances(
        self,
    ):  # populates melds and chances without modifying hand
        # TODO: needs to be written by Abhishek
        suite_list = ["S", "H", "C", "D"]
        self.melds = []
        self.chances = []
        a = self.hand.cardMatrix.copy()
        for i in range(4):
            for j in range(13):
                if a[i][j] == 1:
                    if j != 12 and a[i][(j + 1) % 13] == 1 and a[i][(j + 2) % 13] == 1:
                        if j != 11 and a[i][(j + 3) % 13] == 1:
                            self.melds.append(
                                [
                                    Card((j) % 13 + 1, suite_list[i]),
                                    Card((j + 1) % 13 + 1, suite_list[i]),
                                    Card((j + 2) % 13 + 1, suite_list[i]),
                                    Card((j + 3) % 13 + 1, suite_list[i]),
                                ]
                            )
                        else:
                            self.melds.append(
                                [
                                    Card((j) % 13 + 1, suite_list[i]),
                                    Card((j + 1) % 13 + 1, suite_list[i]),
                                    Card((j + 2) % 13 + 1, suite_list[i]),
                                ]
                            )

        straightMeldCards = list(
            set([card for sublist in self.melds for card in sublist])
        )
        for card in straightMeldCards:
            a[suitDict[card.suit]][card.value - 1] = 0

        for j in range(13):
            temp = []
            for k in range(4):
                if a[k][j] == 1:
                    temp.append(Card(j + 1, suite_list[k]))
            if len(temp) >= 3:
                self.melds.append(temp)

        meldCards = list(set([card for sublist in self.melds for card in sublist]))

        for i in range(4):
            for j in range(13):
                if a[i][j] == 1:
                    first = (j + 1) % 13
                    second = (j + 2) % 13
                    third = (j + 3) % 13
                    if j != 12 and (a[i][first] == 1 or a[i][second] == 1):
                        temp = []
                        temp.append(Card(j + 1, suite_list[i]))
                        if a[i][first] == 1:
                            temp.append(Card(first + 1, suite_list[i]))
                        if a[i][second] == 1:
                            temp.append(Card(second + 1, suite_list[i]))
                        if j != 11 and a[i][third] == 1:
                            temp.append(Card(third + 1, suite_list[i]))
                        self.chances.append(temp)

        for card in meldCards:
            a[suitDict[card.suit]][card.value - 1] = 0

        for j in range(13):
            temp = []
            for i in range(4):
                if a[i][j] == 1:
                    temp.append(Card(j + 1, suite_list[i]))
            if len(temp) == 2:
                self.chances.append(temp)

    # def updateMeldsAndChances(self, card, RemoveFlag=False): # updates melds and chances without modifying hand
    #     # TODO: needs to be written by Abhishek
    #     # RemoveFlag: True - remove card, False - add card
    #     pass

    def calculatePickup(
        self, openCard
    ):  # same logic for both agents so I'm coding it here. Not used by user.
        # return 'D' or 'P'
        ## Calculate all flags first before picking up....

        self.calculateMeldsAndChances()

        flag4carder = 0
        for meld in self.melds:
            if len(meld) >= 4:
                flag4carder += 1

        flagPureSeq = 0
        for meld in self.melds:
            if meld[0].value != meld[0].value:
                flagPureSeq += 1

        countMelds = len(self.melds)
        countChances = len(self.chances)

        # cases for picking up from discard pile
        # priority 1: Check if the card on top of discard pile is a Joker, pickup
        if openCard.value == -1 or openCard.value == self.hand.rummyJokerVal:
            return "P"

        if (
            openCard in self.discardHistory
        ):  # don't pick up a card you've discarded before
            return "D"

        # Assume we pickup a card that is not joker. Recalculate the melds and chances, if the recalculated satisfies, we pickup from the pile
        self.hand.draw(openCard)
        self.calculateMeldsAndChances()
        breakFlag = 0
        if (
            self.getDiscardChoice() == 13
        ):  # don't pick up a card if it's your best discard option immediately after
            breakFlag = 1
        self.hand.discard(13)
        if breakFlag:
            return "D"

        # priority 2: Check if the card on top of discard pile forms a pure Sequence:
        flagPureSeqUpd = 0
        for meld in self.melds:
            if meld[0].value != meld[0].value:
                flagPureSeqUpd += 1

        if flagPureSeqUpd > flagPureSeq:
            return "P"

        # priority 3: Check if the card on top of discard pile forms a 4 carder Sequence
        flag4carderUpd = 0
        for meld in self.melds:
            if len(meld) >= 4:
                flag4carderUpd += 1

        if flag4carderUpd > flag4carder:
            return "P"
        # priority 4: Check if there is any new Sequences created
        countMeldsUpd = len(self.melds)
        if countMeldsUpd > countMelds:
            return "P"
        # priority 5: Check any new chance is created
        countChancesUpd = len(self.chances)
        if countChancesUpd > countChances:
            return "P"
        # Else Pickup from Deck(return D).
        # Remove the card that we picked up from the discard pile
        return "D"

    def isObserving(
        self,
    ):  # info is passed to player if it is "observing", true for only advanced agent
        return False

    # dummy function for inheritance purposes (used by AdvancedAgent)
    def opponentPickChoice(self, openCard, action):
        pass

    # dummy function for inheritance purposes (used by AdvancedAgent)
    def opponentDiscards(self, openCard):
        pass


class BasicAgent(Player):
    def getPickupChoice(self, openCard):
        return self.calculatePickup(openCard)

    def getDiscardChoice(self):  # TODO: update melds and chances at the end
        # print(self.melds)
        # print(self.chances)
        useful = [item for sublist in self.melds + self.chances for item in sublist]
        useful = list(set(useful))
        junk = [
            card
            for card in self.hand.cards
            if (
                card not in useful
                and card.value != -1
                and card.value != self.hand.rummyJokerVal
            )
        ]

        if len(junk):
            junk.sort(key=lambda x: (x.points, x.value, str(x)), reverse=True)
            # print("Discarding Junk")
            return self.hand.cards.index(junk[0])  # discards junk card of highest value

        # if no junk cards, needs to break chances in following order of priority:
        # 1. 4-carder chance if 4-carder already exists (discard the single card on one side of the gap)
        # 2. same number chance card that isn't in a straight chance, but the other card of the chance is, of highest value
        # 3. same number chance where neither card is in a straight chance, of highest value
        # 4. straight sequence chance with a gap, of highest value
        # 5. highest card not in a sequence

        discardOptions = []

        # -------------------------------------- Priority #1 -----------------------------------------------
        flag4carder = 0
        for meld in self.melds:
            if len(meld) == 4:
                flag4carder = 1
                break
        if flag4carder:
            for chance in self.chances:
                if len(chance) == 3:
                    chanceCopy = sorted(chance, key=lambda x: x.value)
                    # figuring out which of the 3 is alone on one side of the gap in this 4-carder straight chance
                    i = chanceCopy[0].value
                    if chanceCopy[1].value != i + 1:
                        discardOptions.append(chanceCopy[0])
                    else:
                        discardOptions.append(chanceCopy[2])
        if len(discardOptions):
            discardOptions = sorted(
                list(set(discardOptions)),
                key=lambda x: (x.points, x.value, str(x)),
                reverse=True,
            )
            # print("Priority 1")
            return self.hand.cards.index(discardOptions[0])

        # -------------------------------------- Priority #2 -----------------------------------------------
        sameNumChanceCards = []
        straightChanceCards = []
        for chance in self.chances:
            if chance[0].value == chance[1].value:
                sameNumChanceCards.extend(chance)
            else:
                straightChanceCards.extend(chance)
        sameNumChanceCards = sorted(
            list(set(sameNumChanceCards)), key=lambda x: x.value, reverse=True
        )
        straightChanceCards = sorted(
            list(set(straightChanceCards)), key=lambda x: x.value, reverse=True
        )

        for card in sameNumChanceCards:
            if card not in straightChanceCards:
                for card2 in sameNumChanceCards:
                    if card2.value == card.value and card != card2:
                        if card2 in straightChanceCards:
                            discardOptions.append(card)
                            break
        if len(discardOptions):
            discardOptions = sorted(
                list(set(discardOptions)),
                key=lambda x: (x.points, x.value, str(x)),
                reverse=True,
            )
            # print("Priority 2")
            return self.hand.cards.index(discardOptions[0])

        # -------------------------------------- Priority #3 -----------------------------------------------
        discardOptions = sameNumChanceCards.copy()
        if len(discardOptions):
            discardOptions = sorted(
                list(set(discardOptions)),
                key=lambda x: (x.points, x.value, str(x)),
                reverse=True,
            )
            # print("Priority 3")
            return self.hand.cards.index(discardOptions[0])

        # -------------------------------------- Priority #4 -----------------------------------------------
        meldCards = [item for sublist in self.melds for item in sublist]
        for chance in self.chances:
            if len(chance) == 2 and abs(chance[0].value - chance[1].value) in [
                2,
                11,
                12,
            ]:  # includes AQ and AK as gap chances
                discardOptions.extend(chance)
        discardOptions = [
            card for card in discardOptions if card not in meldCards
        ]  # necessary because overlaps happen
        if len(discardOptions):
            # print(discardOptions)
            discardOptions = sorted(
                list(set(discardOptions)),
                key=lambda x: (x.points, x.value, str(x)),
                reverse=True,
            )
            # print("Priority 4")
            # print(discardOptions)
            return self.hand.cards.index(discardOptions[0])

        # -------------------------------------- Priority #5 -----------------------------------------------
        discardOptions = straightChanceCards.copy()
        discardOptions = [
            card for card in discardOptions if card not in meldCards
        ]  # necessary because overlaps happen
        if len(discardOptions):
            discardOptions = sorted(
                list(set(discardOptions)),
                key=lambda x: (x.points, x.value, str(x)),
                reverse=True,
            )
            # print("Priority 5")
            return self.hand.cards.index(discardOptions[0])

        # ------------------------------------ Error Handling ----------------------------------------------
        # if it got this far, there are no chances, no junk cards, only melds.
        # since there are 14 cards, there's either two melds of 4 cards or one meld with 5+.
        # so, we can remove one card from the end of the longest meld and win regardless.
        # extra error handling - if all lists are empty, just return 0, though it'll probably break anyway.

        print("Last priority encountered")
        try:
            meldCopy = sorted(self.melds, key=lambda x: len(x), reverse=True)
            longestMeld = meldCopy[0]
            longestMeld.sort(key=lambda x: x.value, reverse=True)
            return self.hand.cards.index(longestMeld[0])
        except:
            return 0


class AdvancedAgent(Player):  # TODO: override getDiscardChoice()
    def __init__(self):
        super().__init__()
        self.heatmap = np.zeros(
            (4, 13)
        )  # keeps track of the cards the opponent needs, +ve means opponent needs it more

    def getPickupChoice(self, openCard):
        return self.calculatePickup(openCard)

    def isObserving(self):
        return True

    def initializeHeatmap(self, jokerVal):
        if jokerVal == -1:  # joker card is rummy joker drawn at start of round
            return
        for i in range(4):
            # setting as large value because agent absolutely cannot throw jokers away. Not np.inf because it's used to track opponent's cards
            self.heatmap[i][jokerVal - 1] = 10**5
            self.heatmap[i][jokerVal - 1] = 10**5

    def opponentPickChoice(
        self, openCard, action
    ):  # action is boolean for whether opponent picked up open card
        # TODO: update heatmap
        if openCard.value == -1 or openCard.value == self.hand.rummyJokerVal:
            return
        if action:  # opponent picks up open card
            # update heatmap to show that opponent has that card, also increase value of surrounding cards
            # if opponent has nearby card, increase value for that chance more
            self.heatmap[suitDict[openCard.suit]][openCard.value - 1] = np.inf

            # horizontal increments
            immLeft = (openCard.value - 2) % 13
            immRight = openCard.value % 13
            skipLeft = (openCard.value - 3) % 13
            skipRight = (openCard.value + 1) % 13
            # when we know opponent has cards on immediate right or immediate left, increase value of first unknown card on left and right
            if (
                self.heatmap[suitDict[openCard.suit]][immLeft] == np.inf
                or self.heatmap[suitDict[openCard.suit]][immRight] == np.inf
            ):
                k = immLeft
                while k >= 0:
                    if self.heatmap[suitDict[openCard.suit]][k] != np.inf:
                        self.heatmap[suitDict[openCard.suit]][k] += 50
                        break
                    k -= 1
                k = immRight
                while k <= 13:
                    if self.heatmap[suitDict[openCard.suit]][k % 13] != np.inf:
                        self.heatmap[suitDict[openCard.suit]][k % 13] += 50
                        break
                    k += 1
            # when a gap chance is created, increase value for gap by a lot, and surroundings by a bit (4-carder chance)
            elif (
                immLeft != 0
                and self.heatmap[suitDict[openCard.suit]][skipLeft] == np.inf
            ) or (
                immRight != 0
                and self.heatmap[suitDict[openCard.suit]][skipRight] == np.inf
            ):
                if (
                    immLeft != 0
                    and self.heatmap[suitDict[openCard.suit]][skipLeft] == np.inf
                ):
                    self.heatmap[suitDict[openCard.suit]][immLeft] += 50
                    self.heatmap[suitDict[openCard.suit]][immRight] += 5
                    self.heatmap[suitDict[openCard.suit]][(skipLeft - 1) % 13] += 5
                if (
                    immRight != 0
                    and self.heatmap[suitDict[openCard.suit]][skipRight] == np.inf
                ):
                    self.heatmap[suitDict[openCard.suit]][immRight] += 50
                    self.heatmap[suitDict[openCard.suit]][immLeft] += 5
                    if immRight <= 11:
                        self.heatmap[suitDict[openCard.suit]][(skipRight + 1) % 13] += 5
            # nothing known in two card horizontal surrounding, increment all by a small amount
            else:
                self.heatmap[suitDict[openCard.suit]][immRight] += 2
                self.heatmap[suitDict[openCard.suit]][immLeft] += 2
                if immLeft != 0:
                    self.heatmap[suitDict[openCard.suit]][skipLeft] += 1
                if immRight != 0:
                    self.heatmap[suitDict[openCard.suit]][skipRight] += 1

            # Vertical increments
            vert = [
                (i, openCard.value - 1)
                for i in range(4)
                if i != suitDict[openCard.suit]
            ]
            flag = False
            for index in vert:
                if self.heatmap[index[0]][index[1]] == np.inf:
                    flag = True
                    break
            if flag:
                # another card of the same value is known to be in the opponent's hand
                for index in vert:
                    self.heatmap[index[0]][index[1]] += 10
            else:
                for index in vert:
                    self.heatmap[index[0]][index[1]] += 2

        else:  # opponent does not pick up open card
            # update heatmap to show that the card is buried till the end of the deck
            # decrease value of surrounding cards
            # if opponent has a nearby card, increase value of the cards related to that card but unrelated to this one
            self.opponentDiscards(
                openCard
            )  # assuming that the opponent not picking up a card is the same as discarding it

    def opponentDiscards(self, openCard):
        # TODO: update heatmap
        # decrease value of surrounding cards
        # if opponent has a nearby card, increase value of the cards related to that card but unrelated to this one
        if self.heatmap[suitDict[openCard.suit]][openCard.value - 1] != -np.inf:
            self.heatmap[suitDict[openCard.suit]][openCard.value - 1] = -np.inf
        else:  # error handling, prevents a previously ignored/discarded card from counting twice
            return

        immLeft = (openCard.value - 2) % 13
        immRight = openCard.value % 13

        if self.heatmap[suitDict[openCard.suit]][immLeft] == np.inf:
            self.heatmap[suitDict[openCard.suit]][immRight] -= 2
            for k in range(4):
                self.heatmap[k][immLeft] += 10
        else:
            self.heatmap[suitDict[openCard.suit]][immLeft] -= 2
        if self.heatmap[suitDict[openCard.suit]][immRight] == np.inf:
            self.heatmap[suitDict[openCard.suit]][immLeft] -= 2
            for k in range(4):
                self.heatmap[k][immRight] += 10
        else:
            self.heatmap[suitDict[openCard.suit]][immRight] -= 2
        for k in range(4):
            if self.heatmap[k][openCard.value - 1] == np.inf:
                self.heatmap[k][immLeft] += 10
                self.heatmap[k][immRight] += 10
            else:
                self.heatmap[k][openCard.value - 1] -= 10

    # EXACTLY THE SAME AS BASIC AGENT EXCEPT IT DISCARDS BY LOWEST HEATMAP VALUE, NOT HIGHEST CARD VALUE
    def getDiscardChoice(self):  # TODO: update melds and chances at the end
        useful = [item for sublist in self.melds + self.chances for item in sublist]
        useful = list(set(useful))
        junk = [
            card
            for card in self.hand.cards
            if (
                card not in useful
                and card.value != -1
                and card.value != self.hand.rummyJokerVal
            )
        ]

        # if len(junk):
        #     junk.sort(key=lambda x: (self.heatmap[suitDict[x.suit]][x.value-1], -x.points), reverse=False)
        #     return self.hand.cards.index(junk[0])  # discards junk card of highest value

        # if no junk cards, needs to break chances in following order of priority:
        # 1. 4-carder chance if 4-carder already exists (discard the single card on one side of the gap)
        # 2. same number chance card that isn't in a straight chance, but the other card of the chance is, of lowest heatmap value
        # 3. same number chance where neither card is in a straight chance, of lowest heatmap value
        # 4. straight sequence chance with a gap, of lowest heatmap value
        # 5. lowest heatmap value card not in a sequence

        # discardOptions = []
        discardOptions = junk.copy()

        # -------------------------------------- Priority #1 -----------------------------------------------
        flag4carder = 0
        for meld in self.melds:
            if len(meld) == 4:
                flag4carder = 1
                break
        if flag4carder:
            for chance in self.chances:
                if len(chance) == 3:
                    chanceCopy = sorted(chance, key=lambda x: x.value)
                    # figuring out which of the 3 is alone on one side of the gap in this 4-carder straight chance
                    i = chanceCopy[0].value
                    if chanceCopy[1].value != i + 1:
                        discardOptions.append(chanceCopy[0])
                    else:
                        discardOptions.append(chanceCopy[2])
        if len(discardOptions):
            discardOptions = sorted(
                list(set(discardOptions)),
                key=lambda x: (self.heatmap[suitDict[x.suit]][x.value - 1], -x.points),
                reverse=False,
            )
            return self.hand.cards.index(discardOptions[0])

        # -------------------------------------- Priority #2 -----------------------------------------------
        sameNumChanceCards = []
        straightChanceCards = []
        for chance in self.chances:
            if chance[0].value == chance[1].value:
                sameNumChanceCards.extend(chance)
            else:
                straightChanceCards.extend(chance)
        sameNumChanceCards = sorted(
            list(set(sameNumChanceCards)), key=lambda x: x.value, reverse=True
        )
        straightChanceCards = sorted(
            list(set(straightChanceCards)), key=lambda x: x.value, reverse=True
        )

        # for card in sameNumChanceCards:
        #     if card not in straightChanceCards:
        #         for card2 in sameNumChanceCards:
        #             if card2.value == card.value and card != card2:
        #                 if card2 in straightChanceCards:
        #                     discardOptions.append(card)
        #                     break
        # if len(discardOptions):
        #     discardOptions = sorted(list(set(discardOptions)), key=lambda x: (self.heatmap[suitDict[x.suit]][x.value-1], -x.points), reverse=False)
        #     return self.hand.cards.index(discardOptions[0])

        # -------------------------------------- Priority #3 -----------------------------------------------
        # discardOptions = sameNumChanceCards.copy()
        discardOptions = [
            card for card in sameNumChanceCards if card not in straightChanceCards
        ]
        if len(discardOptions):
            discardOptions = sorted(
                list(set(discardOptions)),
                key=lambda x: (self.heatmap[suitDict[x.suit]][x.value - 1], -x.points),
                reverse=False,
            )
            return self.hand.cards.index(discardOptions[0])

        # -------------------------------------- Priority #4 -----------------------------------------------
        meldCards = [item for sublist in self.melds for item in sublist]
        for chance in self.chances:
            if len(chance) == 2 and abs(chance[0].value - chance[1].value) in [
                2,
                11,
                12,
            ]:  # includes AQ and AK as gap chances
                discardOptions.extend(chance)
        discardOptions = [
            card for card in discardOptions if card not in meldCards
        ]  # necessary because overlaps happen
        if len(discardOptions):
            discardOptions = sorted(
                list(set(discardOptions)),
                key=lambda x: (self.heatmap[suitDict[x.suit]][x.value - 1], -x.points),
                reverse=False,
            )
            return self.hand.cards.index(discardOptions[0])

        # -------------------------------------- Priority #5 -----------------------------------------------
        discardOptions = straightChanceCards.copy()
        discardOptions = [
            card for card in discardOptions if card not in meldCards
        ]  # necessary because overlaps happen
        if len(discardOptions):
            discardOptions = sorted(
                list(set(discardOptions)),
                key=lambda x: (self.heatmap[suitDict[x.suit]][x.value - 1], -x.points),
                reverse=False,
            )
            return self.hand.cards.index(discardOptions[0])

        # ------------------------------------ Error Handling ----------------------------------------------
        # if it got this far, there are no chances, no junk cards, only melds.
        # since there are 14 cards, there's either two melds of 4 cards or one meld with 5+.
        # so, we can remove one card from the end of the longest meld and win regardless.
        # extra error handling - if all lists are empty, just return 0, though it'll probably break anyway.

        try:
            meldCopy = sorted(self.melds, key=lambda x: len(x), reverse=True)
            longestMeld = meldCopy[0]
            longestMeld.sort(key=lambda x: x.value, reverse=True)
            return self.hand.cards.index(longestMeld[0])
        except:
            return 0

@initialize_intpy(__file__)
def main(n1=1, n2=10):
    for s in range(n1, n1 + n2):
        GameMgr(s, gameMode="avb", verbose=0)


if __name__ == "__main__":
    # resetDB("resultData.csv")
    """
    Uncomment the following 3 lines to reproduce experiment for the paper.
    current mode is avb(experiment), Change to bvb for control data
    """
    n1 = int(sys.argv[1])
    n2 = int(sys.argv[2])
    
    t0 = time.perf_counter()
    main(n1, n2)
    print(time.perf_counter()-t0)
    """ Repository for general use"""
    # import argparse
    # import sys
    
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-seed', type=int, help='Seed to fix game(int)')
    # parser.add_argument('-gm', '--gameMode', default="pva", help='To set Game mode: pva, pvb, avb, bvb, ava, pvp')
    # parser.add_argument('-v', '--verbose', type=int, default=0, help='Enable terminal logging(int): 0=no logs, 1=logs')
    # args = parser.parse_args()
    # print(args)
    # GameMgr(seed=args.seed, gameMode=args.gameMode, verbose=args.verbose)
