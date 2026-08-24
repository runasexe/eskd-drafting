from core import TestCase, run_test_suite

SUITE_ID = "PresetsAndStamps"
SUITE_NAME = "Пресеты линий и геометрия штампов (ГОСТ 2.104-2006)"

# Источники нормативных значений:
# - ГОСТ 2.104-2006 (п. 4, п. 5): Геометрическая ширина штампов ЕСКД составляет строго 185 мм.
#   Высота штампов: Форма 1 = 55 мм, Форма 2 = 40 мм, Форма 2 с шапкой содержания = 52 мм, Форма 2а/2б = 15 мм.
# - Разрешенные пресеты линий: "industry" (0.8 мм толстые разделители САПР) и "gost" (0.35 мм тонкие разделители).

tests = [
    TestCase(
        name="AllowValidLinePresets",
        code='#import "lib.typ": *\n#assert-preset-lines("industry")\n#assert-preset-lines("gost")\n[OK]'
    ),
    TestCase(
        name="ForbidInvalidLinePreset",
        code='#import "lib.typ": *\n#assert-preset-lines("custom-invalid")',
        expect_error="eskd-drafting-preset-lines"
    ),
    TestCase(
        name="IgnoreInvalidLinePresetRule",
        code='#import "lib.typ": *\n#assert-preset-lines("custom-invalid", ignore-rules: "eskd-drafting-preset-lines")\n[OK]'
    ),
    TestCase(
        name="ForbidInvalidStampWidth",
        code='#import "lib.typ": *\n#assert-stamp-geometry((10mm, 20mm), (5mm, 5mm), 35mm, 10mm, "TestStamp")',
        expect_error="gost-2.104-2006-stamp-width"
    ),
    TestCase(
        name="IgnoreInvalidStampWidthRule",
        code='#import "lib.typ": *\n#assert-stamp-geometry((10mm, 20mm), (5mm, 5mm), 35mm, 10mm, "TestStamp", ignore-rules: "gost-2.104-2006-stamp-width")\n[OK]'
    ),
    TestCase(
        name="ForbidInvalidStampHeight",
        code='#import "lib.typ": *\n#assert-stamp-geometry((10mm, 20mm), (5mm, 5mm), 30mm, 15mm, "TestStamp")',
        expect_error="gost-2.104-2006-stamp-height"
    ),
    TestCase(
        name="IgnoreInvalidStampHeightRule",
        code='#import "lib.typ": *\n#assert-stamp-geometry((10mm, 20mm), (5mm, 5mm), 30mm, 15mm, "TestStamp", ignore-rules: "gost-2.104-2006-stamp-height")\n[OK]'
    )
]

if __name__ == "__main__":
    passed, failed = run_test_suite(SUITE_ID, SUITE_NAME, tests)
    if failed > 0: exit(1)