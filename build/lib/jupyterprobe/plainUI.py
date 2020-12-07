
def get_summary_panel(cpu_mem_pct, gpu_mem_pct, bar_size=30, expand=True, v_pad=1, h_pad=2):
    cm = int(cpu_mem_pct*bar_size/100.)
    cs = bar_size-cm
    gm = int(gpu_mem_pct*bar_size/100.)
    gs = bar_size-gm

    gpu_t = 'GPU Memory: {}'.format('#'*gm,)
    gpu_t +='{} {}%\n'.format(' '*gs, gpu_mem_pct)
    cpu_t = 'CPU Memory: {}'.format('#'*cm)
    cpu_t +='{} {}%'.format(' '*cs, cpu_mem_pct)

    text = gpu_t+cpu_t
    return text


def get_usage_table(df, top_n, expand=True):
    return df.reset_index().iloc[:, 1:].round(2)

def console_print(printables):
    for printable in printables:
        print(printable)
        print('\n')
    return None
