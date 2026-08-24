from core import BenchCase, BenchTarget, run_bench_suite

SUITE_ID = "ExplanatoryNote"
SUITE_NAME = "Пояснительная записка (Титул + Содержание + Форма 2 + Форма 2а)"

BASE_NOTE_CODE = '''#import "lib.typ": *
#show: eskd-document.with(
  preset-lines: "industry",
  code: [АБВГ.123456.001ПЗ], name: [Устройство обработки\\nПояснительная записка], lit: [О1],
  members: (("Разраб.", "Алексеев", "12.05"), ("Пров.", "Борисов", "15.05"), (), ("Утв.", "Дмитриев", "20.05"))
)
#show: page-title
#align(center + horizon)[#gost-text(h: h7_0, weight: "bold")[ПОЯСНИТЕЛЬНАЯ ЗАПИСКА]]
#show: page-first-form2.with(toc: (num: [№], name: [Наименование], code: [Обозначение], note: [Примечание]))
#align(center)[#gost-text(h: h5_0, weight: "bold")[СОДЕРЖАНИЕ]]\n#outline(title: none)
#show: page-first-form2
= 1. Введение\n#lorem(200)
#show: page-body
'''

benchmarks = [
    BenchCase(
        id="ExplNoteMedium5P",
        name="Пояснительная записка (5 страниц)",
        code=BASE_NOTE_CODE + "\n".join([f"= Раздел {i}\n#lorem(350)" for i in range(2, 6)]),
        repeats=2,
        targets=[
            BenchTarget("pdf", pdf_std="1.7"), BenchTarget("pdf", pdf_std="a-2b"), BenchTarget("pdf", pdf_std="a-3b"),
            BenchTarget("svg", page="1"), BenchTarget("svg", page="5"), BenchTarget("png", page="5"), BenchTarget("html")
        ]
    ),
    BenchCase(
        id="ExplNoteLarge25P",
        name="Пояснительная записка (25+ страниц)",
        code=BASE_NOTE_CODE + "\n".join([f"= Раздел {i}\n#lorem(500)" for i in range(2, 33)]),
        repeats=1,
        targets=[BenchTarget("pdf", pdf_std="1.7"), BenchTarget("pdf", pdf_std="a-2b"), BenchTarget("svg", page="25")]
    ),
]

if __name__ == "__main__":
    passed, failed = run_bench_suite(SUITE_ID, SUITE_NAME, benchmarks)
    if failed > 0: exit(1)