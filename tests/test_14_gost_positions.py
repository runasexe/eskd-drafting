from core import TestCase, run_test_suite, collect_rectangles_and_groups, assert_element_at_position, assert_box26_present

SUITE_ID = "SvgExactPositioning"
SUITE_NAME = "Абсолютное позиционирование элементов ЕСКД по ГОСТ 2.104 и 2.301"

SHEET_FORMATS = [
    ("A4_Portrait", "a4", "portrait", 210.0, 297.0),
    ("A3_Landscape", "a3", "landscape", 420.0, 297.0),
    ("A3_Portrait", "a3", "portrait", 297.0, 420.0),
    ("A2_Landscape", "a2", "landscape", 594.0, 420.0),
    ("A2_Portrait", "a2", "portrait", 420.0, 594.0),
    ("A1_Landscape", "a1", "landscape", 841.0, 594.0),
    ("A1_Portrait", "a1", "portrait", 594.0, 841.0),
    ("A0_Landscape", "a0", "landscape", 1189.0, 841.0),
    ("A0_Portrait", "a0", "portrait", 841.0, 1189.0),
    ("A4x3_Multiplied", "a4x3", "landscape", 630.0, 297.0),
    ("A4x4_Multiplied", "a4x4", "landscape", 841.0, 297.0),
    ("A3x3_Multiplied", "a3x3", "landscape", 891.0, 420.0),
    ("A3x4_Multiplied", "a3x4", "landscape", 1189.0, 420.0),
    ("A2x3_Multiplied", "a2x3", "landscape", 1261.0, 594.0),
]

def make_position_validator(w: float, h: float, name: str):
    def validator(svg_str: str):
        lines = collect_rectangles_and_groups(svg_str)
        # Внешняя рабочая рамка листа: отступ 20 мм слева, по 5 мм сверху/снизу/справа
        assert_element_at_position(lines, 20.0, 5.0, w - 25.0, h - 10.0, f"Внешняя рамка {name}")
        # Графа 26 строго 70x14 мм в левом верхнем углу (20, 5)
        assert_box26_present(svg_str, exp_x=20.0, exp_y=5.0, exp_w=70.0, exp_h=14.0)
    return validator

tests = [
    TestCase(
        name=f"CheckFrameAndBox26_{fmt_id}",
        format="svg",
        code=f'''#import "lib.typ": *
#show: eskd-document.with(paper: "{paper}", orientation: "{orient}", code: [ЯЯЯЯ.123456.001], code-inverted: auto)
#show: page-first-form1
[]''',
        validator=make_position_validator(exp_w, exp_h, fmt_id)
    ) for fmt_id, paper, orient, exp_w, exp_h in SHEET_FORMATS
]

if __name__ == "__main__":
    passed, failed = run_test_suite(SUITE_ID, SUITE_NAME, tests)
    if failed > 0: exit(1)
