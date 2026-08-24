from core import TestCase, run_test_suite

SUITE_ID = "Lines"
SUITE_NAME = "Толщина и соотношения линий (ГОСТ 2.303-68)"

# Источники нормативных значений:
# - ГОСТ 2.303-68 (п. 2, Таблица 1):
#   - Толщина сплошной толстой основной линии s должна быть в диапазоне от 0.5 до 1.4 мм.
#   - Толщина сплошной тонкой линии s_thin должна быть от s/3 до s/2 (примерно 0.35 мм при s = 0.8 мм).

tests = [
    TestCase(
        name="AllowValidLineThicknesses",
        code='#import "lib.typ": *\n#assert-line-thicknesses(0.8mm, 0.35mm)\n[OK]'
    ),
    TestCase(
        name="ForbidInvalidLineThicknessS",
        code='#import "lib.typ": *\n#assert-line-thicknesses(1.8mm, 0.6mm)',
        expect_error="gost-2.303-68-line-thickness-s"
    ),
    TestCase(
        name="IgnoreInvalidLineThicknessSRule",
        code='#import "lib.typ": *\n#assert-line-thicknesses(1.8mm, 0.6mm, ignore-rules: "gost-2.303-68-line-thickness-s")\n[OK]'
    ),
    TestCase(
        name="ForbidInvalidLineThicknessRatio",
        code='#import "lib.typ": *\n#assert-line-thicknesses(0.5mm, 0.4mm)',
        expect_error="gost-2.303-68-line-thickness-ratio"
    ),
    TestCase(
        name="IgnoreInvalidLineThicknessRatioRule",
        code='#import "lib.typ": *\n#assert-line-thicknesses(0.5mm, 0.4mm, ignore-rules: "gost-2.303-68-line-thickness-ratio")\n[OK]'
    )
]

if __name__ == "__main__":
    passed, failed = run_test_suite(SUITE_ID, SUITE_NAME, tests)
    if failed > 0: exit(1)