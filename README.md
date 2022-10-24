# NLP-Questions-Generation
A rule-based NLP program to generate cohesive and coherent questions based on an English document.

## Backend
`Java 1.8` installed. An API call will be made using Java Virtual Machine to connect to `StanfordCoreNLP` server to parse the strings. Java version (32bit/64bit) depends on individual machine.

`os.system('java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer   -port 9000 -timeout 150000')`

Folder `stanford-core-nlp-4.5.0` needs to be in the same folder for the call to work. The .jar files in this folder have been unzipped and modified to fit the purpose of this project, so the folder is smaller than if downloaded from Stanford Core NLP website. More information: https://stanfordnlp.github.io/CoreNLP/.

Main packages needed are `stanfordcorenlp`, `language_tool_python`, and `nltk`. These should be installed with `pip`, along with the full list of packages in `requirements.txt`. This can also be done in-script with `subprocess.check_call([sys.executable, "-m", "pip", "install", "stanfordcorenlp"])` if the app is to be run locally on different computers.

`punkt` and `averaged_perceptron_tagger` will be downloaded by `nltk`. This is done in-script.

## Frontend
Developed with `flask`, `html`, and `CSS`.

## Ongoing Development
Backend: More robust rules, as well as neural network based generation.

Frontend: Better UI/UX.

## Deployment
Due to the processing requirements of the backend function along with the restrictions on Heroku server memory, only the demo is deployed. Code optimizations and better server options are also in progress.

#### Demo
https://nlp-questions-generation.herokuapp.com/
