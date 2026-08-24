from core import TestCase, run_test_suite, check_svg_page_dimensions

SUITE_ID = "Format"
SUITE_NAME = "Форматы и ориентация листов (ГОСТ 2.301-68)"

# Источники нормативных значений:
# - ГОСТ 2.301-68 (п. 4): Формат А4 (210х297 мм) допускается применять ТОЛЬКО с вертикальным
#   расположением длинной стороны (portrait). Альбомный формат А4 (landscape) стандартом запрещен.
# - Форматы А3, А2, А1, А0 допускается применять как в горизонтальном (landscape), так и вертикальном (portrait) положениях.

tests = [
    # 1. Базовые форматы ГОСТ 2.301-68
    TestCase(
        name="AllowA3Landscape",
        code='#import "lib.typ": *\n#assert-paper-format("a3", "landscape")\n[OK]'
    ),
    TestCase(
        name="AllowA3Portrait",
        code='#import "lib.typ": *\n#assert-paper-format("a3", "portrait")\n[OK]'
    ),
    TestCase(
        name="ForbidA4LandscapeDocument",
        code='#import "lib.typ": *\n#show: eskd-document.with(paper: "a4", orientation: "landscape")\n[Контент]',
        expect_error="gost-2.301-68-a4-landscape"
    ),
    TestCase(
        name="ForbidA4LandscapeDirect",
        code='#import "lib.typ": *\n#assert-paper-format("a4", "landscape")',
        expect_error="gost-2.301-68-a4-landscape"
    ),
    TestCase(
        name="ForbidA4LandscapeInEskdPage",
        code='#import "lib.typ": *\n#show: eskd-document.with(paper: "a4")\n#eskd-page(paper: "a4", orientation: "landscape")[\n  [Контент на странице 2]\n]',
        expect_error="gost-2.301-68-a4-landscape"
    ),
    TestCase(
        name="IgnoreA4LandscapeRuleDocument",
        code='#import "lib.typ": *\n#show: eskd-document.with(paper: "a4", orientation: "landscape", ignore-rules: "gost-2.301-68-a4-landscape")\n[Контент]'
    ),
    TestCase(
        name="IgnoreA4LandscapeRuleDirect",
        code='#import "lib.typ": *\n#assert-paper-format("a4", "landscape", ignore-rules: "gost-2.301-68-a4-landscape")\n[OK]'
    ),
    TestCase(
        name="IgnoreA4LandscapeInEskdPage",
        code='#import "lib.typ": *\n#show: eskd-document.with(paper: "a4")\n#eskd-page(paper: "a4", orientation: "landscape", ignore-rules: "gost-2.301-68-a4-landscape")[\n  [Контент на странице 2]\n]'
    ),
    TestCase(
        name="IgnorePaperFormatDoesNotIgnoreA4Landscape",
        code='#import "lib.typ": *\n#assert-paper-format("a4", "landscape", ignore-rules: "gost-2.301-68-paper-format")',
        expect_error="gost-2.301-68-a4-landscape"
    ),
    TestCase(
        name="IgnoreOrientationDoesNotIgnoreA4Landscape",
        code='#import "lib.typ": *\n#assert-paper-format("a4", "landscape", ignore-rules: "gost-2.301-68-paper-orientation")',
        expect_error="gost-2.301-68-a4-landscape"
    ),
    TestCase(
        name="ForbidInvalidOrientationValue",
        code='#import "lib.typ": *\n#assert-paper-format("a3", "diagonal")',
        expect_error="gost-2.301-68-paper-orientation"
    ),
    TestCase(
        name="IgnoreInvalidOrientationValueRule",
        code='#import "lib.typ": *\n#assert-paper-format("a3", "diagonal", ignore-rules: "gost-2.301-68-paper-orientation")\n[OK]'
    ),

    # 2. Кратные форматы aNxM (ГОСТ 2.301-68, Таблица 2, M >= 2, только landscape)
    TestCase(
        name="AllowA4x3Multiplied",
        code='#import "lib.typ": *\n#show: eskd-document.with(paper: "a4x3")\n[Контент]'
    ),
    TestCase(
        name="AllowA4x3LandscapeExplicit",
        code='#import "lib.typ": *\n#assert-paper-format("a4x3", "landscape")\n[OK]'
    ),
    TestCase(
        name="ForbidMultipliedPortrait_A4x3",
        code='#import "lib.typ": *\n#assert-paper-format("a4x3", "portrait")',
        expect_error="gost-2.301-68-multiplied-landscape-only"
    ),
    TestCase(
        name="ForbidMultipliedPortrait_A3x3",
        code='#import "lib.typ": *\n#assert-paper-format("a3x3", "portrait")',
        expect_error="gost-2.301-68-multiplied-landscape-only"
    ),
    TestCase(
        name="ForbidMultipliedPortraitInEskdPage",
        code='#import "lib.typ": *\n#show: eskd-document.with(paper: "a4")\n#eskd-page(paper: "a4x3", orientation: "portrait")[\n  [Контент на странице 2]\n]',
        expect_error="gost-2.301-68-multiplied-landscape-only"
    ),
    TestCase(
        name="IgnoreMultipliedLandscapeOnlyRuleDirect",
        code='#import "lib.typ": *\n#assert-paper-format("a4x3", "portrait", ignore-rules: "gost-2.301-68-multiplied-landscape-only")\n[OK]'
    ),
    TestCase(
        name="IgnoreMultipliedLandscapeOnlyRulePage",
        code='#import "lib.typ": *\n#show: eskd-document.with(paper: "a4")\n#eskd-page(paper: "a4x3", orientation: "portrait", ignore-rules: "gost-2.301-68-multiplied-landscape-only")[\n  [Контент на странице 2]\n]'
    ),
    TestCase(
        name="AllowA4x4Multiplied",
        code='#import "lib.typ": *\n#show: eskd-document.with(paper: "a4x4")\n[Контент]'
    ),
    TestCase(
        name="AllowA3x4Multiplied",
        code='#import "lib.typ": *\n#show: eskd-document.with(paper: "a3x4")\n[Контент]'
    ),
    TestCase(
        name="AllowA2x3Multiplied",
        code='#import "lib.typ": *\n#show: eskd-document.with(paper: "a2x3")\n[Контент]'
    ),
    TestCase(
        name="AllowA0x2Multiplied",
        code='#import "lib.typ": *\n#show: eskd-document.with(paper: "a0x2")\n[Контент]'
    ),
    TestCase(
        name="AllowA0x3Multiplied",
        code='#import "lib.typ": *\n#show: eskd-document.with(paper: "a0x3")\n[Контент]'
    ),

    # 3. Запрет суффикса 'x1' для базовых форматов (M = 1 недопустимо с суффиксом 'x')
    TestCase(
        name="ForbidA4x1",
        code='#import "lib.typ": *\n#show: eskd-document.with(paper: "a4x1")\n[Контент]',
        expect_error="gost-2.301-68-paper-format"
    ),
    TestCase(
        name="ForbidA3x1",
        code='#import "lib.typ": *\n#assert-paper-format("a3x1", "portrait")',
        expect_error="gost-2.301-68-paper-format"
    ),
    TestCase(
        name="ForbidA0x1",
        code='#import "lib.typ": *\n#assert-paper-format("a0x1", "portrait")',
        expect_error="gost-2.301-68-paper-format"
    ),

    # 4. Валидация недопустимых базовых форматов (gost-2.301-68-paper-format)
    TestCase(
        name="ForbidInvalidPaperFormat_A5",
        code='#import "lib.typ": *\n#assert-paper-format("a5", "portrait")',
        expect_error="gost-2.301-68-paper-format"
    ),
    TestCase(
        name="ForbidInvalidPaperFormat_Letter",
        code='#import "lib.typ": *\n#assert-paper-format("letter", "portrait")',
        expect_error="gost-2.301-68-paper-format"
    ),
    TestCase(
        name="IgnoreInvalidPaperFormatRule",
        code='#import "lib.typ": *\n#assert-paper-format("a5", "portrait", ignore-rules: "gost-2.301-68-paper-format")\n[OK]'
    ),

    # 5. Валидация нестандартных коэффициентов кратности (gost-2.301-68-paper-multiplied-ratio)
    TestCase(
        name="ForbidInvalidMultipliedRatio_A4x2",
        code='#import "lib.typ": *\n#assert-paper-format("a4x2", "landscape")',
        expect_error="gost-2.301-68-paper-multiplied-ratio"
    ),
    TestCase(
        name="ForbidInvalidMultipliedRatio_A3x2",
        code='#import "lib.typ": *\n#assert-paper-format("a3x2", "landscape")',
        expect_error="gost-2.301-68-paper-multiplied-ratio"
    ),
    TestCase(
        name="ForbidInvalidMultipliedRatio_A2x2",
        code='#import "lib.typ": *\n#assert-paper-format("a2x2", "landscape")',
        expect_error="gost-2.301-68-paper-multiplied-ratio"
    ),
    TestCase(
        name="ForbidInvalidMultipliedRatio_A1x2",
        code='#import "lib.typ": *\n#assert-paper-format("a1x2", "landscape")',
        expect_error="gost-2.301-68-paper-multiplied-ratio"
    ),
    TestCase(
        name="ForbidInvalidMultipliedRatio_A4x10",
        code='#import "lib.typ": *\n#assert-paper-format("a4x10", "landscape")',
        expect_error="gost-2.301-68-paper-multiplied-ratio"
    ),
    TestCase(
        name="ForbidInvalidMultipliedRatio_A0x4",
        code='#import "lib.typ": *\n#assert-paper-format("a0x4", "landscape")',
        expect_error="gost-2.301-68-paper-multiplied-ratio"
    ),
    TestCase(
        name="IgnoreInvalidMultipliedRatioRule",
        code='#import "lib.typ": *\n#assert-paper-format("a4x2", "landscape", ignore-rules: "gost-2.301-68-paper-multiplied-ratio")\n[OK]'
    ),
    TestCase(
        name="IgnoreBothMultipliedRules",
        code='#import "lib.typ": *\n#assert-paper-format("a4x2", "portrait", ignore-rules: ("gost-2.301-68-paper-multiplied-ratio", "gost-2.301-68-multiplied-landscape-only"))\n[OK]'
    ),

    # 6. Физические размеры SVG (viewBox) базовых и кратных форматов
    TestCase(
        name="SvgDimensions_A4_Portrait",
        format="svg",
        code='#import "lib.typ": *\n#show: eskd-document.with(paper: "a4", orientation: "portrait")\n[OK]',
        validator=lambda svg: check_svg_page_dimensions(svg, 210.0, 297.0)
    ),
    TestCase(
        name="SvgDimensions_A3_Landscape",
        format="svg",
        code='#import "lib.typ": *\n#show: eskd-document.with(paper: "a3", orientation: "landscape")\n[OK]',
        validator=lambda svg: check_svg_page_dimensions(svg, 420.0, 297.0)
    ),
    TestCase(
        name="SvgDimensions_A3_Portrait",
        format="svg",
        code='#import "lib.typ": *\n#show: eskd-document.with(paper: "a3", orientation: "portrait")\n[OK]',
        validator=lambda svg: check_svg_page_dimensions(svg, 297.0, 420.0)
    ),
    TestCase(
        name="SvgDimensions_A2_Landscape",
        format="svg",
        code='#import "lib.typ": *\n#show: eskd-document.with(paper: "a2", orientation: "landscape")\n[OK]',
        validator=lambda svg: check_svg_page_dimensions(svg, 594.0, 420.0)
    ),
    TestCase(
        name="SvgDimensions_A1_Landscape",
        format="svg",
        code='#import "lib.typ": *\n#show: eskd-document.with(paper: "a1", orientation: "landscape")\n[OK]',
        validator=lambda svg: check_svg_page_dimensions(svg, 841.0, 594.0)
    ),
    TestCase(
        name="SvgDimensions_A0_Landscape",
        format="svg",
        code='#import "lib.typ": *\n#show: eskd-document.with(paper: "a0", orientation: "landscape")\n[OK]',
        validator=lambda svg: check_svg_page_dimensions(svg, 1189.0, 841.0)
    ),
    TestCase(
        name="SvgDimensions_A4x3_Multiplied",
        format="svg",
        code='#import "lib.typ": *\n#show: eskd-document.with(paper: "a4x3")\n[OK]',
        validator=lambda svg: check_svg_page_dimensions(svg, 630.0, 297.0)
    ),
    TestCase(
        name="SvgDimensions_A4x4_Multiplied",
        format="svg",
        code='#import "lib.typ": *\n#show: eskd-document.with(paper: "a4x4")\n[OK]',
        validator=lambda svg: check_svg_page_dimensions(svg, 841.0, 297.0)
    ),
    TestCase(
        name="SvgDimensions_A4x5_Multiplied",
        format="svg",
        code='#import "lib.typ": *\n#show: eskd-document.with(paper: "a4x5")\n[OK]',
        validator=lambda svg: check_svg_page_dimensions(svg, 1051.0, 297.0)
    ),
    TestCase(
        name="SvgDimensions_A3x3_Multiplied",
        format="svg",
        code='#import "lib.typ": *\n#show: eskd-document.with(paper: "a3x3")\n[OK]',
        validator=lambda svg: check_svg_page_dimensions(svg, 891.0, 420.0)
    ),
    TestCase(
        name="SvgDimensions_A3x4_Multiplied",
        format="svg",
        code='#import "lib.typ": *\n#show: eskd-document.with(paper: "a3x4")\n[OK]',
        validator=lambda svg: check_svg_page_dimensions(svg, 1189.0, 420.0)
    ),
    TestCase(
        name="SvgDimensions_A2x3_Multiplied",
        format="svg",
        code='#import "lib.typ": *\n#show: eskd-document.with(paper: "a2x3")\n[OK]',
        validator=lambda svg: check_svg_page_dimensions(svg, 1261.0, 594.0)
    ),
    TestCase(
        name="SvgDimensions_A0x2_Multiplied",
        format="svg",
        code='#import "lib.typ": *\n#show: eskd-document.with(paper: "a0x2")\n[OK]',
        validator=lambda svg: check_svg_page_dimensions(svg, 1682.0, 1189.0)
    ),
    TestCase(
        name="SvgDimensions_A0x3_Multiplied",
        format="svg",
        code='#import "lib.typ": *\n#show: eskd-document.with(paper: "a0x3")\n[OK]',
        validator=lambda svg: check_svg_page_dimensions(svg, 2523.0, 1189.0)
    ),
]

if __name__ == "__main__":
    passed, failed = run_test_suite(SUITE_ID, SUITE_NAME, tests)
    if failed > 0: exit(1)