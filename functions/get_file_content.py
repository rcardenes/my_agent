import pathlib

from google.genai import types

from .common import validate_path, ValidatePathResult

MAX_CHARS = 10000

schema = types.FunctionDeclaration(
        name = "get_files_content",
        description = "Reads and returns the contents of a file, truncating it if too large",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="Mandatory. Path to the file to be read, relative to the working directory",
                    ),
                },
            ),
        )

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        match validate_path(working_directory, file_path):
            case ValidatePathResult.ForbiddenPath:
                return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
            case ValidatePathResult.ValidFile:
                target_path = pathlib.Path(working_directory) / file_path
                actual_size = target_path.stat().st_size
                with open(target_path, "r") as target_file:
                    read = target_file.read(MAX_CHARS)

                if actual_size > MAX_CHARS:
                    return read + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                else:
                    return read
            case _:
                return f'Error: File not found or is not a regular file: "{file_path}"'
    except Exception as ex:
        return f'Error: {ex}'

exported_function = get_file_content
