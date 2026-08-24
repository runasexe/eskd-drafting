from core import BenchCase, BenchTarget, run_bench_suite

SUITE_ID = "MicroAndStartup"
SUITE_NAME = "Холодный запуск, инициализация и микро-штампы"

benchmarks = [
    BenchCase(
        id="BlankPageA4",
        name="Минимальная инициализация документа (1 пустая страница)",
        code='#set document(title: "BlankPageA4")\n#import "lib.typ": *\n#show: eskd-document\n[Тест]\n',
        repeats=3,
        targets=[
            BenchTarget("pdf", pdf_std="1.7"),
            BenchTarget("pdf", pdf_std="a-2b"),
            BenchTarget("pdf", pdf_std="ua-1"),
            BenchTarget("png", page="1"),
            BenchTarget("svg", page="1"),
            BenchTarget("html"),
        ]
    ),
    BenchCase(
        id="SingleForm1Drawing",
        name="Рендеринг единичного чертежа Формы 1 (А4 Portrait)",
        code='''#set document(title: "SingleForm1Drawing")
#import "lib.typ": *
#show: eskd-document.with(code: [АБВГ.000001.001], name: [Тестовая деталь], lit: [О1])
#show: page-first-form1
[Чертеж детали]''',
        repeats=3,
        targets=[
            BenchTarget("pdf", pdf_std="1.7"),
            BenchTarget("pdf", pdf_std="a-2b"),
            BenchTarget("png", page="1"),
            BenchTarget("svg", page="1"),
            BenchTarget("html"),
        ]
    ),
    BenchCase(
        id="AutoFitGostStress50",
        name="Изолированный замер 50 вызовов auto-fit-gost",
        code='''#set document(title: "AutoFitGostStress50")
#import "lib.typ": *
#show: eskd-document
#for i in range(50) [ #auto-fit-gost([Длинный текст для подгонки], target-h: h5_0, min-h: h1_8, max-w: 60mm, max-h: 15mm) ]''',
        repeats=2,
        targets=[BenchTarget("pdf", pdf_std="1.7"), BenchTarget("svg", page="1")]
    ),
]

if __name__ == "__main__":
    passed, failed = run_bench_suite(SUITE_ID, SUITE_NAME, benchmarks)
    if failed > 0: exit(1)