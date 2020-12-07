from rich.console import Console
from rich.table import Column, Table
from rich.padding import Padding
from rich.panel import Panel
from rich import box


def end(style):
    return style[0]+'/'+style[1:]

def format_val(value):
    if isinstance(value, float):
        return str(round(value, 2))+'%'
    else:
        return str(value)

def get_summary_panel(info_dict, bar_size=30, expand=True, v_pad=1, h_pad=2):
    all_text = ''
    for device in info_dict:
        mem_pct = info_dict[device]['percent']
        m = int(mem_pct*bar_size/100.)
        s = bar_size-m
        if 'gpu' not in device:
            style = '[color(255) on bright_red]'
        else:
            style = '[color(255) on bright_green]'
        used_mem = info_dict[device]['used']
        total_mem = info_dict[device]['total']
        t = '{} Memory: {} {} {}'.format(device, style, ' '*m, end(style))
        t +='{} {}%     Used: {}G   Total: {}G\n'.format(' '*s, mem_pct, used_mem, total_mem)

        all_text +=t

    text = Padding(all_text, (v_pad, h_pad))
    return Panel(text, expand=expand)


def get_usage_table(df, top_n, expand=True):
    box_style = box.SQUARE
    notebook_style = 'color(255) on magenta'
    show_cols = ['Name', 'PID', 'CPU Memory (%)', 'GPU Memory (%)', 'State']
    show_cols = [col for col in show_cols if col in df.columns]
    table = Table(show_header=True, box=box_style, expand=expand)
    table.add_column("Notebook", header_style=notebook_style, overflow='fold')
    for col in show_cols[1:]:
        table.add_column(col, justify='center')

    if top_n==-1:
        max_rows = len(df)
    else:
        max_rows = min(top_n, len(df))

    for row in range(max_rows):
        values = df.iloc[row][show_cols]
        values = [format_val(i) for i in values]
        table.add_row(*values)
    return table

def console_print(printables):
    console = Console()
    for printable in printables:
        console.print(printable)
    return console
