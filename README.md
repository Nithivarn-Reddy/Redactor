# cs5293p20-project-1




Approach for extracting names:
  During extraction of names from the text files , first I have broken all paragraphs into sentences and later each sentence into individual words. Creating a words_list.Then applied the pos_tag to get the parts of speech tag for each word and then apply ne_chunk to get the named_entities like PERSON names from the text. But this approach was even giving me extra words like GOODS, SERVICE, TEX so on. But later I realized that the approach of creating a words_list and then applying pos_tag is wrong as the parts of speech of each word depends on the context where it is used in the sentence. So I have changed my approach and applied ne_chunk on pos_tagged words of each sentence and extracted the named_entities from them. This approach has given me good results than the previous way.
  
[https://stackoverflow.com/questions/14841997/how-to-navigate-a-nltk-tree-tree]
  
