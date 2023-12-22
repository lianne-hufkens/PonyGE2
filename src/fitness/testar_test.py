import subprocess, os, csv


#https://stackoverflow.com/questions/431684/equivalent-of-shell-cd-command-to-change-the-working-directory
class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


##url = 'https://webformsut.testar.org/forms/ema'
##strategy_file = 'C:/Users/testar/Desktop/test_strategy.txt'
##
##with open(strategy_file, 'w') as filetowrite:
##    filetowrite.write('select-random')
##
##command = r'testar sse=webdriver_generic_strategy ShowVisualSettingsDialogOnStartup=false Sequences=1 SequenceLength=2 SUTConnectorValue=" ""C:\\windows\\chromedriver.exe"" ""https://webformsut.testar.org/forms/ema"" " Mode=Generate StateModelEnabled=false StrategyFile=C:/Users/testar/Desktop/test_strategy.txt'
##

with cd(r'C:\Users\testar\Desktop\TESTAR_dev\testar\output'):
    with open('_.csv') as csvfile:
##        reader = csv.reader(csvfile, delimiter=';')
##        for row in reader:
##            print(row)
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
##            print(row['actions executed'], row['number of fields'], row['successful submit'])
            fitness = (int(row['actions executed']) / int(row['number of fields'])) * int(row['successful submit'] == 'yes')
            print(fitness)
