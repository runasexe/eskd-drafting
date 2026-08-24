from core import TestCase, run_test_suite

SUITE_ID = "Litera"
SUITE_NAME = "Литеры документа (ГОСТ 2.103-2013, Таблица 1)"

# Источники нормативных значений:
# - ГОСТ 2.103-2013 (п. 4, Таблица 1): Допустимые литеры стадий разработки:
#   П (проект), Э (эскизный), Т (технический), И (изделие), О, О1, О2 (опытная партия), А, Б (серийное), У (учебное).
# - ГОСТ 2.104-2006 (п. 5.1): Графа 4 состоит из трех ячеек шириной по 5 мм для поочередного заполнения литер.

tests = [
    TestCase(
        name="ParseSingleLitera",
        code='''#import "lib.typ": *
#let (l1, l2, l3) = parse-lit-cells("У")
#assert(l1 == "У" and l2 == [] and l3 == [], message: "Single litera parse failed")
[OK]'''
    ),
    TestCase(
        name="ParseMultiLiteraArray",
        code='''#import "lib.typ": *
#let (l1, l2, l3) = parse-lit-cells(("О1", "А"))
#assert(l1 == "О1" and l2 == "А" and l3 == [], message: "Multi-litera parse failed")
[OK]'''
    ),
    TestCase(
        name="ForbidInvalidLiteraValue",
        code='#import "lib.typ": *\n#assert-lit("Я")',
        expect_error="gost-2.103-2013-litera-value"
    ),
    TestCase(
        name="IgnoreInvalidLiteraValueRule",
        code='#import "lib.typ": *\n#assert-lit("Я", ignore-rules: "gost-2.103-2013-litera-value")\n[OK]'
    ),
    TestCase(
        name="RenderCompoundLiteraForm1",
        code='''#import "lib.typ": *
#let f1 = frame-form-1(lit: [О1])
[OK]'''
    ),
    TestCase(
        name="RenderCompoundLiteraForm2",
        code='''#import "lib.typ": *
#let f2 = frame-form-2(lit: [О1])
[OK]'''
    ),
    TestCase(
        name="RenderMultiLiteraHarmonized",
        code='''#import "lib.typ": *
#let f1 = frame-form-1(lit: ("О1", "А"))
#let f2 = frame-form-2(lit: ("О1", "А"))
[OK]'''
    ),
    TestCase(
        name="ForbidCompoundLiteraBaseHeightBelow2_5mm",
        code='#import "lib.typ": *\n#frame-form-1(lit: [О1], sizes: (lit: h1_8))',
        expect_error="gost-2.304-81-subscript-base-height"
    ),
    TestCase(
        name="IgnoreCompoundLiteraBaseHeightBelow2_5mmRule",
        code='#import "lib.typ": *\n#frame-form-1(lit: [О1], sizes: (lit: h1_8), ignore-rules: "gost-2.304-81-subscript-base-height")\n[OK]'
    )
]

if __name__ == "__main__":
    passed, failed = run_test_suite(SUITE_ID, SUITE_NAME, tests)
    if failed > 0: exit(1)