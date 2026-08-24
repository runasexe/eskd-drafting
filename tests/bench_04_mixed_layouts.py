from core import BenchCase, BenchTarget, run_bench_suite

SUITE_ID = "MixedLayouts"
SUITE_NAME = "Комплексные сборки (Form 1 + Form 2 + Form 2 + Form 2b + А4/А3)"

benchmarks = [
    BenchCase(
        id="MultiFormMixedDoc",
        name="Чередование штампов и форматов бумаги (6 страниц)",
        code='''#set document(title: "MultiFormMixedDoc")
#import "lib.typ": *
#show: eskd-document.with(code: [КОМП.777000.001], name: [Сборный проект], lit: [О1])

#show: page-first-form2\n= Текстовый ввод\n#lorem(100)
#show: page-first-form2.with(toc: (num: [№], name: [Наименование]))\n= Оглавление\n#outline(title: none)
#show: page-first-form1\n= Графическая часть А4\n#lorem(50)
#show: eskd-page.with(paper: "a3", orientation: "landscape", bottom: frame-form-1)\n= Чертёж общего вида А3\n#lorem(50)
#show: page-body-double\n= Двусторонняя страница\n#lorem(100)
#show: page-body\n= Заключительный лист\n#lorem(100)
''',
        repeats=2,
        targets=[
            BenchTarget("pdf", pdf_std="1.7"), BenchTarget("pdf", pdf_std="2.0"),
            BenchTarget("pdf", pdf_std="a-1b"), BenchTarget("pdf", pdf_std="ua-1"),
            BenchTarget("svg", page="1"), BenchTarget("svg", page="4"), BenchTarget("svg", page="6"),
            BenchTarget("png", page="6"), BenchTarget("html")
        ]
    )
]

if __name__ == "__main__":
    passed, failed = run_bench_suite(SUITE_ID, SUITE_NAME, benchmarks)
    if failed > 0: exit(1)