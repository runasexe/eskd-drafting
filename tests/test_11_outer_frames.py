from core import TestCase, run_test_suite, parse_svg_dimensions, collect_rectangles_and_groups, assert_element_at_position

SUITE_ID = "SvgOuterFrames"
SUITE_NAME = "Эталонная геометрия внешней рамки листа (ГОСТ 2.301 / 2.104)"

FORMATS = {
    "A4_Portrait": ("a4", "portrait", 210.0, 297.0),
    "A3_Landscape": ("a3", "landscape", 420.0, 297.0),
    "A3_Portrait": ("a3", "portrait", 297.0, 420.0),
    "A2_Landscape": ("a2", "landscape", 594.0, 420.0),
    "A2_Portrait": ("a2", "portrait", 420.0, 594.0),
    "A1_Landscape": ("a1", "landscape", 841.0, 594.0),
    "A1_Portrait": ("a1", "portrait", 594.0, 841.0),
    "A0_Landscape": ("a0", "landscape", 1189.0, 841.0),
    "A0_Portrait": ("a0", "portrait", 841.0, 1189.0),
}

def make_frame_validator(expected_w: float, expected_h: float, name: str):
    def validator(svg_str: str):
        sheet_w, sheet_h = parse_svg_dimensions(svg_str)
        assert abs(sheet_w - expected_w) < 1.0, f"Ширина {sheet_w:.1f} != {expected_w}"
        assert abs(sheet_h - expected_h) < 1.0, f"Высота {sheet_h:.1f} != {expected_h}"

        lines = collect_rectangles_and_groups(svg_str)
        expected_inner_w = expected_w - 25.0
        expected_inner_h = expected_h - 10.0

        assert_element_at_position(lines, 20.0, 5.0, expected_inner_w, expected_inner_h, f"Рамка {name}")
    return validator

tests = [
    TestCase(
        name=f"ValidateFrame_{k}",
        format="svg",
        code=f'#import "lib.typ": *\n#show: eskd-document.with(paper: "{p}", orientation: "{o}")\n#show: page-body\n[]',
        validator=make_frame_validator(ew, eh, k)
    ) for k, (p, o, ew, eh) in FORMATS.items()
]

if __name__ == "__main__":
    passed, failed = run_test_suite(SUITE_ID, SUITE_NAME, tests)
    if failed > 0: exit(1)