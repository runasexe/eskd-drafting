from core import TestCase, run_test_suite

SUITE_ID = "CapacityOverflow"
SUITE_NAME = "Контроль физической вместимости граф штампа (ГОСТ 2.104-2006)"

# Источники нормативных значений:
# - ГОСТ 2.104-2006 (п. 5.1):
#   - Форма 1 содержит ровно 6 строк подписей граф 10–13 (высота 30 мм, 6 строк по 5 мм).
#     Передача 7 и более строк приводит к потере данных (gost-2.104-2006-members-overflow).
#   - Форма 2 и Форма 2 с шапкой содержания содержат ровно 5 строк подписей (высота 25 мм, 5 строк по 5 мм).
#     Передача 6 и более строк приводит к потере данных (gost-2.104-2006-members-overflow).
#   - Стандартный угловой штамп листа содержит 1 строку текущего изменения (графы 14–18).
#     Попытка передать большее количество записей без специализированного штампа приводит
#     к потере данных (gost-2.104-2006-changes-overflow).

tests = [
    TestCase(
        name="AllowMembersWithinCapacityForm1",
        code='''#import "lib.typ": *
#show: eskd-document.with(
  paper: "a4",
  members: (
    ("Разраб.", "Иванов", "01.09.26"),
    ("Пров.", "Петров", "02.09.26"),
    ("Т.контр.", "Сидоров", "03.09.26"),
    (),
    ("Н.контр.", "Кузнецов", "04.09.26"),
    ("Утв.", "Смирнов", "05.09.26"),
  ),
  code: [АБВГ.100200.001],
)
#show: page-first-form1
[]'''
    ),
    TestCase(
        name="ForbidMembersOverflowForm1",
        code='''#import "lib.typ": *
#show: eskd-document.with(
  paper: "a4",
  members: (
    ("Разраб.", "Иванов", "01.09.26"),
    ("Пров.", "Петров", "02.09.26"),
    ("Т.контр.", "Сидоров", "03.09.26"),
    (),
    ("Н.контр.", "Кузнецов", "04.09.26"),
    ("Утв.", "Смирнов", "05.09.26"),
    ("Лишний", "Седьмой", "06.09.26"),
  ),
  code: [АБВГ.100200.001],
)
#show: page-first-form1
[]''',
        expect_error="gost-2.104-2006-members-overflow"
    ),
    TestCase(
        name="IgnoreMembersOverflowForm1Rule",
        code='''#import "lib.typ": *
#show: eskd-document.with(
  paper: "a4",
  members: (
    ("Разраб.", "Иванов", "01.09.26"),
    ("Пров.", "Петров", "02.09.26"),
    ("Т.контр.", "Сидоров", "03.09.26"),
    (),
    ("Н.контр.", "Кузнецов", "04.09.26"),
    ("Утв.", "Смирнов", "05.09.26"),
    ("Лишний", "Седьмой", "06.09.26"),
  ),
  code: [АБВГ.100200.001],
  ignore-rules: "gost-2.104-2006-members-overflow",
)
#show: page-first-form1
[]'''
    ),
    TestCase(
        name="AllowMembersWithinCapacityForm2",
        code='''#import "lib.typ": *
#show: eskd-document.with(
  paper: "a4",
  members: (
    ("Разраб.", "Иванов", "01.09.26"),
    ("Пров.", "Петров", "02.09.26"),
    ("Т.контр.", "Сидоров", "03.09.26"),
    ("Н.контр.", "Кузнецов", "04.09.26"),
    ("Утв.", "Смирнов", "05.09.26"),
  ),
  code: [АБВГ.100200.001РЭ],
)
#show: page-first-form2
[]'''
    ),
    TestCase(
        name="ForbidMembersOverflowForm2",
        code='''#import "lib.typ": *
#show: eskd-document.with(
  paper: "a4",
  members: (
    ("Разраб.", "Иванов", "01.09.26"),
    ("Пров.", "Петров", "02.09.26"),
    ("Т.контр.", "Сидоров", "03.09.26"),
    (),
    ("Н.контр.", "Кузнецов", "04.09.26"),
    ("Утв.", "Смирнов", "05.09.26"),
  ),
  code: [АБВГ.100200.001РЭ],
)
#show: page-first-form2
[]''',
        expect_error="gost-2.104-2006-members-overflow"
    ),
    TestCase(
        name="AllowChangesWithinCapacityForm1",
        code='''#import "lib.typ": *
#show: eskd-document.with(
  paper: "a4",
  changes: (
    (num: [1], doc: [ИИ-100], date: [01.09.26]),
    (num: [2], doc: [ИИ-101], date: [02.09.26]),
    (num: [3], doc: [ИИ-102], date: [03.09.26]),
    (num: [4], doc: [ИИ-103], date: [04.09.26]),
  ),
  code: [АБВГ.100200.001],
)
#show: page-first-form1
[]'''
    ),
    TestCase(
        name="ForbidChangesOverflowForm1",
        code='''#import "lib.typ": *
#show: eskd-document.with(
  paper: "a4",
  changes: (
    (num: [1], doc: [ИИ-100], date: [01.09.26]),
    (num: [2], doc: [ИИ-101], date: [02.09.26]),
    (num: [3], doc: [ИИ-102], date: [03.09.26]),
    (num: [4], doc: [ИИ-103], date: [04.09.26]),
    (num: [5], doc: [ИИ-104], date: [05.09.26]),
  ),
  code: [АБВГ.100200.001],
)
#show: page-first-form1
[]''',
        expect_error="gost-2.104-2006-changes-overflow"
    ),
    TestCase(
        name="AllowChangesWithinCapacityForm2",
        code='''#import "lib.typ": *
#show: eskd-document.with(
  paper: "a4",
  changes: (
    (num: [1], doc: [ИИ-100], date: [01.09.26]),
    (num: [2], doc: [ИИ-101], date: [02.09.26]),
  ),
  code: [АБВГ.100200.001РЭ],
)
#show: page-first-form2
[]'''
    ),
    TestCase(
        name="ForbidChangesOverflowForm2",
        code='''#import "lib.typ": *
#show: eskd-document.with(
  paper: "a4",
  changes: (
    (num: [1], doc: [ИИ-100], date: [01.09.26]),
    (num: [2], doc: [ИИ-101], date: [02.09.26]),
    (num: [3], doc: [ИИ-102], date: [03.09.26]),
  ),
  code: [АБВГ.100200.001РЭ],
)
#show: page-first-form2
[]''',
        expect_error="gost-2.104-2006-changes-overflow"
    ),
    TestCase(
        name="ForbidChangesOverflowForm2a",
        code='''#import "lib.typ": *
#show: eskd-document.with(
  paper: "a4",
  changes: (
    (num: [1], doc: [ИИ-100], date: [01.09.26]),
    (num: [2], doc: [ИИ-101], date: [02.09.26]),
  ),
  code: [АБВГ.100200.001РЭ],
)
#show: page-body
[]''',
        expect_error="gost-2.104-2006-changes-overflow"
    ),
    TestCase(
        name="IgnoreChangesOverflowRule",
        code='''#import "lib.typ": *
#show: eskd-document.with(
  paper: "a4",
  changes: (
    (num: [1], doc: [ИИ-100], date: [01.09.26]),
    (num: [2], doc: [ИИ-101], date: [02.09.26]),
  ),
  code: [АБВГ.100200.001РЭ],
  ignore-rules: "gost-2.104-2006-changes-overflow",
)
#show: page-body
[]'''
    ),
]

if __name__ == "__main__":
    passed, failed = run_test_suite(SUITE_ID, SUITE_NAME, tests)
    if failed > 0: exit(1)
