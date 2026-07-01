import pathlib

from google.genai import types

from .common import validate_path, ValidatePathResult

schema = types.FunctionDeclaration(
        name = "get_files_info",
        description = "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="Optional. Directory path to list files from, relative to the working directory (default is the working directory itself)",
                    ),
                },
            ),
        )

def get_files_info(working_directory: str, directory: str = ".") -> str:
    match validate_path(working_directory, directory):
        case ValidatePathResult.ForbiddenPath:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        case ValidatePathResult.ValidFile:
            target_path = pathlib.Path(working_directory) / directory
            results: list[str] = []
            for fpath in target_path.iterdir():
                name = fpath.name
                size = fpath.stat().st_size
                is_dir = fpath.is_dir()
                results.append(f"- {name}: file_size={size} bytes, is_dir={is_dir}")
            return '\n'.join(results)
        case _:
            return f'Error: "{directory}" is not a directory'

exported_function = get_files_info
