from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import pdfplumber
import json
import re
import os
import requests
from dotenv import load_dotenv

load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")

app = Flask(__name__)
# Allow CORS only from Live Server port 5503
CORS(app, origins=["http://127.0.0.1:5503", "http://localhost:5503"])

# Load JSON skills database
def load_skills_data():
    try:
        with open('skills.json', 'r') as f:
            data = json.load(f)
            all_skills = set()
            for role_skills in data.values():
                for s in role_skills:
                    all_skills.add(s.lower())
            return data, list(all_skills)
    except FileNotFoundError:
        return {}, []

ROLES_DB, SKILLS_LIST = load_skills_data()

def extract_text_from_pdf(file_obj):
    text = ""
    try:
        with pdfplumber.open(file_obj) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + " "
    except Exception as e:
        print("PDF parse error:", e)
    return text.lower()

def extract_skills_from_text(text):
    found = set()
    for skill in SKILLS_LIST:
        # Use simple word boundary regex match for each tech skill
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text):
            found.add(skill.capitalize())
    return found

def get_required_skills_from_role(text):
    text_lower = text.lower()
    for role, skills in ROLES_DB.items():
        if role.lower() in text_lower:
            # Return the exact skills required for that exact role
            return set([s.capitalize() for s in skills])
    return set()

# ── REMOVED: index() and serve_static() routes ──
# Live Server now handles all HTML/CSS/JS files from the frontend/ folder.
# Flask only serves API routes below.

@app.route('/api/config.js', methods=['GET'])
def get_config_js():
    js_content = f"const API_CONFIG = {{\n    SUPABASE_URL: '{SUPABASE_URL}',\n    SUPABASE_ANON_KEY: '{SUPABASE_ANON_KEY}'\n}};"
    return Response(js_content, mimetype='application/javascript')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files:
        return jsonify({"success": False, "message": "No resume file attached."})
    
    file = request.files['resume']
    jd_text = request.form.get('job_description', '').lower()

    if file.filename == '' or not jd_text:
        return jsonify({"success": False, "message": "Missing file or Job Description."})

    if not file.filename.endswith('.pdf'):
        return jsonify({"success": False, "message": "Only PDF file format is supported."})

    try:
        # 1. Extract Text from Uploaded PDF
        resume_text = extract_text_from_pdf(file)
        
        # 2. NLP Keyword Extraction from Resume
        resume_skills = extract_skills_from_text(resume_text)
        
        # 3. Check if user typed a specific Job Role (e.g. "frontend developer")
        jd_skills = get_required_skills_from_role(jd_text)
        
        # 4. If no specific Job Role found, extract Individual Skills from JD text
        if not jd_skills:
            jd_skills = extract_skills_from_text(jd_text)
        
        # 5. Fallback if still empty
        if not jd_skills:
            jd_skills = {"Javascript", "Api", "React", "Cloud", "Html"}

        found_skills = list(resume_skills.intersection(jd_skills))
        missing_skills = list(jd_skills.difference(resume_skills))

        percentage = 0
        if len(jd_skills) > 0:
            percentage = int((len(found_skills) / len(jd_skills)) * 100)

        return jsonify({
            "success": True,
            "match_percentage": percentage,
            "found_skills": found_skills,
            "missing_skills": missing_skills
        })

    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

def search_youtube_videos(query, max_results=3):
    safe_search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}+programming+tutorial"
    
    # Safe fallback if API Key is dummy string, empty, or hasn't loaded properly
    if not YOUTUBE_API_KEY or "your_youtube_api_key" in YOUTUBE_API_KEY:
        return [
            {"title": f"Search '{query}' Tutorials Here", "channel": "YouTube Database", "url": safe_search_url, "thumbnail": "https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=640&h=360&fit=crop&q=80"}
        ]
    
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query} programming tutorial course&type=video&key={YOUTUBE_API_KEY}&maxResults={max_results}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            videos = []
            for item in data.get('items', []):
                vid = {
                    "title": item['snippet']['title'],
                    "channel": item['snippet']['channelTitle'],
                    "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                    "thumbnail": item['snippet']['thumbnails']['high']['url']
                }
                videos.append(vid)
            # Ensure safe fallback dynamically if returned empty from API quota limits.
            if not videos:
                 return [{"title": f"Search '{query}' Tutorials Here", "channel": "YouTube Database", "url": safe_search_url, "thumbnail": "https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=640&h=360&fit=crop&q=80"}]
            return videos
        else:
             # Handle 403 API errors effectively fallback to the Search Results instead of breaking!
             return [{"title": f"Search '{query}' Tutorials Here", "channel": "YouTube Database", "url": safe_search_url, "thumbnail": "https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=640&h=360&fit=crop&q=80"}]
    except Exception as e:
        print("YouTube API error:", e)
        return [{"title": f"Search '{query}' Tutorials Here", "channel": "YouTube Database", "url": safe_search_url, "thumbnail": "https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=640&h=360&fit=crop&q=80"}]

@app.route('/api/skill-gap', methods=['POST'])
def skill_gap():
    if 'resume' not in request.files:
        return jsonify({"success": False, "message": "No resume file attached."})
    
    file = request.files['resume']
    target_role = request.form.get('target_role', '').lower()

    if file.filename == '' or not target_role:
        return jsonify({"success": False, "message": "Missing file or target role."})

    if not file.filename.endswith('.pdf'):
        return jsonify({"success": False, "message": "Only PDF file format is supported."})

    try:
        resume_text = extract_text_from_pdf(file)
        resume_skills = extract_skills_from_text(resume_text)
        
        jd_skills = get_required_skills_from_role(target_role)
        if not jd_skills:
            # Fallback text parsing if actual Role wasn't strictly found
            jd_skills = extract_skills_from_text(target_role)
            if not jd_skills:
                jd_skills = {"Javascript", "React", "Db"}

        missing_skills = list(jd_skills.difference(resume_skills))
        
        # Youtube Integration API Call Loop - Uncapped skills mapping
        recommendations = []
        
        # Iterate through entirely every single missing skill found
        for skill in missing_skills:
            # Request exactly 1 top video tutorial for every missing skill dynamically
            vids = search_youtube_videos(skill, max_results=1)
            if vids:
                recommendations.append({"skill": skill.capitalize(), "video": vids[0]})

        return jsonify({
            "success": True,
            "missing_skills": missing_skills,
            "recommendations": recommendations
        })

    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

def get_groq_role_predictions(resume_text):
    if not GROQ_API_KEY or "your_" in GROQ_API_KEY:
        return [{"role": "API Key Not Loaded", "match_percentage": 0, "reasoning": "Please ensure you have saved your .env file and restarted the python app.py server to load the new key.", "tags": ["Error", "Env", "Restart"]}]
        
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    prompt = f"""
    You are an expert AI Career Coach. Analyze the following candidate experience/skills extracted from a resume. Predict ALL the potential job roles the candidate is eligible for based on their skillset. Provide a comprehensive and lengthy list of as many roles as are highly or moderately suitable.
    For each role, provide a match percentage (0-100), a short reasoning (max 2 sentences explaining why they are eligible based on their exact experience), and 3 key technology/skill tags.
    Output ONLY valid parseable JSON in this exact structure, with no markdown formatting or setup words:
    [
      {{"role": "Role Name", "match_percentage": 95, "reasoning": "Why they fit...", "tags": ["Skill1", "Skill2", "Skill3"]}}
    ]

    Resume Text:
    {resume_text[:3000]}
    """
    
    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            # Clean up potential markdown formatting from LLM
            content = content.replace("```json", "").replace("```", "").strip()
            return json.loads(content)
        else:
            print("Groq API Error:", response.text)
    except Exception as e:
        print("Groq API Execution Error:", str(e))
        
    # Fallback if parsing fails totally
    return [
            {
                "role": "Groq API Error",
                "match_percentage": 0,
                "reasoning": "The AI API could not execute. This could be due to quota limits or an invalid API token key. Please check your python terminal for the exact error log.",
                "tags": ["Groq", "API", "Error"]
            }
    ]

@app.route('/api/predict-roles', methods=['POST'])
def predict_roles():
    if 'resume' not in request.files:
        return jsonify({"success": False, "message": "No resume file attached."})
    
    file = request.files['resume']
    if file.filename == '' or not file.filename.endswith('.pdf'):
        return jsonify({"success": False, "message": "Valid PDF resume is required."})

    try:
        resume_text = extract_text_from_pdf(file)
        
        # Call Groq API for insights
        predictions = get_groq_role_predictions(resume_text)

        return jsonify({
            "success": True,
            "roles": predictions
        })

    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

if __name__ == '__main__':
    print("===========================================")
    print("🚀 NLP Engine Running on port 5000")
    print("===========================================")
    app.run(port=5000, debug=True)