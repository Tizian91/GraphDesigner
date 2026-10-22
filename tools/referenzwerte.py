# Berechnet Vergleichswerte für tests.html mit numpy/scipy/seaborn.
import json, numpy as np, pandas as pd, seaborn as sns, matplotlib
matplotlib.use('Agg')
from scipy import stats
a = np.array([2.5, 3.1, 4.7, 1.2, 9.8, 5.5, 6.0, 3.3, 7.7, 4.4, 2.2])
n = len(a); sd = a.std(ddof=1); se = sd / np.sqrt(n)
ref = {
  'mean': a.mean(), 'median': float(np.median(a)), 'sd': sd, 'se': se, 'ci': stats.t.ppf(0.975, n - 1) * se,
  'q1': float(np.percentile(a, 25)), 'q3': float(np.percentile(a, 75)),
  't975_df1': stats.t.ppf(0.975, 1), 't975_df5': stats.t.ppf(0.975, 5), 't975_df30': stats.t.ppf(0.975, 30),
}
v = pd.read_csv('samples/verteilung.tsv', sep='\t')['Messwert'].to_numpy()
e = np.histogram_bin_edges(v, 'fd'); c, _ = np.histogram(v, e)
ref['fd_n'] = len(e) - 1; ref['fd_e0'] = e[0]; ref['fd_e1'] = e[1]; ref['fd_counts'] = c.tolist()
kde = stats.gaussian_kde(a); ref['kde_at_5'] = float(kde(5.0)[0])
# seaborn barplot: Mittelwert und 95-%-KI (Bootstrap) je Zeit x Gruppe
df = pd.read_csv('samples/gruppen.csv')
ax = sns.barplot(df, x='Zeit', y='Wert', hue='Gruppe', errorbar=('ci', 95), seed=0)
bars = []
for cont, (g, _) in zip(ax.containers, df.groupby('Gruppe', sort=False)):
    for z, p in zip(sorted(df.Zeit.unique()), cont):
        bars.append([g, int(z), p.get_height()])
lines = ax.get_lines()
ci = [[l.get_ydata()[0], l.get_ydata()[1]] for l in lines]
for b, c2 in zip(bars, ci): b += c2
ref['sns_bars'] = bars
print(json.dumps(ref))
