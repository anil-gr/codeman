import requests
import json
import gradio as gr
import os

# Server URL and headers
# Allow URL to be configurable via an environment variable for flexibility
url = os.getenv("SERVER_URL", "http://localhost:11434/api/generate")
headers = {
    "Content-Type": "application/json"
}

# History to track prompts
history = []

def generate_response(prompt):
    """
    Generates a response by sending the prompt to the API and processing the streamed response.

    Args:
        prompt (str): User's input prompt.

    Returns:
        str: The complete response from the API or an error message.
    """
    # Append the prompt to the history
    history.append(prompt)
    final_prompt = "\n".join(history)

    # Request payload
    data = {
        "model": "codeman",
        "prompt": final_prompt
    }

    try:
        # Send the POST request and enable streaming
        response = requests.post(
            url=url,
            headers=headers,
            data=json.dumps(data),
            stream=True,  # Enable streaming
        )

        # Ensure the response is successful
        response.raise_for_status()

        # Accumulate the streamed responses
        full_response = ""
        for line in response.iter_lines(decode_unicode=True):
            if line:  # Avoid empty lines
                partial_data = json.loads(line)
                full_response += partial_data.get("response", "")
                if partial_data.get("done", False):
                    break

        return full_response

    except requests.exceptions.RequestException as req_err:
        # Handle connection-related errors
        return f"Connection error: {req_err}"

    except json.JSONDecodeError as json_err:
        # Handle JSON parsing errors
        return f"Error decoding response: {json_err}"

    except Exception as e:
        # Handle other unexpected errors
        return f"An unexpected error occurred: {str(e)}"


# Gradio interface for the front end
interface = gr.Interface(
    fn=generate_response,
    inputs=gr.Textbox(lines=4, placeholder="Enter your query"),
    outputs="text",
    title="CodeMan AI",
    description="Enter a prompt to interact with the CodeMan model."
)

# Launch the Gradio app
if __name__ == "__main__":
    interface.launch(share=True)
