import streamlit as st
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

st.title("Live Semantic Embedding Explorer")

st.write("Type sentences and see how meaning becomes vectors.")

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Default dataset
default_sentences = [
    "I love dogs",
    "Cats are amazing pets",
    "Tigers are wild animals",
    "Cars move on roads",
    "Buses transport people",
    "Trucks carry goods",
    "Apples are fruits",
    "Bananas are yellow fruits"
]

if "sentences" not in st.session_state:
    st.session_state.sentences = default_sentences

text_input = st.text_area(
    "Enter sentences (one per line)",
    "\n".join(st.session_state.sentences)
)

st.session_state.sentences = [s.strip() for s in text_input.split("\n") if s.strip()]
sentences = st.session_state.sentences

# Generate embeddings automatically (not behind button)
embeddings = model.encode(sentences)

st.subheader("Embedding Vector Example")
st.write("First 10 values of first sentence vector:")
st.write(embeddings[0][:10])

st.subheader("Semantic Similarity Matrix")
sim_matrix = cosine_similarity(embeddings)
st.dataframe(sim_matrix)

st.subheader("Find Most Similar Sentences")
query = st.text_input("Enter a query sentence")

if query:
    query_vec = model.encode([query])
    similarities = cosine_similarity(query_vec, embeddings)[0]

    results = list(zip(sentences, similarities))
    results = sorted(results, key=lambda x: x[1], reverse=True)

    for sent, score in results[:5]:
        st.write(f"{sent}  → similarity: {score:.3f}")

st.subheader("2D Semantic Map")
pca = PCA(n_components=2)
reduced = pca.fit_transform(embeddings)

fig, ax = plt.subplots()

for i, s in enumerate(sentences):
    x, y = reduced[i]
    ax.scatter(x, y)
    ax.text(x + 0.02, y + 0.02, s, fontsize=8)

st.pyplot(fig)