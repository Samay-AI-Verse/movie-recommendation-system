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
# Helper Functions for UI Styling
# -----------------------------
def get_gradient_for_genres(genres_str):
    genres = [g.strip().lower() for g in genres_str.split("|")]
    if any(g in ["action", "adventure", "thriller", "war"] for g in genres):
        return "linear-gradient(135deg, #F43F5E 0%, #FB7185 100%)" # Rose
    elif any(g in ["comedy", "animation", "children", "family", "musical"] for g in genres):
        return "linear-gradient(135deg, #10B981 0%, #34D399 100%)" # Emerald
    elif any(g in ["drama", "romance", "documentary"] for g in genres):
        return "linear-gradient(135deg, #EC4899 0%, #F472B6 100%)" # Pink
    elif any(g in ["sci-fi", "fantasy", "mystery", "horror", "crime"] for g in genres):
        return "linear-gradient(135deg, #06B6D4 0%, #22D3EE 100%)" # Cyan
    return "linear-gradient(135deg, #6366F1 0%, #818CF8 100%)" # Indigo

def get_emoji_for_genres(genres_str):
    genres = [g.strip().lower() for g in genres_str.split("|")]
    if "animation" in genres or "children" in genres:
        return "🧸"
    elif "sci-fi" in genres:
        return "🚀"
    elif "action" in genres or "adventure" in genres:
        return "💥"
    elif "horror" in genres:
        return "👻"
    elif "mystery" in genres or "crime" in genres:
        return "🕵️"
    elif "romance" in genres:
        return "💖"
    elif "comedy" in genres:
        return "🍿"
    elif "drama" in genres:
        return "🎬"
    return "🎬"

# -----------------------------
# Recommendation Function (HTML Cards Output)
# -----------------------------
def recommend_html(movie_name, num_recommendations):
    if not movie_name or len(movie_name.strip()) == 0:
        return "<div class='info-message'>Type a movie title above to get recommendations!</div>"
    
    query = movie_name.lower().strip()
    exact_matches = movies[movies["title_lower"] == query]
    
    if not exact_matches.empty:
        idx = exact_matches.index[0]
        matched_title = movies.iloc[idx]["title"]
    else:
        closest = difflib.get_close_matches(
            query,
            movies["title_lower"].tolist(),
            n=1,
            cutoff=0.5
        )
        if closest:
            idx = movies[movies["title_lower"] == closest[0]].index[0]
            matched_title = movies.iloc[idx]["title"]
        else:
            return f"<div class='error-message'>❌ Movie <strong>'{movie_name}'</strong> not found. Try another movie (e.g., 'Toy Story', 'Inception', 'Jumanji').</div>"
            
    # Compute similarity
    similarity = linear_kernel(
        tfidf_matrix[idx],
        tfidf_matrix
    ).flatten()
    
    indices = similarity.argsort()[::-1]
    # Filter out the searched movie itself
    indices = [i for i in indices if i != idx][:int(num_recommendations)]
    
    result = movies.iloc[indices].copy()
    result["Similarity (%)"] = (similarity[indices] * 100).round(1)
    
    # Generate HTML grid
    html = f"""
    <div class='results-header'>
        <h3>Recommended for: <span class='highlight'>{matched_title}</span></h3>
    </div>
    <div class='movie-grid'>
    """
    
    for idx, row in result.iterrows():
        genres_list = row["genres"].split("|")
        genres_html = "".join([f"<span class='genre-pill'>{g}</span>" for g in genres_list])
        gradient = get_gradient_for_genres(row["genres"])
        emoji = get_emoji_for_genres(row["genres"])
        similarity_score = row["Similarity (%)"]
        
        html += f"""
        <div class="movie-card">
            <div class="movie-card-header" style="background: {gradient};">
                <span class="movie-icon">{emoji}</span>
                <div class="similarity-badge">{similarity_score}% Match</div>
            </div>
            <div class="movie-card-body">
                <h4 class="movie-title">{row["title"]}</h4>
                <div class="movie-genres">
                    {genres_html}
                </div>
            </div>
        </div>
        """
        
    html += "</div>"
    return html

# -----------------------------
# Custom Premium Styling (CSS)
# -----------------------------
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');

body, .gradio-container {
    font-family: 'Outfit', sans-serif !important;
    background-color: #0d0e15 !important;
    color: #f3f4f6 !important;
}

.gradio-container {
    max-width: 1100px !important;
    margin: 0 auto !important;
    padding: 30px 15px !important;
}

.header-container {
    text-align: center;
    margin-bottom: 40px;
    padding: 30px;
    background: radial-gradient(circle at top right, rgba(99, 102, 241, 0.12), transparent 60%);
    border-radius: 24px;
    border: 1px solid rgba(255, 255, 255, 0.03);
}

.header-container h1 {
    font-size: 2.8rem !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, #818CF8, #C084FC, #F472B6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px !important;
}

.header-container p {
    font-size: 1.1rem !important;
    color: #9CA3AF !important;
    margin: 0 !important;
}

.control-row {
    background: rgba(255, 255, 255, 0.02) !important;
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-radius: 20px !important;
    padding: 20px !important;
    margin-bottom: 30px !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.control-row input {
    background-color: rgba(255, 255, 255, 0.03) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
    color: white !important;
    font-size: 1.05rem !important;
    padding: 12px 16px !important;
}

.control-row input:focus {
    border-color: #818CF8 !important;
    box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.2) !important;
}

.search-btn {
    background: linear-gradient(135deg, #6366F1, #8B5CF6) !important;
    color: white !important;
    border: none !important;
    font-weight: 700 !important;
    font-size: 1.05rem !important;
    padding: 12px 24px !important;
    border-radius: 12px !important;
    cursor: pointer !important;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
    transition: all 0.25s ease !important;
}

.search-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5) !important;
}

.info-message {
    text-align: center;
    color: #9CA3AF;
    font-size: 1.15rem;
    padding: 40px;
    border: 2px dashed rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    margin-top: 20px;
}

.error-message {
    text-align: center;
    color: #F87171;
    background: rgba(248, 113, 113, 0.05);
    border: 1px solid rgba(248, 113, 113, 0.15);
    font-size: 1.1rem;
    padding: 20px;
    border-radius: 16px;
    margin-top: 20px;
}

.results-header {
    margin-top: 10px;
    margin-bottom: 25px;
}

.results-header h3 {
    font-size: 1.4rem;
    font-weight: 600;
    color: #E5E7EB;
}

.results-header .highlight {
    color: #C084FC;
    font-weight: 700;
}

.movie-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
    gap: 24px;
    padding: 10px 0;
}

.movie-card {
    background: rgba(255, 255, 255, 0.02) !important;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-radius: 18px;
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    display: flex;
    flex-direction: column;
    height: 240px;
}

.movie-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 25px rgba(99, 102, 241, 0.15);
    border-color: rgba(129, 140, 248, 0.35) !important;
}

.movie-card-header {
    height: 95px;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
}

.movie-icon {
    font-size: 2.6rem;
    filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.15));
}

.similarity-badge {
    position: absolute;
    top: 12px;
    right: 12px;
    background: rgba(15, 23, 42, 0.75);
    color: #34D399;
    font-weight: 700;
    font-size: 0.72rem;
    padding: 4px 10px;
    border-radius: 9999px;
    border: 1px solid rgba(52, 211, 153, 0.25);
    backdrop-filter: blur(4px);
}

.movie-card-body {
    padding: 16px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    flex-grow: 1;
}

.movie-title {
    color: #F3F4F6;
    font-size: 1.05rem;
    font-weight: 600;
    margin: 0;
    line-height: 1.4;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
}

.movie-genres {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 8px;
}

.genre-pill {
    background: rgba(255, 255, 255, 0.04);
    color: #9CA3AF;
    font-size: 0.68rem;
    padding: 3px 8px;
    border-radius: 6px;
    border: 1px solid rgba(255, 255, 255, 0.03);
}
"""

# -----------------------------
# Gradio Blocks Layout
# -----------------------------
with gr.Blocks(css=custom_css, title="AI Movie Recommender") as demo:
    gr.HTML("""
    <div class="header-container">
        <h1>🎬 AI Movie Recommendation System</h1>
        <p>Discover personalized movie recommendations powered by Content-Based Filtering & Natural Language Processing</p>
    </div>
    """)
    
    with gr.Row(elem_classes=["control-row"]):
        with gr.Column(scale=4):
            search_input = gr.Textbox(
                placeholder="Enter a movie title (e.g. Toy Story, Inception, Jumanji)...",
                label="Search Movie",
                show_label=False
            )
        with gr.Column(scale=2):
            slider_input = gr.Slider(
                minimum=4,
                maximum=24,
                value=8,
                step=4,
                label="Recommendations to show"
            )
        with gr.Column(scale=1):
            search_btn = gr.Button("Search", elem_classes=["search-btn"])
            
    output_html = gr.HTML(
        value="<div class='info-message'>Type a movie title above and press Search to see recommendations!</div>"
    )
    
    # Event Handlers
    search_btn.click(
        fn=recommend_html,
        inputs=[search_input, slider_input],
        outputs=output_html
    )
    
    search_input.submit(
        fn=recommend_html,
        inputs=[search_input, slider_input],
        outputs=output_html
    )

# -----------------------------
# Launch
# -----------------------------
if __name__ == "__main__":
    demo.launch()