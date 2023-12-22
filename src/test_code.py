import os, subprocess, re

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



params = {"URL": "para.testar.org", "PROTOCOL":"webdriver_parabank_strategy", "ACTIONS":30, "STRATEGY_FILE":"C:/Users/testar/Desktop/grammar_strategy.txt"}


#command_params = " ".join([fr'"{p}={params[p]}"' for p in ['URL', 'STRATEGY_FILE', 'ACTIONS', 'PROTOCOL']]) #list all params to include in the command
#command_params = [fr'"{p}={params[p]}"' for p in ['URL', 'STRATEGY_FILE', 'ACTIONS', 'PROTOCOL']]
#command_params = [fr'"{p}={params[p]}"' for p in ['k1', 'k2', 'k3']]


#param_values = [ str(param[p]) for p in params ]
#subprocess.call([batch_path] + param_values)

#subprocess.call(['start_testar2.bat'] + command_params, creationflags=subprocess.CREATE_NEW_CONSOLE)
#subprocess.call(['start_testar2.bat'] + command_params)


# Prepare the command to execute the batch script
batch_script_path = "start_testar2.bat"
#batch_script_path = "variables.bat"

# Construct the command line arguments in the format "KEY=VALUE"
command_args = [f'"{key}={value}"' for key, value in params.items()]

# Construct the command to start the batch script in a new window
#start_command = ['start', 'cmd', '/c', batch_script_path] + command_args
start_command = ['start', 'cmd', '/k', batch_script_path] + command_args

print(start_command)

os.putenv("ACTIONS", "30")
os.putenv("URL", "para.testar.org")
os.putenv("PROTOCOL","webdriver_parabank_strategy")
os.putenv("STRATEGY_FILE","C:/Users/testar/Desktop/grammar_strategy.txt")


# Launch the batch script in a new window
#try:
    # Execute the command
    #process = subprocess.run(start_command, shell=True, check=True)
process = subprocess.call([batch_script_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
    #print(process)
    #print("Batch script executed successfully.")
#except subprocess.CalledProcessError as e:
    #print(f"Error executing batch script: {e}")

path = r'C:\Users\testar\Desktop\TESTAR_dev\testar\target\install\testar\bin\output'
if os.path.isdir(path):
    folder = sorted([os.path.join(path,d) for d in os.listdir(path)], key=os.path.getmtime)[-2] #find folder second most recently modified
    with cd(folder):
        with open('log_filled_forms.txt') as file:
            for row in file:
                print(row)
                if "total" in row:
                    totalSubmits = re.search(r'\d+', row).group()
                    print(totalSubmits)
                    failedSubmits = 0 #init variable
                else:
                    integers = re.findall(r'\d+', row)
                    print(integers)
                    if len(integers) > 1:
                        failedSubmits = failedSubmits + int(integers[-1])
                        print(failedSubmits)



                


