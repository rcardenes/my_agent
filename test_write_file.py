from functions.write_file import write_file
import pathlib

test_cases = [
        ("calculator", "lorem.txt", "wait, this isn't lorem ipsum"),
        ("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
        ("calculator", "/tmp/temp.txt", "this should not be allowed"),
        ]

for (wd, fpath, content) in test_cases:
    result = write_file(wd, fpath, content)
    print(result)
    if not result.startswith("Error"):
        (pathlib.Path(wd) / fpath).unlink()
