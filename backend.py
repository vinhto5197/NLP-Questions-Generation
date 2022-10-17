def gen(num_q, txt):

    from threading import Thread
    import time
    import os
    cur_dir = os.getcwd()

    def connect():
        # need to change back to current directory, otherwise we would be in another folder
        os.chdir("stanford-corenlp-4.5.0")
        os.system('java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer   -port 9000 -timeout 150000')

    Thread(target=connect).start()
    time.sleep(1)
    os.chdir(cur_dir)
    from ask import ask

    res = ask(num_q, txt)
    time.sleep(1)
    return res
