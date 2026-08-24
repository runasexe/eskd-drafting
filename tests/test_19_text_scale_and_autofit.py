from core import TestCase, run_test_suite

SUITE_ID = "TextScaleAndAutofit"
SUITE_NAME = "Масштабирование и читаемость чертежного текста (ГОСТ 2.304-81, 2.004-88)"

# Значения для сравнения:
# - ГОСТ 2.304-81 (п. 2.1): Минимальная регламентированная высота шрифта h = 1.8 мм.
# - ГОСТ 2.004-88 (п. 1.8): Требования к читаемости надписей при автоматизированном выводе.
#   Сжатие текста scale < 70% (0.70) снижает читаемость и требует предупреждения (правило "gost-text-scale-warning").
#   Экстремальное сжатие scale < 40% (0.40) делает текст неразличимым и требует подавления обоих правил
#   ("gost-text-scale-warning" и "gost-text-scale-extreme").

tests = [
    TestCase(
        name="NormalTextFitWithoutScaling",
        code='''#import "lib.typ": *
#auto-fit-gost([Вал ступенчатый], target-h: h5_0, min-h: h1_8, max-w: 68mm, max-h: 24mm)
[OK]'''
    ),
    TestCase(
        name="ForbidUnreadableTextScaleBelow70Percent",
        code='''#import "lib.typ": *
#auto-fit-gost([Очень длинное наименование детали изделия для узкой ячейки], target-h: h3_5, min-h: h1_8, max-w: 15mm, max-h: 4.5mm, single-line: true)''',
        expect_error="gost-text-scale-warning"
    ),
    TestCase(
        name="AllowTextScaleBelow70PercentWithIgnoreRule",
        code='''#import "lib.typ": *
#auto-fit-gost([Очень длинное наименование детали изделия], target-h: h3_5, min-h: h1_8, max-w: 22mm, max-h: 4.5mm, single-line: true, ignore-rules: "gost-text-scale-warning")
[OK]'''
    ),
    TestCase(
        name="ForbidExtremeTextShrinkBelow40PercentWhenOnlyWarningIgnored",
        code='''#import "lib.typ": *
#auto-fit-gost([Колоссально огромное и экстремально длинное текстовое наименование для микроскопической ячейки], target-h: h3_5, min-h: h1_8, max-w: 10mm, max-h: 4.5mm, single-line: true, ignore-rules: "gost-text-scale-warning")''',
        expect_error="gost-text-scale-extreme"
    ),
    TestCase(
        name="ForbidExtremeTextShrinkBelow40PercentWhenOnlyExtremeIgnored",
        code='''#import "lib.typ": *
#auto-fit-gost([Колоссально огромное и экстремально длинное текстовое наименование для микроскопической ячейки], target-h: h3_5, min-h: h1_8, max-w: 10mm, max-h: 4.5mm, single-line: true, ignore-rules: "gost-text-scale-extreme")''',
        expect_error="gost-text-scale-warning"
    ),
    TestCase(
        name="AllowExtremeTextShrinkWhenBothRulesIgnored",
        code='''#import "lib.typ": *
#auto-fit-gost([Колоссально огромное и экстремально длинное текстовое наименование для микроскопической ячейки], target-h: h3_5, min-h: h1_8, max-w: 10mm, max-h: 4.5mm, single-line: true, ignore-rules: ("gost-text-scale-warning", "gost-text-scale-extreme"))
[OK]'''
    ),
    TestCase(
        name="AllowExtremeTextShrinkWithWildcardIgnore",
        code='''#import "lib.typ": *
#auto-fit-gost([Колоссально огромное и экстремально длинное текстовое наименование для микроскопической ячейки], target-h: h3_5, min-h: h1_8, max-w: 10mm, max-h: 4.5mm, single-line: true, ignore-rules: "*")
[OK]'''
    )
]

if __name__ == "__main__":
    passed, failed = run_test_suite(SUITE_ID, SUITE_NAME, tests)
    if failed > 0: exit(1)
