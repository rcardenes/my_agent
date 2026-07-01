from .common import validate_path, ValidatePathResult
import pathlib
import subprocess

RUN_TIMEOUT_SEC = 30

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        match validate_path(working_directory=working_directory, target=file_path):
            case ValidatePathResult.ForbiddenPath:
                return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
            case ValidatePathResult.ValidFile:
                if not file_path.endswith('.py'):
                    return f'Error: "{file_path}" is not a Python file'
                cwd = pathlib.Path(working_directory).resolve()
                if args is None:
                    args = []
                command = ["python", str((cwd / file_path).resolve()), *args]
                result = subprocess.run(command, cwd=cwd,
                                        capture_output=True,
                                        text=True,
                                        timeout=RUN_TIMEOUT_SEC)
                ret = ""
                if result.returncode != 0:
                    ret = f"Process exited with code {result.returncode}\n"
                if result.stdout == "" and result.stderr == "":
                    ret += "No output produced\n"
                else:
                    if result.stdout != "":
                        ret += "STDOUT:" + result.stdout
                    if result.stderr != "":
                        ret += "STDERR:" + result.stderr
                return ret
            case ValidatePathResult.DoesNotExist | ValidatePathResult.ValidDir:
                return f'Error: "{file_path}" does not exist or is not a regular file'
            case ValidatePathResult.CantOperate:
                return f'Error: Can\'t read "{file_path}" due to lack of permissions'
    except Exception as ex:
        return f'Error: {ex}'

