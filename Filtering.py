import pickle
import re
import string
import nltk
import pandas as pd
import numpy as np
from html.parser import HTMLParser
html_parser = HTMLParser()
from sklearn.feature_extraction.text import CountVectorizer
import pickle
filename="./newmodel/"
loaded_model = pickle.load(open(filename+"final-model.sav", 'rb'))
loaded_feature_names=pickle.load(open(filename+"feature_names.sav",'rb'))
loaded_vocabulary=pickle.load(open(filename+"feature_vocabulary.sav",'rb'))

#nltk.download('stopwords')
#nltk.download('punkt')
#nltk.download('wordnet')
from nltk.corpus import stopwords
english_stopwords = set(stopwords.words('english'))

from nltk.tokenize import word_tokenize, TweetTokenizer
tokenizer=TweetTokenizer()

from nltk.stem import PorterStemmer, LancasterStemmer, SnowballStemmer
stemming = SnowballStemmer("english")

from nltk.stem.wordnet import WordNetLemmatizer
lemmatizing = WordNetLemmatizer()

#---------------this section for later used preprocessing----------------------------------
apostrophe_dict = {
      "ain't": "am not / are not",
      "aren't": "are not / am not", 
      "can't": "cannot", 
      "can't've": "cannot have",
      "'cause": "because", 
      "could've": "could have", 
      "couldn't": "could not", 
      "couldn't've": "could not have",
      "didn't": "did not", 
      "doesn't": "does not",
      "don't": "do not", 
      "hadn't": "had not", 
      "hadn't've": "had not have",
      "hasn't": "has not", 
      "haven't": "have not", 
      "he'd": "he had / he would", 
      "he'd've": "he would have",
      "he'll": "he shall / he will", 
      "he'll've": "he shall have / he will have", 
      "he's": "he has / he is",
      "how'd": "how did", 
      "how'd'y": "how do you", 
      "how'll": "how will", 
      "how's": "how has / how is",
      "i'd": "I had / I would", 
      "i'd've": "I would have", 
      "i'll": "I shall / I will", 
      "i'll've": "I shall have / I will have",
      "i'm": "I am", "I'm": "I am", 
      "i've": "I have", 
      "isn't": "is not", 
      "it'd": "it had / it would",
      "it'd've": "it would have",
      "it'll": "it shall / it will",
      "it'll've": "it shall have / it will have",
      "it's": "it has / it is",
      "let's": "let us",
      "ma'am": "madam",
      "mayn't": "may not",
      "might've": "might have",
      "mightn't": "might not",
      "mightn't've": "might not have",
      "must've": "must have",
      "mustn't": "must not",
      "mustn't've": "must not have",
      "needn't": "need not",
      "needn't've": "need not have",
      "o'clock": "of the clock",
      "oughtn't": "ought not",
      "oughtn't've": "ought not have",
      "shan't": "shall not",
      "sha'n't": "shall not",
      "shan't've": "shall not have",
      "she'd": "she had / she would",
      "she'd've": "she would have",
      "she'll": "she shall / she will",
      "she'll've": "she shall have / she will have",
      "she's": "she has / she is",
      "should've": "should have",
      "shouldn't": "should not",
      "shouldn't've": "should not have",
      "so've": "so have",
      "so's": "so as / so is",
      "that'd": "that would / that had",
      "that'd've": "that would have",
      "that's": "that has / that is",
      "there'd": "there had / there would",
      "there'd've": "there would have",
      "there's": "there has / there is",
      "they'd": "they had / they would",
      "they'd've": "they would have",
      "they'll": "they shall / they will",
      "they'll've": "they shall have / they will have",
      "they're": "they are",
      "they've": "they have",
      "to've": "to have",
      "wasn't": "was not",
      "we'd": "we had / we would",
      "we'd've": "we would have",
      "we'll": "we will",
      "we'll've": "we will have",
      "we're": "we are",
      "we've": "we have",
      "weren't": "were not",
      "what'll": "what shall / what will",
      "what'll've": "what shall have / what will have",
      "what're": "what are",
      "what's": "what has / what is",
      "what've": "what have",
      "when's": "when has / when is",
      "when've": "when have",
      "where'd": "where did",
      "where's": "where has / where is",
      "where've": "where have",
      "who'll": "who shall / who will",
      "who'll've": "who shall have / who will have",
      "who's": "who has / who is",
      "who've": "who have",
      "why's": "why has / why is",
      "why've": "why have",
      "will've": "will have",
      "won't": "will not",
      "won't've": "will not have",
      "would've": "would have",
      "wouldn't": "would not",
      "wouldn't've": "would not have",
      "y'all": "you all",
      "y'all'd": "you all would",
      "y'all'd've": "you all would have",
      "y'all're": "you all are",
      "y'all've": "you all have",
      "you'd": "you had / you would",
      "you'd've": "you would have",
      "you'll": "you shall / you will",
      "you'll've": "you shall have / you will have",
      "you're": "you are",
      "you've": "you have"
      }

short_word_dict = {
      " 121 ": "one to one", " a/s/l ": "age, sex, location", " adn ": "any day now", " afaik ": "as far as I know",
      " afk ": "away from keyboard", " aight ": "alright", " alol ": "actually laughing out loud", " b4 ": "before",
      " b4n ": "bye for now", " bak ": "back at the keyboard", " bf ": "boyfriend", " bff ": "best friends forever", 
      " bfn ": "bye for now", " bg ": "big grin", " bta ": "but then again", " btw ": "by the way", 
      " cid ": "crying in disgrace", " cnp ": "continued in my next post", " cp ": "chat post", " cu ": "see you",
      " cul ": "see you later", " cul8r ": "see you later", " cya ": "bye", " cyo ": "see you online",
      " dbau ": "doing business as usual", " fud ": "fear, uncertainty, and doubt", " fwiw ": "for what it's worth",
      " fyi ": "for your information", " g ": "grin", " g2g ": "got to go", " ga ": "go ahead", " gal ": "get a life",
      " gf ": "girlfriend", " gfn ": "gone for now", " gmbo ": "giggling my butt off", " gmta ": "great minds think alike",
      " h8 ": "hate", " hagn ": "have a good night", " hdop ": "help delete online predators", " hhis ": "hanging head in shame",
      " iac ": "in any case", " ianal ": "I am not a lawyer", " ic ": "I see", " idk ": "I don't know",
      " imao ": "in my arrogant opinion", " imnsho ": "in my not so humble opinion", " imo ": "in my opinion",
      " iow ": "in other words", " ipn ": "I’m posting naked", " irl ": "in real life", " jk ": "just kidding",
      " l8r ": "later", " ld ": "later, dude", " ldr ": "long distance relationship", " llta ": "lots and lots of thunderous applause",
      " lmao ": "laugh my ass off", " lmirl ": "let's meet in real life", " lol ": "laugh out loud", 
      " ltr ": "longterm relationship", " lulab ": "love you like a brother", " lulas ": "love you like a sister",
      " luv ": "love", " m/f ": "male or female", " m8 ": "mate", " milf ": "mother I would like to fuck", 
      " oll ": "online love", " omg ": "oh my god", " otoh ": "on the other hand", " pir ": "parent in room", 
      " ppl ": "people", " r ": "are", " rofl ": "roll on the floor laughing", " rpg ": "role playing games",
      " ru ": "are you", " shid ": "slaps head in disgust", " somy ": "sick of me yet", " sot ": "short of time",
      " thanx ": "thanks", " thx ": "thanks", " ttyl ": "talk to you later", " u ": "you", " ur ": "you are",
      " uw ": "you’re welcome", " wb ": "welcome back", " wfm ": "works for me", " wibni ": "wouldn't it be nice if",
      " wtf ": "what the fuck", " wtg ": "way to go", " wtgp ": "want to go private", " ym ": "young man", " gr8 ": "great","fkin":"fuck","fk":"fuck"
      }

def create_dataframe(comment=""):
  comment_as_list=[comment]
  data = {'comment_text':comment_as_list} 
  df_train = pd.DataFrame(data)
  return df_train
    


def remove_html(df_train):
  df_train['comment_text'] = df_train['comment_text'].apply(lambda x: html_parser.unescape(x))
  return df_train

def make_lower(df_train):
  df_train['comment_text'] = df_train['comment_text'].str.lower()
  return df_train

def expand_apstrophe(df_train,apostrophe_dict=apostrophe_dict):
      df_train['comment_text'] = df_train['comment_text'].replace(apostrophe_dict, regex=True)
      return df_train

      
      
def expand_short_words(df_train,short_word_dict=short_word_dict):
  df_train['comment_text'] = df_train['comment_text'].replace(short_word_dict, regex=True)
  return df_train
        
      

def train_words_cleaning(text):
#     #replace paranthesis
#     text = text.str.replace(r"\(.*\)","")
#     #replace square brackets
#     text = text.str.replace(r"\[.*\]","")
    #replace newline characters
    text = text.replace('\n',' ', regex=True)
    #replace carriage return characters
    text = text.replace('\r',' ', regex=True)
    #replace tab characters
    text = text.replace('\t',' ', regex=True)
    #replace form feed characters
    text = text.replace('\f',' ', regex=True)
    #replace " " " 
    text = text.replace("\"",'', regex=True)
    #replace " ' "
    text = text.replace("\'",'', regex=True)
    #replace "anything except alphanumeric"
    text = text.replace('[^A-Za-z\s]+', '', regex=True)
    #replace "multiple whitespace with single whitespace
    text = text.replace('[ ]+', ' ', regex=True)
    #stripping the sentense from left and right
    text = text.str.strip()
    # deleting numbers
    text = text.str.replace('\d+', '', regex=True)
    return text

def words_engineering(text):
    text = text.apply(lambda x: word_tokenize(x))
    text = text.apply(lambda x: [w for w in x if not w in english_stopwords])
    text = text.apply(lambda x: [stemming.stem(i) for i in x])
    text = text.apply(lambda x: ' '.join([lemmatizing.lemmatize(i, "v") for i in x]))
    return text

def train_cleaning(df_train):
    df_train['comment_text'] = train_words_cleaning(df_train['comment_text'])
    df_train['comment_text'] = words_engineering(df_train['comment_text'])
    return df_train['comment_text']
  

def filtering(comment):
  predict=[]
  df_train=create_dataframe()
  df_train['comment_text'] = train_cleaning(expand_short_words(expand_apstrophe(make_lower(remove_html(create_dataframe(comment))))))
  tokenizer =  CountVectorizer(stop_words='english',vocabulary=loaded_feature_names)
  tokenizer.fit(df_train['comment_text'])
  df_traintf = tokenizer.transform(df_train['comment_text'])
  cleaned_comment = pd.DataFrame(df_traintf.toarray(), columns = tokenizer.get_feature_names())
  for index in range(7):
    predict.append((loaded_model[index].predict(cleaned_comment)).item())
  return predict

  

print(filtering(''))