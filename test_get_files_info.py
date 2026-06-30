#!/usr/bin/env python3

from functions.get_files_info import get_files_info

test_cases = [
        ("calculator", "."),
        ("calculator", "pkg"),
        ("calculator", "/bin"),
        ("calculator", "../"),
        ]


for (wd, d) in test_cases:
    print(f"Result for '{d}' directory:")
    res = get_files_info(wd, d).split('\n')
    for line in res:
        print(f"    {line}")

