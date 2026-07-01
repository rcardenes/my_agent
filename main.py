import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
import functions

MODEL = "gemini-2.5-flash"

def call_function(function_call: types.FunctionCall, verbose: bool = False) -> types.Content:
    function_name = function_call.name or ""
    try:
        fn = functions.fn_dispatch[function_name]
    except KeyError:
        return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"error": f"Unknown function: {function_name}"},
                        )
                    ],
                )

    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

    args = dict(function_call.args) if function_call.args else {}
    args["working_directory"] = "./calculator"

    function_result: str = fn(**args)

    return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                    )
                ],
            )


def prompt_gemini(messages: list[types.Content], verbose: bool = False):
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

    usage = response.usage_metadata
    if usage is not None:
        if verbose:
            user_prompt = messages[-1].parts[0]
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {usage.prompt_token_count}")
            print(f"Response tokens: {usage.candidates_token_count}")
            print("Response:")
        if response.function_calls is not None:
            for fn_call in response.function_calls:
                result = call_function(fn_call, verbose=verbose)
                if result.parts is None or len(result.parts) == 0:
                    raise RuntimeError("No response contents!")
                elif result.parts[0].function_response is None:
                    raise RuntimeError("No function response!")
                elif result.parts[0].function_response.response is None:
                    raise RuntimeError("Empty function response!")
                if verbose:
                    print(f"-> {result.parts[0].function_response.response}")
        else:
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
