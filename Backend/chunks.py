from nltk.chunk import RegexpParser
import nltk

def chunks_parse(tgd_sgmt , grammar):
    grammar = r"CHUNK: " + grammar
    regex = RegexpParser(grammar)
    res = regex.parse(tgd_sgmt)
    return res

def chunks_find(chunks):
    if not isinstance(chunks, nltk.tree.Tree):
         return [[sub_tree for sub_tree in chunk.subtrees(filter = lambda x: x.label() in ['CHUNK'])] for chunk in chunks]   
    else :
        return [sub_tree for sub_tree in chunks.subtrees(filter = lambda x: x.label() in ['CHUNK'])]
    
def is_clause(chunks):
    if not isinstance(chunks, nltk.Tree):
         return [not not chunk for chunk in chunks_find(chunks)]
    else :
        return not not chunks_find(chunks)