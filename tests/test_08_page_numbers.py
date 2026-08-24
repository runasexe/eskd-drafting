from core import TestCase, run_test_suite

SUITE_ID = "PageNumbers"
SUITE_NAME = "Нумерация листов (Графы 7 и 8, ГОСТ 2.104-2006)"

# Источники нормативных значений:
# - ГОСТ 2.104-2006 (п. 5.1): Графа 7 — порядковый номер листа документа, Графа 8 — общее число листов.
#   Номер текущего листа должен быть целым положительным числом >= 1 и не может превышать общее количество листов.

tests = [
    TestCase(
        name="AllowValidPageNumbers",
        code='#import "lib.typ": *\n#assert-page-numbers(2, 5)\n[OK]'
    ),
    TestCase(
        name="ForbidCurrentExceedsTotal",
        code='#import "lib.typ": *\n#assert-page-numbers(6, 5)',
        expect_error="eskd-drafting-page-numbers"
    ),
    TestCase(
        name="IgnoreCurrentExceedsTotalRule",
        code='#import "lib.typ": *\n#assert-page-numbers(6, 5, ignore-rules: "eskd-drafting-page-numbers")\n[OK]'
    ),
    TestCase(
        name="RenderLargePageNumbersForm1",
        code='''#import "lib.typ": *
#let f1 = frame-form-1(page: [150], total: [250])
[OK]'''
    ),
    TestCase(
        name="RenderLargePageNumbersForm2",
        code='''#import "lib.typ": *
#let f2 = frame-form-2(page: [150], total: [250])
[OK]'''
    ),
    TestCase(
        name="RenderLargePageNumbersForm2a",
        code='''#import "lib.typ": *
#let f2a = frame-form-2a(page: [150])
[OK]'''
    )
]

if __name__ == "__main__":
    passed, failed = run_test_suite(SUITE_ID, SUITE_NAME, tests)
    if failed > 0: exit(1)