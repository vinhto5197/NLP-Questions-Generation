import numpy as np
from PreProcessing import Question_generation
import nltk.data
import language_tool_python

def ask(num_questions = 3, text_link = "sample_txt.txt"):
    nltk.download('punkt')
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    tool = language_tool_python.LanguageTool('en-US')
    
    count = 0
    sentences_done = {}
    res = []
    
    num_questions = 3
    text_link = "sample_txt.txt"
    
    with open(text_link, "r") as f:
        text = f.read()
        
    text = text.split("\n")
    text = ".".join(text)
    text = text.split(":")
    text = ".".join(text)
    text = text.split(";")
    text = ".".join(text)
    text = text.split(".")
    text = list(filter(None, text))
    
    while count < int(num_questions):
        idx = np.random.randint(0, len(text))
        if idx not in sentences_done:
            sentences_done[idx] = 1
            sentence = text[idx]
            try:
                questions = Question_generation(sentence)
                for i in range(len(questions)):
                    if not questions[i]:
                        next
                    else:
                        matches = tool.check(questions[i])
                        if not len(matches):
                            res.append(questions[i])
                            count += 1
                            break
            except:
                continue
        else:
            continue
    
    return res