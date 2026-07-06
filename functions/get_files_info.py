import pathlib
from .common import validate_path, ValidatePathResult

def get_files_info(working_directory: str, directory: str = ".") -> str:
    match validate_path(working_directory, directory):
        case ValidatePathResult.ForbiddenPath:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        case ValidatePathResult.ValidDir:
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

