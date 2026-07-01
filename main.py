import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
import functions

MODEL = "gemini-2.5-flash"
MAX_ITERATIONS_PER_LOOP = 20


def prompt_gemini(messages: list[types.Content], verbose: bool = False) -> bool:
    """
    Prompts the model. Returns `True` if any function calls were requested,
    signaling that the loop should continue.
    """
    _ = load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("Need credentials. Define GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
            model=MODEL,
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[functions.available_functions],
                system_instruction=system_prompt),
            )

    if response.candidates is not None:
        for candidate in response.candidates:
            if candidate.content is not None:
                messages.append(candidate.content)

    usage = response.usage_metadata
    if usage is not None:
        if verbose and messages[-1].parts is not None:
            user_prompt = messages[-1].parts[0]
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {usage.prompt_token_count}")
            print(f"Response tokens: {usage.candidates_token_count}")
            print("Response:")
    has_function_calls = response.function_calls is not None and len(response.function_calls) > 0
    if has_function_calls:
        for fn_call in response.function_calls:
            result = functions.call_function(fn_call, verbose=verbose)
            if result.parts is None or len(result.parts) == 0:
                raise RuntimeError("No response contents!")
            elif result.parts[0].function_response is None:
                raise RuntimeError("No function response!")
            elif result.parts[0].function_response.response is None:
                raise RuntimeError("Empty function response!")
            if verbose:
                print(f"-> {result.parts[0].function_response.response}")
            messages.append(result)
    else:
        print(response.text)

    return has_function_calls

def agentic_loop(user_prompt: str, verbose: bool):
    messages: list[types.Content] = [
            types.Content(role="user", parts=[types.Part(text=user_prompt)])
            ]
    try:
        for _ in range(MAX_ITERATIONS_PER_LOOP):
            if not prompt_gemini(messages, verbose=verbose):
                break
        else:
            print("Too many iterations", file=sys.stderr)
            sys.exit(1)
    except RuntimeError as ex:
        print("Error while processing the prompt: {ex}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    _ = parser.add_argument("user_prompt", type=str, help="User prompt")
    _ = parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    agentic_loop(user_prompt=args.user_prompt, verbose=args.verbose)


if __name__ == "__main__":
    main()
