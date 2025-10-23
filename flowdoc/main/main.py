import anthropic
from anthropic import Anthropic

def chat_with_claude(prompt: str) -> str:
    """
    Send a prompt to Claude and get the response.
    
    Args:
        prompt (str): The input prompt for Claude
        
    Returns:
        str: Claude's response
    """
    # Initialize the Anthropic client
    # Replace with your API key
    client = Anthropic(api_key="your-api-key-here")
    
    # Create a message
    message = client.messages.create(
        model="claude-3-opus-20240229",  # You can change the model as needed
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )
    
    return message.content[0].text

def main():
    # Example usage
    prompt = "Hello Claude! What can you help me with today?"
    response = chat_with_claude(prompt)
    print(f"Claude's response: {response}")

if __name__ == "__main__":
    main()
