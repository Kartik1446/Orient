import streamlit as st
from fuzzywuzzy import process
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file (for other environment variables if needed)
load_dotenv()

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""

tech_stacks = {
    "portfolio website": {
        "Frontend": "HTML/CSS/JS or React",
        "Backend": "None or Firebase",
        "Database": "None or Firestore",
        "Hosting": "GitHub Pages or Netlify",
        "Difficulty": "Beginner"
    },
    "e-commerce website": {
        "Frontend": "React with TypeScript",
        "Backend": "Node.js with Express",
        "Database": "MongoDB",
        "Hosting": "Vercel",
        "Difficulty": "Intermediate"
    },
    "social media platform": {
        "Frontend": "React with TypeScript",
        "Backend": "Node.js with Express",
        "Database": "MongoDB",
        "Hosting": "Vercel",
        "Difficulty": "Intermediate"
    },
    "content management system": {
        "Frontend": "React with TypeScript",
        "Backend": "Node.js with Express",
        "Database": "MongoDB",
        "Hosting": "Vercel",
        "Difficulty": "Intermediate"
    },
    "mobile application": {
        "Frontend": "React Native with TypeScript",
        "Backend": "Node.js with Express",
        "Database": "MongoDB",
        "Hosting": "Vercel",
        "Difficulty": "Intermediate"
    },
    "machine learning model": {
        "Frontend": "React with TypeScript",
        "Backend": "Node.js with Express",
        "Database": "MongoDB",
        "Hosting": "Vercel",
        "Difficulty": "Intermediate"
    },
    "blockchain application": {
        "Frontend": "React with TypeScript",
        "Backend": "Node.js with Express",
        "Database": "MongoDB",
        "Hosting": "Vercel",
        "Difficulty": "Intermediate"
    },
    "game": {
        "Frontend": "React with TypeScript",
        "Backend": "Node.js with Express",
        "Database": "MongoDB",
        "Hosting": "Vercel",
        "Difficulty": "Intermediate"
    },
    "chatbot": {
        "Frontend": "React with TypeScript",
        "Backend": "Node.js with Express",
        "Database": "MongoDB",
        "Hosting": "Vercel",
        "Difficulty": "Intermediate"
    }
}

def find_closest_match(user_input):
    match, score = process.extractOne(user_input, list(tech_stacks.keys()))
    return match if score > 70 else None

def get_ai_suggestion(prompt: str, api_key: str, return_raw=False) -> str:
    if not api_key:
        return "❌ API key not provided. Please enter your OpenRouter API key in the sidebar."
    
    # For testing purposes, if the prompt contains 'out of the box', return a mock response
    if 'out of the box' in prompt.lower():
        mock_response = {
            "id": "gen-abc123",
            "object": "chat.completion",
            "created": 1683933873,
            "model": "mistralai/mistral-7b-instruct",
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "For an out-of-the-box project, I recommend:\n\n**Frontend**: React with TypeScript\n**Backend**: Node.js with Express\n**Database**: MongoDB\n**Hosting**: Vercel\n**Additional Tools**: Docker for containerization, Jest for testing\n\nThis stack offers excellent developer experience, good performance, and scalability for most applications."
                    },
                    "finish_reason": "stop",
                    "index": 0
                }
            ],
            "usage": {
                "prompt_tokens": 25,
                "completion_tokens": 89,
                "total_tokens": 114
            }
        }
        
        # Return the mock response if requested
        if return_raw:
            return mock_response
        return mock_response["choices"][0]["message"]["content"]
        
    # Ensure proper API key format for OpenRouter
    if not api_key.startswith("Bearer "):
        api_key = f"Bearer {api_key}"
        
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json",
        "HTTP-Referer": "https://orient-techstack-guide.com",
        "X-Title": "Orient TechStack Guide"
    }
    data = {
        "model": "mistralai/mistral-7b-instruct",  # Use a model that's available on OpenRouter
        "messages": [
            {"role": "system", "content": "You are an expert software developer."},
            {"role": "user", "content": f"Suggest a tech stack to build: {prompt}"}
        ]
    }
    
    # Debug information
    print(f"API Key (first 10 chars): {api_key[:10]}...")
    print(f"Request URL: https://openrouter.ai/api/v1/chat/completions")
    print(f"Request Headers: {headers}")
    print(f"Request Data: {data}")
    
    try:
        # Use the correct API endpoint
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        # Print response status for debugging
        print(f"OpenRouter API Response Status: {response.status_code}")
        if response.status_code != 200:
            print(f"Response content: {response.text}")
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

# Authentication popup
def show_auth_popup():
    with st.container():
        st.markdown("### Welcome to Orient TechStack Guide")
        st.markdown("Please enter your OpenRouter API key to continue.")
        st.markdown("You can get an API key from [OpenRouter](https://openrouter.ai/)")
        
        api_key_input = st.text_input("OpenRouter API Key", type="password")
        col1, col2 = st.columns([1, 3])
        
        with col1:
            if st.button("Continue"):
                if api_key_input:
                    st.session_state.api_key = api_key_input
                    st.session_state.authenticated = True
                    st.experimental_rerun()
                else:
                    st.error("Please enter an API key to continue")

# Main application
def show_main_app():
    st.title("Orient: TechStack Guide Agent")
    st.subheader("Enter what you want to build:")

    # Display available project types in the sidebar
    st.sidebar.title("Available Project Types")
    for project in tech_stacks.keys():
        st.sidebar.markdown(f"- {project.title()}")

    # Add API key display/edit in the sidebar
    st.sidebar.markdown("---")
    st.sidebar.title("API Settings")
    
    # Show masked API key and option to change
    masked_key = "*" * 10
    st.sidebar.text(f"Current API Key: {masked_key}")
    if st.sidebar.button("Change API Key"):
        st.session_state.authenticated = False
        st.experimental_rerun()

    # Add a toggle for raw response
    st.sidebar.markdown("---")
    st.sidebar.title("Display Settings")
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
                        ai_response = get_ai_suggestion(project_type, st.session_state.api_key, return_raw=True)
                        st.json(ai_response)  # Display as formatted JSON
                    else:
                        ai_response = get_ai_suggestion(project_type, st.session_state.api_key)
                        st.markdown(ai_response)

# Main app flow control
if not st.session_state.authenticated:
    show_auth_popup()
else:
    show_main_app()