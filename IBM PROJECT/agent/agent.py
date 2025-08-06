# agent.py

# 1. Define the dictionary of project types and their tech stacks
tech_stacks = {
    "portfolio website": {
        "Frontend": "HTML/CSS/JavaScript or React",
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

# 2. Function to return stack if it exists
def get_stack(project_type):
    project_type = project_type.lower().strip()
    if project_type in tech_stacks:
        print(f"\n✅ Recommended stack for '{project_type.title()}':")
        print("-" * 50)
        for key, value in tech_stacks[project_type].items():
            print(f"{key:10}: {value}")
        print("-" * 50)
    else:
        print("\n❌ Sorry, I don't have a suggestion for that yet.")
        print("Available project types:")
        for project in tech_stacks.keys():
            print(f"- {project}")


# 3. CLI Interaction Loop
def main():
    print("🔧 Welcome to TechStack Guide Agent")
    print("Type a project like 'portfolio website', 'e-commerce website', or 'chat app (python)'")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("👉 What do you want to build?\n> ")
        if user_input.lower() == "exit":
            print("👋 Goodbye!")
            break
        get_stack(user_input)

# 4. Run the main loop
if __name__ == "__main__":
    main()
