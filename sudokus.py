
import sys
import copy
import numpy as np

row = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
column = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

def main():
    
    #aaa = 55
        
    #inputList = np.loadtxt('sudokus_start.txt', dtype='str')
    #outputList = np.loadtxt('sudokus_finish.txt', dtype='str')
     
    inputString = sys.argv
       
    #inputString = ['1', inputList[aaa][2:-1]]
       
    inputList = []
       
    sudoku = {}
       
    if len(inputString) >= 2:
        l = map(int, inputString[1])
        inputList = list(l)
           
    gridInit(sudoku, inputList)
       
    print ("Question:")
    printGrid(sudoku)
    print ("")
       
    position = getVoidValuePosition(sudoku)
    neighbours = getNeighbours(position)
    
    result, arcs = AC3(sudoku, position, neighbours)
    
    assignment = backTracking(sudoku, arcs, {}, position, neighbours)
    
    genFinalSudoku(sudoku, assignment)
    printGrid(sudoku)
    
    result = genResult(sudoku)
    
    #print (result)

#     zzz = 0
#     for xxx in inputList:
#         inputString = sys.argv
#       
#         inputString = ['1', xxx[2:-1]]
#       
#         inputList = []
#       
#         sudoku = {}
#       
#         if len(inputString) >= 2:
#             l = map(int, inputString[1])
#             inputList = list(l)
#           
#         gridInit(sudoku, inputList)
#           
#         result, arcsOrginial, arcsFinial = AC3(sudoku)
# #         print ("AC3 result = " + str(result))
#         for a in arcsFinial:
#             sudoku[a] = arcsFinial[a][0]
#          
#         answer = ""
#         for s in sudoku:
#             answer = answer + str(sudoku[s])
#          
#         if (answer == outputList[zzz][2:-1]):
# #             print ("Final result = True")
#             print (True)
#         else:
# #             print ("Final result = False")
# #             print ("model answer = " + outputList[zzz][2:-1])
# #             print (arcsFinial)
# #             print (arcsFinial)
#             print (False)
#         print ("")
#         
# #         if (arcsOrginial == arcsFinial):
# #             print (True)
# #         else:
# #             print (False)
# #         print ("")
    
def gridInit(sudoku, inputList):
    inputIndex = 0
    
    for i in row:
        for j in column:
            d = i + j
            sudoku.update({d:inputList[inputIndex]})
            inputIndex = inputIndex + 1

def printGrid(sudoku):
    count = 0
    
    key = []
    for i in row:
        for j in column:
            d = i + j
            key.append(d)
    
    for k in key:
        print (str(sudoku[k]), end = ' ')
        
        count = count + 1
        if (count % 3 == 0):
            print ("|", end = " ")
            
            if (count % 9 == 0):
                print ("")
                if (count % 27 == 0):
                    print ("-----------------------")

def findBoxRange(key):
    x = row.index(key[0])
    y = column.index(key[1])
    
    xRange = range(int(x/3)*3, int(x/3)*3+2)
    yRange = range(int(y/3)*3, int(y/3)*3+2)
    
    return xRange, yRange

def AC3(sudoku, position, neighbours):
    
    arcs, queue = genArcs(sudoku, position, neighbours)
    
    while len(queue) != 0:
        testCase = queue.pop(0)
        
        if (revise(testCase, arcs)):
            if (len(arcs[testCase[0]])) == 0:
                return False, arcs
            
            for queueKey in neighbours[testCase[0]]:
                if queueKey in position:
                    queueCase = [queueKey, testCase[0]]
                    if queueCase not in queue:
                        queue.append(queueCase)
            
    finalAcrs = copy.deepcopy(arcs)
    for key in arcs:
        if (len(arcs[key])) == 1:
            value = arcs[key][0]
            sudoku[key] = value
            finalAcrs.pop(key, None)
            position.remove(key)
            neighbours.pop(key, None)
    
    return True, arcs

def getVoidValuePosition(sudoku):
    position = []
    
    for k in sudoku:
        if (sudoku[k] == 0):
            position.append(k)
    
    return position

def genArcs(sudoku, position, neighbours):
    
    arcs = {}
    
    queue = []
    
    for key in position:
        value = set()
        n = neighbours[key]
        a = []
        for v in n:
            if (sudoku[v] != 0):
                value.add(sudoku[v])
        
        i = 1
        while i <= 9:
            if not (i in value):
                a.append(i)
            
            i = i + 1
    
        arcs.update({key:a})
        
        for queueKey in neighbours[key]:
            if queueKey in position:
                queueCase = [key, queueKey]
                queue.append(queueCase)
        
    return arcs, queue

def getNeighbours(position):
    
    neighbours = {}
    
    for i in position:
        n = set()
        
        k0 = i[0]
        k1 = i[1]
        
        xPosition, yPosition = findBoxRange(i)
        xPosition = xPosition[0]
        yPosition = yPosition[0]
        
        x = xPosition
        for xx in range(3):
            y = yPosition
            for yy in range(3):
                k = row[x] + column[y]
                y = y + 1
                n.add(k)
            
            x  = x + 1
        
        for xx in column:
            k = k0 + xx
            n.add(k)
        
        for yy in row:
            k = yy + k1
            n.add(k)
        
        n.remove(i)
        neighbours.update({i:n})
        
    return neighbours

def revise(testCase, arcs):
    result = False
    
    xi = testCase[0]
    xj = testCase[1]
    
    for x in arcs[xi]:
        if not any(x != y for y in arcs[xj]):
            arcs[xi].remove(x)
            result = True
    
    return result

def genResult(sudoku):
    result = ''
    
    key = []
    for i in row:
        for j in column:
            d = i + j
            key.append(d)
    
    for k in key:
        result = result + str(sudoku[k])
        
    file = open('output.txt', 'w')
    file.write(result)
    file.close()

    return result

def selectUnassgnedVariable(arcs, position, assignment):
    result = None
    length = 10
    
    for var in position:
        if len(arcs[var]) < length and not var in assignment:
            length = len(arcs[var])
            result = var
    
    return result

def backTracking(sudoku, arcs, assignment, position, neighbours):
    if len(assignment) == len(position):
        return assignment
    
    var = selectUnassgnedVariable(arcs, position, assignment)
    
    for value in arcs[var]:
        newAssign = {var:value}
        
        notConsistent = False
        
        for i in neighbours[var]:
            if i in assignment:
                if value == assignment[i]:
                    notConsistent = True
                    break
            
        if notConsistent != True:
            assignment.update(newAssign)
        
            result = backTracking(sudoku, arcs, assignment, position, neighbours)
        
            if result != False: return result
        
            assignment.pop(var, value)
        
    return False

def genFinalSudoku(sudoku, assignment):
    for key in assignment:
        sudoku[key] = assignment[key]

if __name__ == "__main__":
    main()