#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Pig game """


import random
import argparse
import sys


parser = argparse.ArgumentParser()
parser.add_argument('--numPlayers', help='number of players in game')
args = parser.parse_args()


class Dice(object):
    def __init__(self, sides=6):
        self.sides = sides

    def roll(self):
        return random.randint(1, self.sides)


class Player(object):
    def __init__(self):
        self.score = 0
        self.name = 'Player'

    def addToScore(self, amount):
        self.score += amount


class Game(object):
    def __init__(self, playerCount):
        self.playerIdx = 0
        self.turnScore = 0
        self.players = []
        self.dice = Dice()
        for i in range(1, int(playerCount) + 1):
            player = Player()
            player.name = player.name + ' ' + str(i)
            self.players.append(player)
        self.currentPlayer = self.players[self.playerIdx]


    def ask(self):
        '''User input to decide whether to roll or hold. Returns T/F'''

        print '---' + self.currentPlayer.name + '---'
        choice = raw_input("Do you want to roll or hold? (r/h): ")
        while choice.lower()[0] != 'r' and choice.lower()[0] != 'h':
            print "Sorry, I don't understand."
            choice = raw_input("Do you want to roll or hold? (r/h): ")
        else:
            if choice == 'r':
                return True
            elif choice == 'h':
                return False


    def maxScore(self):
        '''Keeps track of the highest score, updates accordingly'''

        maxScore = 0
        for player in self.players:
            if (player.score > maxScore):
                maxScore = player.score
        return maxScore


    def changePlayer(self):
        self.playerIdx = (self.playerIdx + 1) % 2
        self.turnScore = 0
        self.currentPlayer = self.players[self.playerIdx]


    def turn(self):
        '''Simulates when the dice is rolled (or not)'''

        rolled = self.dice.roll()
        print '\n' + self.currentPlayer.name + ', you rolled ' + str(rolled)
        if rolled == 1:
            print 'You rolled a 1 , your turn is over. You lost ' + \
                str(self.turnScore) + ' possible points.'
            print 'Your current score is ' + str(self.currentPlayer.score) + \
            '\n'
            self.changePlayer()
            print 'Next up: ' + self.currentPlayer.name
        else:
            self.turnScore += rolled
            print 'Your score this turn is ' + str(self.turnScore)
            print 'Your overall saved score is ' + \
            str(self.currentPlayer.score) + '\n'


    def addToScore(self):
        self.currentPlayer.addToScore(self.turnScore)


def main():
    playerCount = args.numPlayers
    game = Game(playerCount)

    print 'Up first is ' + game.currentPlayer.name
    while game.maxScore() < 100:
        if game.ask():
            game.turn()
        else:
            game.addToScore()
            if game.currentPlayer.score >= 100:
                break

            print'You decided to keep {0}\n'.format(game.currentPlayer.score)
            game.changePlayer()
            print 'Next up: ' + game.currentPlayer.name

    print('''\n*******************
        \n{0} wins with a score of {1}
        \n*******************'''.format(
        game.currentPlayer.name, game.currentPlayer.score))
    sys.exit()

    main()
