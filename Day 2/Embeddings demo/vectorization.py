# Required packages (install once):
# pip install sentence-transformers numpy matplotlib scikit-learn

from sentence_transformers import SentenceTransformer, util
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity

# ─── 1. Load the embedding model ───
# This is a fast, good-quality model (~80 MB, runs well on CPU)
model = SentenceTransformer('all-MiniLM-L6-v2')

# ─── 2. Example words and short sentences ───
examples = [
    "cat",
    "kitten",
    "dog",
    "puppy",
    "lion",
    "tiger",
    "car",
    "automobile",
    "bicycle",
    "motorcycle",
    "apple",
    "banana",
    "orange",
    "king",
    "queen",
    "prince",
    "I love my cat",
    "My kitten is very cute",
    "I drive a fast car",
    "Riding a bicycle is fun"
]

# ─── 3. Generate embeddings ───
embeddings = model.encode(examples, show_progress_bar=True)
dim = embeddings.shape[1]
print(f"\nModel: {model.get_sentence_embedding_dimension()} dimensions")
print(f"→ We have {len(examples)} items, each represented by a {dim}-dimensional vector\n")

# ─── 4. Show a few raw vectors (people like seeing actual numbers) ───
print("Example vectors (showing first 6 values only):")
for text, vec in zip(examples[:6], embeddings[:6]):
    print(f"{text:18} → {vec[:6].round(4)} ...")
print()

# ─── 5. Show some cosine similarities (most intuitive proof) ───
pairs = [
    ("cat", "kitten"),
    ("cat", "dog"),
    ("cat", "car"),
    ("king", "queen"),
    ("king", "apple"),
    ("I love my cat", "My kitten is very cute"),
    ("I love my cat", "I drive a fast car")
]

print("Cosine similarities (higher = more similar):")
for a, b in pairs:
    i = examples.index(a)
    j = examples.index(b)
    sim = util.cos_sim(embeddings[i], embeddings[j]).item()
    print(f"{a:22} ↔ {b:22} = {sim:.4f}")
print()

# ─── 6. Nearest neighbors for a few items ───
print("Nearest neighbors (top 4 most similar items):")
for idx, text in enumerate(["cat", "car", "king", "I love my cat"]):
    print(f"\n→ {text}")
    sims = cosine_similarity([embeddings[idx]], embeddings)[0]
    nearest_idx = np.argsort(sims)[::-1][1:5]  # skip self
    for ni in nearest_idx:
        print(f"   {sims[ni]:.4f}  {examples[ni]}")

# ─── 7. 2D visualization ───
print("\nCreating 2D visualization...")

pca = PCA(n_components=2)
reduced = pca.fit_transform(embeddings)

plt.figure(figsize=(11, 8))
plt.scatter(reduced[:, 0], reduced[:, 1], c='white', edgecolor='black', s=80)

for i, txt in enumerate(examples):
    plt.annotate(
        txt,
        (reduced[i, 0], reduced[i, 1]),
        fontsize=9,
        ha='center',
        va='center',
        bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=1.5)
    )

plt.title("2D PCA projection of sentence embeddings\n(similar meanings should appear close together)", fontsize=13)
plt.xlabel("PCA component 1")
plt.ylabel("PCA component 2")
plt.grid(True, alpha=0.3, linestyle='--')
plt.tight_layout()
plt.show()

print("\nDone. You should now see a scatter plot in a new window.")