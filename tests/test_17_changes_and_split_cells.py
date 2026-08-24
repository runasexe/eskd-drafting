from core import TestCase, run_test_suite, collect_rectangles_and_groups, assert_element_at_position

SUITE_ID = "SvgChangesTableAndSplitCells"
SUITE_NAME = "Детальная сетка таблицы изменений (графы 14-18, ГОСТ 2.104-2006)"

# Источники нормативных значений:
# - ГОСТ 2.104-2006 (п. 5.1, Форма 2а):
#   - Положение штампа: X0 = 20.0 мм (отступ подшивки), Y0 = 297 - 5 - 15 = 277.0 мм на листе А4.
#   - Графа 14 («Изм.»): 7.0 мм.
#   - Графа 15 («Лист»): 10.0 мм.
#   - Графа 16 («№ докум.»): 23.0 мм.
#   - Графа 17 («Подп.»): 15.0 мм.
#   - Графа 18 («Дата»): 10.0 мм.
#   - Графа 2 («Обозначение»): 110.0 мм.
#   - Графа 7 («Лист»): 10.0 мм.
#   - Сумма ширин: 7 + 10 + 23 + 15 + 10 + 110 + 10 = 185.0 мм, высота = 15.0 мм.

X0_2A, Y0_2A = 20.0, 277.0

CHANGES_COLUMNS_2A = {
    "Change_Col_Num":   (X0_2A + 0.0,  Y0_2A, 7.0,  15.0),
    "Change_Col_Sheet": (X0_2A + 7.0,  Y0_2A, 10.0, 15.0),
    "Change_Col_Doc":   (X0_2A + 17.0, Y0_2A, 23.0, 15.0),
    "Change_Col_Sign":  (X0_2A + 40.0, Y0_2A, 15.0, 15.0),
    "Change_Col_Date":  (X0_2A + 55.0, Y0_2A, 10.0, 15.0),
    "Main_Col_Code":    (X0_2A + 65.0, Y0_2A, 110.0, 15.0),
    "Sheet_Num_Total":  (X0_2A + 175.0, Y0_2A, 10.0, 15.0),
}

def validate_changes_table(svg_str: str):
    boxes = collect_rectangles_and_groups(svg_str)
    for cell_id, (x, y, w, h) in CHANGES_COLUMNS_2A.items():
        assert_element_at_position(boxes, x, y, w, h, cell_id)

tests = [
    TestCase(
        name="Form2a_ChangesArray",
        format="svg",
        code='''#import "lib.typ": *
#show: eskd-document.with(paper: "a4", changes: ((num: [1], doc: [ИИ-100], date: [01.09.26]),))
#show: page-body
[]''',
        validator=validate_changes_table
    ),
    TestCase(
        name="Form2a_ChangesObjectArrayWithSizes",
        format="svg",
        code='''#import "lib.typ": *
#show: eskd-document.with(
  paper: "a4",
  changes: (
    (
      num: [1],
      sheet: [Зам.],
      doc: [ИИ.102-2026],
      sig: [Иванов],
      date: [01.09.26],
      doc-size: h2_5,
      sig-size: h2_5,
    ),
  ),
)
#show: page-body
[]''',
        validator=validate_changes_table
    ),
    TestCase(
        name="ForbidInvalidChangeFontSize",
        code='''#import "lib.typ": *
#show: eskd-document.with(
  paper: "a4",
  changes: ((num: [1], doc: [ИИ-100], doc-size: 4.2mm),),
)
#show: page-body
[]''',
        expect_error="gost-2.304-81-font-height"
    ),
    TestCase(
        name="Form1_MultiRowChangesHarmonization",
        code='''#import "lib.typ": *
#show: eskd-document.with(
  paper: "a4",
  changes: (
    (num: [1], sheet: [Зам.], doc: [ИИ.102-2026], sig: [Иванов], date: [01.09.26]),
    (num: [2], sheet: [Нов.], doc: [ИИ.145-2026], sig: [Смирнов], date: [15.10.26]),
  ),
  code: [АБВГ.100200.001],
)
#show: page-first-form1
[]'''
    ),
    TestCase(
        name="Form2_MultiRowChangesHarmonization",
        code='''#import "lib.typ": *
#show: eskd-document.with(
  paper: "a4",
  changes: (
    (num: [1], sheet: [Зам.], doc: [ИИ.102-2026], sig: [Иванов], date: [01.09.26]),
    (num: [2], sheet: [Нов.], doc: [ИИ.145-2026], sig: [Петров], date: [15.10.26]),
  ),
  code: [АБВГ.100200.001РЭ],
)
#show: page-first-form2
[]'''
    ),
]

if __name__ == "__main__":
    passed, failed = run_test_suite(SUITE_ID, SUITE_NAME, tests)
    if failed > 0: exit(1)