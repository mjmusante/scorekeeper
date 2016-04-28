#! /usr/bin/python

from __future__ import print_function

import sys

with open("results.txt", "r") as f:
    lines = f.readlines()

class Player:
    def __init__(self, name):
        self.name = name
        self.opponent = {}
        self.vs_opponent = {}
        self.games_vs = {}
        self.points_for = 0
        self.points_against = 0

    def add_result(self, op, game, myscore, opscore):
        self.points_for += myscore
        self.points_against += opscore
        if op not in self.opponent:
            self.opponent[op] = [(), (), (), (), ()]
            self.vs_opponent[op] = 0
            self.games_vs[op] = 0
        self.opponent[op][game - 1] = (myscore, opscore)
        self.games_vs[op] += 1
        if myscore > opscore:
            self.vs_opponent[op] += 10
        elif myscore == opscore:
            self.vs_opponent[op] += 5
        print("op %s game %s -> %s to %s" % (op, game, myscore, opscore))

    def fmt_result(self, oplist):
        for i in oplist:
            if i in self.opponent:
                for score in self.opponent[i]:
                    if score:
                        if score[0] > score[1]:
                            print("1  ", end="")
                        elif score[0] == score[1]:
                            print("&frac12;  ", end="")
                        else:
                            print("0  ", end="")
                    else:
                        print("   ", end="")
            else:
                print("               ", end="")
            print("| ", end="")
        print("")

#
# Format of the file we're reading in:
# - lines which start with "p " give the player name
# - lines which start with "g " provide game results
# - all other lines are ignored
#
# Example of p:
# p player1
# p player2
#
# Example of g:
# g 3 player1:23,player2:45
#
# Format is: "game_number player:score,player:score"
#

player = {}
maxlen = 0
for l in lines:
    v = l.split()
    if v[0] == "p":
        player[v[1]] = (Player(v[1]))
        maxlen = max(maxlen, len(v[1]))
    elif v[0] == "g":
        game = int(v[1])
        rslt = v[2].split(",")
        p1 = rslt[0].split(":")
        p2 = rslt[1].split(":")
        p1sc = int(p1[1])
        p2sc = int(p2[1])

        if p1[0] not in player:
            print("Player %s not defined" % p1[0])
            sys.exit(1)
        if p2[0] not in player:
            print("Player %s not defined" % p2[0])
            sys.exit(1)

        player[p1[0]].add_result(p2[0], game, p1sc, p2sc)
        player[p2[0]].add_result(p1[0], game, p2sc, p1sc)

fmt = "%%%ss" % maxlen
lfmt = "  %%-%ss" % maxlen
pad = 15 - maxlen  # 15 magic number comes from 5 games * 3 spaces per game
plist = sorted(player, key=lambda s: s.lower())

print("Results:")
print(fmt % "", end="")
for p in plist:
    print(lfmt % p, end="")
    print(" " * pad, end="")
print("")

print(fmt % "", end="")
print(" ", end="")
for p in plist:
    print(" 1  2  3  4  5  |", end="")
print("")

for p in plist:
    print(fmt % p, end="")
    print(": ", end="")
    player[p].fmt_result(plist)

print("---")

print("Match wins:")
for p in plist:
    wins = 0
    losses = 0
    ties = 0
    for op in player[p].vs_opponent:
        if player[p].games_vs[op] < 5:
            continue
        rslt = player[p].vs_opponent[op]
        print("player %s r %s" % (p, rslt))
        if rslt > 25:
            wins += 1
        elif rslt < 25:
            losses += 1
        else:
            ties += 1
    if wins > 0 or ties > 0 or losses > 0:
        print("%s: " % p, end="")
        if wins > 0:
            print("%s wins" % wins, end="")
        if ties > 0:
            print("%s ties" % ties, end="")
        if losses > 0:
            print("%s losses" % losses, end="")
        print("")

print("---")

print("Total points:")
for p in plist:
    print(lfmt % p, end="")
    print(" %10s points for / %10s points against" % \
            (player[p].points_for, player[p].points_against))
