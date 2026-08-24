from core import TestCase, run_test_suite, collect_rectangles_and_groups, assert_element_at_position

SUITE_ID = "SvgOtherFormsInternalCells"
SUITE_NAME = "Внутренняя геометрия Форм 2 (с toc и без), 2а и 2б (ГОСТ 2.104)"

def validate_form2a(svg_str: str):
    lines = collect_rectangles_and_groups(svg_str)
    # Широкая графа "Обозначение документа" (110 мм)
    assert_element_at_position(lines, 85.0, 277.0, 110.0, 15.0, "Графа Код 2a")
    # Графа "Лист" (10 мм)
    assert_element_at_position(lines, 195.0, 277.0, 10.0, 15.0, "Графа Лист 2a")

def validate_form2b(svg_str: str):
    lines = collect_rectangles_and_groups(svg_str)
    # Зеркальная форма 2б: Код начинается с X=20+10=30
    assert_element_at_position(lines, 30.0, 277.0, 110.0, 15.0, "Графа Код 2б")

def validate_form2_toc(svg_str: str):
    lines = collect_rectangles_and_groups(svg_str)
    # Форма 2 с toc: верхний ярус шапки 12 мм над правой частью 120 мм (X=85..205, Y=240..252)
    assert_element_at_position(lines, 85.0, 240.0, 120.0, 52.0, "Внешний контур правой части Формы 2 с toc")

tests = [
    TestCase(
        name="ValidateForm2a_CodeAndSheetCells",
        format="svg",
        code='''#import "lib.typ": *\n#show: eskd-document.with(paper: "a4")\n#show: page-body\n[]''',
        validator=validate_form2a
    ),
    TestCase(
        name="ValidateForm2b_MirroredCells",
        format="svg",
        code='''#import "lib.typ": *\n#show: eskd-document.with(paper: "a4")\n#show: page-body-double\n[]''',
        validator=validate_form2b
    ),
    TestCase(
        name="ValidateForm2Toc_DefaultDict",
        format="svg",
        code='''#import "lib.typ": *
#show: eskd-document.with(paper: "a4")
#show: page-first-form2.with(
  toc: (
    num: [№],
    name: [Наименование],
    code: [Обозначение],
    note: [Примечание],
  ),
)
[]''',
        validator=validate_form2_toc
    ),
    TestCase(
        name="ValidateForm2Toc_PartialDict",
        format="svg",
        code='''#import "lib.typ": *
#show: eskd-document.with(paper: "a4")
#show: page-first-form2.with(
  toc: (
    num: [1],
    name: [Введение],
  ),
)
[]''',
        validator=validate_form2_toc
    ),
    TestCase(
        name="ValidateForm2Toc_ArrayFormat",
        format="svg",
        code='''#import "lib.typ": *
#show: eskd-document.with(paper: "a4")
#show: page-first-form2.with(
  toc: ([№], [Наименование], [Обозначение], [Примечание]),
)
[]''',
        validator=validate_form2_toc
    ),
    TestCase(
        name="ValidateForm2_PageFirstForm2WithTocParam",
        format="svg",
        code='''#import "lib.typ": *
#show: eskd-document.with(
  paper: "a4",
)
#show: page-first-form2.with(
  toc: (num: [1], name: [Текст]),
)
[]''',
        validator=validate_form2_toc
    ),
    TestCase(
        name="ForbidTocInForm1",
        format="svg",
        code='''#import "lib.typ": *
#frame-form-1(toc: (num: [1], name: [Текст]))
[]''',
        expect_error="gost-2.104-2006-toc-unsupported"
    ),
    TestCase(
        name="ForbidTocInForm2a",
        format="svg",
        code='''#import "lib.typ": *
#frame-form-2a(toc: (num: [1], name: [Текст]))
[]''',
        expect_error="gost-2.104-2006-toc-unsupported"
    ),
    TestCase(
        name="ForbidTocInForm2b",
        format="svg",
        code='''#import "lib.typ": *
#frame-form-2b(toc: (num: [1], name: [Текст]))
[]''',
        expect_error="gost-2.104-2006-toc-unsupported"
    ),
    TestCase(
        name="AllowNoneTocInForm1",
        format="svg",
        code='''#import "lib.typ": *
#frame-form-1(toc: none)
[]'''
    ),
    TestCase(
        name="AllowAutoTocInForm1",
        format="svg",
        code='''#import "lib.typ": *
#frame-form-1(toc: auto)
[]'''
    ),
    TestCase(
        name="ValidateForm2Toc_EmptyArray",
        format="svg",
        code='''#import "lib.typ": *
#show: eskd-document.with(paper: "a4")
#show: page-first-form2.with(
  toc: (),
)
[]''',
        validator=validate_form2_toc
    ),
    TestCase(
        name="ValidateForm2Toc_EmptyDict",
        format="svg",
        code='''#import "lib.typ": *
#show: eskd-document.with(paper: "a4")
#show: page-first-form2.with(
  toc: (:),
)
[]''',
        validator=validate_form2_toc
    ),
    TestCase(
        name="ForbidEmptyArrayInForm1",
        format="svg",
        code='''#import "lib.typ": *
#frame-form-1(toc: ())
[]''',
        expect_error="gost-2.104-2006-toc-unsupported"
    ),
    TestCase(
        name="ForbidEmptyDictInForm1",
        format="svg",
        code='''#import "lib.typ": *
#frame-form-1(toc: (:))
[]''',
        expect_error="gost-2.104-2006-toc-unsupported"
    ),
    TestCase(
        name="IgnoreTocInForm1",
        format="svg",
        code='''#import "lib.typ": *
#frame-form-1(toc: (num: [1]), ignore-rules: "gost-2.104-2006-toc-unsupported")
[]'''
    ),
    TestCase(
        name="IgnoreTocInForm2a",
        format="svg",
        code='''#import "lib.typ": *
#frame-form-2a(toc: (num: [1]), ignore-rules: "gost-2.104-2006-toc-unsupported")
[]'''
    ),
]

if __name__ == "__main__":
    passed, failed = run_test_suite(SUITE_ID, SUITE_NAME, tests)
    if failed > 0: exit(1)
