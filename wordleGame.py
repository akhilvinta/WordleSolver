from multiprocessing.connection import answer_challenge
from random import randint
from wordleSolver import WordleSolver

badWords = [[5, 'abode'], [7, 'adage'], [5, 'admit'], [5, 'adobe'], [5, 'adore'], [5, 'adorn'], [7, 'agape'], [6, 'agate'], [5, 'aglow'], [5, 'agora'], [5, 'alibi'], [5, 'alter'], [5, 'amass'], [5, 'angry'], [5, 'ankle'], [5, 'aphid'], [5, 'aping'], [5, 'apron'], [6, 'ardor'], [5, 'argue'], [5, 'arrow'], [5, 'askew'], [5, 'aunty'], [5, 'awake'], [5, 'award'], [6, 'awoke'], [5, 'azure'], [6, 'baggy'], [5, 'basil'], [6, 'baste'], [7, 'batch'], [5, 'batty'], [5, 'bawdy'], [5, 'beard'], [5, 'beefy'], [5, 'befit'], [5, 'beget'], [5, 'beret'], [5, 'betel'], [6, 'bevel'], [5, 'biddy'], [5, 'blaze'], [5, 'bleat'], [5, 'bless'], [5, 'borne'], [6, 'brace'], [5, 'brave'], [6, 'bribe'], [5, 'bride'], [5, 'brine'], [5, 'brood'], [6, 'broom'], [5, 'budge'], [5, 'buggy'], [5, 'cabby'], [5, 'cadet'], [5, 'caper'], [6, 'catch'], [5, 'chaff'], [5, 'chard'], [5, 'chasm'], [5, 'chill'], [5, 'cinch'], [5, 'clang'], [5, 'clasp'], [5, 'cliff'], [5, 'corer'], [5, 'coven'], [5, 'crack'], [6, 'cramp'], [5, 'crank'], [5, 'crave'], [5, 'creak'], [5, 'creep'], [5, 'crepe'], [5, 'crier'], [5, 'crook'], [5, 'cumin'], [5, 'curvy'], [5, 'cynic'], [5, 'dandy'], [6, 'defer'], [5, 'deter'], [5, 'detox'], [5, 'dilly'], [5, 'dingo'], [5, 'dingy'], [5, 'ditch'], [7, 'ditty'], [6, 'dizzy'], [5, 'dodgy'], [5, 'dolly'], [5, 'dowdy'], [5, 'dowel'], [5, 'downy'], [5, 'drake'], [6, 'drape'], [5, 'dread'], [5, 'dress'], [5, 'drone'], [5, 'droop'], [5, 'drove'], [5, 'drown'], [5, 'dully'], [5, 'dummy'], [6, 'dumpy'], [6, 'eager'], [5, 'eater'], [6, 'eject'], [5, 'elate'], [5, 'elide'], [5, 'elope'], [5, 'enema'], [5, 'erase'], [5, 'erect'], [6, 'erode'], [5, 'ether'], [6, 'evade'], [5, 'evoke'], [5, 'exert'], [6, 'expel'], [5, 'fable'], [5, 'fairy'], [6, 'fanny'], [5, 'feast'], [5, 'feign'], [5, 'femme'], [5, 'fetid'], [7, 'fever'], [6, 'fewer'], [5, 'fifth'], [5, 'fight'], [5, 'filer'], [5, 'filet'], [6, 'filly'], [6, 'filth'], [6, 'finer'], [6, 'fixer'], [5, 'fizzy'], [5, 'fleck'], [5, 'flesh'], [5, 'flock'], [5, 'flung'], [5, 'focal'], [6, 'foggy'], [6, 'folly'], [5, 'forth'], [5, 'frail'], [5, 'freer'], [5, 'fried'], [5, 'frill'], [6, 'frown'], [6, 'froze'], [5, 'furry'], [6, 'gamer'], [5, 'gavel'], [7, 'gawky'], [5, 'gayly'], [7, 'gazer'], [5, 'geeky'], [5, 'geese'], [7, 'giddy'], [6, 'giver'], [5, 'glade'], [6, 'glaze'], [5, 'glove'], [5, 'gnash'], [5, 'golem'], [7, 'golly'], [5, 'gonad'], [6, 'goody'], [5, 'goofy'], [5, 'goose'], [5, 'gorge'], [5, 'grade'], [6, 'grail'], [5, 'grain'], [6, 'grape'], [5, 'grasp'], [5, 'grate'], [5, 'grave'], [7, 'graze'], [5, 'greet'], [5, 'grime'], [5, 'gripe'], [5, 'groom'], [5, 'guava'], [5, 'guilt'], [6, 'gully'], [7, 'gummy'], [6, 'guppy'], [5, 'harpy'], [7, 'haste'], [5, 'hasty'], [8, 'hatch'], [6, 'hater'], [5, 'haunt'], [6, 'heave'], [5, 'hefty'], [7, 'hilly'], [6, 'hippy'], [6, 'hitch'], [6, 'homer'], [8, 'hound'], [5, 'hovel'], [7, 'hover'], [6, 'howdy'], [6, 'hunch'], [5, 'hutch'], [5, 'infer'], [5, 'inlet'], [5, 'ionic'], [6, 'jaunt'], [8, 'jazzy'], [5, 'jerky'], [6, 'jetty'], [5, 'jewel'], [5, 'jiffy'], [5, 'joist'], [7, 'joker'], [6, 'jumpy'], [5, 'kitty'], [6, 'knack'], [5, 'knave'], [5, 'koala'], [6, 'krill'], [5, 'laden'], [6, 'ladle'], [7, 'lager'], [6, 'lapel'], [5, 'leach'], [7, 'leafy'], [6, 'leaky'], [5, 'leant'], [5, 'leapt'], [5, 'leggy'], [5, 'lemur'], [6, 'leper'], [5, 'lever'], [5, 'libel'], [5, 'liege'], [5, 'lipid'], [5, 'liver'], [5, 'livid'], [5, 'louse'], [5, 'lover'], [6, 'lowly'], [5, 'lumen'], [5, 'lunar'], [5, 'lusty'], [6, 'mafia'], [5, 'maker'], [7, 'mammy'], [6, 'mangy'], [5, 'maxim'], [5, 'mealy'], [5, 'merge'], [5, 'merry'], [5, 'milky'], [5, 'miner'], [5, 'minty'], [5, 'mirth'], [5, 'modal'], [5, 'model'], [5, 'modem'], [5, 'molar'], [5, 'moody'], [6, 'moose'], [5, 'motel'], [7, 'mound'], [6, 'mover'], [6, 'mower'], [5, 'muddy'], [5, 'mulch'], [6, 'mummy'], [5, 'munch'], [5, 'murky'], [5, 'mushy'], [5, 'musky'], [6, 'musty'], [5, 'naive'], [5, 'nanny'], [5, 'needy'], [5, 'nerve'], [5, 'newer'], [5, 'nobly'], [7, 'noose'], [6, 'nudge'], [5, 'odder'], [5, 'offer'], [5, 'ombre'], [5, 'otter'], [5, 'outer'], [5, 'overt'], [5, 'ovine'], [5, 'pagan'], [5, 'paler'], [6, 'parer'], [5, 'parry'], [5, 'paste'], [6, 'pasty'], [5, 'patch'], [5, 'payer'], [5, 'pecan'], [5, 'pedal'], [5, 'penal'], [5, 'pence'], [6, 'perch'], [5, 'petal'], [6, 'piggy'], [5, 'pique'], [5, 'pithy'], [6, 'pixie'], [5, 'plane'], [5, 'plank'], [5, 'plead'], [6, 'pleat'], [5, 'plier'], [5, 'plunk'], [5, 'poppy'], [5, 'pound'], [5, 'prank'], [5, 'preen'], [5, 'prick'], [6, 'pried'], [5, 'primo'], [5, 'privy'], [5, 'prize'], [5, 'prone'], [5, 'prong'], [5, 'prowl'], [5, 'pudgy'], [5, 'pupal'], [5, 'pupil'], [5, 'puppy'], [5, 'purer'], [6, 'pushy'], [5, 'quack'], [5, 'quail'], [5, 'quark'], [5, 'quart'], [6, 'quash'], [5, 'queer'], [5, 'query'], [6, 'ramen'], [7, 'rarer'], [5, 'raven'], [5, 'razor'], [5, 'rearm'], [5, 'rebar'], [5, 'reedy'], [5, 'refer'], [5, 'refit'], [5, 'regal'], [5, 'remit'], [5, 'retch'], [5, 'retro'], [5, 'revel'], [5, 'rider'], [5, 'rivet'], [5, 'robot'], [5, 'roomy'], [5, 'rotor'], [5, 'rover'], [5, 'rowdy'], [7, 'rower'], [6, 'ruder'], [5, 'rumor'], [5, 'salsa'], [6, 'sappy'], [5, 'sassy'], [5, 'savoy'], [5, 'scalp'], [5, 'scamp'], [6, 'scoff'], [5, 'scold'], [6, 'scowl'], [5, 'seize'], [6, 'sever'], [5, 'sewer'], [5, 'shack'], [5, 'shade'], [6, 'shake'], [8, 'shale'], [5, 'shank'], [6, 'shard'], [5, 'shark'], [7, 'shave'], [6, 'sheep'], [5, 'shelf'], [5, 'shove'], [5, 'showy'], [5, 'sissy'], [5, 'skate'], [5, 'skiff'], [5, 'skunk'], [6, 'slack'], [5, 'slant'], [6, 'slate'], [5, 'slave'], [5, 'sleek'], [5, 'sleep'], [6, 'sleet'], [5, 'slump'], [5, 'smash'], [6, 'smear'], [5, 'smell'], [6, 'snake'], [6, 'snare'], [5, 'snipe'], [5, 'snort'], [5, 'snout'], [7, 'spade'], [5, 'spank'], [5, 'spark'], [5, 'spasm'], [6, 'spawn'], [5, 'spear'], [5, 'spelt'], [5, 'sperm'], [5, 'spiel'], [5, 'spoof'], [5, 'spore'], [6, 'spout'], [5, 'spree'], [5, 'squat'], [5, 'stage'], [6, 'stake'], [7, 'stale'], [5, 'stand'], [6, 'stank'], [5, 'stare'], [5, 'stark'], [5, 'stash'], [8, 'stave'], [6, 'stead'], [5, 'steak'], [6, 'steed'], [5, 'steel'], [8, 'steep'], [5, 'steer'], [5, 'stiff'], [5, 'sting'], [6, 'stink'], [5, 'stint'], [5, 'stoke'], [5, 'stoop'], [5, 'stork'], [5, 'straw'], [6, 'stump'], [7, 'stung'], [6, 'stunk'], [5, 'stunt'], [6, 'suave'], [5, 'swash'], [7, 'sweep'], [5, 'sweet'], [6, 'swell'], [5, 'swept'], [5, 'swill'], [5, 'swine'], [6, 'swore'], [5, 'swung'], [5, 'taffy'], [6, 'taker'], [5, 'taper'], [6, 'tatty'], [5, 'tempo'], [5, 'thank'], [5, 'threw'], [5, 'thump'], [5, 'tibia'], [5, 'tiger'], [6, 'tight'], [6, 'timer'], [5, 'token'], [5, 'tonic'], [5, 'totem'], [5, 'tower'], [5, 'trace'], [5, 'trait'], [5, 'trawl'], [5, 'trite'], [5, 'trump'], [5, 'tubal'], [5, 'tuber'], [5, 'tunic'], [5, 'tutor'], [6, 'twang'], [5, 'tweet'], [6, 'udder'], [5, 'umbra'], [5, 'unfit'], [5, 'unwed'], [5, 'unzip'], [5, 'utter'], [5, 'vapor'], [7, 'vaunt'], [5, 'vegan'], [6, 'verge'], [6, 'verve'], [5, 'viola'], [6, 'voter'], [5, 'vouch'], [6, 'vowel'], [6, 'wafer'], [5, 'waver'], [7, 'waxen'], [5, 'weave'], [5, 'weedy'], [5, 'welch'], [7, 'whack'], [5, 'whale'], [5, 'wheel'], [5, 'whine'], [5, 'widen'], [7, 'wight'], [5, 'wimpy'], [6, 'winch'], [6, 'witty'], [5, 'woken'], [7, 'wooly'], [5, 'woozy'], [5, 'wordy'], [6, 'wound'], [6, 'wrack'], [5, 'wrath'], [5, 'wreak']]


class WordleGame:
    def __init__(self, word=-1):
        f = open("output.txt", "w")
        self.solver = WordleSolver("allwords.txt", "20k.txt", "output.txt")
        if word == -1:
            while 1:
                rand = randint(0,len(self.solver.commonFivesList))
                try:
                    self.answer = self.solver.commonFivesList[rand]
                except IndexError:
                    continue
                if (self.answer in self.solver.fives) and (self.answer not in self.solver.notInWordle) and (rand >= 0 and rand < len(self.solver.commonFivesList)):
                    break
        else:
            self.answer = self.solver.wordleFivesList[word]
            # self.answer = badWords[word][1]
        # self.answer = "goose"
        f.write("The answer to this wordle is \"" + self.answer + "\".\n")
        print("The answer to this wordle is \"" + self.answer + "\".")
        self.green, self.yellow, self.red, self.turn = ['_','_','_','_','_'], [], set(), 1
        self.currentGameState = self.convertListsToGameState()

    def play(self, outputToConsole = 1, printSolverOutput = 1):
        while 1:
            if outputToConsole:
                print("The current game state is: " + self.currentGameState)
            ret = self.solver.promptAndProcessInput(self.currentGameState,printSolverOutput)
            stateSpace = ret[1]
            suggestion = ret[0][1]
            # suggestion = self.solver.promptAndProcessInput(self.currentGameState,printSolverOutput)[0][1]
            # if len(stateSpace) <= 2:
            #     # print("EXITED THIS WAY")
            #     return [self.turn-1, self.answer]
            if outputToConsole:
                print("The suggestion for turn " + str(self.turn) + " is \"" + str(suggestion) + "\".")
            if suggestion == self.answer:
                if outputToConsole:
                    print("YOU GOT THE ANSWER. CONGRATS!!! This is turn " + str(self.turn))
                    print("Again, the answer to this wordle was " + str(self.answer))
                return [self.turn, self.answer]
            self.currentGameState = self.updateGameState(suggestion)
            # print(self.currentGameState)

    def updateGameState(self, suggestion):
        # print(suggestion)
        for i in range(5):
            try:
                if suggestion[i] == self.answer[i]:
                    self.green[i] = suggestion[i]
            except IndexError:
                print("The wordle solver is not compatible with the word \"" + self.answer + "\". It is possible that your word is not in the english dictionary.")
                exit(0)
            if (suggestion[i] in self.answer) and (self.answer[i] != suggestion[i]):
                self.yellow.append(str(suggestion[i]) + str(i))
            if suggestion[i] not in self.answer:
                self.red.add(suggestion[i])
        self.turn += 1
        return self.convertListsToGameState()

    def convertListsToGameState(self):
        string = ""
        for char in self.green:
            string += char
        string += "-"
        for char in self.yellow:
            string += char
        string += "-"
        for char in self.red:
            string += char
        string = string + "-" + str(self.turn)
        return string
        

game = WordleGame()
[turn,answer] = game.play(1,0)

