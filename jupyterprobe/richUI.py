from rich.console import Console
from rich.table import Column, Table
from rich.padding import Padding
from rich.panel import Panel
from rich import box, print as rprint

from jupyterprobe.config import COL_LIST, NO_TEAM_COL_NAMES, TEAM_COL_NAMES

def end(style):
    return style[0]+'/'+style[1:]

def preprocess_df(df_in):
    df = df_in.copy()
    memory_cols = [cols for cols in df.columns if cols.endswith('Memory (%)')]
    for col in memory_cols:
        df[col] = df[col].apply(lambda x: str(round(x, 2))+'%')
    if 'Priority' in df.columns:
        df['Priority'] = df['Priority'].apply(lambda x: str(x).split('.')[0])
    return df.astype(str)

def get_summary_panel(results, pid, info_dict, bar_size=30, expand=True, v_pad=1, h_pad=2):
    all_text = '[bold]Probe Summary[/bold]\n\n'
    for device in info_dict:
        mem_pct = info_dict[device]['percent']
        m = int(mem_pct*bar_size/100.)
        s = bar_size-m
        if device.startswith('GPU'):
            style = '[color(255) on bright_green]'
        else:
            style = '[color(255) on bright_red]'
        used_mem = info_dict[device]['used']
        total_mem = info_dict[device]['total']
        t = '{} Memory: {} {} {}'.format(device, style, ' '*m, end(style))
        t +=' {}% {}     Used: {}G   Total: {}G\n'.format(mem_pct, ' '*s, used_mem, total_mem)

        all_text +=t
    all_text += current_nb_summary(results, pid)
    text = Padding(all_text, (0, h_pad))
    return Panel(text, expand=expand)

def current_nb_summary(results, pid):
    info = results[results['PID']==pid]
    text = '\nCurrent notebook uses {} of CPU memory'.format(str(round(info['CPU Memory (%)'].iloc[0], 2))+'%')
    if 'GPU Memory (%)' in info.columns:
        text += ' and {} of GPU memory'.format(str(round(info['GPU Memory (%)'].iloc[0], 2))+'%')
    text+='. '
    declared = False
    if info['Owner'].iloc[0] != '-':
        text += '\nOwner: {},  '.format(info['Owner'].iloc[0])
        decalared=True
    if info['Priority'].iloc[0] != '-':
        text += 'Priority: {},  '.format(int(info['Priority'].iloc[0]))
        declared=True
    if info['Project'].iloc[0] != '-':
        text += 'Project: {} '.format(info['Project'].iloc[0])
        declared=True
    if not declared:
        text += 'Yet to declare experiment ownership.'
    return text

def get_usage_table(df, top_n, is_team, expand=False):
    df = preprocess_df(df)
    box_style = box.SQUARE
    notebook_style = 'color(255) on magenta'

    table = Table(show_header=True, box=box_style, expand=expand)
    table.add_column("S.No.", justify='center')

    if is_team:
        col_dict = TEAM_COL_NAMES
    else:
        col_dict = NO_TEAM_COL_NAMES

    show_cols = []
    for col_id in list(col_dict.keys()):
        if COL_LIST[col_id] not in df.columns:
            continue
        if col_id == 0:
            table.add_column("Notebook", header_style=notebook_style, overflow='fold')
        else:
            table.add_column(col_dict[col_id], justify='center')
        show_cols.append(COL_LIST[col_id])

    if top_n==-1:
        max_rows = len(df)
    else:
        max_rows = min(top_n, len(df))

    for row in range(max_rows):
        values = [str(row)]+list(df.iloc[row][show_cols])
        table.add_row(*values)
    return table

def console_print(printables):
    titles = ['Summary', 'Notebook Resource Usage', 'Notebook Ownership']
    console = Console()
    for idx, printable in enumerate(printables):
        # rprint(" [bold]{}[/bold]".format(titles[idx]))
        console.print(printable)
        # print('')
    return console
