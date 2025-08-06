import streamlit as st
from fuzzywuzzy import process
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load API key from environment
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

tech_stacks = {
    "portfolio website": {
        "Frontend": "HTML/CSS/JS or React",
        "Backend": "None or Firebase",
        "Database": "None or Firestore",
        "Hosting": "GitHub Pages or Netlify",
        "Difficulty": "Beginner"
    },
    "e-commerce website": {
        "Frontend": "React or Next.js",
        "Backend": "Node.js + Express",
        "Database": "MongoDB",
        "Hosting": "Vercel or Render",
        "Difficulty": "Intermediate"
    },
    "chat app (python)": {
        "Frontend": "Tkinter or PyQt",
        "Backend": "Flask + Socket.IO",
        "Database": "SQLite",
        "Hosting": "PythonAnywhere",
        "Difficulty": "Beginner"
    },
    "blog website": {
        "Frontend": "React or Next.js",
        "Backend": "Node.js + Express or Django",
        "Database": "MongoDB or PostgreSQL",
        "Hosting": "Vercel or Heroku",
        "Difficulty": "Beginner to Intermediate"
    },
    "mobile app": {
        "Frontend": "React Native or Flutter",
        "Backend": "Firebase or Node.js",
        "Database": "Firestore or MongoDB",
        "Hosting": "Google Play Store / Apple App Store",
        "Difficulty": "Intermediate"
    }
}

def find_closest_match(user_input):
    match, score = process.extractOne(user_input, list(tech_stacks.keys()))
    return match if score > 70 else None

def get_ai_suggestion(prompt: str, return_raw=False) -> str:
    if not OPENROUTER_API_KEY:
        return "❌ API key not found. Please set the OPENROUTER_API_KEY in your .env file."
        
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [
            {"role": "system", "content": "You are an expert software developer."},
            {"role": "user", "content": f"Suggest a tech stack to build: {prompt}"}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        result = response.json()
        
        # Return the raw JSON response if requested
        if return_raw:
            return result
            
        if "choices" in result:
            return result["choices"][0]["message"]["content"]
        elif "error" in result:
            return f"❌ API error: {result['error'].get('message', result)}"
        else:
            return f"⚠️ Unexpected API response: {result}"
    except requests.exceptions.RequestException as e:
        return f"❌ Request error: {str(e)}"

st.title("Orient: TechStack Guide Agent")
st.subheader("Enter what you want to build:")

# Display available project types in the sidebar
st.sidebar.title("Available Project Types")
for project in tech_stacks.keys():
    st.sidebar.markdown(f"- {project.title()}")

# Add a toggle for raw response
st.sidebar.markdown("---")
st.sidebar.title("Settings")
show_raw_response = st.sidebar.checkbox("Show raw API response", False, help="Display the complete JSON response from the API instead of just the content")

query = st.text_input("e.g. portfolio website, chat app (python)")

if query:
    project_type = query.lower().strip()

    if project_type in tech_stacks:
        st.success(f"✅ Stack for '{project_type.title()}':")
        
        # Create a styled table for the tech stack
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown("**Component**")
            for k in tech_stacks[project_type].keys():
                st.markdown(f"**{k}**")
        with col2:
            st.markdown("**Technology**")
            for v in tech_stacks[project_type].values():
                st.markdown(f"{v}")

    else:
        match = find_closest_match(project_type)
        if match:
            st.info(f"Showing results for closest match: **{match.title()}**")
            
            # Create a styled table for the tech stack
            col1, col2 = st.columns([1, 3])
            with col1:
                st.markdown("**Component**")
                for k in tech_stacks[match].keys():
                    st.markdown(f"**{k}**")
            with col2:
                st.markdown("**Technology**")
                for v in tech_stacks[match].values():
                    st.markdown(f"{v}")
        else:
            st.warning("No predefined match found – asking AI...")
            with st.spinner("Getting AI recommendation..."):
                # Check if user wants raw response
                if show_raw_response or "raw" in project_type or "json" in project_type or "out of the box" in project_type:
                    ai_response = get_ai_suggestion(project_type, return_raw=True)
                    st.json(ai_response)  # Display as formatted JSON
                else:
                    ai_response = get_ai_suggestion(project_type)
                    st.markdown(ai_response)
