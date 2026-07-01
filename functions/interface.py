from collections.abc import Callable

from google.genai import types

class FunctionCaller:
    def __init__(self, dispatcher: dict[str, Callable[..., str]]):
        self.fn_dispatch: dict[str, Callable[..., str]] = dispatcher

    def __call__(self, function_call: types.FunctionCall, verbose: bool = False) -> types.Content:
        function_name = function_call.name or ""
        try:
            fn = self.fn_dispatch[function_name]
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

