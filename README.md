---
title: AI Movie Recommendation System
emoji: 🎬
colorFrom: red
colorTo: blue
sdk: gradio
sdk_version: 4.37.2
app_file: app.py
pinned: false
---

# 🎬 Production Content-Based Movie Recommendation System

An end-to-end Machine Learning web application that provides content-based movie recommendations using TF-IDF vectorization and Cosine Similarity on the MovieLens dataset.

## 🌟 Key Features
- **Exploratory Data Analysis (EDA):** Complete distribution and text character analysis.
- **NLP Feature Extraction:** TF-IDF text vectorization across multi-label movie genres.
- **Fuzzy String Search:** Handles user typos and lowercase entries using `difflib`.
- **Memory-Optimized Engine:** Real-time on-the-fly similarity computations designed for low-memory cloud deployment (<50 MB RAM).
- **Interactive UI:** Web dashboard built using Streamlit.

## 📊 Dataset
- Dataset Name: MovieLens `movies.csv`
- Records: 62,423 movies
- Features: `movieId`, `title`, `genres`

## 🛠️ Installation & Setup
1. Clone the repository:
   ```bash
   git clone [https://github.com/your-username/movie-recommendation-system.git](https://github.com/your-username/movie-recommendation-system.git)
   cd movie-recommendation-system