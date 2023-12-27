# import module
from module import *

# calculate wight term (TF-IDF)
def tfidffuc(sentc): 
    vectorizer = TfidfVectorizer() 
    vectors = vectorizer.fit_transform(sentc) 
    return vectors

# dataframe tfidf
def dftfidf(sentc): 
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(sentc)
    feature_names = vectorizer.get_feature_names_out(vectors) 
    dense = vectors.todense() 
    denselist = dense.tolist()
    df = pd.DataFrame(denselist, columns=feature_names) 
    return df  