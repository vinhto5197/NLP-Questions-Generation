# NLP-Questions-Generation
A rule-based NLP program to generate cohesive and coherent questions based on an English document. Frontend development in progress.

## Requirements
`Java 1.8` installed. An API call will be made using Java to connect to `StanfordCoreNLP` server to parse the strings. Java version (32bit/64bit) depends on individual machine.

`os.system('java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer   -port 9000 -timeout 150000')`

Folder `stanford-core-nlp-4.5.0` needs to be in the same folder for the call to work.

To ensure packages are installed, the required packages will be installed when `main.py` is run without user installing themselves.

`subprocess.check_call([sys.executable, "-m", "pip", "install", "stanfordcorenlp"])`

`subprocess.check_call([sys.executable, "-m", "pip", "install", "language_tool_python"])`

`subprocess.check_call([sys.executable, "-m", "pip", "install", "nltk"])`

`punkt` will also be downloaded by `nltk`. This is done in-script.

## Ongoing Development
Frontend and more robust rules, as well as neural network based generation.
