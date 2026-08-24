from core import TestCase, run_test_suite

SUITE_ID = "StampGeometry"
SUITE_NAME = "Геометрия основных надписей и штампов (ГОСТ 2.104-2006)"

# Источники нормативных значений:
# - ГОСТ 2.104-2006 (п. 4.1, п. 5.1):
#   - Форма 1 (чертежи): 185 х 55 мм (11 строк по 5 мм, 12 колонок).
#   - Форма 2 (текстовые заглавные): 185 х 40 мм (8 строк по 5 мм, 11 колонок).
#   - Форма 2 с шапкой содержания (содержание): 185 х 52 мм (10 строк: 5+7+5*8 мм, 11 колонок).
#   - Форма 2а (последующие листы): 185 х 15 мм (3 строки по 5 мм, 7 колонок).
#   - Форма 2б (двусторонняя печать): 185 х 15 мм (зеркальная раскладка).
#   - Боковые штампы: 3r (85 х 12 мм), 5r (145 х 12 мм), 7r (287 х 12 мм).

tests = [
    TestCase(
        name="ValidateAllStandardStampGeometries",
        code='''#import "lib.typ": *
#assert-stamp-geometry((7mm, 10mm, 23mm, 15mm, 10mm, 70mm, 5mm, 5mm, 5mm, 5mm, 12mm, 18mm), (5mm,)*11, 185mm, 55mm, "Форма 1")
#assert-stamp-geometry((7mm, 10mm, 23mm, 15mm, 10mm, 70mm, 5mm, 5mm, 5mm, 15mm, 20mm), (5mm,)*8, 185mm, 40mm, "Форма 2")
#assert-stamp-geometry((7mm, 10mm, 23mm, 15mm, 10mm, 70mm, 5mm, 5mm, 5mm, 15mm, 20mm), (5mm, 7mm, 5mm, 5mm, 5mm, 5mm, 5mm, 5mm, 5mm, 5mm), 185mm, 52mm, "Форма 2 с шапкой содержания")
#assert-stamp-geometry((7mm, 10mm, 23mm, 15mm, 10mm, 110mm, 10mm), (5mm, 5mm, 5mm), 185mm, 15mm, "Форма 2а")
#assert-stamp-geometry((10mm, 110mm, 7mm, 10mm, 23mm, 15mm, 10mm), (5mm, 5mm, 5mm), 185mm, 15mm, "Форма 2б")
#assert-stamp-geometry((25mm, 35mm, 25mm), (5mm, 7mm), 85mm, 12mm, "Боковой 3r")
#assert-stamp-geometry((25mm, 35mm, 25mm, 25mm, 35mm), (5mm, 7mm), 145mm, 12mm, "Боковой 5r")
#assert-stamp-geometry((25mm, 35mm, 25mm, 25mm, 35mm, 47mm, 35mm, 60mm), (5mm, 7mm), 287mm, 12mm, "Боковой 7r A4")
#assert-stamp-geometry((25mm, 35mm, 25mm, 25mm, 35mm, 170mm, 35mm, 60mm), (5mm, 7mm), 410mm, 12mm, "Боковой 7r A3")
#assert-stamp-geometry((25mm, 35mm, 25mm, 25mm, 35mm, 344mm, 35mm, 60mm), (5mm, 7mm), 584mm, 12mm, "Боковой 7r A2")
#assert-stamp-geometry((25mm, 35mm, 25mm, 25mm, 35mm, 591mm, 35mm, 60mm), (5mm, 7mm), 831mm, 12mm, "Боковой 7r A1")
#assert-stamp-geometry((25mm, 35mm, 25mm, 25mm, 35mm, 939mm, 35mm, 60mm), (5mm, 7mm), 1179mm, 12mm, "Боковой 7r A0")
[OK]'''
    ),
    TestCase(
        name="ForbidIncorrectStampWidthGeometry",
        code='#import "lib.typ": *\n#assert-stamp-geometry((10mm, 20mm), (5mm, 5mm), 35mm, 10mm, "BadWidthStamp")',
        expect_error="gost-2.104-2006-stamp-width"
    ),
    TestCase(
        name="IgnoreIncorrectStampWidthGeometryRule",
        code='#import "lib.typ": *\n#assert-stamp-geometry((10mm, 20mm), (5mm, 5mm), 35mm, 10mm, "BadWidthStamp", ignore-rules: "gost-2.104-2006-stamp-width")\n[OK]'
    ),
    TestCase(
        name="ForbidIncorrectStampHeightGeometry",
        code='#import "lib.typ": *\n#assert-stamp-geometry((10mm, 20mm), (5mm, 5mm), 30mm, 15mm, "BadHeightStamp")',
        expect_error="gost-2.104-2006-stamp-height"
    ),
    TestCase(
        name="IgnoreIncorrectStampHeightGeometryRule",
        code='#import "lib.typ": *\n#assert-stamp-geometry((10mm, 20mm), (5mm, 5mm), 30mm, 15mm, "BadHeightStamp", ignore-rules: "gost-2.104-2006-stamp-height")\n[OK]'
    )
]

if __name__ == "__main__":
    passed, failed = run_test_suite(SUITE_ID, SUITE_NAME, tests)
    if failed > 0: exit(1)