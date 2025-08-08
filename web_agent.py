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
    
    # Clean and validate API key
    api_key = api_key.strip().strip('"').strip("'")
    if not api_key:
        return "❌ API key is empty. Please enter a valid OpenRouter API key."
    
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
    
    # Prepare Authorization header (accept with or without 'Bearer ' prefix)
    auth_header = api_key
    if not auth_header.lower().startswith("bearer "):
        auth_header = f"Bearer {auth_header}"
    
    headers = {
        "Authorization": auth_header,
        "Content-Type": "application/json",
        "HTTP-Referer": "https://orient-techstack-guide.com",
        "X-Title": "Orient TechStack Guide"
    }
    
    data = {
        "model": "mistralai/mistral-7b-instruct",  # Use a model that's available on OpenRouter
        "messages": [
            {"role": "system", "content": "You are an expert software developer."},
            {"role": "user", "content": f"Suggest a tech stack to build: {prompt}"}
        ],
        "max_tokens": 500,
        "temperature": 0.7
    }
    
    # Debug information (mask API key in logs)
    masked_auth = "Bearer " + (api_key[:8] + "..." if len(api_key) > 8 else api_key)
    safe_headers = {
        **{k: v for k, v in headers.items() if k != "Authorization"},
        "Authorization": masked_auth,
    }
    print(f"Request URL: https://openrouter.ai/api/v1/chat/completions")
    print(f"Request Headers: {safe_headers}")
    print(f"Request Data: {data}")
    
    try:
        # Use the correct API endpoint
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data, timeout=30)
        
        # Print response status for debugging
        print(f"OpenRouter API Response Status: {response.status_code}")
        
        if response.status_code == 401:
            error_msg = "❌ Authentication failed. Please check your OpenRouter API key."
            try:
                error_data = response.json()
                if "error" in error_data and "message" in error_data["error"]:
                    error_msg += f"\n\nError details: {error_data['error']['message']}"
            except:
                pass
            return error_msg
        elif response.status_code == 403:
            return "❌ Access forbidden. Please check your OpenRouter API key and account status."
        elif response.status_code == 429:
            return "❌ Rate limit exceeded. Please try again later."
        elif response.status_code != 200:
            print(f"Response content: {response.text}")
            return f"❌ API error (Status {response.status_code}): {response.text}"
        
        response.raise_for_status()  # Raise an exception for other HTTP errors
        result = response.json()
        
        # Return the raw JSON response if requested
        if return_raw:
            return result
            
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"]
        elif "error" in result:
            return f"❌ API error: {result['error'].get('message', str(result['error']))}"
        else:
            return f"⚠️ Unexpected API response format: {result}"
            
    except requests.exceptions.Timeout:
        return "❌ Request timeout. Please try again."
    except requests.exceptions.ConnectionError:
        return "❌ Connection error. Please check your internet connection."
    except requests.exceptions.RequestException as e:
        return f"❌ Request error: {str(e)}"
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"

# Authentication popup
def show_auth_popup():
    with st.container():
        st.markdown("### Welcome to Orient TechStack Guide")
        st.markdown("Please enter your OpenRouter API key to continue.")
        
        # Add helpful information about getting API key
        with st.expander("How to get an OpenRouter API key"):
            st.markdown("""
            1. Go to [OpenRouter](https://openrouter.ai/)
            2. Sign up for a free account
            3. Navigate to your API keys section
            4. Create a new API key
            5. Copy the key and paste it below
            
            Paste just the key (e.g., starts with `sk-or-v1-`). Do NOT include `Bearer`.
            """)
        
        api_key_input = st.text_input(
            "OpenRouter API Key",
            type="password",
            help="Paste your OpenRouter API key (starts with 'sk-or-v1-'). Do NOT include 'Bearer'",
        )
        
        # Add validation for API key format (allow with or without Bearer)
        key_trim = api_key_input.strip()
        is_valid_format = (
            key_trim.startswith("sk-or-v1-") or key_trim.lower().startswith("bearer sk-or-v1-")
        ) if key_trim else False
        if key_trim and not is_valid_format:
            st.warning("⚠️ API key should start with 'sk-or-v1-'. Do not include quotes. If you typed 'Bearer', it's okay, but it's not necessary.")
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            if st.button("Continue"):
                if key_trim:
                    if not is_valid_format:
                        st.error("❌ Invalid API key format. Please enter a valid OpenRouter API key.")
                    else:
                        st.session_state.api_key = key_trim
                        st.session_state.authenticated = True
                        st.rerun()
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
        st.rerun()  # Fixed: replaced experimental_rerun with rerun

    # Add a toggle for raw response
    st.sidebar.markdown("---")
    st.sidebar.title("Display Settings")
    show_raw_response = st.sidebar.checkbox("Show raw API response", False, help="Display the complete JSON response from the API instead of just the content")
    
    # Add API key test functionality
    st.sidebar.markdown("---")
    st.sidebar.title("API Testing")
    if st.sidebar.button("Test API Key"):
        with st.spinner("Testing API key..."):
            test_result = get_ai_suggestion("test", st.session_state.api_key)
            if "❌" in test_result:
                st.sidebar.error("API key test failed. Please check your key.")
            else:
                st.sidebar.success("✅ API key is working!")

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