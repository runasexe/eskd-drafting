import re
from pathlib import Path
from core import TestCase, run_test_suite, PROJECT_ROOT

SUITE_ID = "CompileExamples"
SUITE_NAME = "Компиляция всех примеров и шаблонов (in-memory)"

def build_example_tests():
    test_cases = []

    examples_dir = PROJECT_ROOT / "examples"
    example_files = sorted(examples_dir.rglob("*.typ")) if examples_dir.exists() else []

    template_file = PROJECT_ROOT / "template" / "main.typ"
    all_files = list(example_files)
    if template_file.exists():
        all_files.append(template_file)

    if not all_files:
        return []

    for p in all_files:
        rel = p.relative_to(PROJECT_ROOT)
        name = str(rel).replace("\\", "/").replace(".typ", "")

        with open(p, "r", encoding="utf-8") as f:
            raw_code = f.read()

        code = re.sub(r'@preview/eskd-drafting:[0-9a-zA-Z._-]+', 'lib.typ', raw_code)

        test_cases.append(TestCase(
            name=name,
            code=code,
            format="pdf"
        ))

    return test_cases

tests = build_example_tests()

if __name__ == "__main__":
    if tests:
        passed, failed = run_test_suite(SUITE_ID, SUITE_NAME, tests)
        if failed > 0:
            exit(1)
