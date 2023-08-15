from wordleGame import WordleGame
from os import system
import statistics

# Average of 2313 is 3.4382926829268290, 0.6021444361533987
# SD of data is 0.6021444361533987


#---------allWords------------# [mean 3.6912537829658454], [sd 0.9979825023761469]
# < 200 state space: [mean 1.0912235192390833], [sd 0.28798896845503724]
# < 150 state space: [mean 1.1763942931258107], [sd 0.381237699560305]
# < 100 state space: [mean 1.2775616083009078], [sd 0.44789272432657207]
# < 50 state space: [mean 1.5010808473843493], [sd 0.5001069513129475]
# < 30 state space: [mean 1.667963683527886], [sd 0.5290015195413744]
# < 20 state space: [mean 1.8815391266753], [sd 0.553981234266227]
# < 15 state space: [mean 1.9351491569390], [sd 0.584648022621338]
# < 10 state space: [mean 2.1089494163424], [sd 0.621328227299229]
# < 7 state space: [mean 2.28102031993082], [sd 0.664646272719193]
# < 5 state space: [mean 2.42153047989623], [sd 0.726419318892584]
# < 4 state space: [mean 2.53826199740596], [sd 0.758704907859454]
# < 3 state space: [mean 2.68352788586251], [sd 0.823619326092384]
# < 2 state space: [mean 2.909208819714656], [sd 0.9024509715856871]

#---------badWords------------# [mean 5.356060606060606], [sd 0.66501145794955]
# < 200 state space: [mean 1.1022727272727273], [sd 0.30329397418446774]
# < 150 state space: [mean 1.2367424242424243], [sd 0.4254859861625026]
# < 100 state space: [mean 1.3428030303030303], [sd 0.47509641788863244]
# < 50 state space: [mean 1.581439393939394], [sd 0.4937908699691674]
# < 30 state space: [mean 1.8276515151515151], [sd 0.5532657707221083]
# < 20 state space: [mean 2.1117424242424243], [sd 0.6073665383415177]
# < 15 state space: [mean 2.2329545454545454], [sd 0.6466181046506756]
# < 10 state space: [mean 2.4886363636363638], [sd 0.728820911231704]
# < 7 state space: [mean 2.774621212121212], [sd 0.734330200226541]
# < 5 state space: [mean 3.024621212121212], [sd 0.8318607251906157]
# < 4 state space: [mean 3.240530303030303], [sd 0.8037538252498105]
# < 3 state space: [mean 3.524621212121212], [sd 0.8576919784350164]
# < 2 state space: [mean 3.962121212121212], [sd 0.8210263677100683]


#crate -- 3.3182926829268290, 0.6021444361533987
#raise -- 3.3670731707317074, 0.6002632725660384
#irate -- 3.3784552845528455, 0.5890333082942754


# < 75
# < 100
# < 50
# < 25
#  < 150

badWords = [[5, 'augur'], [5, 'berry'], [5, 'bevel'], [5, 'bluer'], [5, 'blush'], [5, 'booby'], [5, 'boxer'], [5, 'buggy'], [5, 'daunt'], [5, 'dizzy'], [5, 'dowdy'], [5, 'every'], [5, 'faint'], [5, 'fanny'], [5, 'fever'], [5, 'fiber'], [5, 'filly'], [5, 'finer'], [5, 'fixer'], [5, 'fluff'], [5, 'folly'], [5, 'found'], [5, 'fudge'], [5, 'giver'], [5, 'gully'], [5, 'gummy'], [5, 'guppy'], [5, 'haunt'], [5, 'hilly'], [5, 'hippy'], [5, 'homer'], [5, 'hound'], [5, 'hover'], [5, 'hussy'], [5, 'impel'], [5, 'infer'], [5, 'jaunt'], [5, 'jazzy'], [5, 'jelly'], [5, 'jerky'], [5, 'joker'], [5, 'jolly'], [5, 'mafia'], [5, 'magma'], [5, 'mamma'], [5, 'maxim'], [5, 'merry'], [5, 'mover'], [5, 'mower'], [5, 'newer'], [5, 'polyp'], [5, 'pound'], [5, 'power'], [5, 'purer'], [5, 'pushy'], [5, 'rarer'], [5, 'razor'], [5, 'rover'], [5, 'rower'], [5, 'savor'], [5, 'sever'], [5, 'shelf'], [5, 'slyly'], [5, 'sperm'], [5, 'swell'], [5, 'tight'], [5, 'vigil'], [5, 'viper'], [5, 'waver'], [5, 'witty'], [5, 'woozy']]

class WordleGenerator:
    def __init__(self, numTrials=2313):
        self.numTrials = numTrials
        self.trials = []
        self.doublesConstant = 2313/2460

    def runTrials(self):
        for i in range(self.numTrials):
            game = WordleGame(i)
            try: 
                self.trials.append(game.play(1,0))
            except IndexError:
                system('afplay /System/Library/Sounds/Glass.aiff')
                print("The above ^^^^ word failed.")
                exit(0)
            
        return self.trials

    def analyzeTrials(self):
        troubleWords = []
        for entry in self.trials:
            if entry[0] >= 5:
                troubleWords.append(entry)
        print(troubleWords)
        avg = sum([entry[0] for entry in self.trials])/len(self.trials)
        print("Average of " + str(self.numTrials) + " is " + str(avg * self.doublesConstant))
        turns = [entry[0] for entry in self.trials]
        print("SD of data is " + str(statistics.stdev(turns)))
        return avg 

generate = WordleGenerator()
print(generate.runTrials())
generate.analyzeTrials()
system('afplay /System/Library/Sounds/Glass.aiff')
system('afplay /System/Library/Sounds/Glass.aiff')
