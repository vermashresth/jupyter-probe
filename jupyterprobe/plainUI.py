from jupyterprobe.config import COL_LIST, NO_TEAM_COL_NAMES, TEAM_COL_NAMES

def get_summary_panel(results, pid, info_dict, bar_size=30, expand=True, v_pad=1, h_pad=2):
    all_text = ''
    for device in info_dict:
        mem_pct = info_dict[device]['percent']
        m = int(mem_pct*bar_size/100.)
        s = bar_size-m

        used_mem = info_dict[device]['used']
        total_mem = info_dict[device]['total']

        t = '{} Memory: {}'.format(device, '#'*m,)
        t +=' {}% {}     Used: {}G   Total: {}G\n'.format(mem_pct, ' '*s, used_mem, total_mem)

        all_text +=t
    all_text += current_nb_summary(results, pid)
    return all_text

def current_nb_summary(results, pid):
    info = results[results['PID']==pid]
    text = '\nCurrent notebook uses {} CPU memory'.format(str(round(info['CPU Memory (%)'].iloc[0], 2))+'%')
    if 'GPU Memory (%)' in info.columns:
        text += ' and {} GPU memory'.format(info['GPU Memory (%)'])
    text+='. '
    declared = False
    if info['Owner'].iloc[0] != '-':
        text += '\nOwner: {},  '.format(info['Owner'].iloc[0])
        decalared=True
    if info['Priority'].iloc[0] != '-':
        text += 'Priority: {},  '.format(info['Priority'].iloc[0])
        declared=True
    if info['Project'].iloc[0] != '-':
        text += 'Project: {} '.format(info['Project'].iloc[0])
        declared=True
    if not declared:
        text += 'Yet to declare experiment ownership.'
    return text

def get_usage_table(df, top_n, is_team, expand=True):
    out =  df.reset_index().iloc[:, 1:].round(2)
    out['CPU Memory (%)'] = out['CPU Memory (%)'].apply(lambda x: str(x)+'%')

    if is_team:
        col_dict = TEAM_COL_NAMES
    else:
        col_dict = NO_TEAM_COL_NAMES

    show_cols = []
    for col_id in list(col_dict.keys()):
        if COL_LIST[col_id] not in df.columns:
            continue
        show_cols.append(COL_LIST[col_id])

    return out[show_cols]

def console_print(printables):
    for printable in printables:
        print(printable)
        print('\n')
    return None
