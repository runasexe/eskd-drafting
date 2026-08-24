from core import TestCase, run_test_suite

SUITE_ID = "Scale"
SUITE_NAME = "Масштабы чертежей (Графа 6, ГОСТ 2.302-68)"

# Источники нормативных значений:
# - ГОСТ 2.302-68 (п. 2, Таблица 1): Ряд стандартных масштабов уменьшения (1:2, 1:2.5, 1:4, 1:5, 1:10 и др.)
#   и увеличения (2:1, 2.5:1, 4:1, 5:1, 10:1 и др.), а также натуральной величины (1:1).
# - Запрещается указывать префиксы «М:» или «М» в графе 6 основной надписи.
# - В качестве десятичного разделителя в масштабах 1:2,5 используется запятая.

tests = [
    TestCase(
        name="AllowValidGostScale",
        code='#import "lib.typ": *\n#assert-scale("1:2,5")\n[OK]'
    ),
    TestCase(
        name="ForbidPrefixMInScale",
        code='#import "lib.typ": *\n#assert-scale("М 1:1")',
        expect_error="gost-2.302-68-scale-m-prefix"
    ),
    TestCase(
        name="IgnorePrefixMInScaleRule",
        code='#import "lib.typ": *\n#assert-scale("М 1:1", ignore-rules: ("gost-2.302-68-scale-m-prefix", "gost-2.302-68-scale-series"))\n[OK]'
    ),
    TestCase(
        name="ForbidDecimalDotInScale",
        code='#import "lib.typ": *\n#assert-scale("1:2.5")',
        expect_error="gost-2.302-68-scale-decimal-comma"
    ),
    TestCase(
        name="IgnoreDecimalDotInScaleRule",
        code='#import "lib.typ": *\n#assert-scale("1:2.5", ignore-rules: ("gost-2.302-68-scale-decimal-comma", "gost-2.302-68-scale-series"))\n[OK]'
    ),
    TestCase(
        name="ForbidNonStandardScaleSeries",
        code='#import "lib.typ": *\n#assert-scale("1:3")',
        expect_error="gost-2.302-68-scale-series"
    ),
    TestCase(
        name="IgnoreNonStandardScaleSeriesRule",
        code='#import "lib.typ": *\n#assert-scale("1:3", ignore-rules: "gost-2.302-68-scale-series")\n[OK]'
    )
]

if __name__ == "__main__":
    passed, failed = run_test_suite(SUITE_ID, SUITE_NAME, tests)
    if failed > 0: exit(1)