from algorithm.parameters import params
from pathlib import Path
import random, os, subprocess, csv, re

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
        
def call_testar(ind, new_window = True):
    
##    params = {
##        'SUT' : 'https://webformsut.testar.org/forms/da3dt1emanf1nu0pasra0seateltextimurlusrwee',
##        'STRATEGY_FILE' : f'C:/Users/testar/Desktop/grammar_strategy.txt',
##        'ACTIONS' : '30',
##        'PROTOCOL' : 'webdriver_webformsut_strategy'}
    
    #write individual strategy to file
    with open(params['STRATEGY_FILE'], 'w') as filetowrite:
        filetowrite.write(ind.phenotype)
        #filetowrite.write(ind)

    #list TESTAR-specific parameters
    strategy_params = ['SUT', 'STRATEGY_FILE', 'ACTIONS', 'PROTOCOL']

    for p in strategy_params:
        os.environ[p] = str(params[p]) #add to environment variables before call
    
    if 'http' in params['SUT']: #if sut is an url
        bat_file = "start_testar_url.bat"
    else:
        bat_file = "start_testar_desktop.bat"

    rootpath = Path(__file__).parent.absolute()
    file_to_open = rootpath / bat_file #append to root path

    if new_window:
        subprocess.run([file_to_open], creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        subprocess.run([bat_file])

