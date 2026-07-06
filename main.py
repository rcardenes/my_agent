import argparse
import os

from openai import OpenAI
from dotenv import load_dotenv

BASE_URL = "https://openrouter.ai/api/v1"
API_KEY_VAR = "OPENROUTER_API_KEY"

def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Chatbot")
    _ = parser.add_argument("user_prompt", type=str, help="User prompt")
    _ = parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    user_prompt = str(args.user_prompt)

    api_key = os.environ.get(API_KEY_VAR)

    if api_key is None:
        raise RuntimeError(f"Provide an API key in the environment variable {API_KEY_VAR}")

    client = OpenAI(
            base_url = BASE_URL,
            api_key = api_key)

    if args.verbose:
        print(f"User prompt: {user_prompt}")

    messages = [
            {
                "role": "user",
                "content": user_prompt,
                }
            ]
    response = client.responses.create(
            model="openrouter/free",
            input=messages,
        )

# chat.completions.create
# response.choices[0].message.content

    if args.verbose:
        print(f"Prompt tokens: {response.usage.input_tokens}")
        print(f"Response tokens: {response.usage.output_tokens}")

    print(response.output_text)

if __name__ == '__main__':
    main()
