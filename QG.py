from chunks import chunks_find, chunks_parse
from helper import ner_tags_pos, QG_help, find_subj, find_VP, pos_tokens_chunk_tree, VP_ID,\
    QG_help1, ner_tag_tokens, QG_help2, QG_help3
from LCA import findLCA


def QG_1(chunks, parse_trees, is_clause_val, ner_split, tokens, verb_phrases):
    try:
        for chunk, parse_tree, is_cl, ner, tok in zip(chunks, parse_trees, is_clause_val, ner_split, tokens):
            if is_cl:
                chunk_pos = [pos[0] for pos in chunks_find(chunk)[0].pos()]
                grammar = "{<DT>?<JJ.?>*<NN.?|PRP|PRP$|POS|IN|DT|CC|VBG|VBN>+}"
                rule1_chunks = chunks_parse(chunk_pos, grammar)
                noun_chunk = chunks_find(rule1_chunks)
                if noun_chunk:
                    noun_pos = noun_chunk[0].leaves()
                    tok = tok[:]
                    ner_tags = ner_tags_pos(ner, noun_pos)
                    _, q_disambg = QG_help(ner_tags, "QG_1")
                    answer_words = [p[0] for p in noun_pos]
                    [tok.remove(ans) for ans in answer_words if ans in tok]
                    quest_tok = [q_disambg] + tok
                    question = " ".join(quest_tok) + "?"

                    question = question[0].upper() + question[1:]
                    return question
    except:
        return ""


def QG_2(chunks, parse_trees, is_clause_val, ner_split, tokens, verb_phrases):
    try:
        for chunk, parse_tree, is_cl, ner, tok, verb in zip(chunks, parse_trees, is_clause_val,
                                                            ner_split, tokens, verb_phrases):
            rule_grammar = "{<DT>?<CD>+<RB>?<JJ|JJR|JJS>?<NN|NNS|NNP|NNPS|VBG>+}"
            seg_pos = parse_tree.pos()
            rule7_chunks = chunks_parse(seg_pos, rule_grammar)
            prep_chunk = chunks_find(rule7_chunks)
            if prep_chunk:
                prep_pos = [pos[0] for pos in prep_chunk[0].pos()]
                prep_tokens = [pos[0][0] for pos in prep_chunk[0].pos()]
                ans_tokens = [p[0]for p in chunks_find(chunks_parse(prep_pos, "{<CD>+}"))[0].leaves()]
                VP = find_VP(parse_tree)
                if not VP:
                    break
                rem_verb_phrase = verb if verb in VP else VP[0]
                [prep_tokens.remove(x) for x in ans_tokens if x in prep_tokens]
                subject = find_subj(parse_tree)
                [VP.remove(x) for x in prep_tokens + ans_tokens + [rem_verb_phrase] if x in VP]
                tok = tok[:]
                [tok.remove(x) for x in subject + VP + prep_tokens + ans_tokens + [rem_verb_phrase] if x in tok]
                quest_tok = ["how", "many"]+ prep_tokens + [verb] + subject + VP + tok
                question = " ".join(quest_tok) + "?"

                question = question[0].upper() + question[1:]
                return question
    except:
        return ""


def QG_3(chunks, parse_trees, is_clause_val, ner_split, tokens, verb_phrases):
    try:
        for chunk, parse_tree, is_cl, ner, tok, verb in zip(chunks, parse_trees, is_clause_val,
                                                            ner_split, tokens, verb_phrases):

            rule_grammar = "{<IN>+<DT>?<RB.?>*<JJ.?>*<NN.?|PRP|PRP\$|POS|VBG|DT|CD|VBN>+}"
            seg_pos = parse_tree.pos()
            rule2_2_chunks = chunks_parse(seg_pos, rule_grammar)
            seg = " ".join([p[0] for p in seg_pos])

            prep_chunk = chunks_find(rule2_2_chunks)
            prep_pos, prep_tokens = pos_tokens_chunk_tree(prep_chunk[0]) if prep_chunk else (None, None)

            clause_chunk = chunks_find(chunk)

            if len(clause_chunk) > 1:
                clause_strings = [" ".join(pos_tokens_chunk_tree(c)[1]) for c in clause_chunk]
                prep_index = seg.index(seg)
                clause_index = [abs(seg.index(cs)-prep_index) for cs in clause_strings]
                cl_chunk = clause_chunk[clause_index.index(min(clause_index))]
                cl_string = clause_strings[clause_index.index(min(clause_index))].split(" ")
                verb = VP_ID([findLCA(parse_tree, cl_string[0], cl_string[-1])], [True], [cl_chunk])[0]
            else:
                cl_chunk = clause_chunk[0] if clause_chunk else None
            cl_pos, cl_tokens = pos_tokens_chunk_tree(cl_chunk)

            if prep_chunk:
                q_prep = chunks_find(chunks_parse(seg_pos, "{<IN+>}"))[0]
                q_prep_pos, q_prep_tokens = pos_tokens_chunk_tree(q_prep)

                ques = "what"
                qsd1, ques = QG_help1(prep_pos)
                if not qsd1:
                    prep_ners = ner_tag_tokens(ner, prep_tokens)
                    qsd3, ques = QG_help2(prep_pos, prep_ners)
                    ques = ques
                    if not qsd3:
                        qsd4, ques = QG_help(prep_ners, "QG_3")
                    if not qsd4:
                        ques = QG_help3(prep_pos, prep_ners)

                VP = find_VP(parse_tree)
                if not VP:
                    break
                rem_verb_phrase = verb if verb in VP else VP[0]

                subject = find_subj(parse_tree)

                [VP.remove(x) for x in prep_tokens + [rem_verb_phrase] if x in tok]
                tok = tok[:]
                [tok.remove(x) for x in prep_tokens + VP + [rem_verb_phrase] + subject if x in tok]
                quest_tok = q_prep_tokens + [ques] + [verb] + subject + VP + tok
                question = " ".join(quest_tok) + "?"

                question = question[0].upper() + question[1:]
                return question
    except:
        return ""
