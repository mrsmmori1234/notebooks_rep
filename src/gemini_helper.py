import sys
from google import genai
from IPython.display import display, Markdown

# Initialize the GenAI client (Automatically picks up GEMINI_API_KEY from environment variables)
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing GenAI Client. Ensure GEMINI_API_KEY is set. Details: {e}")

def ai(prompt: str = None) -> None:
    """
    Jupyter Helper function to interact with Gemini 2.5 Flash.
    
    Usage:
    - ai()          : Automatically extracts the code and error traceback from the 
                      previous cell and requests a fix/refactor.
    - ai("prompt")  : Regular chatbot interaction for generating new scripts or asking questions.
    """
    # Access the interactive shell instance to read cell history safely
    ip = get_ipython()
    if not ip:
        print("Error: This helper function must be executed inside a Jupyter Notebook environment.")
        return

    if prompt is None:
        # Retrieve the historical execution data from Jupyter
        history = ip.history_manager.input_hist_raw
        if len(history) < 2:
            print("No execution history found to analyze.")
            return
            
        # Get the code snippet from the immediately preceding cell
        last_code = history[-2]
        
        # Capture the standard execution output or exception tracebacks
        last_output = ""
        
        # Check if the last cell threw an exception and extract the traceback
        if hasattr(sys, 'last_value') and sys.last_value is not None:
            import traceback
            last_output = "".join(traceback.format_exception(sys.last_type, sys.last_value, sys.last_traceback))
        else:
            # Fallback to the latest execution output variable '_'
            last_output = ip.user_ns.get('_', '')

        # Build the structured prompt for code debugging
        prompt = f"""
Please review the following Python code snippet. Provide bug fixes, code optimization, or refactoring suggestions as needed.

[Target Code snippet]
{last_code}

[Execution Output / Error Logs]
{last_output}
"""

    try:
        # Request a response using the current main stable Free-Tier model
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        # Render the response beautifully using Markdown
        display(Markdown(response.text))
        
    except Exception as e:
        display(Markdown(f"**API Error:** Failed to communicate with Gemini API. Details:\n`{e}`"))