import re, shutil

class FileHandler:
    
    @staticmethod
    def replaceStrategy(file, strategy):
        with open(file, 'w') as filetowrite:
            filetowrite.write(strategy)

    @staticmethod
    def readMetrics(file):
        with open(file, 'r') as filetoread:
            return filetoread.read()

    @staticmethod
    def copyMetrics(source, destination):
        shutil.copy2(source, destination) #including metadata
