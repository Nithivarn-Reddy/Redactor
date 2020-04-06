import glob
import nltk
import re
from nltk import pos_tag
from nltk import ne_chunk, sent_tokenize, word_tokenize
from nltk.corpus import wordnet as wn
from collections import OrderedDict
import os
from subprocess import check_output
import sys
import numpy
from json import dumps

nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

redacted_entity_count=[]
redacted_gender_count=[]
redacted_date_count=[]
redacted_sentences=[]
concept_words=[]



read = lambda x: open(x,'r').read()
filenames=[]
def readFiles(pattern="*.txt"):
    data=[]
    for pat in pattern:
        for file in glob.glob(pat):
            filenames.append(file)
            data.append(read(file))
        #print(data)
    return data

def redact_names(data):
    redacted_list=[]
    for text in data:
        for sentence in sent_tokenize(text):
            ne_tree = nltk.ne_chunk(pos_tag(word_tokenize(sentence)))
            for tree in ne_tree.subtrees(filter=lambda t: t.label() == 'PERSON'):
                for leaf in tree.leaves():
                    redacted_list.append(leaf[0])
    redacted_set = list(set(redacted_list))
    modifieddata_list=[]
    global redacted_entity_count
    for text in data:
        count =0
        final_sentences=[]
        for sentence in sent_tokenize(text):
            modifiedwords=[]
            for word in word_tokenize(sentence):
                if word in redacted_set:
                    modifiedwords.append('\u2588')
                    count+=1
                else:
                    modifiedwords.append(word)
            modified_sentence=' '.join([str(x) for x in modifiedwords])
            final_sentences.append(modified_sentence)
        finaltext =' '.join([str(x) for x in final_sentences])
        modifieddata_list.append(finaltext)
        redacted_entity_count.append(count)
        #print(modifieddata_list)
    return modifieddata_list,redacted_entity_count

def redact_genders(data):
    male_words=set(['guy','spokesman','chairman',"men's",'men'
                ,'him',"he's",'his','boy','boyfriend','boyfriends','boys','brother','brothers',
                'dad','dads','dude','father','fathers','fiance','gentleman','gentlemen','god',
                'grandfather','grandpa','grandson','groom','he','himself','husband','husbands',
                'king','male','man','mr','nephew','nephews','priest','prince','son','sons','uncle',
                'uncles','waiter','widower','widowers'])
    female_words=set(['heroine','spokeswoman','chairwoman',"women's",'actress','women',
                  "she's",'her','aunt','aunts','bride','daughter','daughters','female',
                  'fiancee','girl','girlfriend','girlfriends','girls','goddess','granddaughter',
                  'grandma','grandmother','herself','ladies','lady','lady','mom','moms','mother',
                  'mothers','mrs','ms','niece','nieces','priestess','princess','queens','she',
                  'sister','sisters','waitress','widow','widows','wife','wives','woman'])
    gender_words=list(male_words)+list(female_words)
    gender_words=gender_words + [x.capitalize() for x in gender_words]
    modifieddata_list=[]
    global redacted_gender_count
    for text in data:
        count =0
        final_sentences=[]
        for sentence in sent_tokenize(text):
            modifiedwords=[]
            for word in word_tokenize(sentence):
                if word in gender_words:
                    modifiedwords.append('\u2588')
                    count+=1
                else:
                    modifiedwords.append(word)
            modified_sentence=' '.join([str(x) for x in modifiedwords])
            final_sentences.append(modified_sentence)
        finaltext =' '.join([str(x) for x in final_sentences])
        modifieddata_list.append(finaltext)
        redacted_gender_count.append(count)
    return modifieddata_list,redacted_gender_count

def redact_dates(data):
    date_patterns = '\d{1,2}[\s|th|st]+(?:Jan|Feb|Mar|Apr|May|Jun|July|Aug|Sept|Oct|Nov|Dec)[\s,]*\d{4}|\d{1,2}[\s|th|st]+(?:jan|feb|mar|apr|may|jun|july|aug|sept|oct|nov|dec)[\s,]*\d{4}|\d{1,2}[\s|th|st]+(?:January|February|March|April|May|June|July|August|September|October|November|December)[\s,]*\d{4}|\d{1,2}[\s|th|st]+(?:january|february|march|april|may|june|july|august|september|october|november|december)[\s,]*\d{4}|\d{1,2}[\/-][0-9]{1,2}[\/-]\d{2,4}[\s]?|\d{2,4}[\/-][0-9]{1,2}[\/-]\d{1,2}|(?:Jan|Feb|Mar|Apr|May|Jun|July|Aug|Sept|Oct|Nov|Dec|jan|feb|mar|apr|may|jun|july|aug|sept|oct|nov|dec|January|February|March|April|May|June|July|August|September|October|November|December|january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2}[\s,]+\d{4}'
    modifieddata_list=[]
    global redacted_date_count
    for text in data:
        dates_extracted=re.findall(date_patterns,text)
        redacted_date_count.append(len(dates_extracted))
        for date in dates_extracted:
            text = text.replace(date,'\u2588')
        modifieddata_list.append(text)
    return modifieddata_list,redacted_date_count

def redact_concept(data,concept):
    synsets=[]
    for con in concept:
        synsets += wn.synsets(con)
    global concept_words
    global redacted_sentences
    for each_synset in synsets:
        concept_words+=each_synset.lemma_names()
        hypernymns=each_synset.hypernyms()
        for each_hypernymn in hypernymns:
            concept_words+=each_hypernymn.lemma_names()
        hyponymns=each_synset.hyponyms()
        for each_hyponymn in hyponymns:
            concept_words+=each_hyponymn.lemma_names()
        holonyms=each_synset.member_holonyms()
        for each_holonym in holonyms:
            concept_words+=each_holonym.lemma_names()
        r_hypernymns=each_synset.root_hypernyms()
        for each_r_hypernymn in r_hypernymns:
            concept_words+=each_r_hypernymn.lemma_names()
    concept_words=list(set(concept_words))
    modified_data=[]
    for text in data:
        for sentence in sent_tokenize(text):
            for word in concept_words:
                if word in sentence:
                    text= text.replace(sentence,'\u2588')
                    redacted_sentences.append(sentence)
                    break
        modified_data.append(text)
    return modified_data,redacted_sentences,concept_words

def stats(args):
    d = OrderedDict()
    d["names"]=redacted_entity_count
    d["dates"]=redacted_date_count
    d["genders"]=redacted_gender_count
    d["redacted_sentences"]=redacted_sentences
    d["concept words"]=concept_words
    if args == "stderr" or args=="STDERR":
        print(dumps(d),file=sys.stderr)
    elif args == "stdout" or args == "STDOUT":
        print(dumps(d))
    else:
        with open(args+".txt","w") as f:
            f.write(dumps(d))

def write_output(data,outpath):
    if not os.path.exists(os.getcwd()+"/"+outpath):
        os.mkdir(outpath)
    for (file,outdata) in zip(filenames,data):
        file_name,extension=file.split("/")[-1].split(".")[0],file.split("/")[-1].split(".")[1]
        output_filename=file_name+".redacted."+extension
        path=os.getcwd()+"/"+outpath+"/"+output_filename
        with open(path,"w") as f:
            f.write(outdata)

