from core import TestCase, run_test_suite

SUITE_ID = "Mass"
SUITE_NAME = "Масса изделия (Графа 5, ГОСТ 2.104-2006)"

# Источники нормативных значений:
# - ГОСТ 2.104-2006 (п. 5.1, Графа 5): Масса изделия указывается в килограммах без обозначения единицы измерения («кг»).
#   Если масса приводится в других единицах (граммах, тоннах), единица измерения («г», «т») указывается явно.
#   Десятичным разделителем в русскоязычной нормативной документации является запятая.

tests = [
    TestCase(
        name="AllowValidDecimalCommaMass",
        code='#import "lib.typ": *\n#assert-mass("15,4")\n[OK]'
    ),
    TestCase(
        name="AllowGramsMassUnit",
        code='#import "lib.typ": *\n#assert-mass("400 г")\n[OK]'
    ),
    TestCase(
        name="ForbidKgMassUnit",
        code='#import "lib.typ": *\n#assert-mass("15,4 кг")',
        expect_error="gost-2.104-2006-mass-unit"
    ),
    TestCase(
        name="IgnoreKgMassUnitRule",
        code='#import "lib.typ": *\n#assert-mass("15,4 кг", ignore-rules: "gost-2.104-2006-mass-unit")\n[OK]'
    ),
    TestCase(
        name="ForbidDecimalDotMass",
        code='#import "lib.typ": *\n#assert-mass("0.45")',
        expect_error="gost-2.104-2006-mass-decimal-comma"
    ),
    TestCase(
        name="IgnoreDecimalDotMassRule",
        code='#import "lib.typ": *\n#assert-mass("0.45", ignore-rules: "gost-2.104-2006-mass-decimal-comma")\n[OK]'
    )
]

if __name__ == "__main__":
    passed, failed = run_test_suite(SUITE_ID, SUITE_NAME, tests)
    if failed > 0: exit(1)