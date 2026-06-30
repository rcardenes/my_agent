import pathlib
import os
import enum

class ValidatePathResult(enum.Enum):
    ForbiddenPath = enum.auto()
    ValidFile = enum.auto()
    ValidDir = enum.auto()
    InvalidPath = enum.auto()

def validate_path(working_directory: str, target: str) -> ValidatePathResult:
    wd_path = pathlib.Path(working_directory).resolve().absolute()
    target_path = (wd_path / target).resolve().absolute()

    if not target_path.exists() or not os.access(target_path, mode=os.R_OK):
        return ValidatePathResult.InvalidPath
    if not target_path.is_relative_to(wd_path):
        return ValidatePathResult.ForbiddenPath
    elif target_path.is_dir():
        return ValidatePathResult.ValidDir
    else:
        return ValidatePathResult.ValidFile
