from chunks import chunks_find, chunks_parse
from nltk import Tree

def only_VP(trees):
    return [tree.label() == 'VP' for tree in trees]

def closest_NP_VP(trees):
    is_VP = only_VP(trees)
    closest_NP = []
    for index,truth_val in enumerate(is_VP):
        if not truth_val:
            closest_NP.append(None)
        else:
            found_NP = False
            for index_tree in reversed(range(0,index)):
                for child in trees[index_tree] :
                    if child.label() == 'NP':
                        closest_NP.append(child)
                        found_NP = True
                        break
                if found_NP:
                    break
            if not found_NP :
                closest_NP.append(None)
    return closest_NP

def enrich_VP(trees):
    data = closest_NP_VP(trees)
    enriched_trees =  []
    for tree,enrich in zip(trees,data):
        if enrich:
            enriched_trees.append(Tree('S', [enrich.copy(deep=True),tree]))
        else:
            enriched_trees.append(tree)
    return enriched_trees, [not not dat for dat in data]


def find_VP_tree(tree):
    for child in tree :
        if child.label() == "VP":
            return child   
def find_NP_tree(tree):
    for child in tree :
        if child.label() == "NP":
            return child

        
def VP_NP_parts(parse_tree,chunk_tree) :
    NP = find_NP_tree(parse_tree).leaves()
    VP = find_VP_tree(parse_tree).leaves()
    NP_POS = []
    VP_POS = []
    chunk_pos = chunk_tree.pos()
    for pos in chunk_pos:
        if pos[0][0] in NP :
            NP.remove(pos[0][0])
            NP_POS.append(pos[0])
        elif pos[0][0] in VP:
            VP.remove(pos[0][0])
            VP_POS.append(pos[0])
    return NP_POS,VP_POS


def ner_tags_pos(ners,pos):
    return list(filter(lambda x : x[0] in [p[0] for p in pos] , ners))


def find_subj(parse_tree):
    for child in parse_tree :
        if child.label() == "NP":
            return child.leaves()
    return []
def find_VP(parse_tree):
    for child  in parse_tree :
        if child.label() == "VP":
            return child.leaves()
    return []

def VP_ID(trees,is_clause,chunks):
    VP = [] 
    for tree,chunk,is_clause in zip(trees,chunks,is_clause) :
        if is_clause :
            chunk_tree = chunks_find(chunk)[0]
            NP_POS,VP_POS = VP_NP_parts(tree,chunk_tree)
            if len(VP_POS) > 1 :
                VP.append(VP_POS[0][0])
            else :
                vp_tag = VP_POS[0][1]
                if vp_tag == "VBD" :
                    VP.append("did")
                elif vp_tag == "VBP" or vp_tag == "VB" :
                    VP.append("do")
                elif vp_tag == "VBZ" :
                    VP.append("does")
                else :
                    VP.append(None)
        else :
            VP.append(None)
    return VP


def ner_tag_tokens(ners,tokens):
    return list(filter(lambda x : x[0] in tokens , ners))


def ner_tag_token(ners,token):
    for tag in ners:
        if tag[0] == token :
            return tag[1]
    return None


def pos_tokens_chunk_tree(c_tree):
    pos = [p for p in c_tree.leaves()] if c_tree else []
    tokens = [pos[0] for pos in pos] if c_tree else []
    return pos,tokens

        
def QG_help(ner_chunk_tags,QSG_rule) :
    disambg_value =  ner_chunk_tags[0][1] in ['LOCATION','ORGANIZATION', 'CITY','COUNTRY']
    if QSG_rule == "QG_1" :
        if disambg_value :
            return disambg_value,"what"
        elif ner_chunk_tags[0][1] in ['PERSON']:
            return disambg_value, "who"
        else:
            return disambg_value, "what"
    if QSG_rule == "QG_3":
        if disambg_value :
            return disambg_value,"where"
        else :
            return disambg_value,"what"


def QG_help1(chunk_pos) :
    disambg_value =  all( [x == "PRP" for x in [p[1] for p in chunk_pos]])
    if disambg_value :
        return disambg_value,"whom"
    else:
        return disambg_value,"what"


def QG_help2(chunk_pos,chunk_ners) :
    first_noun_chunk  = chunks_find(chunks_parse(chunk_pos , "{<NN.?>+}"))
    if first_noun_chunk :
        first_noun_pos, first_noun_tokens = pos_tokens_chunk_tree(first_noun_chunk[0])
        if ner_tag_token(chunk_ners,first_noun_tokens[0]) == "PERSON":
            return True,"Whom"
        else:
            return False,"What"
    else: 
        return False,"What"
    
    
def QG_help3(chunk_pos,chunk_ners) :
    noun_chunk  = chunks_find(chunks_parse(chunk_pos , "{<NN.?>+}"))
    if noun_chunk :
        noun_pos, noun_tokens = pos_tokens_chunk_tree(noun_chunk[0])
        noun_ners = ner_tag_tokens(chunk_ners,noun_tokens)
        ners = set([ x[1] for x in noun_ners])
        if "TIME" in ners or "DATE" in ners :
            return "when"
        else:
            return "what"
    else: 
        return "What"