# import module
from module import *

# evaluation summary
def evaluation_rouge(summarytext,summaryreference): 
    ROUGE = Rouge() 
    evaluationtext = ROUGE.get_scores(summarytext, summaryreference) 
    return evaluationtext 