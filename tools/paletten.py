# Erzeugt die Paletten-Tabellen für PlotTransformer.html aus matplotlib/seaborn.
import matplotlib, seaborn as sns
from matplotlib import colors as mc
hx = lambda c: mc.to_hex(c).upper().lstrip('#')
cat = {}
for n in ['tab10', 'tab20', 'Set1', 'Set2', 'Dark2', 'Paired']:
    cat[n] = [hx(c) for c in matplotlib.colormaps[n].colors]
for n in ['deep', 'muted', 'pastel', 'bright', 'dark', 'colorblind']:
    cat[n] = [hx(c) for c in sns.color_palette(n)]
for st, n in [('ggplot', 'ggplot'), ('fivethirtyeight', '538'), ('bmh', 'bmh')]:
    cat[n] = [hx(c) for c in matplotlib.style.library[st]['axes.prop_cycle'].by_key()['color']]
seq = {}
for n in ['viridis', 'plasma', 'cividis', 'rocket', 'mako', 'Blues', 'RdBu', 'coolwarm', 'vlag']:
    cm = matplotlib.colormaps[n] if n in matplotlib.colormaps else sns.color_palette(n, as_cmap=True)
    seq[n] = [hx(cm(i / 10)) for i in range(11)]
print('const CAT_PAL = {')
for k, v in cat.items(): print(f"  '{k}': '{' '.join(v)}',")
print('};\nconst SEQ_PAL = {')
for k, v in seq.items(): print(f"  '{k}': '{' '.join(v)}',")
print('};')
