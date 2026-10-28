import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variable
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is required. Please set GEMINI_API_KEY in your .env file or environment.")

genai.configure(api_key=api_key)

def generate_project_ideas(skills, domain=None):
    try:
        # Use a supported model
        model = genai.GenerativeModel('gemini-2.0-flash')

        # Construct the prompt
        prompt = f"""
        Given these skills: {skills}
        {'In the domain of: ' + domain if domain else ''}

        Generate 3 unique project ideas. For each idea, include:
        1. Project Name
        2. Required Tools/Technologies
        3. Brief Description
        4. Difficulty Level (Beginner/Intermediate/Advanced)
        5. Estimated Time to Complete

        Format the output in a clear, structured way.
        """

        # Send prompt as plain text
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Error generating project ideas: {str(e)}\n\nPlease check your API key and internet connection."
