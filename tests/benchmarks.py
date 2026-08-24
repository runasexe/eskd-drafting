import sys
import importlib.util
from pathlib import Path
from core import get_typst_version, run_bench_suite

def discover_and_run():
    current_dir = Path(__file__).resolve().parent
    bench_files = sorted(current_dir.glob("bench_*.py"))

    if not bench_files:
        print("Файлы бенчмарков bench_*.py не найдены.")
        sys.exit(0)

    print(f"typst: {get_typst_version()} | os: {sys.platform} | python: {sys.version.split()[0]}\n")

    total_p, total_f = 0, 0

    for bench_file in bench_files:
        spec = importlib.util.spec_from_file_location(bench_file.stem, bench_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, "benchmarks"):
            p, f = run_bench_suite(
                getattr(module, "SUITE_ID", bench_file.stem),
                getattr(module, "SUITE_NAME", ""),
                module.benchmarks
            )
            total_p += p
            total_f += f

    print(f"\nBENCHMARK {'PASS' if total_f == 0 else 'FAIL'} ({total_p} targets ok, {total_f} failed)")
    if total_f > 0:
        sys.exit(1)

if __name__ == "__main__":
    discover_and_run()