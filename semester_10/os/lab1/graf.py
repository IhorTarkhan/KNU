import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sizes = [10, 100, 1_000, 10_000, 100_000, 1_000_000]

df = pd.read_csv('log.csv', delimiter=';')
df_split = np.array_split(df, 4)

fields = ['memory', 'operation', 'compare', 'swap', 'time']

for field in fields:
    fig, axis = plt.subplots(2, 2)
    fig.suptitle(field)
    fig.tight_layout(h_pad=2.0)
    ys = []
    for index in range(len(df_split)):
        df_chunk = pd.DataFrame(df_split[index])
        for _, row in df_chunk.iterrows():
            y = []
            for size in sizes:
                y.append(row[f'{field}_{size}'])
            name = row['name'].split(', ')[1].split('_')
            legend = name[1][:4] + ' ' + name[0][:4]
            axis[index // 2, index % 2].set_title(row['name'].split(', ')[0])
            axis[index // 2, index % 2].plot(sizes, y, 'o-', label=legend)
            ys.append(y)

    for axi in axis.flat:
        axi.set_xscale('log')

        max_x, max_y = sizes[-1], max([max(sublist) for sublist in ys])
        axi.set_xlim(-max_x * 0.1, max_x * 1.1)
        axi.set_ylim(-max_y * 0.1, max_y * 1.1)

    plt.subplots_adjust(right=0.8)
    plt.legend(bbox_to_anchor=(1, 1))
    plt.show()
