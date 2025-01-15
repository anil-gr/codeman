import requests
import json
import gradio as gr

# Server URL and headers
url = "http://localhost:11434/api/generate"
headers = {
    "Content-Type": "application/json"
}

# History to track prompts
history = []

def generate_response(prompt):
    """
    Generates a response by sending the prompt to the API and processing the response.

    Args:
        prompt (str): User's input prompt.

    Returns:
        str: The response from the API or an error message.
    """
    history.append(prompt)
    final_prompt = "\n".join(history)

    data = {
        "model": "codeman",
        "prompt": final_prompt
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print("Raw Response:", response.text)

        if response.headers.get("Content-Type") == "application/json":
            data = json.loads(response.text)
            return data.get("response", "No response key found in the server's JSON.")
        else:
            return f"Error: Received non-JSON response from the server.\nResponse: {response.text}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Gradio interface for the front end
interface = gr.Interface(
    fn=generate_response,
    inputs=gr.Textbox(lines=4, placeholder="Enter your query"),
    outputs="text",
    title="CodeMan AI",
    description="Enter a prompt to interact with the CodeMan model.",
    live=True
)

# Launch the Gradio app
if __name__ == "__main__":
    interface.launch(share=True)
