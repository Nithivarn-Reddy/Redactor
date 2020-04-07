# cs5293p20-project-1
The main aim of this project is to redact the important information like names,dates,genders and also redact information regarding a particular concept. It also finally provides some information of statistics of what has been redacted.
I have taken two sample essays from the internet and performed my analysis on it.

### Author - Nithivarn Reddy Shanigaram 

### Email - nithivarn.reddy.shanigaram-1@ou.edu

### Structure
```
.
└── cs5293p20-project-1
    ├── COLLABORATORS
    ├── LICENSE
    ├── Pipfile
    ├── Pipfile.lock
    ├── README.md
    ├── files
    │   ├── modi.redacted.txt
    │   └── text1.redacted.txt
    ├── modi.txt
    ├── otherfiles
    │   ├── test.md
    │   └── test_1.txt
    ├── project1
    │   ├── __init__.py
    │   ├── project1.py
    │   └── redactor.py
    ├── setup.py
    ├── tests
    │   ├── __init__.py
    │   └── test_redact.py
    └── text1.txt
```

External Packages used 

> nltk

> glob

> Pytest

## Steps to install the project

Open your Terminal..

1) git clone the project 

2) Install pipenv in your system 

  - if it is debain based
    Run the following command
    
    pip install pipenv
    
3) cd into cs5293p20-project-1

4) Run pipenv install
  
 This command installs all the dependencies required by the project. (provided in the Pipfile)

## Steps to Run the project

Now run the project using the following command (Inside the cs5293p20-project-0)

 > pipenv run python project1/redactor.py --input '*.txt' \
                    --input 'otherfiles/*.md' \
                    --names --dates \
                    --concept 'kids' \
                    --output 'files/' \
                    --stats stderr
  
This will display the result in your console / terminal.

## To run testcases 
Go inside the virtual environment by running the following commands.

1) cd cs5293p20-project-1

2) Run pipenv shell

3) Run pytest

## Assumptions made in the project are

1) --names flag redacts only entities of type 'PERSON'.

2) The data present in the multi-line is separated by extra "\n" when it is extracted.

3) Data is Missing in Nature Column only.

4) Missing data is replaced with NULL value.

5) The database is created once with the name "normanpd.db" 

6) The table_name is "incidents" which is dropped everytime.

Approach for extracting names:
  During extraction of names from the text files , first I have broken all paragraphs into sentences and later each sentence into individual words. Creating a words_list.Then applied the pos_tag to get the parts of speech tag for each word and then apply ne_chunk to get the named_entities like PERSON names from the text. But this approach was even giving me extra words like GOODS, SERVICE, TEX so on. But later I realized that the approach of creating a words_list and then applying pos_tag is wrong as the parts of speech of each word depends on the context where it is used in the sentence. So I have changed my approach and applied ne_chunk on pos_tagged words of each sentence and extracted the named_entities from them. This approach has given me good results than the previous way.
  
[https://stackoverflow.com/questions/14841997/how-to-navigate-a-nltk-tree-tree]

Approach for extracting genders from text:
  During the extraction of genders from the text , I have tried using WordNet and synoymns but it didn't workout the corpus for synoymns and antonymns are to less, so I have explicitly taken a list of male_words and female_words and combined them into a list of gender_words . I have also added camel-cased gender_words to the gender_words list and then redacted the words which are part of this list.
  [http://nealcaren.github.io/text-as-data/html/times_gender.html]
  
Approach for matching dates :

date formats considered = 'dd/mm/yyyy | dd-mm-yyyy | yyyy-mm-dd | yyyy/mm/dd | yyyy-dd-mm | yyyy/dd/mm | mm/dd/yyyy | mm-dd-yyyy | dd (January-December|jan-dec|Jan-Dec|january-decemeber) , yyyy | dd(th) (January-December|jan-dec|Jan-Dec|january-decemeber) yyyy | dd(st) (January-December|jan-dec|Jan-Dec|january-decemeber) yyyy | (January-December|jan-dec|Jan-Dec|january-decemeber) dd , yyyy .

I am extracting the dates of the above format and redacting them. For this to work , I have written a regular expression that matches the above mentioned date formats. It doesn't redact text containing only months and year or only year.

[https://stackoverflow.com/questions/10308970/matching-dates-with-regular-expressions-in-python]
[https://docs.python.org/3/library/re.html]


Approach for extracting concept :
I am passing each concept into the extract_concept function along with the concept to be searched for. I have wordnet synset derived from nltk.corpus for getting all the synsets related to the concept. Then I have searched for hypernymns, homonymns,holonymns of each synset of the concept. I have not taken into account the meronymns as they talk about part of the concept or the substances which contain the concept. I have formed a list of words from each synset of the concept and searched whether each sentence contains any word of the list of words(the synonymns.hypernymns,hyonymns,holonymns). If the sentence contains any word then it is redacted. This approach may have certain errors as wordnet works well for verbs and noun.

Reference - Text book.







