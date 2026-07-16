import streamlit as st
import pandas as pd
import os
import gdown
import pickle

# Title
st.title("Job Recommendation System")

# Load Dataset
df = pd.read_csv("cleaned_job_data.csv")

df = df.drop_duplicates(subset=["Job Title"])
df = df.reset_index(drop=True)

# Load Similarity Matrix
file_id = "1paoD9rHEMVKHih8Eba24rWdlQhtIonTQ"

if not os.path.exists("similarity.pkl"):
    gdown.download(
        f"https://drive.google.com/uc?id={file_id}",
        "similarity.pkl",
        quiet=False
    )

with open("similarity.pkl", "rb") as f:
    similarities = pickle.load(f)
# Job List
jobs = df["Job Title"].tolist()

# Dropdown
name = st.selectbox("Select a Job Title", jobs)


# Function: Get Job Title by Index
def get_job_title(index):

    if index < len(df):
        return df.loc[index, "Job Title"]

    return ""


# Function: Get Job Index
def get_job_index(job_name):

    clean_name = job_name.strip().lower()

    match = df[
        df["Job Title"]
        .str.lower()
        .str.strip()
        == clean_name
    ]

    if not match.empty:
        return match.index[0]

    return -1


# Recommend Button
if st.button("Recommend Jobs"):

    index = get_job_index(name)

    if index == -1:

        st.write("Job Not Found")

    else:

        st.subheader(f"Recommendations for '{name}'")

        similarity_scores = list(enumerate(similarities[index]))

        similarity_scores = sorted(
            similarity_scores,
            key=lambda x: x[1],
            reverse=True
        )
        similarity_scores = similarity_scores[1:] 

        count = 0

        for job_index, score in similarity_scores:

            # Skip the selected job itself
            if job_index == index:
                continue

            st.markdown(f"### {count+1}. {df.loc[job_index,'Job Title']}")
            st.write(df.loc[job_index, "Job Description"][:250] + "...")
            st.write(f"**Similarity Score:** {round(score*100,2)}%")
            st.write("---")

            count += 1

            if count == 5:
                break
            
