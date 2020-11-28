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

def get_summary_panel(cpu_mem_pct, gpu_mem_pct, bar_size=30, expand=True, v_pad=1, h_pad=2):
    cm = int(cpu_mem_pct*bar_size/100.)
    cs = bar_size-cm
    gm = int(gpu_mem_pct*bar_size/100.)
    gs = bar_size-gm

    cpu_style = '[color(255) on bright_red]'
    gpu_style = '[color(255) on bright_green]'

    gpu_t = 'GPU Memory: {} {} {}'.format(gpu_style, ' '*gm, end(gpu_style))
    gpu_t +='{} {}%\n'.format(' '*gs, gpu_mem_pct)
    cpu_t = 'CPU Memory: {} {} {}'.format(cpu_style, ' '*cm, end(cpu_style))
    cpu_t +='{} {}%'.format(' '*cs, cpu_mem_pct)

    text = Padding(gpu_t+cpu_t, (v_pad, h_pad))
    return Panel(text, expand=expand)


def get_usage_table(df, top_n, expand=True):
    box_style = box.SQUARE
    notebook_style = 'color(255) on magenta'

    table = Table(show_header=True, box=box_style, expand=expand)
    table.add_column("Notebook", header_style=notebook_style)
    table.add_column("PID", justify='center')
    table.add_column("CPU Memory", justify='center')

    for row in range(min(top_n, len(df))):
        values = df.iloc[row][['Name', 'PID', 'CPU Memory']]
        values = [format_val(i) for i in values]
        table.add_row(*values)
    return table

def console_print(printables):
    console = Console()
    for printable in printables:
        console.print(printable)
    return console
