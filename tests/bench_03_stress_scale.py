from core import BenchCase, BenchTarget, run_bench_suite

SUITE_ID = "StressScale"
SUITE_NAME = "Стресс-тестирование генерации страниц (100 и 500+ страниц)"

STRESS_TEMPLATE = '''#import "lib.typ": *
#show: eskd-document.with(code: [ТЕСТ.000000.100РЭ], name: [Стресс-тест производительности], lit: [У])
#show: page-first-form2\n= Введение\n#lorem(100)\n#show: page-body
'''

benchmarks = [
    BenchCase(
        id="DocStress100P",
        name="Генерация 100+ страниц текста с Form 2a штампами",
        code=STRESS_TEMPLATE + "#lorem(80000)\n",
        repeats=1,
        targets=[
            BenchTarget("pdf", pdf_std="1.7"), BenchTarget("pdf", pdf_std="a-2b"),
            BenchTarget("svg", page="100"), BenchTarget("png", page="100"), BenchTarget("html")
        ]
    ),
    BenchCase(
        id="DocStress500P",
        name="Генерация 500+ страниц текста с Form 2a штампами",
        code=STRESS_TEMPLATE + "#lorem(400000)\n",
        repeats=1,
        targets=[BenchTarget("pdf", pdf_std="1.7"), BenchTarget("svg", page="500")]
    ),
]

if __name__ == "__main__":
    passed, failed = run_bench_suite(SUITE_ID, SUITE_NAME, benchmarks)
    if failed > 0: exit(1)