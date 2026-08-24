import xml.etree.ElementTree as ET
from core import TestCase, run_test_suite

SUITE_ID = "SvgLinesAndColors"
SUITE_NAME = "Цвет и толщина линий рамок (ГОСТ 2.303)"

def validate_gost_lines(svg_str: str):
    root = ET.fromstring(svg_str)

    # 0.8 мм и 0.35 мм в пунктах Typst
    main_pt = 0.8 * 72.0 / 25.4
    sec_pt = 0.35 * 72.0 / 25.4

    has_main = False
    has_sec = False

    for el in root.iter():
        if el.tag.endswith("path") or el.tag.endswith("rect") or el.tag.endswith("line"):
            stroke = el.attrib.get("stroke")
            stroke_width = el.attrib.get("stroke-width")

            if not stroke or stroke == "none":
                continue

            assert stroke.lower() == "#000000", f"Цвет линии должен быть #000000, получен {stroke}"

            if stroke_width:
                w_pt = float(stroke_width.replace("pt", ""))
                is_main = abs(w_pt - main_pt) < 0.05
                is_sec = abs(w_pt - sec_pt) < 0.05

                assert is_main or is_sec, (
                    f"Нестандартная толщина линии: {w_pt:.3f} pt ({(w_pt * 25.4 / 72.0):.2f} мм). "
                    f"ГОСТ 2.303 разрешает строго основные (0.8 мм) и вспомогательные (0.35 мм) линии."
                )

                if is_main: has_main = True
                if is_sec: has_sec = True

    assert has_main and has_sec, "В документе должны присутствовать как основные (0.8 мм), так и вспомогательные (0.35 мм) линии"

tests = [
    TestCase(
        name="ValidateIndustryPresetStrokes",
        format="svg",
        code='''#import "lib.typ": *
#show: eskd-document.with(paper: "a4", preset-lines: "industry")
#show: page-first-form1
[]''',
        validator=validate_gost_lines
    ),
    TestCase(
        name="ValidateGostPresetStrokes",
        format="svg",
        code='''#import "lib.typ": *
#show: eskd-document.with(paper: "a4", preset-lines: "gost")
#show: page-first-form1
[]''',
        validator=validate_gost_lines
    )
]

if __name__ == "__main__":
    passed, failed = run_test_suite(SUITE_ID, SUITE_NAME, tests)
    if failed > 0: exit(1)