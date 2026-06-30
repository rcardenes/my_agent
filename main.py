import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

MODEL = "gemini-2.5-flash"

def prompt_gemini(messages: list[types.Content], verbose: bool = False):
    _ = load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("Need credentials. Define GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
            model=MODEL,
            contents=messages
            )

    usage = response.usage_metadata
    if usage is not None:
        if verbose:
            user_prompt = messages[-1].parts[0]
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {usage.prompt_token_count}")
            print(f"Response tokens: {usage.candidates_token_count}")
            print("Response:")
        print(response.text)

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    _ = parser.add_argument("user_prompt", type=str, help="User prompt")
    _ = parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    user_prompt = str(args.user_prompt)

    messages: list[types.Content] = [
            types.Content(role="user", parts=[types.Part(text=user_prompt)])
            ]

    prompt_gemini(messages, verbose=args.verbose)


if __name__ == "__main__":
    main()
