#! /usr/bin/python

from __future__ import print_function

import sys

with open(sys.argv[1], "r") as f:
    lines = f.readlines()

class Player:
    def __init__(self, name):
        self.name = name
        self.opponent = {}
        self.vs_opponent = {}
        self.games_vs = {}
        self.points_for = 0
        self.points_against = 0

    def won_game(self, rslt):
        sc1, sc2, turn = rslt
        return (sc1 > sc2) or (sc1 == sc2 and turn == 2)

    # op -> name of opponent
    # game -> game number against this opponent
    # myscore -> score for this player for this game
    # opscore -> score for opponent for this game
    # turn -> 1 if first player, 2 if second player
    def add_result(self, op, game, myscore, opscore, turn):
        self.points_for += myscore
        self.points_against += opscore
        if op not in self.opponent:
            self.opponent[op] = [(), (), (), (), ()]
            self.vs_opponent[op] = 0
            self.games_vs[op] = 0
        self.opponent[op][game - 1] = (myscore, opscore, turn)
        self.games_vs[op] += 1
        if self.won_game(self.opponent[op][game - 1]):
            self.vs_opponent[op] += 1

    def fmt_result(self, oplist):
        won = 0
        for i in oplist:
            if i in self.opponent:
                for score in self.opponent[i]:
                    if score:
                        if self.won_game(score):
                            print("1  ", end="")
                            won += 1
                        else:
                            print("0  ", end="")
                    else:
                        print("   ", end="")
            elif i == self.name:
                print("-  -  -  -  -  ", end="")
            else:
                print("               ", end="")
            print("| ", end="")
        print("%2s" % won)

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
    l = l.rstrip()
    if not l:
        continue
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

        player[p1[0]].add_result(p2[0], game, p1sc, p2sc, 1)
        player[p2[0]].add_result(p1[0], game, p2sc, p1sc, 2)

fmt = "%%%ss" % maxlen
lfmt = "  %%-%ss" % maxlen
pad = 15 - maxlen  # 15 magic number comes from 5 games * 3 spaces per game
plist = sorted(player, key=lambda s: s.lower())

print("Game Results:")
print(fmt % "", end="")
for p in plist:
    print(lfmt % p, end="")
    print(" " * pad, end="")
print("")

print(fmt % "", end="")
print(" ", end="")
for p in plist:
    print(" 1  2  3  4  5  |", end="")
print(" Total Games Won")

for p in plist:
    print(fmt % p, end="")
    print(": ", end="")
    player[p].fmt_result(plist)

print("---")

print("Match Results:")
for p in plist:
    wins = 0
    losses = 0
    for op in player[p].vs_opponent:
        if player[p].games_vs[op] < 5:
            continue
        rslt = player[p].vs_opponent[op]
        if rslt > 2:
            wins += 1
        elif rslt <= 2:
            losses += 1
    if wins > 0 or losses > 0:
        print("%s%s: " % (" " * (pad - len(p)), p), end="")
        match = list()

        def sing_or_pl(score, sing, pl):
            if score == 1:
                return "%s %s" % (score, sing)
            return "%s %s" % (score, pl)

        if wins > 0:
            match.append(sing_or_pl(wins, "win", "wins"))
        if losses > 0:
            match.append(sing_or_pl(losses, "loss", "losses"))
        print(", ".join(match))

print("---")

print("Total Points:")
for p in plist:
    print(lfmt % p, end="")
    print(" %10s points for / %10s points against" % \
            (player[p].points_for, player[p].points_against))
