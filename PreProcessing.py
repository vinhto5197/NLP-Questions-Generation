from nltk import Tree, pos_tag
from stanfordcorenlp import StanfordCoreNLP

nlp = StanfordCoreNLP('http://localhost', port=9000, quiet=False)
from nltk.tokenize import word_tokenize
from LCA import findLCA
import itertools
from chunks import chunks_parse, is_clause
from helper import enrich_VP, VP_ID
from QG import QG_1, QG_2, QG_3

with open("stopWordList.txt", "r") as file:
    stopWordList = file.read().replace("\n", " ")
stopWordList = dict.fromkeys(stopWordList.split(), 0)


def Question_generation(sentence):
    sentence = sentence.split()
    for idx, word in enumerate(sentence):
        if word[0].lower() + word[1:] in stopWordList:
            sentence[idx] = word[0].lower() + word[1:]
    
    sentence = " ".join(sentence)
    
    segments = sentence.rstrip().rstrip(".").split(", ")
    tree = Tree.fromstring(nlp.parse(sentence))
    ner = nlp.ner(sentence)
    tokens = [word_tokenize(segment) for segment in segments]
    parse_trees = [findLCA(tree, seg[0], seg[-1]) for seg in tokens]
    ner_split = [list(g) for k, g in itertools.groupby(ner, lambda x: x[0] == ',') if not k]
    clause_identification_grammar = "{<DT>?<JJ.?>*<\$|CD|NN.?|PRP|PRP\$|POS|IN|DT|CC|VBG|VBN>+<RB.?|VB.?|MD|RP>+}"
    chunks = [chunks_parse(pos_tag(word_tokenize(segment)), clause_identification_grammar) for segment in segments]
    
    is_clause_val = is_clause(chunks)
    
    new_trees, enrichment_update = enrich_VP(parse_trees)
    parse_trees = new_trees
    update_indices = [i for i, x in enumerate(enrichment_update) if x == True]
    
    for index in update_indices:
        tree = parse_trees[index]
        # Not changing original segments as they will be used later to form questions
        # segments[index] =  " ".join(tree.leaves())
        chunks[index] = chunks_parse(tree.pos(), clause_identification_grammar)
        ner_split[index] = nlp.ner(" ".join(tree.leaves()))
        tokens[index] = tree.leaves()
        # print(ner_split)
        # print(tree.pos())
    
    verb_phrases = VP_ID(parse_trees, is_clause_val, chunks)
    
    Q1 = QG_1(chunks, parse_trees, is_clause_val, ner_split, tokens, verb_phrases)
    Q2 = QG_2(chunks, parse_trees, is_clause_val, ner_split, tokens, verb_phrases)
    Q3 = QG_3(chunks, parse_trees, is_clause_val, ner_split, tokens, verb_phrases)
    
    return [Q1, Q2, Q3]
