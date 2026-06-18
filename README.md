🎬 Movie Recommendation System
� � � � �
A machine learning-powered movie recommendation system built using FastAPI that suggests similar movies based on user selection using a trained similarity model.
🚀 Live Demo
👉 https://movies-recommendation-tokd.onrender.com/
🧠 Features
🎯 Intelligent movie recommendation system
⚡ Fast & lightweight FastAPI backend
🤖 ML-based similarity scoring model
🎬 Movie poster-based UI
🔥 Instant recommendations
📦 Precomputed .pkl similarity matrix for speed
🛠️ Tech Stack
🐍 Python
⚡ FastAPI
🌐 HTML, CSS, JavaScript
🤖 Scikit-learn
📊 Pandas & NumPy
💾 Pickle (Model Storage)
☁️ Render (Deployment)
📁 Project Structure

project/
│── main.py
│── requirements.txt
│── similarity.pkl
│── users.pkl
│── templates/
│     └── index.html
│── static/
│     ├── style.css
│     ├── script.js
│     └── images/
│── README.md
⚙️ How It Works
User selects a movie 🎬
Backend loads similarity matrix 🤖
System calculates closest matches ⚡
Top recommendations are returned 🎯
UI displays movie posters 📺
🖥️ UI Screenshots
🏠 Home Page
�
🎬 Movie Selection
�
🔥 Recommendations
�
⚠️ Replace these placeholder images with your actual screenshots:
static/images/home.png
static/images/recommendations.png
📦 Installation (Local Setup)
Bash
git clone https://github.com/your-username/movie-recommender.git

cd movie-recommender

pip install -r requirements.txt

uvicorn main:app --reload
🌐 Run Locally

http://127.0.0.1:8000
🚀 Deployment (Render)
🔧 Build Command
Bash
pip install -r requirements.txt
🚀 Start Command
Bash
uvicorn main:app --host 0.0.0.0 --port 10000
⚠️ Important Notes
Ensure .pkl files exist in root directory
Correct file paths in main.py
Add __pycache__/ and .pkl to .gitignore if needed
📈 Future Improvements
👤 User authentication system
☁️ Cloud database integration
🎯 Better recommendation accuracy
🎨 Netflix-like UI upgrade
🔍 Search + filters
👨‍💻 Author
Raj Solanki
💻 Engineering Student | ML & Backend Developer
⭐ Support
If you like this project: 👉 Star the repo ⭐
👉 Fork it 🍴
👉 Share it 🚀
