# TechStack Guide Agent

A simple tool to recommend technology stacks for different types of projects. Available in both CLI and web interface versions.

## Features

- Get recommended tech stacks for common project types
- CLI interface for quick access
- Web interface with Streamlit for a more user-friendly experience
- AI-powered suggestions for project types not in the predefined list

## Setup

### Prerequisites

- Python 3.6 or higher
- pip (Python package manager)

### Installation

1. Clone this repository or download the files
2. Install the required packages:

```bash
pip install streamlit fuzzywuzzy python-dotenv requests
```

3. For AI-powered suggestions, create a `.env` file in the project root:

```
# Copy from .env.example
OPENROUTER_API_KEY=your_api_key_here
```

You can get an API key from [OpenRouter](https://openrouter.ai/).

## Usage

### CLI Version

Run the CLI version with:

```bash
python agent.py
```

Follow the prompts to enter the type of project you want to build.

### Web Version

Run the web version with:

```bash
streamlit run web_agent.py
```

This will open a browser window with the web interface.

## Available Project Types

- Portfolio Website
- E-commerce Website
- Chat App (Python)
- Blog Website
- Mobile App

For other project types, the web version will attempt to provide AI-generated recommendations if an API key is configured.

## License

MIT