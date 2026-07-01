from functions.run_python_file import run_python_file

test_cases: list[tuple[str, str, list[str]]] = [
        ("calculator", "main.py", []),
        ("calculator", "main.py", ["3 + 5"]),
        ("calculator", "tests.py", []),
        ("calculator", "../main.py", []),
        ("calculator", "nonexistent.py", []),
        ("calculator", "lorem.txt", []),
        ]

for tcase in test_cases:
    wd, fpath, args = tcase
    print(run_python_file(working_directory=wd, file_path=fpath, args=args))
