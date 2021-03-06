import streamlit as st
import pandas as pd
import spacy
from spacy.pipeline import EntityRuler
from spacy.lang.en import English
from spacy.tokens import Doc
from spacy import displacy
#nltk
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download(['stopwords','wordnet','omw-1.4'])


#warning
import warnings 
warnings.filterwarnings('ignore')

st.title("NLP - Resume Analysis")
skill_pattern_path = "jz_skill_patterns.jsonl"

@st.cache(allow_output_mutation=True)
def init_df(path):
    df = pd.read_csv(path)
    df = df[['id', 'Category', 'Resume', 'Raw_html']]
    return df

@st.cache
def init_nlp():
    pass

df = init_df('temp.csv')

nlp = spacy.load("en_core_web_lg")
ruler = nlp.add_pipe("entity_ruler")
ruler.from_disk(skill_pattern_path)


# # st.dataframe(df)

def get_skills(text):
    doc = nlp(text)
    myset = []
    subset = []
    for ent in doc.ents:
        if ent.label_ == "SKILL":
            subset.append(ent.text)
    myset.append(subset)
    return subset

def unique_skills(x):
    return list(set(x))

sent = nlp(df["Resume"].iloc[3])
# img1 = displacy.render(sent, style="ent", jupyter=False)
# st.markdown(img1, unsafe_allow_html=True)

img2 = displacy.render(sent[0:10], style="dep", jupyter=False, options={"distance": 90})
st.image(img2, width=400, use_column_width='never')

patterns = df.Category.unique()
for a in patterns:
    ruler.add_patterns([{"label": "Job-Category", "pattern": a}])

colors = {
    "Job-Category": "linear-gradient(90deg, #aa9cfc, #fc9ce7)",
    "SKILL": "linear-gradient(90deg, #9BE15D, #00E3AE)",
    "ORG": "#ffd966",
    "PERSON": "#e06666",
    "GPE": "#9fc5e8",
    "DATE": "#c27ba0",
    "ORDINAL": "#674ea7",
    "PRODUCT": "#f9cb9c",
}
options = {
    "ents": [
        "Job-Category",
        "SKILL",
        "ORG",
        "PERSON",
        "GPE",
        "DATE",
        "ORDINAL",
        "PRODUCT",
    ],
    "colors": colors,
}
sent2 = nlp(df["Resume"].iloc[3])
img3 = displacy.render(sent2, style="ent", jupyter=False, options=options)

st.markdown(img3, unsafe_allow_html=True)

input_resume = st.text_input("Enter Resume Text")

sent3 = nlp(input_resume)
img4 = displacy.render(sent3, style="ent", jupyter=False, options=options)
st.markdown(img4, unsafe_allow_html=True)

input_skills = st.text_input("Enter Skills")

req_skills = input_skills.lower().split(",")
resume_skills = unique_skills(get_skills(input_resume.lower()))
score = 0
for x in req_skills:
    if x in resume_skills:
        score += 1
req_skills_len = len(req_skills)
match = round(score / req_skills_len * 100, 1)

st.write("The current Resume is",match,"matched to your requirements")