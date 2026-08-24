from core import (
    TestCase,
    run_test_suite,
    collect_rectangles_and_groups,
    assert_element_at_position,
    check_svg_text_in_rect,
)

SUITE_ID = "SvgForm1InternalCells"
SUITE_NAME = "Внутренняя геометрия и отображение данных в графах Формы 1 (ГОСТ 2.104-2006)"

X0, Y0 = 20.0, 237.0
FORM1_CELLS = {
    "Cell_2_DocCode":      (X0 + 65.0,  Y0 + 0.0,   120.0, 15.0),
    "Cell_1_DocName":      (X0 + 65.0,  Y0 + 15.0,  70.0,  25.0),
    "Cell_3_Material":     (X0 + 65.0,  Y0 + 40.0,  70.0,  15.0),
    "Cell_4_Litera_Block": (X0 + 135.0, Y0 + 15.0,  15.0,  20.0),
    "Cell_5_Mass":         (X0 + 150.0, Y0 + 15.0,  17.0,  20.0),
    "Cell_6_Scale":        (X0 + 167.0, Y0 + 15.0,  18.0,  20.0),
    "Cell_7_Sheet":        (X0 + 135.0, Y0 + 35.0,  20.0,  5.0),
    "Cell_8_SheetsTotal":  (X0 + 155.0, Y0 + 35.0,  30.0,  5.0),
    "Cell_9_Organization": (X0 + 135.0, Y0 + 40.0,  50.0,  15.0),
}

def validate_all_cells(svg_str: str):
    lines = collect_rectangles_and_groups(svg_str)
    for cell_id, (x, y, w, h) in FORM1_CELLS.items():
        assert_element_at_position(lines, x, y, w, h, cell_id)

def validate_field_values(svg_str: str):
    # Cell 2: Обозначение документа (X=85..205 mm, Y=237..252 mm)
    c2 = FORM1_CELLS["Cell_2_DocCode"]
    assert check_svg_text_in_rect(svg_str, c2[0], c2[1], c2[2], c2[3], min_glyphs=8), "Обозначение документа (Графа 2) не найдено в SVG"
    # Cell 1: Наименование (X=85..155 mm, Y=252..277 mm)
    c1 = FORM1_CELLS["Cell_1_DocName"]
    assert check_svg_text_in_rect(svg_str, c1[0], c1[1], c1[2], c1[3], min_glyphs=6), "Наименование (Графа 1) не найдено в SVG"
    # Cell 4: Литера (X=155..170 mm, Y=252..272 mm)
    c4 = FORM1_CELLS["Cell_4_Litera_Block"]
    assert check_svg_text_in_rect(svg_str, c4[0], c4[1], c4[2], c4[3], min_glyphs=2), "Литера (Графа 4) не найдена в SVG"
    # Cell 5: Масса (X=170..187 mm, Y=252..272 mm)
    c5 = FORM1_CELLS["Cell_5_Mass"]
    assert check_svg_text_in_rect(svg_str, c5[0], c5[1], c5[2], c5[3], min_glyphs=3), "Масса (Графа 5) не найдена в SVG"
    # Cell 6: Масштаб (X=187..205 mm, Y=252..272 mm)
    c6 = FORM1_CELLS["Cell_6_Scale"]
    assert check_svg_text_in_rect(svg_str, c6[0], c6[1], c6[2], c6[3], min_glyphs=3), "Масштаб (Графа 6) не найден в SVG"
    # Cell 9: Организация (X=155..205 mm, Y=277..292 mm)
    c9 = FORM1_CELLS["Cell_9_Organization"]
    assert check_svg_text_in_rect(svg_str, c9[0], c9[1], c9[2], c9[3], min_glyphs=5), "Организация (Графа 9) не найдена в SVG"

def validate_field_suppression(svg_str: str):
    # При lit: none, mass: none, scale: none в области значений (y + 5 мм..y + 20 мм) не должно быть текста
    c4 = FORM1_CELLS["Cell_4_Litera_Block"]
    c5 = FORM1_CELLS["Cell_5_Mass"]
    c6 = FORM1_CELLS["Cell_6_Scale"]
    c2 = FORM1_CELLS["Cell_2_DocCode"]
    assert not check_svg_text_in_rect(svg_str, c4[0], c4[1] + 5.0, c4[2], c4[3] - 5.0, min_glyphs=1, margin_mm=0.5), "Литера не должна отображаться при lit: none"
    assert not check_svg_text_in_rect(svg_str, c5[0], c5[1] + 5.0, c5[2], c5[3] - 5.0, min_glyphs=1, margin_mm=0.5), "Масса не должна отображаться при mass: none"
    assert not check_svg_text_in_rect(svg_str, c6[0], c6[1] + 5.0, c6[2], c6[3] - 5.0, min_glyphs=1, margin_mm=0.5), "Масштаб не должен отображаться при scale: none"
    # При этом Графа 2 (code) присутствует
    assert check_svg_text_in_rect(svg_str, c2[0], c2[1], c2[2], c2[3], min_glyphs=8), "Обозначение документа должно присутствовать"

tests = [
    TestCase(
        name="ValidateAllForm1CellsGeometry",
        format="svg",
        code='''#import "lib.typ": *\n#show: eskd-document.with(paper: "a4", code: [АБВГ.100200.001])\n#show: page-first-form1\n[]''',
        validator=validate_all_cells
    ),
    TestCase(
        name="ValidateForm1FieldValuesInSvg",
        format="svg",
        code='''#import "lib.typ": *
#show: eskd-document.with(
  paper: "a4",
  code: [АБВГ.123456.001],
  name: [Вал привода],
  org: [КБ Радуга],
  lit: [О1],
  mass: [2,5],
  scale: [1:2],
)
#show: page-first-form1
[OK]''',
        validator=validate_field_values
    ),
    TestCase(
        name="ValidateForm1FieldSuppressionInSvg",
        format="svg",
        code='''#import "lib.typ": *
#show: eskd-document.with(
  paper: "a4",
  code: [АБВГ.123456.001],
  name: [Вал привода],
  lit: none,
  mass: none,
  scale: none,
)
#show: page-first-form1
[OK]''',
        validator=validate_field_suppression
    ),
]

if __name__ == "__main__":
    passed, failed = run_test_suite(SUITE_ID, SUITE_NAME, tests)
    if failed > 0: exit(1)