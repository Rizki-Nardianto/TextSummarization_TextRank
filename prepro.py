#import module
from module import *

# filtering(stopword)
def filtering_text(text):

    factory = StopWordRemoverFactory()
    stopword = factory.create_stop_word_remover()
    stop = stopword.remove(text)

    return stop