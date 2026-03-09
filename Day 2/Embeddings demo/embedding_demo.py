import streamlit as st
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

st.title("Embedding Visualization Demo")

st.write("Enter words or sentences to see how embeddings cluster.")

text_input = st.text_area(
    "Enter words or sentences (one per line)",
    "dog\ncat\ntiger\ncar\nbus\ntruck\napple\nbanana"
)

items = [x.strip() for x in text_input.split("\n") if x.strip()]

if st.button("Generate Embeddings"):

    embeddings = model.encode(items)

    st.subheader("Embedding Vector (first item)")
    st.write(embeddings[0][:10])

    st.subheader("Cosine Similarity Matrix")

    similarity = cosine_similarity(embeddings)
    st.dataframe(similarity)

    st.subheader("2D Visualization of Embeddings")

    pca = PCA(n_components=2)
    reduced = pca.fit_transform(embeddings)

    fig, ax = plt.subplots()

    for i, label in enumerate(items):
        x, y = reduced[i]
        ax.scatter(x, y)
        ax.text(x + 0.01, y + 0.01, label)

    st.pyplot(fig)