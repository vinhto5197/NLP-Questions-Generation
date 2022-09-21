import subprocess
import sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "stanfordcorenlp"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "language_tool_python"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "nltk"])

from threading import Thread
import time
import os
cur_dir = os.getcwd()

def connect():
    os.chdir("stanford-corenlp-4.5.0") # need to change back to current directory, otherwise we would be in another folder
    os.system('java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer   -port 9000 -timeout 150000')

Thread(target = connect).start()
time.sleep(1)
os.chdir(cur_dir)
from ask import ask

if __name__ == "__main__":
    res = ask()
    time.sleep(1)
    print(res)