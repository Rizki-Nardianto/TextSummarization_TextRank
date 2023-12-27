# import module
from module import *

# segmentation text
def tokenisasi(text): 
    sentences =[] 
    
    sentences = sent_tokenize(text) 
    for sentence in sentences: 
        sentence.replace("[^a-zA-Z0-9]"," ")

    return sentences 