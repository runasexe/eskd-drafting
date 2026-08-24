from core import TestCase, run_test_suite, collect_rectangles_and_groups, assert_element_at_position, assert_box26_present

SUITE_ID = "SvgLeftStampsAndBox26"
SUITE_NAME = "Боковые штампы (графы 19-25) и Графа 26 (ГОСТ 2.104)"

tests = [
    TestCase(
        name="ValidateBox26WithDocCode_70x14mm",
        format="svg",
        code='''#import "lib.typ": *
#show: eskd-document.with(paper: "a4", code: [ЯЯЯЯ.123456.001], code-inverted: auto)
#show: page-first-form1
[]''',
        validator=lambda svg: assert_box26_present(svg, exp_x=20.0, exp_y=5.0, exp_w=70.0, exp_h=14.0, check_text=True)
    ),
    TestCase(
        name="ValidateBox26EmptyDocCode_70x14mm",
        format="svg",
        code='''#import "lib.typ": *
#show: eskd-document.with(paper: "a4", code: [], code-inverted: (text: [], frame: true))
#show: page-first-form1
[]''',
        validator=lambda svg: assert_box26_present(svg, exp_x=20.0, exp_y=5.0, exp_w=70.0, exp_h=14.0, check_text=False)
    ),
    TestCase(
        name="ValidateLeftStamp3r_85x12mm_A4",
        format="svg",
        code='''#import "lib.typ": *
#show: eskd-document.with(paper: "a4")
#show: eskd-page.with(left: frame-left-3r)
[]''',
        validator=lambda svg: assert_element_at_position(collect_rectangles_and_groups(svg), 8.0, 207.0, 12.0, 85.0, "Боковик 3r A4", edges=(True, True, False, True))
    ),
    TestCase(
        name="ValidateLeftStamp3r_85x12mm_A3_Portrait",
        format="svg",
        code='''#import "lib.typ": *
#show: eskd-document.with(paper: "a3", orientation: "portrait")
#show: eskd-page.with(left: frame-left-3r)
[]''',
        validator=lambda svg: assert_element_at_position(collect_rectangles_and_groups(svg), 8.0, 330.0, 12.0, 85.0, "Боковик 3r A3 Portrait", edges=(True, True, False, True))
    ),
    TestCase(
        name="ValidateLeftStamp3r_85x12mm_A1_Landscape",
        format="svg",
        code='''#import "lib.typ": *
#show: eskd-document.with(paper: "a1", orientation: "landscape")
#show: eskd-page.with(left: frame-left-3r)
[]''',
        validator=lambda svg: assert_element_at_position(collect_rectangles_and_groups(svg), 8.0, 504.0, 12.0, 85.0, "Боковик 3r A1 Landscape", edges=(True, True, False, True))
    ),
    TestCase(
        name="ValidateLeftStamp5r_145x12mm_A4",
        format="svg",
        code='''#import "lib.typ": *
#show: eskd-document.with(paper: "a4")
#show: eskd-page.with(left: frame-left-5r)
[]''',
        validator=lambda svg: assert_element_at_position(collect_rectangles_and_groups(svg), 8.0, 147.0, 12.0, 145.0, "Боковик 5r A4", edges=(True, True, False, True))
    ),
    TestCase(
        name="ValidateLeftStamp5r_145x12mm_A3_Portrait",
        format="svg",
        code='''#import "lib.typ": *
#show: eskd-document.with(paper: "a3", orientation: "portrait")
#show: eskd-page.with(left: frame-left-5r)
[]''',
        validator=lambda svg: assert_element_at_position(collect_rectangles_and_groups(svg), 8.0, 270.0, 12.0, 145.0, "Боковик 5r A3 Portrait", edges=(True, True, False, True))
    ),
    TestCase(
        name="ValidateLeftStamp5r_145x12mm_A2_Landscape",
        format="svg",
        code='''#import "lib.typ": *
#show: eskd-document.with(paper: "a2", orientation: "landscape")
#show: eskd-page.with(left: frame-left-5r)
[]''',
        validator=lambda svg: assert_element_at_position(collect_rectangles_and_groups(svg), 8.0, 270.0, 12.0, 145.0, "Боковик 5r A2 Landscape", edges=(True, True, False, True))
    ),
    TestCase(
        name="ValidateLeftStamp5r_145x12mm_A0_Landscape",
        format="svg",
        code='''#import "lib.typ": *
#show: eskd-document.with(paper: "a0", orientation: "landscape")
#show: eskd-page.with(left: frame-left-5r)
[]''',
        validator=lambda svg: assert_element_at_position(collect_rectangles_and_groups(svg), 8.0, 691.0, 12.0, 145.0, "Боковик 5r A0 Landscape", edges=(True, True, False, True))
    ),
    TestCase(
        name="ValidateLeftStamp7r_287x12mm_A4_Portrait",
        format="svg",
        code='''#import "lib.typ": *
#show: eskd-document.with(paper: "a4")
#show: eskd-page.with(left: frame-left-7r)
[]''',
        validator=lambda svg: assert_element_at_position(collect_rectangles_and_groups(svg), 8.0, 5.0, 12.0, 287.0, "Боковик 7r A4", edges=(True, True, False, True))
    ),
    TestCase(
        name="ValidateLeftStamp7r_287x12mm_A3_Landscape",
        format="svg",
        code='''#import "lib.typ": *
#show: eskd-document.with(paper: "a3", orientation: "landscape")
#show: eskd-page.with(left: frame-left-7r)
[]''',
        validator=lambda svg: assert_element_at_position(collect_rectangles_and_groups(svg), 8.0, 5.0, 12.0, 287.0, "Боковик 7r A3 Landscape", edges=(True, True, False, True))
    ),
    TestCase(
        name="ValidateLeftStamp7r_287x12mm_A3_Portrait",
        format="svg",
        code='''#import "lib.typ": *
#show: eskd-document.with(paper: "a3", orientation: "portrait")
#show: eskd-page.with(left: frame-left-7r)
[]''',
        validator=lambda svg: assert_element_at_position(collect_rectangles_and_groups(svg), 8.0, 128.0, 12.0, 287.0, "Боковик 7r A3 Portrait (Auto 287mm)", edges=(True, True, False, True))
    ),
    TestCase(
        name="ValidateLeftStamp7r_287x12mm_A2_Landscape",
        format="svg",
        code='''#import "lib.typ": *
#show: eskd-document.with(paper: "a2", orientation: "landscape")
#show: eskd-page.with(left: frame-left-7r)
[]''',
        validator=lambda svg: assert_element_at_position(collect_rectangles_and_groups(svg), 8.0, 128.0, 12.0, 287.0, "Боковик 7r A2 Landscape (Auto 287mm)", edges=(True, True, False, True))
    ),
    TestCase(
        name="ValidateLeftStamp7r_287x12mm_A2_Portrait",
        format="svg",
        code='''#import "lib.typ": *
#show: eskd-document.with(paper: "a2", orientation: "portrait")
#show: eskd-page.with(left: frame-left-7r)
[]''',
        validator=lambda svg: assert_element_at_position(collect_rectangles_and_groups(svg), 8.0, 302.0, 12.0, 287.0, "Боковик 7r A2 Portrait (Auto 287mm)", edges=(True, True, False, True))
    ),
    TestCase(
        name="ValidateLeftStamp7r_287x12mm_A1_Landscape",
        format="svg",
        code='''#import "lib.typ": *
#show: eskd-document.with(paper: "a1", orientation: "landscape")
#show: eskd-page.with(left: frame-left-7r)
[]''',
        validator=lambda svg: assert_element_at_position(collect_rectangles_and_groups(svg), 8.0, 302.0, 12.0, 287.0, "Боковик 7r A1 Landscape (Auto 287mm)", edges=(True, True, False, True))
    ),
    TestCase(
        name="ValidateLeftStamp7r_287x12mm_A0_Landscape",
        format="svg",
        code='''#import "lib.typ": *
#show: eskd-document.with(paper: "a0", orientation: "landscape")
#show: eskd-page.with(left: frame-left-7r)
[]''',
        validator=lambda svg: assert_element_at_position(collect_rectangles_and_groups(svg), 8.0, 549.0, 12.0, 287.0, "Боковик 7r A0 Landscape (Auto 287mm)", edges=(True, True, False, True))
    ),
    TestCase(
        name="ValidateLeftStamp7r_MaxGap_A2_Landscape",
        format="svg",
        code='''#import "lib.typ": *
#show: eskd-document.with(paper: "a2", orientation: "landscape")
#show: eskd-page.with(left: frame-left-7r.with(gap: "max"))
[]''',
        validator=lambda svg: assert_element_at_position(collect_rectangles_and_groups(svg), 8.0, 5.0, 12.0, 410.0, "Боковик 7r A2 Landscape Max Gap", edges=(True, True, False, True))
    ),
    TestCase(
        name="ValidateLeftStamp7r_MaxGap_A1_Landscape",
        format="svg",
        code='''#import "lib.typ": *
#show: eskd-document.with(paper: "a1", orientation: "landscape")
#show: eskd-page.with(left: frame-left-7r.with(gap: "max"))
[]''',
        validator=lambda svg: assert_element_at_position(collect_rectangles_and_groups(svg), 8.0, 5.0, 12.0, 584.0, "Боковик 7r A1 Landscape Max Gap", edges=(True, True, False, True))
    ),
    TestCase(
        name="ValidateLeftStamp7r_MaxGap_A0_Landscape",
        format="svg",
        code='''#import "lib.typ": *
#show: eskd-document.with(paper: "a0", orientation: "landscape")
#show: eskd-page.with(left: frame-left-7r.with(gap: "max"))
[]''',
        validator=lambda svg: assert_element_at_position(collect_rectangles_and_groups(svg), 8.0, 5.0, 12.0, 831.0, "Боковик 7r A0 Landscape Max Gap", edges=(True, True, False, True))
    )
]

if __name__ == "__main__":
    passed, failed = run_test_suite(SUITE_ID, SUITE_NAME, tests)
    if failed > 0: exit(1)