import sys
from collections.abc import Callable

from google.genai import types

from . import (
        get_file_content,
        get_files_info,
        run_python_file,
        write_file
        )

modules = (
        get_file_content,
        get_files_info,
        run_python_file,
        write_file
        )

tools: list[types.FunctionDeclaration] = []
fn_dispatch: dict[str, Callable[..., str]] = {}

for mod in modules:
    try:
        tools.append(mod.schema)
        fn_dispatch[mod.exported_function.__name__] = mod.exported_function
    except AttributeError as ex:
        print(f"Could not import function in module {mod.__name__}: {ex}", file=sys.stderr)

available_functions = types.Tool(
        function_declarations=tools
        )
