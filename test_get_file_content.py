from functions.get_file_content import get_file_content

test_cases = [
        ("calculator", "lorem.txt"),
        ("calculator", "main.py"),
        ("calculator", "pkg/calculator.py"),
        ("calculator", "/bin/cat"),
        ("calculator", "pkg/does_not_exist.py"),
        ]

for (wd, fpath) in test_cases:
    result = get_file_content(wd, fpath)
    truncated = 'truncated' in result
    if truncated:
        print(f"{fpath} length: {len(result)}")
    else:
        print(result)
    print(f"{fpath} truncated: {truncated}")
