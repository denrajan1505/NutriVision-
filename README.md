# 🥗 NutriVision — A Multimodal Generative AI Application for Food Nutrition Analysis using Large Language Models (LLM), GPT-4o Vision and LangChain

## 📋 Description
NutriVision is a Multimodal Generative AI application that analyzes 
food images and provides detailed nutritional information using 
GPT-4o Vision and LangChain.

## ✨ Features
- 📸 Upload food image (JPG, PNG, WEBP)
- 🍎 AI identifies all food items
- 📊 Detailed nutrition breakdown (calories, protein, carbs, fats)
- 💊 Vitamins and minerals analysis
- ❤️ Health score out of 10
- ⚠️ Allergen warnings
- 🎯 Diet goal compatibility check
- 🌐 Multilingual output (Hindi, Tamil, Telugu, Kannada, Malayalam)
- ⬇️ Download report as TXT or Markdown

## 🛠️ Tech Stack
- Python
- Streamlit
- LangChain
- GPT-4o Vision (OpenAI)
- Large Language Models (LLM)
- python-dotenv

## ⚙️ How to Run

### Step 1 — Clone the repository
git clone https://github.com/yourusername/NutriVision.git
cd NutriVision

### Step 2 — Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

### Step 3 — Install dependencies
pip install -r requirements.txt

### Step 4 — Setup environment variables
cp .env.example .env
# Open .env and add your OpenAI API key
OPENAI_API_KEY=your_api_key_here

### Step 5 — Run the app
streamlit run app.py

## 📸 Screenshots
![Home Page](screenshots/home.png)
![Analysis](screenshots/analysis.png)
![Download](screenshots/download.png)

## ⚠️ Disclaimer
This app is for educational and informational purposes only.
Always consult a certified dietitian for personalized advice.

## 👨‍💻 Author
Your Name
Course Name
Institution Name
