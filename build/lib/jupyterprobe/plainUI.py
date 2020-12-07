
def get_summary_panel(info_dict, bar_size=30, expand=True, v_pad=1, h_pad=2):
    all_text = ''
    for device in info_dict:
        mem_pct = info_dict[device]['percent']
        m = int(mem_pct*bar_size/100.)
        s = bar_size-m

        used_mem = info_dict[device]['used']
        total_mem = info_dict[device]['total']

        t = '{} Memory: {}'.format(device, '#'*m,)
        t +='{} {}%     Used: {}G   Total: {}G\n'.format(' '*s, mem_pct, used_mem, total_mem)

        all_text +=t

    return all_text


def get_usage_table(df, top_n, expand=True):
    return df.reset_index().iloc[:, 1:].round(2)

def console_print(printables):
    for printable in printables:
        print(printable)
        print('\n')
    return None
