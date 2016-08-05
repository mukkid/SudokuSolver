#!/usr/bin/python

import math
import numpy
from copy import deepcopy
import sys

test1 = [[3,4,0,2],
        [1,0,0,0],
        [0,0,0,1],
        [2,0,4,3]]
test2 = [[0,0,3,5,4,6,0,0,0],
         [9,0,0,0,1,8,0,0,7],
         [0,5,1,3,0,0,4,2,0],
         [0,0,9,2,0,0,0,8,0],
         [0,5,0,6,0,3,0,7,0],
         [0,3,0,0,0,4,2,0,0],
         [0,9,7,0,0,1,8,5,0],
         [3,0,0,8,2,0,0,0,4],
         [0,0,0,9,4,7,6,0,0]]
test3 = [[0,1,2,0],
         [3,0,0,0],
         [0,0,0,2],
         [0,3,1,0]]
test4 = [[0,0,0,0],
         [0,3,0,1],
         [1,0,2,0],
         [0,0,0,0]]
test5 = [[0,0,8,3,0,0,4,1,0],
        [0,3,0,4,0,7,0,0,8],
        [5,4,0,9,0,0,0,0,2],
        [0,4,3,5,0,0,0,6,0],
        [5,0,2,0,0,0,3,0,9],
        [0,6,0,0,0,8,4,1,0],
        [1,0,0,0,0,5,0,2,9],
        [8,0,0,6,0,3,0,7,0],
        [0,2,7,0,0,4,8,0,0]]

def convertFormat(rawPuzzle):
    n = len(rawPuzzle)
    posList = [None] * n
    spacer = deepcopy(posList)
    dud =  deepcopy(posList)
    for m in range(len(dud)):
        dud[m] = m+1
    for n in range(len(spacer)):
        spacer[n] = dud
    for n in range(len(posList)):
        posList[n] = deepcopy(spacer)

    return posList

def elimGiven(rawPuzzle):
    template = convertFormat(rawPuzzle)
    for n in range(len(rawPuzzle)):
        for m in range(len(rawPuzzle)):
            if rawPuzzle[n][m] != 0:
                template[n][m] = [rawPuzzle[n][m]]
    return template

def elimCell(rawPuzzle):
    limit = len(rawPuzzle)
    for x in range(limit):
        elims = []
        for y in range(limit):
            if len(rawPuzzle[x][y]) == 1:
                elims.append(rawPuzzle[x][y][0])
        for z in range(limit):
            if len(rawPuzzle[x][z]) != 1:
                temp = deepcopy(rawPuzzle[x][z])
                for n in elims:
                    if not temp.__contains__(n):
                        pass
                    else:
                        temp.remove(n)
                rawPuzzle[x][z] = deepcopy(temp)
        elims[:] = []
    return rawPuzzle

def elimRow(rawPuzzle):
    limit = len(rawPuzzle)
    root = int(math.sqrt(limit))
    elims = []
    for n in range(root):
        for m in range(root):
            for x in range(n*root,(n+1)*root):
                for y in range(m*root,(m+1)*root):
                    if len(rawPuzzle[x][y]) == 1:
                        elims.append(rawPuzzle[x][y][0])
            for i in range(n*root,(n+1)*root):
                for j in range(m*root,(m+1)*root):
                    if len(rawPuzzle[i][j]) != 1:
                        temp = deepcopy(rawPuzzle[i][j])
                        for item in elims:
                            if not temp.__contains__(item):
                                pass
                            else:
                                temp.remove(item)
                        rawPuzzle[i][j] = deepcopy(temp)
            elims[:] = []
    return rawPuzzle

def elimCol(rawPuzzle):
    limit = len(rawPuzzle)
    root = int(math.sqrt(limit))
    elims = []
    for xoff in range(root):
        for yoff in range(root):
            for n in range(root):
                for m in range(root):
                    for x in range(n*root+xoff, (n+1)*root+xoff, root):
                        for y in range(m*root+yoff,(m+1)*root+yoff,\
                                root):
                            if len(rawPuzzle[x][y]) == 1:
                                elims.append(rawPuzzle[x][y][0])
            for a in range(root):
                for b in range(root):
                    for i in range(a*root+xoff, (n+1)*root+xoff, root):
                        for j in range(b*root+yoff,(b+1)*root+yoff,\
                                root):
                            if len(rawPuzzle[i][j]) != 1:
                                temp = deepcopy(rawPuzzle[i][j])
                                for item in elims:
                                    if not temp.__contains__(item):
                                        pass
                                    else:
                                        temp.remove(item)
                                rawPuzzle[i][j] = deepcopy(temp)
            elims[:] = []
    return rawPuzzle

def elimPossibilities(rawPuzzle):
    limit = len(rawPuzzle)
    stillSolo = False
    for x in range(limit):
        for y in range(limit):
            for a in rawPuzzle[x][y]:
                for b in range(limit):
                    if b == y:
                        continue
                    if rawPuzzle[x][b].__contains__(a):
                        temp = 0
                        break
                    else:
                        stillSolo = True
                        temp = deepcopy(a)
                if stillSolo and temp != 0:
                    rawPuzzle[x][y] = [deepcopy(temp)]
                stilSolo = False
                temp = 0
    return rawPuzzle

def isSolved(rawPuzzle):
    for x in rawPuzzle:
        for y in x:
            if len(y) != 1:
                return False
    return True

def guess(rawPuzzle, initx, inity, initz, lastGuess):
    tempPuzzle = deepcopy(rawPuzzle)
    limit = len(tempPuzzle)
    root = math.sqrt(limit)
    temp = None
    initx = initx % limit
    inity = inity % limit
    initz = initz % limit
    for x in range(initx, limit):
        for y in range(inity, limit):
            for z in range(initz, len(tempPuzzle[x][y])):
                if len(tempPuzzle[x][y]) != 1 and\
                        tempPuzzle[x][y][z] != lastGuess:
                    temp = tempPuzzle[x][y][z]
                    tempPuzzle[x][y] = [deepcopy(temp)]
                    return tempPuzzle, x, y, z, temp

def display(rawPuzzle):
    limit = len(rawPuzzle)
    root = int(math.sqrt(limit))
    rows = []
    counter = 0
    rowcounter = 0
    print ""
    print " |",
    dashes ="-" * (root*8-1)
    enddash = dashes+"|"
    sys.stdout.write(dashes)
    sys.stdout.flush()
    print "|"
    for n in range(root):
        for m in range(root):
            for x in range(n*root,(n+1)*root):
                for y in range(m*root,(m+1)*root):
                    rows.append(rawPuzzle[x][y])
                for things in rows:
                    if counter  == 0:
                        print " |",
                    if len(things) > 1:
                        print "-",
                    else:
                        print things[0],
                    if counter % limit == limit - 1:
                        print "|"
                        print "",
                    if counter % root == root-1:
                        print "|",
                    counter += 1
                rows[:] = []
            if rowcounter % root == root -1:
                sys.stdout.write(enddash)
                sys.stdout.flush()
                print ""
                if rowcounter != limit-1:
                    print " |",
            rowcounter += 1
    print ""

def altDisplay(rawPuzzle):
    limit = len(rawPuzzle)
    root = int(math.sqrt(limit))
    rows = []
    counter = 0
    rowcounter = 0
    print ""
    print " |",
    dashes ="-" * (root*8-1)
    enddash = dashes+"|"
    sys.stdout.write(dashes)
    sys.stdout.flush()
    print "|"
    for n in range(root):
        for m in range(root):
            for x in range(n*root,(n+1)*root):
                for y in range(m*root,(m+1)*root):
                    rows.append(rawPuzzle[x][y])
                for things in rows:
                    if counter  == 0:
                        print " |",
                    if things == 0:
                        print "-",
                    else:
                        print things,
                    if counter % limit == limit - 1:
                        print "|"
                        print "",
                    if counter % root == root-1:
                        print "|",
                    counter += 1
                rows[:] = []
            if rowcounter % root == root -1:
                sys.stdout.write(enddash)
                sys.stdout.flush()
                print ""
                if rowcounter != limit-1:
                    print " |",
            rowcounter += 1
    print ""

def formatInput(strIn, dimensions):
    dim = int(dimensions)
    innerList = []
    outerList = []
    for m in range(dim):
        for n in range(dim):
            innerList.append(int(strIn[m*dim+n]))
        outerList.append(deepcopy(innerList))
        innerList[:] = []
    return list(outerList)

def solve(rawPuzzle):
    newPuzzle = []
    while True:
        sample = deepcopy(rawPuzzle)
        test = elimCell(rawPuzzle)
        test = elimRow(test)
        test = elimCol(test)
        test = elimPossibilities(test)
        if sample == test:
            break
    return newPuzzle


if __name__ == '__main__':
    usrInp = raw_input("INPUT PUZZLE: ")
    inp = formatInput(usrInp, math.sqrt(len(usrInp)))
    altDisplay(inp)
    test = elimGiven(inp)
    solve(test)
    if not isSolved(test):
        print "THIS IS AS FAR AS I CAN GO"
        display(test)
        print "TIME TO GUESS"
        lastx = 0
        lasty = 0
        lastz = 0
        lastThing = None
        while True:
            lastPos = guess(test,lastx,lasty,lastz, lastThing)
            solve(lastPos[0])
            if isSolved(lastPos[0]):
                test = lastPos[0]
                break
            else:
                lastx = lastPos[1]
                lasty = lastPos[2]
                lastz = lastPos[3]
                lastThing = lastPos[4]
    else:
        print "NO GUESSING NEEDED"
    display(test)
