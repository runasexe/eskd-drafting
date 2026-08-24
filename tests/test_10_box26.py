from core import TestCase, run_test_suite

SUITE_ID = "Box26"
SUITE_NAME = "Повернутое обозначение документа (Графа 26, ГОСТ 2.104-2006, п. 4.1)"

# Источники нормативных значений:
# - ГОСТ 2.104-2006 (п. 4.1): Для чертежей и схем (Форма 1) в левом верхнем углу рабочей рамки
#   выполняется повернутое на 180 градусов обозначение документа (размеры 70 х 14 мм).
# - Параметр `code-inverted`:
#   - auto: включается автоматически для Формы 1, отключается для текстовых форм (Форма 2, 2а, 2б).
#   - none: принудительно отключает графу.
#   - content / string: выводит переданный текст (рамка рисуется по умолчанию).
#   - dictionary: гранулярная настройка (text, frame, size, min-size).

tests = [
    TestCase(
        name="RenderDocCodeInvertedAutoDrawing",
        code='''#import "lib.typ": *
#show: eskd-document.with(code: [ЯЯЯЯ.123456.001], code-inverted: auto)
#show: page-first-form1
#align(center)[Чертеж с автоматически включенным повернутым обозначением]'''
    ),
    TestCase(
        name="RenderDocCodeInvertedExplicitText",
        code='''#import "lib.typ": *
#show: eskd-document.with(code: [ЯЯЯЯ.123456.001], code-inverted: [ИНВ.26.СПЕЦ])
#show: page-first-form1
#align(center)[Чертеж с явным текстом в графе 26]'''
    ),
    TestCase(
        name="RenderDocCodeInvertedDictWithFrame",
        code='''#import "lib.typ": *
#show: eskd-document.with(code: [ЯЯЯЯ.123456.001], code-inverted: (text: [ДИКТ.123], frame: true, size: 3.5mm))
#show: page-first-form1
#align(center)[Чертеж со словарем настроек и рамкой]'''
    ),
    TestCase(
        name="RenderDocCodeInvertedDictWithoutFrame",
        code='''#import "lib.typ": *
#show: eskd-document.with(code: [ЯЯЯЯ.123456.001], code-inverted: (text: [БЕЗ.РАМКИ], frame: false, size: 3.5mm))
#show: page-first-form1
#align(center)[Чертеж со словарем настроек без рамки]'''
    ),
    TestCase(
        name="RenderDocCodeInvertedEmptyContentWithFrame",
        code='''#import "lib.typ": *
#show: eskd-document.with(code: [ЯЯЯЯ.123456.001], code-inverted: (text: [], frame: true))
#show: page-first-form1
#align(center)[Чертеж с пустой рамкой в верхнем углу]'''
    ),
    TestCase(
        name="RenderDocCodeInvertedDisabledExplicitly",
        code='''#import "lib.typ": *
#show: eskd-document.with(code: [ЯЯЯЯ.123456.001], code-inverted: none)
#show: page-first-form1
#align(center)[Чертеж с принудительно отключенным повернутым обозначением]'''
    )
]

if __name__ == "__main__":
    passed, failed = run_test_suite(SUITE_ID, SUITE_NAME, tests)
    if failed > 0: exit(1)