"""Flask 데모 — 구현된 마방진 검증·힌트 확인."""

from __future__ import annotations

from pathlib import Path

from flask import Flask, render_template, request

from src.boundary.grid_parser import grid_to_form_values, parse_grid_from_form
from src.control.grid_analysis import analyze_grid
from src.entity.find_blank_coords import find_blank_coords
from src.entity.hint_one_cell import hint_one_cell

_ERROR_LABELS: dict[str, str] = {
    "E003": "격자가 비어 있습니다 (None).",
    "E004": "셀 값이 유효 범위(0, 1~16)를 벗어났습니다.",
    "E005": "1~16 숫자가 중복되었습니다.",
    "E006": "격자 크기가 4×4가 아닙니다.",
}

_STATUS_LABELS: dict[str, str] = {
    "incomplete": "미완성 — 빈칸이 남아 있습니다.",
    "fail": "실패 — 합이 34가 아닌 줄이 있습니다.",
    "pass": "통과 — 10선 합이 모두 34입니다.",
}

# G1 예제 — conftest grid_g1 SSOT
_EXAMPLE_GRID = [
    [16, 2, 3, 13],
    [5, 11, 0, 8],
    [9, 7, 6, 12],
    [4, 14, 15, 0],
]


def create_app() -> Flask:
    template_dir = Path(__file__).parent / "templates"
    app = Flask(__name__, template_folder=str(template_dir))

    @app.get("/")
    def index_get():
        return _render_page(cells=grid_to_form_values(_EXAMPLE_GRID))

    @app.post("/")
    def index_post():
        action = request.form.get("action", "analyze")
        cells = [request.form.get(f"cell_{i}", "") for i in range(16)]

        try:
            grid = parse_grid_from_form(cells)
        except ValueError:
            return _render_page(
                cells=cells,
                parse_error="숫자만 입력하거나 빈칸으로 두세요.",
            )

        if action == "hint":
            return _render_hint(cells, grid)

        return _render_analyze(cells, grid)

    return app


def _render_analyze(cells: list[str], grid: list[list[int]]):
    result = analyze_grid(grid)
    error = result["error"]
    validation = result["validation"]
    status = validation.get("status") if validation else None

    return _render_page(
        cells=cells,
        error=error,
        error_message=_ERROR_LABELS.get(error) if error else None,
        blank_coords=result["blank_coords"],
        status=status,
        status_message=_STATUS_LABELS.get(status) if status else None,
        failed_lines=validation.get("failed_lines", []) if validation else [],
    )


def _render_hint(cells: list[str], grid: list[list[int]]):
    input_error = analyze_grid(grid)["error"]
    if input_error is not None:
        return _render_page(
            cells=cells,
            error=input_error,
            error_message=_ERROR_LABELS.get(input_error),
            hint_error="입력이 유효할 때만 힌트를 받을 수 있습니다.",
        )

    if not find_blank_coords(grid):
        return _render_page(
            cells=cells,
            hint_error="빈칸이 없어 힌트를 줄 수 없습니다.",
        )

    hint = hint_one_cell(grid)
    return _render_page(cells=cells, hint=hint)


def _render_page(**context):
    return render_template("index.html", **context)


def main() -> None:
    app = create_app()
    app.run(debug=True, port=5000)


if __name__ == "__main__":
    main()
