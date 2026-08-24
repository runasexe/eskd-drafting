import subprocess
import sys
import time
import re
import io
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import Optional, List, Callable
from pathlib import Path

try:
    import svgelements
    from svgelements import SVG, Path as SvgPath, Line as SvgLine, Close as SvgClose, Rect as SvgRect
    HAVE_SVGELEMENTS = True
except ImportError:
    HAVE_SVGELEMENTS = False

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PT_TO_MM = 25.4 / 72.0

def get_typst_version() -> str:
    try:
        res = subprocess.run(["typst", "--version"], capture_output=True, text=True, encoding="utf-8")
        return res.stdout.strip() if res.returncode == 0 else "typst unknown"
    except Exception as e:
        return f"typst not found: {e}"

# ==========================================
# 1. ТЕСТОВЫЙ ДВИЖОК
# ==========================================

@dataclass
class TestCase:
    name: str
    code: str
    format: str = "pdf"
    expect_error: Optional[str] = None
    expect_stdout: Optional[str] = None
    validator: Optional[Callable[[str], None]] = None
    pretty: bool = False

def run_single_test(suite_id: str, test: TestCase) -> bool:
    full_name = f"Test{suite_id}/{test.name}"
    print(f"=== RUN   {full_name}")

    cmd = ["typst", "compile", "--root", str(PROJECT_ROOT), "--format", test.format]
    if test.format == "html":
        cmd.extend(["--features", "html"])
    if test.pretty:
        cmd.append("--pretty")
    cmd.extend(["-", "-"])

    start = time.perf_counter()
    res = subprocess.run(cmd, input=test.code.encode("utf-8"), capture_output=True)
    elapsed = time.perf_counter() - start

    stderr_str = res.stderr.decode("utf-8", errors="replace")

    # 1. Проверка на ожидаемую ошибку ГОСТ
    if test.expect_error:
        if test.expect_error in stderr_str:
            print(f"--- PASS: {full_name} ({elapsed:.3f}s)")
            return True
        else:
            print(f"--- FAIL: {full_name} ({elapsed:.3f}s)\n    Ожидалась ошибка: '{test.expect_error}'\n    Получено: {stderr_str.strip() or 'Нет ошибок'}")
            return False

    # 2. Неожиданное падение компиляции
    if res.returncode != 0:
        print(f"--- FAIL: {full_name} ({elapsed:.3f}s)\n    Ошибка компиляции:\n{stderr_str.strip()}")
        return False

    # Декодирование stdout только при валидации текстового формата (SVG/HTML)
    if test.format in ("svg", "html"):
        stdout_str = res.stdout.decode("utf-8", errors="replace")
        
        # 3. Поиск текста в успешном рендере
        if test.expect_stdout:
            if test.expect_stdout not in stdout_str:
                print(f"--- FAIL: {full_name} ({elapsed:.3f}s)\n    Подстрока '{test.expect_stdout}' не найдена в {test.format}")
                return False

        # 4. Кастомная валидация
        if test.validator:
            try:
                test.validator(stdout_str)
            except AssertionError as e:
                print(f"--- FAIL: {full_name} ({elapsed:.3f}s)\n    Ошибка валидации: {e}")
                return False

    print(f"--- PASS: {full_name} ({elapsed:.3f}s)")
    return True

def run_test_suite(suite_id: str, suite_name: str, tests: List[TestCase]) -> tuple[int, int]:
    if suite_name:
        print(f"\n# {suite_id}: {suite_name}")
    passed, failed = 0, 0
    for t in tests:
        if run_single_test(suite_id, t): passed += 1
        else: failed += 1
    return passed, failed

# ==========================================
# 2. ДВИЖОК БЕНЧМАРКОВ
# ==========================================

@dataclass
class BenchTarget:
    format: str
    pdf_std: Optional[str] = None
    page: Optional[str] = None

@dataclass
class BenchCase:
    id: str
    name: str
    code: str
    repeats: int = 1
    targets: List[BenchTarget] = field(default_factory=list)

def run_bench_target(bench_id: str, target: BenchTarget, code: str, repeats: int) -> tuple[bool, str]:
    tags = [target.format]
    if target.pdf_std: tags.append(f"std_{target.pdf_std}")
    if target.page: tags.append(f"page_{target.page}")
    
    ident = f"Bench{bench_id}/{'/'.join(tags)}"
    cmd = ["typst", "compile", "--root", str(PROJECT_ROOT), "--format", target.format]
    
    page = target.page
    if target.format in ("svg", "png") and not page:
        page = "1"
    if page:
        cmd.extend(["--pages", str(page)])
    if target.format == "html":
        cmd.extend(["--features", "html"])
    if target.format == "pdf" and target.pdf_std:
        cmd.extend(["--pdf-standard", target.pdf_std])
        if "ua-1" in target.pdf_std and "set document(" not in code:
            code = '#set document(title: "Bench", author: "Runner")\n' + code
    cmd.extend(["-", "-"])

    code_bytes = code.encode("utf-8")
    durations = []
    out_size = 0

    for _ in range(repeats):
        start = time.perf_counter()
        res = subprocess.run(cmd, input=code_bytes, capture_output=True)
        elapsed = time.perf_counter() - start
        
        if res.returncode != 0:
            err = res.stderr.decode("utf-8", errors="replace").strip().split('\n')[0]
            return False, f"{ident:<56} FAIL  {err}"
            
        durations.append(elapsed)
        out_size = len(res.stdout)

    avg_ms = (sum(durations) / repeats) * 1000.0
    kb_out = out_size / 1024.0
    return True, f"{ident:<56} {repeats:>3} {avg_ms:>8.2f} ms/op {kb_out:>8.2f} KB/out"

def run_bench_suite(suite_id: str, suite_name: str, benchmarks: List[BenchCase]) -> tuple[int, int]:
    if suite_name:
        print(f"\n# {suite_id}: {suite_name}")
    passed, failed = 0, 0
    for b in benchmarks:
        for tgt in b.targets:
            ok, log = run_bench_target(b.id, tgt, b.code, b.repeats)
            print(log)
            if ok: passed += 1
            else: failed += 1
    return passed, failed

# ==========================================
# 3. ГЕОМЕТРИЧЕСКИЙ АНАЛИЗ SVG (ГОСТ 2.104 / 2.301 / 2.303)
# ==========================================

class Transform:
    """Матрица аффинных преобразований 3x3 для SVG."""
    def __init__(self, a=1.0, b=0.0, c=0.0, d=1.0, e=0.0, f=0.0):
        self.a, self.b, self.c, self.d, self.e, self.f = a, b, c, d, e, f

    def multiply(self, other):
        return Transform(
            self.a * other.a + self.c * other.b,
            self.b * other.a + self.d * other.b,
            self.a * other.c + self.c * other.d,
            self.b * other.c + self.d * other.d,
            self.a * other.e + self.c * other.f + self.e,
            self.b * other.e + self.d * other.f + self.f
        )

    def apply(self, x, y):
        return (self.a * x + self.c * y + self.e,
                self.b * x + self.d * y + self.f)

def parse_transform_attr(attr_str: str) -> Transform:
    t = Transform()
    if not attr_str: return t
    for match in re.finditer(r'(matrix|translate)\(([^)]+)\)', attr_str):
        cmd = match.group(1)
        args = list(map(float, match.group(2).replace(',', ' ').split()))
        if cmd == 'matrix' and len(args) == 6:
            t = t.multiply(Transform(*args))
        elif cmd == 'translate' and len(args) >= 1:
            t = t.multiply(Transform(1, 0, 0, 1, args[0], args[1] if len(args) > 1 else 0))
    return t

def parse_svg_dimensions(svg_input: str) -> tuple[float, float]:
    root = ET.fromstring(svg_input)
    w_raw = root.attrib.get("width", "0").replace("pt", "").replace("mm", "")
    h_raw = root.attrib.get("height", "0").replace("pt", "").replace("mm", "")
    return float(w_raw) * PT_TO_MM, float(h_raw) * PT_TO_MM

def collect_rectangles_and_groups(svg_str: str) -> tuple[list, list]:
    """
    Извлекает все линии (горизонтальные и вертикальные) из SVG, применяет матрицы
    трансформаций и переводит координаты в миллиметры.
    При наличии библиотеки svgelements использует ее для надежного геометрического
    разбора любых сложных кривых, относительных координат и матриц; иначе использует
    встроенный fallback-парсер XML.
    """
    if HAVE_SVGELEMENTS:
        try:
            svg = SVG.parse(io.StringIO(svg_str))
            PX_TO_MM = 25.4 / 96.0
            h_lines = []
            v_lines = []
            for elem in svg.elements():
                if isinstance(elem, SvgPath):
                    for seg in elem:
                        if isinstance(seg, (SvgLine, SvgClose)):
                            p1 = seg.start
                            p2 = seg.end
                            if p1 is not None and p2 is not None:
                                x1_mm, y1_mm = p1.x * PX_TO_MM, p1.y * PX_TO_MM
                                x2_mm, y2_mm = p2.x * PX_TO_MM, p2.y * PX_TO_MM
                                if abs(x1_mm - x2_mm) < 0.2:
                                    v_lines.append((x1_mm, min(y1_mm, y2_mm), max(y1_mm, y2_mm)))
                                elif abs(y1_mm - y2_mm) < 0.2:
                                    h_lines.append((y1_mm, min(x1_mm, x2_mm), max(x1_mm, x2_mm)))
                elif isinstance(elem, SvgRect):
                    path = SvgPath(elem)
                    for seg in path:
                        if isinstance(seg, (SvgLine, SvgClose)):
                            p1 = seg.start
                            p2 = seg.end
                            if p1 is not None and p2 is not None:
                                x1_mm, y1_mm = p1.x * PX_TO_MM, p1.y * PX_TO_MM
                                x2_mm, y2_mm = p2.x * PX_TO_MM, p2.y * PX_TO_MM
                                if abs(x1_mm - x2_mm) < 0.2:
                                    v_lines.append((x1_mm, min(y1_mm, y2_mm), max(y1_mm, y2_mm)))
                                elif abs(y1_mm - y2_mm) < 0.2:
                                    h_lines.append((y1_mm, min(x1_mm, x2_mm), max(x1_mm, x2_mm)))
            return h_lines, v_lines
        except Exception:
            pass  # Fallback to built-in XML parser if svgelements encounters an issue

    root = ET.fromstring(svg_str)
    h_lines = []
    v_lines = []

    def traverse(node, current_t: Transform):
        t_str = node.attrib.get("transform", "")
        new_t = current_t.multiply(parse_transform_attr(t_str))

        if node.tag.endswith("path"):
            d = node.attrib.get("d", "")
            d = re.sub(r'([a-zA-Z])', r' \1 ', d)
            tokens = d.split()
            
            lines, x, y, sx, sy = [], 0.0, 0.0, 0.0, 0.0
            i = 0
            while i < len(tokens):
                cmd = tokens[i]
                if cmd == 'M': x, y = sx, sy = float(tokens[i+1]), float(tokens[i+2]); i += 3
                elif cmd == 'm': x += float(tokens[i+1]); y += float(tokens[i+2]); sx, sy = x, y; i += 3
                elif cmd == 'L': nx, ny = float(tokens[i+1]), float(tokens[i+2]); lines.append((x,y,nx,ny)); x, y = nx, ny; i += 3
                elif cmd == 'l': nx, ny = x+float(tokens[i+1]), y+float(tokens[i+2]); lines.append((x,y,nx,ny)); x, y = nx, ny; i += 3
                elif cmd == 'H': nx = float(tokens[i+1]); lines.append((x,y,nx,y)); x = nx; i += 2
                elif cmd == 'h': nx = x+float(tokens[i+1]); lines.append((x,y,nx,y)); x = nx; i += 2
                elif cmd == 'V': ny = float(tokens[i+1]); lines.append((x,y,x,ny)); y = ny; i += 2
                elif cmd == 'v': ny = y+float(tokens[i+1]); lines.append((x,y,x,ny)); y = ny; i += 2
                elif cmd in ('Z', 'z'): lines.append((x,y,sx,sy)); x, y = sx, sy; i += 1
                else: i += 1

            for x1, y1, x2, y2 in lines:
                tx1, ty1 = new_t.apply(x1, y1)
                tx2, ty2 = new_t.apply(x2, y2)
                tx1, ty1 = tx1 * PT_TO_MM, ty1 * PT_TO_MM
                tx2, ty2 = tx2 * PT_TO_MM, ty2 * PT_TO_MM
                
                if abs(tx1 - tx2) < 0.1: v_lines.append((tx1, min(ty1,ty2), max(ty1,ty2)))
                elif abs(ty1 - ty2) < 0.1: h_lines.append((ty1, min(tx1,tx2), max(tx1,tx2)))

        for child in node:
            traverse(child, new_t)

    traverse(root, Transform())
    return h_lines, v_lines

def check_line_exists(lines, coord, req_start, req_end, tol=1.0) -> bool:
    segments = []
    for c, s, e in lines:
        if abs(c - coord) <= tol:
            segments.append((min(s, e), max(s, e)))
    if not segments:
        return False
        
    segments.sort(key=lambda x: x[0])
    merged = [segments[0]]
    for curr_s, curr_e in segments[1:]:
        last_s, last_e = merged[-1]
        if curr_s <= last_e + tol:
            merged[-1] = (last_s, max(last_e, curr_e))
        else:
            merged.append((curr_s, curr_e))
            
    for ms, me in merged:
        if ms - tol <= req_start and me + tol >= req_end:
            return True
    return False

def assert_element_at_position(lines_tuple, exp_x: float, exp_y: float, exp_w: float, exp_h: float, name: str, tol: float = 1.0, edges: tuple = (True, True, True, True)):
    """Проверяет наличие границ элемента. Позволяет селективно отключать стороны: (Top, Bottom, Left, Right)."""
    h_lines, v_lines = lines_tuple
    chk_t, chk_b, chk_l, chk_r = edges
    
    top = check_line_exists(h_lines, exp_y, exp_x, exp_x + exp_w, tol) if chk_t else True
    bottom = check_line_exists(h_lines, exp_y + exp_h, exp_x, exp_x + exp_w, tol) if chk_b else True
    left = check_line_exists(v_lines, exp_x, exp_y, exp_y + exp_h, tol) if chk_l else True
    right = check_line_exists(v_lines, exp_x + exp_w, exp_y, exp_y + exp_h, tol) if chk_r else True
    
    assert top and bottom and left and right, (
        f"ГОСТ-несоответствие: Границы элемента '{name}' не найдены. "
        f"Требуется: X={exp_x:.1f}, Y={exp_y:.1f}, W={exp_w:.1f}, H={exp_h:.1f}. "
        f"Найденные линии: [Верх:{top}, Низ:{bottom}, Лев:{left}, Прав:{right}]"
    )

def assert_box26_present(svg_str: str, exp_x: float = 20.0, exp_y: float = 5.0, exp_w: float = 70.0, exp_h: float = 14.0, tol: float = 1.0, check_text: bool = False):
    """
    Строгая валидация Графы 26: проверяет наличие собственного замкнутого
    контура (70x14 мм) и при необходимости наличие повернутого текста.
    """
    lines = collect_rectangles_and_groups(svg_str)
    assert_element_at_position(lines, exp_x, exp_y, exp_w, exp_h, "Графа 26", tol=tol, edges=(True, True, True, True))

    if check_text:
        root = ET.fromstring(svg_str)
        has_text = False
        for g in root.iter():
            if g.tag.endswith("g"):
                t_str = g.attrib.get("transform", "")
                if "matrix(-1" in t_str or "rotate(180" in t_str:
                    t = parse_transform_attr(t_str)
                    tx_mm, ty_mm = t.e * PT_TO_MM, t.f * PT_TO_MM
                    if (exp_x - 5.0) <= tx_mm <= (exp_x + exp_w + 15.0) and (exp_y - 5.0) <= ty_mm <= (exp_y + exp_h + 15.0):
                        has_text = True
                        break
        assert has_text, f"Повернутый текст Графы 26 не найден в координатах [{exp_x}..{exp_x+exp_w}, {exp_y}..{exp_y+exp_h}]"

def check_bottom_labels_present(svg_str: str, exp_x: float, page_h: float, tol: float = 5.0) -> bool:
    """
    Проверяет наличие служебных надписей Граф 31/32 на нижнем поле листа
    (в диапазоне Y: [page_h - 5.0, page_h], X: [exp_x - tol, exp_x + tol]).
    """
    root = ET.fromstring(svg_str)
    for g in root.iter():
        t_str = g.attrib.get("transform", "")
        if "translate" in t_str:
            m = re.search(r'translate\(([^)]+)\)', t_str)
            if m:
                parts = [float(p) for p in m.group(1).replace(',', ' ').split()]
                if len(parts) == 2:
                    x_mm, y_mm = parts[0] * PT_TO_MM, parts[1] * PT_TO_MM
                    if (exp_x - tol) <= x_mm <= (exp_x + tol) and (page_h - 5.0) <= y_mm <= page_h:
                        return True
    return False

def check_bottom_cells_status(svg_str: str, page_h: float = 297.0) -> tuple[bool, bool]:
    """
    Проверяет статус отображения Графы 31 («Копировал») и Графы 32 («Формат»)
    на нижнем поле листа.
    Возвращает (has_copier, has_format).
    """
    root = ET.fromstring(svg_str)
    has_copier = False
    has_format = False
    for g in root.iter('{http://www.w3.org/2000/svg}g'):
        t_str = g.attrib.get("transform", "")
        if "translate" in t_str:
            m = re.search(r'translate\(([^)]+)\)', t_str)
            if m:
                parts = [float(p) for p in m.group(1).replace(',', ' ').split()]
                if len(parts) == 2:
                    y_mm = parts[1] * PT_TO_MM
                    if (page_h - 5.0) <= y_mm <= page_h:
                        for sub in g:
                            sub_t = sub.attrib.get("transform", "")
                            if "matrix" in sub_t:
                                mat = [float(x) for x in re.findall(r'[-+]?\d*\.\d+|\d+', sub_t)]
                                if len(mat) >= 6:
                                    dx_pt = mat[4]
                                    if dx_pt < 100.0 and len(sub) > 0:
                                        has_copier = True
                                    elif dx_pt >= 100.0 and len(sub) > 0:
                                        has_format = True
    return has_copier, has_format

def check_svg_page_dimensions(svg_str: str, exp_w_mm: float, exp_h_mm: float, tol: float = 0.5) -> bool:
    """
    Проверяет физические габариты листа (viewBox) в SVG.
    """
    root = ET.fromstring(svg_str)
    vb = root.attrib.get("viewBox", "")
    parts = [float(p) for p in vb.split()]
    if len(parts) != 4:
        return False
    w_mm = parts[2] * PT_TO_MM
    h_mm = parts[3] * PT_TO_MM
    return abs(w_mm - exp_w_mm) <= tol and abs(h_mm - exp_h_mm) <= tol

def check_svg_text_cluster(svg_str: str, exp_x_mm: float, exp_y_mm: float, min_glyphs: int = 1, tol_x: float = 8.0, tol_y: float = 8.0) -> bool:
    """
    Проверяет наличие текстового кластера глифов рядом с заданными координатами (x, y) в мм.
    """
    root = ET.fromstring(svg_str)
    for g in root.iter('{http://www.w3.org/2000/svg}g'):
        t_str = g.attrib.get("transform", "")
        if "translate" in t_str:
            m = re.search(r'translate\(([^)]+)\)', t_str)
            if m:
                parts = [float(p) for p in m.group(1).replace(',', ' ').split()]
                if len(parts) == 2:
                    x_mm, y_mm = parts[0] * PT_TO_MM, parts[1] * PT_TO_MM
                    if (exp_x_mm - tol_x) <= x_mm <= (exp_x_mm + tol_x) and (exp_y_mm - tol_y) <= y_mm <= (exp_y_mm + tol_y):
                        uses = g.findall('.//{http://www.w3.org/2000/svg}use')
                        if len(uses) >= min_glyphs:
                            return True
    return False

def check_svg_text_in_rect(svg_str: str, x_mm: float, y_mm: float, w_mm: float, h_mm: float, min_glyphs: int = 1, margin_mm: float = 2.0) -> bool:
    """
    Проверяет наличие глифов внутри заданной прямоугольной области (ячейки) в мм.
    """
    root = ET.fromstring(svg_str)
    x1, y1 = x_mm - margin_mm, y_mm - margin_mm
    x2, y2 = x_mm + w_mm + margin_mm, y_mm + h_mm + margin_mm
    total_glyphs = 0
    for g in root.iter('{http://www.w3.org/2000/svg}g'):
        t_str = g.attrib.get("transform", "")
        if "translate" in t_str:
            m = re.search(r'translate\(([^)]+)\)', t_str)
            if m:
                parts = [float(p) for p in m.group(1).replace(',', ' ').split()]
                if len(parts) == 2:
                    gx, gy = parts[0] * PT_TO_MM, parts[1] * PT_TO_MM
                    if x1 <= gx <= x2 and y1 <= gy <= y2:
                        uses = g.findall('.//{http://www.w3.org/2000/svg}use')
                        total_glyphs += len(uses)
                        if total_glyphs >= min_glyphs:
                            return True
    return total_glyphs >= min_glyphs



