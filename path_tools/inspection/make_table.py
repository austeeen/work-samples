from typing import List, Dict
from collections import namedtuple

HeaderEntry = namedtuple("HeaderEntry", ["name", "width", "text"])
Line = namedtuple("Line", ["begin", "fill", "sep", "end"])
Row = namedtuple("DataRow", ["begin", "sep", "end"])
Style = namedtuple(
    "Style", ["title_above", "title_below", "line_above", "line_below_header", "line_below",
              "header_row",
              "data_row", "padding"])

STYLES = {
    "grid": Style(
        title_above=Line("+", "=", "=", "+"),
        title_below=Line("+", "-", "-", "+"),
        line_above=Line("+", "-", "+", "+"),
        line_below_header=Line("+", "=", "+", "+"),
        line_below=Line("+", "-", "+", "+"),
        header_row=Row("|", "|", "|"),
        data_row=Row("|", "|", "|"),
        padding=1
    ),
    "fancy_grid": Style(
        title_above=Line("╒", "═", "═", "╕"),
        title_below=Line("╞", "═", "╤", "╡"),
        line_above=Line("╒", "═", "╤", "╕"),
        line_below_header=Line("╞", "═", "╪", "╡"),
        line_below=Line("╘", "═", "╧", "╛"),
        header_row=Row("│", "│", "│"),
        data_row=Row("│", "│", "│"),
        padding=1),
}
ALIGNMENTS = {"left": ">", "right": "<", "center": "^"}


class Table:
    def __init__(self, rows: list, title: str, style: Style, align: str, empty_cell: str,
                 max_w: int):
        self.rows = rows
        self.title = title
        self.style = style
        self.align = align
        self.empty_cell = empty_cell
        self.max_w = max_w
        self.header = self._set_up_header()
        self.line_above = self.get_line(self.style.line_above)
        self.line_below = self.get_line(self.style.line_below)
        self.line_below_header = self.get_line(self.style.line_below_header)

    def _set_up_header(self) -> list:
        header = []
        widths = {}
        pad = self.style.padding * 2
        for row in self.rows:
            for col_name, value in row.items():
                # find the widest cell in this column, capped at the max column width
                widths[col_name] = min(max([len(col_name) + pad,
                                            len(str(value)) + pad,
                                            widths.get(col_name, pad)]),
                                       self.max_w)

        # for each col, width, create a header entry with the actual column name, width of column,
        # and it's formatted name.
        for col, width in widths.items():
            # if 'COLUMN NAME' > max width, change to 'COL...' for legibility
            text = col
            if len(col) + pad > self.max_w:
                text = text[:2] + "..."
            header.append(HeaderEntry(col, width, text))
        return header

    def _format_cell(self, entry: str, w: int, align=None):
        return "{0:{1}{2}}".format(entry, ALIGNMENTS.get(align) or self.align, w)

    def get_line(self, line_style: Line) -> str:
        fill = line_style.fill
        row = {n: fill * w for n, w, t in self.header}
        return self.get_row([row], line_style)[0]

    def get_title(self) -> list:
        w = sum([t for n, w, t in self.header]) + len(self.header)
        begin = self.style.header_row.begin
        end = self.style.header_row.end
        return [self.get_line(self.style.title_above),
                begin + self._format_cell(self.title, w - 1, 'center') + end,
                self.get_line(self.style.title_below)]

    def get_header(self) -> list:
        begin = self.style.header_row.begin
        end = self.style.header_row.end
        sep = self.style.header_row.sep
        return [begin + sep.join([self._format_cell(t, w) for n, w, t in self.header]) + end,
                self.line_below_header]

    def get_row(self, f_row: list, row_style: Line or Row) -> list:
        begin = row_style.begin
        end = row_style.end
        sep = row_style.sep
        return [begin + sep.join([s_row[n] for n, w, t in self.header]) + end for s_row in f_row]

    def format_row(self, row: dict) -> list:
        # break each column in the row entry into a list of cells
        sub_rows = {n: self._split_cells(row.get(n, self.empty_cell))
                    for n, w, t in self.header}
        # add empty cells to fill up each column in the row
        total_sub_rows = max([len(s_row) for s_row in sub_rows.values()])
        for n, w, t in self.header:
            while len(sub_rows[n]) < total_sub_rows:
                sub_rows[n].append(" " * w)
        return [{n: self._format_cell(sub_rows[n][i], w) for n, w, t in self.header}
                for i in range(total_sub_rows)]

    def _split_cells(self, cell_str: str) -> list:
        cells = []
        # try to split the cell by spaces, if that doesn't work then just wrap the text
        while cell_str and len(cell_str) > self.max_w:
            entry = cell_str.strip().split(" ", maxsplit=1)[0]
            if len(entry) > self.max_w:
                entry = cell_str[:self.max_w]
            cells.append(entry)
            cell_str = cell_str[len(entry):]
        if cell_str:
            cells.append(cell_str)
        return cells


def generate_table(rows, table: Table) -> str:
    """
        --
        title (optional)
        --
        header
        --
        row 1
        ...
        row n
        ---
    """
    lines = []
    if table.title:
        lines.extend(table.get_title())
    else:
        lines.append(table.line_above)
    lines.extend(table.get_header())
    for row in rows:
        lines.extend(table.get_row(table.format_row(row), table.style.data_row))
    lines.append(table.get_line(table.style.line_below))
    output = "\n".join(lines)
    return output


def make_table(rows: List[Dict[str, str]], title="", style='grid', align="center",
               empty_cell="N/A", max_column_width=25) -> str:
    """
        create a formatted table for 'pretty' terminal/file outputting. table is returned as a
        single string with new line separated rows.
    Args:
        rows: list of dictionaries to format into a table. dict keys are used as column names.
            [
            { # row 1
                [column name]: [row value],
                ...
            },
            { # row 2
                ...
            },
            ... # row n
            ]
        title:              title text to go above the header for this table
        style:              table style choice [grid, fancy_grid]
        align:              cell value alignment [left, center, right]
        empty_cell:         default value to use for empty cells
        max_column_width:   set the max column width for all cells
    Returns:
        the table as a single string formatted and ready to be printed.
    """
    table = Table(rows=rows,
                  title=title,
                  style=STYLES[style],
                  align=ALIGNMENTS[align],
                  empty_cell=empty_cell,
                  max_w=max_column_width)
    return generate_table(rows, table)
