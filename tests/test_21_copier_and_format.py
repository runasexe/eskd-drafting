from core import TestCase, run_test_suite, check_bottom_labels_present, check_bottom_cells_status

SUITE_ID = "CopierAndFormat"
SUITE_NAME = "Отображение и автоопределение граф 31 («Копировал») и 32 («Формат») по ГОСТ 2.104-2006"

# Правила отображения:
# 1. copier: auto, format: auto -> оба поля активны («Копировал», «Формат <бумага>»).
# 2. copier: none, format: auto -> поле format отображается («Формат <бумага>»), copier скрыт.
# 3. copier: auto, format: none (или false) -> поле copier отображается («Копировал»), format скрыт.
# 4. copier: none, format: none (или false) -> оба поля не отображаются.
# 5. copier: boolean (true/false) -> недопустимо (ошибка).
# 6. format: true -> принудительно включает с параметрами бумаги; false -> скрывает (действует как none); str/content -> переопределяет текст.

def validate_both_labels_a4(svg_str: str):
    copier, fmt = check_bottom_cells_status(svg_str, 297.0)
    assert copier, "Графа 31 («Копировал») должна отображаться"
    assert fmt, "Графа 32 («Формат») должна отображаться"
    assert check_bottom_labels_present(svg_str, 20.0, 297.0), "Графы должны быть на позициях внизу листа А4"

def validate_both_labels_a4x3(svg_str: str):
    copier, fmt = check_bottom_cells_status(svg_str, 297.0)
    assert copier, "Графа 31 («Копировал») должна отображаться"
    assert fmt, "Графа 32 («Формат») должна отображаться"
    assert check_bottom_labels_present(svg_str, 440.0, 297.0), "Графы должны быть на позициях внизу листа А4х3"

def validate_only_format_visible(svg_str: str):
    copier, fmt = check_bottom_cells_status(svg_str, 297.0)
    assert not copier, "Графа 31 («Копировал») должна быть скрыта"
    assert fmt, "Графа 32 («Формат») должна отображаться"

def validate_only_copier_visible(svg_str: str):
    copier, fmt = check_bottom_cells_status(svg_str, 297.0)
    assert copier, "Графа 31 («Копировал») должна отображаться"
    assert not fmt, "Графа 32 («Формат») должна быть скрыта"

def validate_neither_visible(svg_str: str):
    copier, fmt = check_bottom_cells_status(svg_str, 297.0)
    assert not copier, "Графа 31 («Копировал») не должна отображаться"
    assert not fmt, "Графа 32 («Формат») не должна отображаться"
    assert not check_bottom_labels_present(svg_str, 20.0, 297.0), "Графы 31 и 32 не должны выводиться"

tests = [
    # 1. copier: auto, format: auto -> оба поля активны
    TestCase(
        name="DefaultAutoBothEnabled_A4",
        format="svg",
        code='#import "lib.typ": *\n#show: eskd-document.with(paper: "a4")\n#show: page-body\n[OK]',
        validator=validate_both_labels_a4
    ),
    TestCase(
        name="DefaultAutoBothEnabled_A4x3",
        format="svg",
        code='#import "lib.typ": *\n#show: eskd-document.with(paper: "a4x3")\n#show: page-first-form1\n[OK]',
        validator=validate_both_labels_a4x3
    ),

    # 2. copier: none, format: auto -> поле format отображается
    TestCase(
        name="CopierNoneFormatAuto",
        format="svg",
        code='#import "lib.typ": *\n#show: eskd-document.with(paper: "a4", copier: none, format: auto)\n#show: page-body\n[OK]',
        validator=validate_only_format_visible
    ),

    # 3. copier: auto, format: none (или false) -> поле copier отображается
    TestCase(
        name="CopierAutoFormatNone",
        format="svg",
        code='#import "lib.typ": *\n#show: eskd-document.with(paper: "a4", copier: auto, format: none)\n#show: page-body\n[OK]',
        validator=validate_only_copier_visible
    ),
    TestCase(
        name="CopierAutoFormatFalse",
        format="svg",
        code='#import "lib.typ": *\n#show: eskd-document.with(paper: "a4", copier: auto, format: false)\n#show: page-body\n[OK]',
        validator=validate_only_copier_visible
    ),

    # 4. copier: none, format: none (или false) -> оба поля не отображаются
    TestCase(
        name="BothNone_NeitherVisible",
        format="svg",
        code='#import "lib.typ": *\n#show: eskd-document.with(paper: "a4", copier: none, format: none)\n#show: page-body\n[OK]',
        validator=validate_neither_visible
    ),
    TestCase(
        name="BothNoneAndFalse_NeitherVisible",
        format="svg",
        code='#import "lib.typ": *\n#show: eskd-document.with(paper: "a4", copier: none, format: false)\n#show: page-body\n[OK]',
        validator=validate_neither_visible
    ),

    # 5. Запрет boolean (true/false) для copier
    TestCase(
        name="ForbidCopierBooleanTrue",
        code='#import "lib.typ": *\n#show: eskd-document.with(paper: "a4", copier: true)\n#show: page-body\n[]',
        expect_error="не может быть boolean"
    ),
    TestCase(
        name="ForbidCopierBooleanFalse",
        code='#import "lib.typ": *\n#show: eskd-document.with(paper: "a4", copier: false)\n#show: page-body\n[]',
        expect_error="не может быть boolean"
    ),

    # 6. Пользовательские значения (str / content / true)
    TestCase(
        name="AllowCustomCopierAndFormatTrue",
        format="svg",
        code='#import "lib.typ": *\n#show: eskd-document.with(paper: "a4", copier: [Федоров], format: true)\n#show: page-body\n[OK]',
        validator=lambda svg: check_bottom_cells_status(svg)[0] and check_bottom_cells_status(svg)[1]
    ),
    TestCase(
        name="AllowCustomCopierFormatNone",
        format="svg",
        code='#import "lib.typ": *\n#show: eskd-document.with(paper: "a4", copier: [Федоров], format: none)\n#show: page-body\n[OK]',
        validator=lambda svg: check_bottom_cells_status(svg)[0] and not check_bottom_cells_status(svg)[1]
    ),
    TestCase(
        name="AllowCustomFormatCopierNone",
        format="svg",
        code='#import "lib.typ": *\n#show: eskd-document.with(paper: "a4", copier: none, format: [А4х3])\n#show: page-body\n[OK]',
        validator=lambda svg: not check_bottom_cells_status(svg)[0] and check_bottom_cells_status(svg)[1]
    ),

    # 7. Смешанный документ (А4 + складная вклейка А4х3)
    TestCase(
        name="MixedDocumentA4AndA4x3Insert",
        code='''#import "lib.typ": *
#show: eskd-document.with(
  paper: "a4",
  code: [АБВГ.123456.001ПЗ],
)
#show: page-first-form2
[Текст на А4]

#eskd-page(paper: "a4x3", bottom: frame-form-2a)[
  [Широкая таблица на А4х3]
]
'''
    ),
]

if __name__ == "__main__":
    passed, failed = run_test_suite(SUITE_ID, SUITE_NAME, tests)
    if failed > 0: exit(1)
