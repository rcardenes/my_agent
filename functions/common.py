import pathlib
import os
import enum

class Permissions(enum.Flag):
    Ignore = enum.auto()
    Read = enum.auto()
    Write = enum.auto()

class ValidatePathResult(enum.Enum):
    ForbiddenPath = enum.auto()
    ValidFile = enum.auto()
    ValidDir = enum.auto()
    DoesNotExist = enum.auto()
    CantOperate = enum.auto()

def validate_path(working_directory: str, target: str, permissions: Permissions = Permissions.Read) -> ValidatePathResult:
    wd_path = pathlib.Path(working_directory).resolve().absolute()
    target_path = (wd_path / target).resolve().absolute()

    ignore_perm = bool(permissions & Permissions.Ignore)
    mode = 0
    if Permissions.Read & permissions:
        mode |= os.R_OK
    if Permissions.Write & permissions:
        mode |= os.W_OK

    if not target_path.is_relative_to(wd_path):
        return ValidatePathResult.ForbiddenPath
    elif not target_path.exists():
        return ValidatePathResult.DoesNotExist
    elif not (ignore_perm or os.access(target_path, mode=mode)):
        return ValidatePathResult.CantOperate
    elif target_path.is_dir():
        return ValidatePathResult.ValidDir
    else:
        return ValidatePathResult.ValidFile
