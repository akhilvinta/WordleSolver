
from operator import contains
from re import S

# bestStartWords = [["saice", 1511], "salet", 9343], ["saner, 9326"], ["saned", 9247], ["caret", 9210]
#Can't solve words with a 3-peat letter such as "emcee" and "tener".

class WordleSolver:
    
    def __init__(self, allFiveWords, commonFiveWords, outputFile, playStyle="quick"):
        self.playStyle = playStyle
        self.notInWordle = ["salet", "carey", "amlet", "corey", "boily", "bolty", "moity", "milan",\
        "marie", "boise", "casey", "bruce", "bryce", "karen", "loren", "mario", "saite", "slare", "simon", "linus", "lyons",\
        "leroy", "klein", "naomi", "webmd"]
        self.mostFreqentLetters = {'o':250, 'r':240, 't': 230, 'm': 230, 'n': 220, 'l':200, 'u':200, 'h':180, 'd':150, 'p': 150,\
            'b':120, 'f':120, 'g':100, 'y': 100, 'k':90}
        self.frequencyOfLetters = [['a', 981], ['b', 281], ['c', 476], ['d', 394], ['e', 1227], ['f', 230], ['g', 311], ['h', 389], ['i', 671], ['j', 27], ['k', 210], ['l', 719], ['m', 315], ['n', 576], ['o', 754], ['p', 367], ['q', 29], ['r', 899], ['s', 669], ['t', 728], ['u', 467], ['v', 153], ['w', 195], ['x', 37], ['y', 425], ['z', 40]]
        self.fives = self.allFives(allFiveWords)
        (self.commonFives, self.commonFivesList) = self.extractCommonFives(commonFiveWords)
        (self.wordleFives, self.wordleFivesList) = self.extractCommonFives("wordleWords.txt")
        self.frequencyList = self.generateFrequencyList(self.wordleFives)
        self.outputFile = open(outputFile, "w")

    def allFives(self, fileName):
        f = open(fileName)
        fives = set()
        for word in f:
            word = word.rstrip("\n")
            if len(word) == 5:
                fives.add(word)
        return fives

    def extractCommonFives(self, fileName):
        f = open(fileName)
        commonFives = set()
        commonFivesList = []
        for word in f:
            word = word.rstrip("\n")
            if len(word) == 5:
                shouldPlace = True
                for i in range(len(word)):
                    if (ord(word[i])-97 < 0 or ord(word[i])-97 > 25):
                        shouldPlace = False
                if shouldPlace:
                    commonFives.add(word.lower())
                    commonFivesList.append(word.lower())
        return (commonFives, commonFivesList)


    def getPositionalFrequencies(self, wordList, position):
        outputArr = [None] * 26
        for i in range(len(outputArr)):
            outputArr[i] = [None,0] 
        for i in range(26):
            outputArr[i][0] = chr(i+97)
        for word in wordList:
                outputArr[ord(word[position])-97][1] += 1
        if position == 4:
            outputArr[ord('s')-97][1] = 100 #refactor for s not being common in wordle
            outputArr[ord('y')-97][1] = 200 #refactor for s not being common in wordle
        return outputArr

    def generateFrequencyList(self, wordList):
        outputList = []
        for i in range(5):
            outputList.append(list(reversed(sorted((self.getPositionalFrequencies(wordList, i)), key = lambda x: x[1]))))
        return outputList

    def containsDoubles(self, string):
        return len(set(string)) != len(string)

    def filterReds(self, inputArr, red):
        filterReds = []
        for word in inputArr:
            shouldAdd = True
            for i in range(5):
                if word[i] in red:
                    shouldAdd = False
            if shouldAdd:
                filterReds.append(word)
        return filterReds

    def filterGreens(self, inputArr, green):
        filterGreens = []
        for word in inputArr:
            shouldAdd = True
            for i in range(5):
                if green[i] != '_' and green[i] != word[i]:
                    shouldAdd = False
            if shouldAdd:
                filterGreens.append(word)
        return filterGreens

    def filterYellows(self, inputArr, yellow, turn):
        filterLast = []
        for word in inputArr:
            shouldAdd = True
            for entry in yellow:
                if entry[0] not in word or word[entry[1]] == entry[0]:
                    shouldAdd = False
            if shouldAdd:
                filterLast.append(word)
        
        ret = []
        for word in filterLast:
            if word in self.wordleFives:
                ret.append(word)

        return [ret, filterLast, turn]
                
    def calculateScoreOfWord(self, curStr, greenPositions = []):
        result = []
        if self.containsDoubles(curStr):
            result = [idx for idx, item in enumerate(curStr) if item in curStr[:idx]]
        score = 0
        for i in range(5):
            if i in result:
                continue
            if i in greenPositions:
                score += (self.frequencyOfLetters[ord(curStr[i])-97][1] // 2)
            else:
                for entry in self.frequencyList[i]:
                    if entry[0] == curStr[i]:
                        score += entry[1]
                        score += (self.frequencyOfLetters[ord(curStr[i])-97][1] // 2)
        return score

    #Python cannot handle depth > 10
    def allPossibilitiesGivenDepth(self, depth, curStr, retList):
        if len(curStr) == 5:
            retList.append(curStr)
            return retList
        for i in range(depth):
            temp = curStr + str(i)
            self.allPossibilitiesGivenDepth(depth, temp, retList)
        return retList

    def optimalPossibilityGivenDepth(self, depth):
        allPossibilities = self.allPossibilitiesGivenDepth(depth, "", [])
        maxFrequency = -1
        maxStr = ""
        for term in allPossibilities:
            curStr = ""
            curTotalFrequency = 0
            for i in range(5):
                curStr += self.frequencyList[i][int(term[i])][0]
            curTotalFrequency += self.calculateScoreOfWord(curStr)
            if ((curTotalFrequency > maxFrequency) and (curStr in self.fives) and (not self.containsDoubles(curStr)) and (curStr not in self.notInWordle)):
                maxFrequency = curTotalFrequency
                maxStr = curStr

        return maxStr


    def wordFrequencyVsStateReductionHeuristic(self, wordList):
        maxScore = -10000
        maxStr = ""
        for term in wordList:
            word = term[0]
            frequency = term[1]
            score = (self.calculateScoreOfWord(word) + (2000 - frequency))
            if score > maxScore and (word not in self.notInWordle):
                maxScore = score
                maxStr = word
        return maxStr

    #to test this: deeds, rough?, brown, balls
    def smallStateSpaceHeuristic(self, orderedByCommonality):
        # print(orderedByCommonality)
        if orderedByCommonality[1][1] - orderedByCommonality[0][1] >= 750:
            return orderedByCommonality[0][0]
        uniqueChars = []
        for entry in orderedByCommonality:
            for letter in entry[0]:
                shouldAdd = True
                for allElse in orderedByCommonality:
                    if allElse[0] == entry[0]:
                        continue
                    if letter in allElse[0]:
                        shouldAdd = False
                if shouldAdd:
                    uniqueChars.append(letter)
                    break
        print("unique = " + str(uniqueChars))
        if len(uniqueChars)==5:
            del uniqueChars[-1]
        ret = []
        for word in self.commonFives:
            shouldAdd = True
            for char in uniqueChars:
                if char not in word:
                    shouldAdd = False
            if shouldAdd:
                ret.append(word)
        if ret:
            return ret[0]
        for word in self.commonFives:
            shouldAdd = True
            for char in uniqueChars:
                if char not in word:
                    shouldAdd = False
            if shouldAdd:
                ret.append(word)
        if ret:
            return ret[0]
        return ret

    def calculateScoreOfPartition(self, partition):
        total_length = sum(len(entry) for entry in partition)
        lenDict = {}
        for elem in partition:
            if len(elem) not in lenDict:
                lenDict[len(elem)] = 1
            else:
                lenDict[len(elem)] += 1
        return sum([((lenDict[key]*key/total_length)*key) for key in lenDict])

    def applyGreensToPartition(self, partitionList, word, printF=0):
        if printF:
            print(partitionList)
            print()
        for i in range(5):
            s = []  
            for partition in partitionList:
                greenHit = [entry for entry in partition if entry[i] == word[i]]
                greenMiss = [entry for entry in partition if entry[i] != word[i]]
                if greenHit:
                    s.append(greenHit)
                if greenMiss:
                    s.append(greenMiss)
            partitionList = s
            if printF:
                print(partitionList)
                print()

        return partitionList

    def minimizeFromSmallStateSpaceGivenWord(self, wordList, word):
        # wordList = [entry[0] for entry in wordList]
        s = [wordList]
        for i in range(5):
            tempList = []
            for list in s:
                includes = [term for term in list if word[i] in term]
                notIncludes = [term for term in list if word[i] not in term]
                if includes: 
                    tempList.append(includes)
                if notIncludes:
                    tempList.append(notIncludes)
            s = tempList

        s = self.applyGreensToPartition(s, word)

        score = self.calculateScoreOfPartition(s)
        if word in wordList:
            # print("The word is " + str(s) + " and the score is " + str(score))
            score = ((len(wordList)-1)/len(wordList))*score
        return [score,s]


    def minimizeFromSmallStateSpace(self, wordList):
        # print("wordList = " + str(wordList))
        wordList = [entry[0] for entry in wordList]
        minimizingWord = ""
        minNextGuesses = len(wordList)
        minimizingArr = []
        for word in self.commonFivesList:
        # for word in self.commonFives:
            if word in self.notInWordle:
                continue
            ret = self.minimizeFromSmallStateSpaceGivenWord(wordList, word)
            if ret[0] < minNextGuesses:
                minNextGuesses = ret[0]
                minimizingWord = word
                minimizingArr = ret[1]

        # print("The expected size of the remaining state space is " + str(minNextGuesses) + "\n")
        # print("minimize = " + str(minimizingWord))
        # print("minimizingArr = " + str(minimizingArr))
        return minimizingWord


    def smartSelectionForLargeStateSpace(self, common, green, yellow, red):
        if len(common) > 150:
            greenPositions = []
            for i in range(len(green)):
                if green[i] != '_':
                    red.add(green[i])
                    greenPositions.append(i)
            
            filteredReds = self.filterReds(self.commonFives, red)
            filteredYellows = self.filterYellows(filteredReds, yellow, 2)[0]

            maxScore = -10000
            maxWord = ""
            for word in filteredYellows:
                if self.calculateScoreOfWord(word) > maxScore and (word not in self.notInWordle):
                    maxScore = self.calculateScoreOfWord(word)
                    maxWord = word
            return maxWord

    def SelectionOrMinimizeStateSpace(self, common, all, turn, green, yellow, red):

        #Turn 1: Return Precalculated Optimal First Guess
        if int(turn) == 1:
            # suggestion = self.optimalPossibilityGivenDepth(10)
            suggestion = "crate"
            return [0,suggestion]
        
        if len(common) > 500:
            maxWord = self.smartSelectionForLargeStateSpace(common, green, yellow, red)
            if maxWord:
                return [0,maxWord]
        
        selectionSpace = common if self.playStyle == "quick" else all
        selectionSpace = all if (not common) else selectionSpace

        if not all:
            return [-1,"", []] #empty selectionState

        #Common state space length > 20: Max score word of those left in common state space. This is only if smart search fails.
        maxScore = -1
        maxFreqStr = ""
        for word in selectionSpace:
            curScore = self.calculateScoreOfWord(word)
            if curScore > maxScore and (word not in self.notInWordle):
                maxScore = curScore
                maxFreqStr = word


        if not common:
            return [0,maxFreqStr]
        orderedByCommonality = []

        #Common state space length < 20: If our possible solution set is reasonably small, then base suggestion off of both frequency score and and word relavance.
        if len(common) < 500:
            
            #Order words by word relevance. This will be used in a later heuristic.
            for i in range(len(common)):
                for j in range(len(self.commonFivesList)):
                    if common[i] == self.commonFivesList[j]:
                        orderedByCommonality.append([common[i],j])
            orderedByCommonality = sorted(orderedByCommonality, key=lambda x: x[1])
            curMin = min(len(common),10)

            #call heuristic function to determine ideal suggestion
            maxStr = self.wordFrequencyVsStateReductionHeuristic(orderedByCommonality)

            if not orderedByCommonality:
                return [-2,[],[]]

            if len(orderedByCommonality) <= 500 and len(orderedByCommonality) > 2:
                minimizingWord = self.minimizeFromSmallStateSpace(orderedByCommonality)
                maxStr = minimizingWord if minimizingWord else maxStr

            #Return heuristic based suggestion that factors in word relavance
            return [1, maxStr, orderedByCommonality[:curMin]]

        #Return suggestion solely based on frequency score
        return [0, maxFreqStr, common]


    def processInput(self, string):
        arr = string.split("-")
        # print(arr)
        green, yellow, red = [], [], []
        green = [char for char in arr[0]]
        red = set([char for char in arr[2]])
        yellow = []
        self.outputFile.write("This is turn " + str(arr[-1]) + ":\n")
        for i in range(0,len(arr[1])-1,2):
            cur = [arr[1][i],int(arr[1][i+1])]
            yellow.append(cur)
        return (green, red, yellow, arr[-1])

    def promptAndProcessInput(self, string = "", shouldPrint = 1):
        if not string:
            string = input("Please enter string in format: \"green - yellow - red - <turn>\". Example \"r___y-u2-eais\" can represent word \"raise\"\n")
        (green, red, yellow, turn) = self.processInput(string)
        filteredReds = self.filterReds(self.fives, red)
        filteredGreens = self.filterGreens(filteredReds, green)
        remaining = self.filterYellows(filteredGreens, yellow, turn)
        # remaining = self.processInput(string)
        if int(remaining[2]) != 1:
            if shouldPrint:
                print("The length of the remaining state space is " + str(len(remaining[1])) + ".\n")
                print("The state space itself is " + str(remaining[1]) + ".\n")
                print("The " + str(len(remaining[0])) + " realistic results in the state space are " + str(remaining[0]) + ".\n")
        suggestion = self.SelectionOrMinimizeStateSpace(remaining[0],remaining[1],remaining[2], green, yellow, red)
        if suggestion[0] == 1:
            if shouldPrint:
                print("Based on the state space, here are the top 10 suggestions for the next guess and their frequencies in the english language: " + str(suggestion[2]) + ".\n")
                print("Based on the state space, here is the suggestion guess: \"" + str(suggestion[1]) + "\".\n")
        elif suggestion[0] == 0:
            if shouldPrint:
                print("Based on the state space, here is the suggestion guess: \"" + str(suggestion[1]) + "\".")
                print("Please look to the tables above for selections")
        else:
            if shouldPrint:
                print("There exists no word that fits this description.")
        return [suggestion, remaining[0]]




# solver = WordleSolver("allwords.txt", "20k.txt", "output.txt")
# solver.promptAndProcessInput()

# solver.promptAndProcessInput("_____---2")
#_____-r1a2-tce-2
# wordList = [['think', 53], ['still', 71], ['visit', 74], ['point', 82], ['study', 93], ['night', 112], ['light', 119], ['might', 127], ['until', 138], ['thing', 162], ['stuff', 191], ['built', 240], ['input', 258], ['joint', 346], ['limit', 351], ['mount', 369], ['fight', 432], ['pilot', 525], ['doubt', 554], ['split', 560], ['shift', 563], ['tight', 596], ['ghost', 695], ['boost', 735], ['tough', 742], ['sight', 750], ['shoot', 772], ['stood', 840], ['thong', 1073], ['ought', 1092], ['thumb', 1116], ['twist', 1117], ['digit', 1137], ['swift', 1261], ['quilt', 1361], ['idiot', 1453], ['blunt', 1564], ['shout', 1600], ['guilt', 1674], ['stiff', 1709], ['midst', 1737], ['flint', 1775], ['stool', 1837], ['motif', 1856], ['sting', 1916], ['tulip', 2064], ['wight', 2202], ['thigh', 2214], ['moist', 2229], ['stout', 2332], ['stony', 2352], ['tying', 2359], ['stunt', 2453], ['pivot', 2475], ['bigot', 2670], ['donut', 2827], ['flout', 2921], ['foist', 2929], ['glint', 2972], ['hoist', 3028], ['hotly', 3029], ['ingot', 3055], ['joist', 3065], ['joust', 3067], ['moult', 3162], ['outdo', 3197], ['outgo', 3198], ['pithy', 3231], ['posit', 3249], ['shunt', 3364], ['snout', 3409], ['spilt', 3425], ['spout', 3434], ['stilt', 3450], ['stink', 3451], ['stint', 3452], ['stomp', 3454], ['stoop', 3455], ['stump', 3458], ['stung', 3459], ['stunk', 3460], ['thump', 3505], ['timid', 3510], ['tipsy', 3511], ['toddy', 3513], ['toxin', 3518], ['twixt', 3539], ['unfit', 3546], ['unlit', 3548], ['vomit', 3567]]
# print(solver.minimizeFromSmallStateSpaceGivenWord(wordList, "mount"))
# partList = [['sweet', 'towel', 'swept', 'tweed', 'dwelt', 'tweet'], ['exist', 'quiet', 'thief', 'heist'], ['eight', 'debit', 'stein', 'inlet', 'befit', 'fetid', 'filet', 'inept', 'islet', 'tepid'], ['hotel', 'event', 'often', 'guest', 'steel', 'sheet', 'spent', 'setup', 'quest', 'theft', 'fleet', 'depot', 'motel', 'debut', 'token', 'teddy', 'upset', 'onset', 'steep', 'tempo', 'slept', 'detox', 'fetus', 'beget', 'beset', 'betel', 'duvet', 'ethos', 'extol', 'exult', 'knelt', 'sleet', 'smelt', 'spelt', 'steed', 'tenet', 'totem', 'unmet', 'unset']]
# solver.applyGreensToPartition(partList, "sleet",1)
# solver.work()
# print(solver.calculateScoreOfWord("ocean"))
# print(solver.calculateScoreOfWord("adieu"))
# print(solver.optimalPossibilityGivenDepth(10)) 
# __a__-t3e4-cr-2_


