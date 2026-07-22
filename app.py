import pickle
import difflib
import pandas as pd
import gradio as gr
from sklearn.metrics.pairwise import linear_kernel

# -----------------------------
# Load Model Files
# -----------------------------
movies = pickle.load(open("artifacts/movies.pkl", "rb"))
tfidf = pickle.load(open("artifacts/tfidf.pkl", "rb"))
tfidf_matrix = pickle.load(open("artifacts/tfidf_matrix.pkl", "rb"))

# -----------------------------
# Recommendation Function
# -----------------------------
def recommend(movie_name, num_recommendations):

    query = movie_name.lower().strip()

    exact_matches = movies[movies["title_lower"] == query]

    if not exact_matches.empty:
        idx = exact_matches.index[0]

    else:
        closest = difflib.get_close_matches(
            query,
            movies["title_lower"].tolist(),
            n=1,
            cutoff=0.5
        )

        if closest:
            idx = movies[movies["title_lower"] == closest[0]].index[0]
        else:
            return "Movie not found."

    similarity = linear_kernel(
        tfidf_matrix[idx],
        tfidf_matrix
    ).flatten()

    indices = similarity.argsort()[::-1]

    indices = [i for i in indices if i != idx][:num_recommendations]

    result = movies.iloc[indices][["title", "genres"]].copy()

    result["Similarity (%)"] = (
        similarity[indices] * 100
    ).round(2)

    return result


# -----------------------------
# Gradio Interface
# -----------------------------

demo = gr.Interface(
    fn=recommend,
    inputs=[
        gr.Dropdown(
            choices=movies["title"].tolist(),
            label="Select Movie"
        ),
        gr.Slider(
            minimum=5,
            maximum=20,
            value=10,
            step=1,
            label="Number of Recommendations"
        )
    ],
    outputs=gr.Dataframe(
        label="Recommended Movies"
    ),
    title="🎬 AI Movie Recommendation System",
    description="""
Content-Based Movie Recommendation System

Uses:

• TF-IDF Vectorization

• Cosine Similarity

• Genre Matching
"""
)

demo.launch()