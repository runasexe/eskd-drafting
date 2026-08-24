from core import TestCase, run_test_suite, parse_svg_dimensions, collect_rectangles_and_groups, assert_element_at_position

SUITE_ID = "SvgMainStamps"
SUITE_NAME = "Эталонные размеры основных надписей ГОСТ 2.104-2006"

STAMPS_SPECS = [
    ("Form1_Drawings", "page-first-form1", 185.0, 55.0),
    ("Form2_FirstSheet", "page-first-form2", 185.0, 40.0),
    ("Form2a_Subsequent", "page-body", 185.0, 15.0),
    ("Form2b_DoubleSided", "page-body-double", 185.0, 15.0),
]

MULTI_FORMAT_STAMP_TESTS = [
    ("Form1_A3_Landscape", "a3", "landscape", "page-first-form1", 185.0, 55.0),
    ("Form1_A3_Portrait", "a3", "portrait", "page-first-form1", 185.0, 55.0),
    ("Form1_A2_Landscape", "a2", "landscape", "page-first-form1", 185.0, 55.0),
    ("Form1_A2_Portrait", "a2", "portrait", "page-first-form1", 185.0, 55.0),
    ("Form1_A1_Landscape", "a1", "landscape", "page-first-form1", 185.0, 55.0),
    ("Form1_A0_Landscape", "a0", "landscape", "page-first-form1", 185.0, 55.0),
    ("Form2_A3_Landscape", "a3", "landscape", "page-first-form2", 185.0, 40.0),
    ("Form2a_A2_Landscape", "a2", "landscape", "page-body", 185.0, 15.0),
    ("Form2a_A0_Landscape", "a0", "landscape", "page-body", 185.0, 15.0),
]

def make_stamp_validator(exp_w: float, exp_h: float, name: str):
    def validator(svg_str: str):
        lines = collect_rectangles_and_groups(svg_str)
        sheet_w, sheet_h = parse_svg_dimensions(svg_str)
        assert_element_at_position(lines, sheet_w - 5.0 - exp_w, sheet_h - 5.0 - exp_h, exp_w, exp_h, f"Контур {name}")
    return validator

def validate_form2_toc_geometry(svg_str: str):
    lines = collect_rectangles_and_groups(svg_str)
    sheet_w, sheet_h = parse_svg_dimensions(svg_str)
    # 1. Базовый контур Формы 2 (185 x 40 мм)
    assert_element_at_position(lines, sheet_w - 5.0 - 185.0, sheet_h - 5.0 - 40.0, 185.0, 40.0, "Контур Формы 2 в Form2_Toc")
    # 2. Контур совмещенной шапки содержания (120 x 52 мм над правой частью)
    assert_element_at_position(lines, sheet_w - 5.0 - 120.0, sheet_h - 5.0 - 52.0, 120.0, 52.0, "Контур правой части Form2_Toc")

tests = [
    TestCase(
        name=f"CheckGeometry_{name}",
        format="svg",
        code=f'#import "lib.typ": *\n#show: eskd-document.with(paper: "a4", orientation: "portrait")\n#show: {preset}\n[]',
        validator=make_stamp_validator(exp_w, exp_h, name)
    ) for name, preset, exp_w, exp_h in STAMPS_SPECS
] + [
    TestCase(
        name="CheckGeometry_Form2_Toc",
        format="svg",
        code='''#import "lib.typ": *
#show: eskd-document.with(
  paper: "a4",
  orientation: "portrait",
)
#show: page-first-form2.with(
  toc: (num: [1], name: [Текст], code: [АБВГ], note: [Прим]),
)
[]''',
        validator=validate_form2_toc_geometry
    )
] + [
    TestCase(
        name=f"CheckMultiFormat_{name}",
        format="svg",
        code=f'#import "lib.typ": *\n#show: eskd-document.with(paper: "{paper}", orientation: "{orient}")\n#show: {preset}\n[]',
        validator=make_stamp_validator(exp_w, exp_h, name)
    ) for name, paper, orient, preset, exp_w, exp_h in MULTI_FORMAT_STAMP_TESTS
]

if __name__ == "__main__":
    passed, failed = run_test_suite(SUITE_ID, SUITE_NAME, tests)
    if failed > 0: exit(1)