import streamlit as st
import joblib
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer 

with open('product_list', 'rb') as file:
    product_list =joblib.load(file)
with open('similarity', 'rb') as file:
    similarity =joblib.load(file)

def recommended(texts):
    x = []
    y = []
    index = product_list[product_list['Tag_product'].str.contains(pat = texts)].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    for i in distances [0 : 5]:
        x.append(product_list.iloc[i[0]].Product)
        y.append(product_list.iloc[i[0]].ratings)
    xs = pd.DataFrame([x, y]).T
    xs = xs.rename(columns = {0 : 'p', 1 : 'r'})
    xs = xs.sort_values(by='r', ascending=False)
    for index, row in xs.iterrows():
        st.write("Barang : " + str(row["p"]))
        st.write("Rating : " + str(row['r']))

def clean(txt):
    import re
    txt = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", txt)
    return txt

def stop(txt):
    stop_words = set(stopwords.words("english"))
    text = txt
    text = " ".join([word for word in text.split() if word not in stop_words])
    return text

def stemming(txt):
    ps = PorterStemmer()
    y = [] 
    for i in txt.split():
        y.append(ps.stem(i))
    
    return " ".join(y)

def Lemmatizer(txt):
    lemmatizer = WordNetLemmatizer()
    y = []
    
    for i in txt.split():
        y.append(lemmatizer.lemmatize(i))
    
    return " ".join(y)
    
st.title('Recomended Product')
texts = st.text_input('Enter Product : ')
texts = texts.lower()
texts = clean(texts)
texts = stop(texts)
texts = stemming(texts)
texts = Lemmatizer(texts)

if st.button('Searching'):
    if texts:
        while True:
            try:
                recommended(texts)
                break
            except (IndexError):
                st.write('barang tidak ada')
                break
    else:
        st.write('masukan kata kunci')