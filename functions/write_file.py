import pathlib

from google.genai import types

from .common import validate_path, ValidatePathResult, Permissions

schema = types.FunctionDeclaration(
        name = "write_file",
        description = "Write text to a file. Overwrites existing files. Creates a new file and its parent directories if needed",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="Path to the file where the contents will be written, relative to the working directory",
                    ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="The string of text to be written to the file",
                    ),
                },
            required = ["file_path", "content"],
            ),
        )

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        val = validate_path(working_directory, file_path, permissions=Permissions.Write)
        match val:
            case ValidatePathResult.ForbiddenPath:
                return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'
            case ValidatePathResult.ValidFile | ValidatePathResult.DoesNotExist:
                target_path = pathlib.Path(working_directory) / file_path
                target_path.parent.mkdir(parents=True, exist_ok=True)

                with open(target_path, "w") as target_file:
                    _ = target_file.write(content)

                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

            case ValidatePathResult.ValidDir:
                return f'Error: Cannot write to "{file_path}" as it is a directory'
            case ValidatePathResult.CantOperate:
                return f'Error: Lacking write permissions for: "{file_path}"'
    except Exception as ex:
        return f'Error: {ex}'

exported_function = write_file
