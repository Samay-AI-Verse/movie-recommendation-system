# 🎓 Student Guide: Deploying the AI Movie Recommender

This guide explains how to deploy this AI Movie Recommendation application to **GitHub** and **Hugging Face Spaces** without running into any common environment crashes or performance errors.

---

## 🛠️ Step-by-Step Deployment Instructions

Follow these commands to deploy the project from a fresh machine.

### Step 1: Install Git & Git LFS (Large File Storage)
Since our model data is saved in binary files (`.pkl`), we must use Git LFS to prevent repository bloat and ensure fast uploads/downloads:
- **Windows**: Download and install from [git-lfs.github.com](https://git-lfs.github.com) (or run `git lfs install` if already installed).
- **Mac**: `brew install git-lfs`
- **Linux**: `sudo apt-get install git-lfs`

### Step 2: Initialize Git in your project folder
Open your terminal inside the project directory and run:
```bash
# Initialize local git repository
git init

# Create the main branch
git checkout -b main

# Initialize Git LFS inside the repository
git lfs install

# Configure LFS to track pickle models and CSV datasets
git lfs track "*.pkl"
git lfs track "*.csv"

# Make sure LFS configuration is tracked
git add .gitattributes
```

### Step 3: Make the Initial Commit
```bash
# Stage all files
git add .

# Commit
git commit -m "Initial commit: Ready for deployment"
```

### Step 4: Host on GitHub (Backup/Sharing)
1. Go to [GitHub](https://github.com) and create a **new public repository** named `movie-recommendation-system` (leave "Add README/gitignore" unchecked).
2. Link the repository and push your code:
```bash
git remote add origin https://github.com/<YOUR-GITHUB-USERNAME>/movie-recommendation-system.git
git push -u origin main
```

### Step 5: Deploy to Hugging Face Spaces (Live App)
1. Log in to [Hugging Face](https://huggingface.co) and click **New Space**.
2. Set your Space Name (e.g., `movie-recommender`) and choose:
   - **SDK**: `Gradio`
   - **Template**: `Blank`
   - **Space Hardware**: `CPU Basic` (Free)
3. Go to your Hugging Face account settings -> **Access Tokens** -> generate a new token with **Write** access. Copy this token.
4. Link Hugging Face and push your code:
```bash
# Add Hugging Face as a remote
git remote add space https://huggingface.co/spaces/<YOUR-HF-USERNAME>/<YOUR-SPACE-NAME>

# Push the code (use your HF Access Token as the password when prompted)
git push -f space main
```

---

## 💡 Crucial Errors Solved (Why this project is configured this way)

If you modify these configurations, you might run into three common errors. Here is how they were solved in this repository:

### 1. The Hugging Face `ImportError: cannot import name 'HfFolder'` Crash
* **What went wrong**: In older versions of Gradio (Gradio 4.x), the app tries to import a deprecated helper class named `HfFolder` from `huggingface_hub`. On newer Hugging Face system images, `huggingface_hub` is upgraded, which causes the old import statement to crash.
* **How we solved it**: By allowing Hugging Face to launch using its latest default Gradio 6.x environment (by omitting any custom `gradio` or `huggingface_hub` pins from `requirements.txt`), the build system automatically resolves and installs compatible modern dependencies that no longer reference the deprecated `HfFolder` class. This completely prevents startup crashes.

### 2. The `FileNotFoundError` (Missing Pickle Files)
* **What went wrong**: The `.pkl` files (like `movies.pkl`) are pre-computed data tables and vectors. Originally, `.gitignore` had a rule `artifacts/*.pkl` which meant Git completely ignored them during `git add .`, so they were never pushed to Hugging Face, causing the app to crash with a `FileNotFoundError`.
* **How we solved it**: We updated `.gitignore` to remove the `artifacts/*.pkl` rule, allowing Git to track and upload the model files, and activated Git LFS to handle them safely.

### 3. The Browser Freeze / "Hanging" Bug
* **What went wrong**: Originally, the app loaded **62,423 movie titles** into a browser dropdown menu (`gr.Dropdown`). Transferring and rendering this massive dataset inside the client's browser causes the webpage to freeze or hang.
* **How we solved it**: We replaced the dropdown with a fast text search field (`gr.Textbox` + Search Button). When a user types a movie (e.g. `toy story`), the Python backend matches it instantly using fuzzy string matching (`difflib.get_close_matches`), keeping the webpage extremely fast and lightweight.
