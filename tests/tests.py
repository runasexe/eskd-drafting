import sys
import time
import importlib.util
from pathlib import Path
from core import get_typst_version, run_test_suite

def discover_and_run():
    current_dir = Path(__file__).resolve().parent
    test_files = sorted(current_dir.glob("test_*.py"))

    if not test_files:
        print("Файлы тестов test_*.py не найдены.")
        sys.exit(0)

    print(f"typst: {get_typst_version()} | os: {sys.platform} | python: {sys.version.split()[0]}\n")

    total_p, total_f, total_t = 0, 0, 0
    global_start = time.perf_counter()

    for test_file in test_files:
        spec = importlib.util.spec_from_file_location(test_file.stem, test_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, "tests"):
            p, f = run_test_suite(
                getattr(module, "SUITE_ID", test_file.stem),
                getattr(module, "SUITE_NAME", ""),
                module.tests
            )
            total_p += p
            total_f += f
            total_t += len(module.tests)

    print(f"\n{'PASS' if total_f == 0 else 'FAIL'} \t[{total_p}/{total_t} passed] in {time.perf_counter() - global_start:.3f}s")
    if total_f > 0:
        sys.exit(1)

if __name__ == "__main__":
    discover_and_run()