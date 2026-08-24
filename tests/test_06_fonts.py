from core import TestCase, run_test_suite

SUITE_ID = "Fonts"
SUITE_NAME = "Шрифты, начертания и номинальные высоты (ГОСТ 2.304-81)"

# Значения для сравнения:
# - ГОСТ 2.304-81 (Таблица 1, п. 2.1): Номинальный ряд высот шрифта h:
#   1.8 мм, 2.5 мм, 3.5 мм, 5.0 мм, 7.0 мм, 10.0 мм, 14.0 мм, 20.0 мм, 28.0 мм, 40.0 мм.
# - ГОСТ 2.304-81 (Таблица 2, Шрифт типа А): d = (1/14)h, масштаб кегля scale = 1.286.
# - ГОСТ 2.304-81 (Таблица 3, Шрифт типа Б): d = (1/10)h, масштаб кегля scale = 1.40.
# - Внедрение шрифтов (Font Injection): Пользователь может передать font: "FontName"
#   или font: ("Font1", "Font2") — шрифт помещается во главу цепочки fallback-шрифтов.

tests = [
    TestCase(
        name="AllowValidSubscriptBaseHeight",
        code='''#import "lib.typ": *
#assert-gost-subscript-base-h(h3_5)
#assert-gost-subscript-base-h(h2_5)
[OK]'''
    ),
    TestCase(
        name="ForbidSubscriptBaseHeightBelow2_5mm",
        code='#import "lib.typ": *\n#assert-gost-subscript-base-h(h1_8)',
        expect_error="gost-2.304-81-subscript-base-height"
    ),
    TestCase(
        name="IgnoreSubscriptBaseHeightBelow2_5mmRule",
        code='#import "lib.typ": *\n#assert-gost-subscript-base-h(h1_8, ignore-rules: "gost-2.304-81-subscript-base-height")\n[OK]'
    ),
    TestCase(
        name="ForbidGetGostSubscriptForBaseBelow2_5mm",
        code='#import "lib.typ": *\n#let h = get-gost-subscript-h(h1_8)',
        expect_error="gost-2.304-81-subscript-base-height"
    ),
    TestCase(
        name="IgnoreGetGostSubscriptForBaseBelow2_5mm",
        code='#import "lib.typ": *\n#let h = get-gost-subscript-h(h1_8, ignore-rules: "gost-2.304-81-subscript-base-height")\n[OK]'
    ),

    TestCase(
        name="GostSubscriptFontHeightSteps",
        code='''#import "lib.typ": *
#assert(get-gost-subscript-h(h5_0) == h3_5)
#assert(get-gost-subscript-h(h3_5) == h2_5)
#assert(get-gost-subscript-h(h2_5) == h1_8)
#assert(get-gost-subscript-h(h1_8, ignore-rules: "gost-2.304-81-subscript-base-height") == h1_8)
#assert(get-gost-subscript-h(h7_0) == h5_0)
#assert(get-gost-subscript-h(h10_0) == h7_0)
[OK]'''
    ),

    TestCase(
        name="AllowValidGostFontHeight",
        code='#import "lib.typ": *\n#assert-gost-h(h3_5)\n[OK]'
    ),
    TestCase(
        name="ForbidNonStandardFontHeight",
        code='#import "lib.typ": *\n#assert-gost-h(4.2mm)',
        expect_error="gost-2.304-81-font-height"
    ),
    TestCase(
        name="IgnoreNonStandardFontHeightRule",
        code='#import "lib.typ": *\n#assert-gost-h(4.2mm, ignore-rules: "gost-2.304-81-font-height")\n[OK]'
    ),
    TestCase(
        name="ResolveCustomFontString",
        code='''#import "lib.typ": *
#let cfg = resolve-font-cfg(font: "Times New Roman", font-type: "type-a")
#assert(cfg.font.at(0) == "Times New Roman")
#assert(cfg.scale == 1.286)
[OK]'''
    ),
    TestCase(
        name="ResolveCustomFontArray",
        code='''#import "lib.typ": *
#let cfg = resolve-font-cfg(font: ("PT Astra Sans", "Arial"), font-type: "type-b")
#assert(cfg.font.at(0) == "PT Astra Sans")
#assert(cfg.scale == 1.40)
[OK]'''
    ),
    TestCase(
        name="DocumentWithCustomFont",
        code='''#import "lib.typ": *
#show: eskd-document.with(font: "Times New Roman", code: [ЯЯЯЯ.123456.001])
#show: page-first-form1
[Тест со шрифтом пользователя]'''
    ),
    TestCase(
        name="DocumentWithCustomFontArray",
        code='''#import "lib.typ": *
#show: eskd-document.with(font: ("OpenGost Type A TT", "Arial"), font-type: "type-a", code: [ЯЯЯЯ.123456.001])
#show: page-first-form1
[Тест со списком шрифтов пользователя]'''
    ),
    TestCase(
        name="GostFontsMetricsOnlyNoItalic",
        code='''#import "lib.typ": *
#assert("italic" not in gost-fonts.at("type-b"))
#assert("italic" not in gost-fonts.at("type-a"))
#assert(gost-fonts.at("type-b").scale == 1.40)
#assert(gost-fonts.at("type-a").scale == 1.286)
[OK]'''
    ),
    TestCase(
        name="ResolveFontCfgMetricsOnly",
        code='''#import "lib.typ": *
#let cfg = resolve-font-cfg(font-type: "type-a")
#assert("italic" not in cfg)
#assert(cfg.scale == 1.286)
#assert(cfg.font.len() > 0)
[OK]'''
    ),
    TestCase(
        name="GostTextExplicitItalic",
        code='''#import "lib.typ": *
#let t1 = gost-text(italic: true)[Наклонный текст]
#let t2 = gost-text(italic: false)[Прямой текст]
[OK]'''
    ),
    TestCase(
        name="DocumentWithFontItalicDirect",
        code='''#import "lib.typ": *
#show: eskd-document.with(
  font: ("OpenGost Type A TT", "Arial"),
  font-type: "type-a",
  font-italic: true,
  code: [ЯЯЯЯ.123456.001],
  name: [Тестовое наименование с font-italic],
)
#show: page-first-form1
[Тест с прямым параметром font-italic: true]'''
    ),
    TestCase(
        name="LocalFormWithFontItalicOverride",
        code='''#import "lib.typ": *
#let f1 = frame-form-1(font-italic: true, code: [АБВГ.111222.001])
#let f2 = frame-form-2(font-italic: false, code: [АБВГ.111222.002])
[OK]'''
    ),
    TestCase(
        name="GostFontFamiliesDefinitionAndOsifont",
        code='''#import "lib.typ": *
#assert("ascon" in gost-font-families)
#assert("tflex" in gost-font-families)
#assert("solidworks" in gost-font-families)
#assert("autocad" in gost-font-families)
#assert("spds" in gost-font-families)
#assert("osifont" in gost-fonts.at("type-b").font)
#assert(gost-fonts.at("type-b").font.len() <= 8)
#assert(gost-fonts.at("type-a").font.len() <= 8)
[OK]'''
    ),
    TestCase(
        name="ResolveCadFontPresets",
        code='''#import "lib.typ": *
#let cfg-ascon = resolve-font-cfg(font-group: "ascon")
#assert(cfg-ascon.font.at(0) == "Ascon GOST 2.304 Type B")
#let cfg-cad = resolve-font-cfg(font-group: "autocad")
#assert(cfg-cad.font.at(0) == "ISOCPEUR")
#let cfg-sw = resolve-font-cfg(font-group: "solidworks")
#assert(cfg-sw.font.at(0) == "SolidWorks GOST")
#let cfg-osi = resolve-font-cfg(font: "osifont")
#assert(cfg-osi.font.at(0) == "osifont")
#let cfg-both = resolve-font-cfg(font: "MyCustomFont", font-group: "ascon")
#assert(cfg-both.font.at(0) == "MyCustomFont")
#assert(cfg-both.font.at(1) == "Ascon GOST 2.304 Type B")
[OK]'''
    ),
    TestCase(
        name="DocumentWithCadFontGroup",
        code='''#import "lib.typ": *
#show: eskd-document.with(
  font-group: "ascon",
  code: [АБВГ.100200.001],
)
#show: page-first-form1
[Документ с САПР-группой ascon]'''
    ),
    TestCase(
        name="DocumentWithCustomFontAndFontGroup",
        code='''#import "lib.typ": *
#show: eskd-document.with(
  font: "osifont",
  font-group: "autocad",
  code: [АБВГ.100200.002],
)
#show: page-first-form1
[Документ с font: osifont и font-group: autocad]'''
    ),
]

if __name__ == "__main__":
    passed, failed = run_test_suite(SUITE_ID, SUITE_NAME, tests)
    if failed > 0: exit(1)