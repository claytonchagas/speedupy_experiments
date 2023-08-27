import os
import matplotlib.pyplot as plt
import numpy as np
from gen_data_from_raw import gen_data_from_raw
import pandas as pd
import sys

labels = ['2d-ad-t', '1d-ow', '1d-ad', '2d-ad', 'ad', '2d-ad-f', '2d-ad-ft', '2d-lz', "--no-cache"]
set_labels = ['md5', 'xxhash', 'murmur']

def gen_table_data(f_data):
    n_data = {}

    time_no_cache = f_data['no-cache']['no-cache']['no-cache']

    for ks in f_data:
        if ks != 'no-cache':
            n_data[ks] = []
            for memo in labels:
                if memo != "--no-cache":
                    n_data[ks].append([f_data[ks][hash][memo] for hash in set_labels])

            n_data[ks].append([time_no_cache, time_no_cache, time_no_cache])

            n_data[ks] = np.array(n_data[ks], dtype=float)

    return n_data


def create_graph(data, title,graph_num):
    x = np.arange(len(labels))
    width = 0.2

    fig, ax = plt.subplots(figsize=(8,6))

    for i, set_label in enumerate(set_labels):
        ax.bar(x + i * width, data[:, i], width, label=set_label)
        for j, value in enumerate(data[:, i]):
            gp = value - max(data[:, i]) * 0.12 if value - max(data[:, i]) * 0.5 > 0 else value + max(data[:, i]) * 0.03
            ax.text(x[j] + i * width, gp, f'{value:.7f}', ha='center',rotation=90, fontsize=7)
            
    ax.set_xlabel('Memos')
    ax.set_ylabel('Tempo em Segundos')
    ax.set_title(title)
    ax.set_xticks(x + width)
    ax.set_xticklabels(labels)
    ax.legend()

    plt.xticks(rotation=22)
    plt.tight_layout()
    plt.savefig(f'./results/{title}_{graph_num}.png', bbox_inches='tight')
    plt.clf()

def create_table(table, ks):
    table_data = pd.DataFrame(table, columns=set_labels, index=labels)
    table_data.insert(0,ks,"       ")
    print(table_data)

def main():
    try:
        graph_num = int(sys.argv[1])
    except IndexError:
        graph_num = 0

    os.system(f"rm -rf results/*_{graph_num}.png")
    f_data, min_param = gen_data_from_raw(graph_num) # Podemos inserir varios graficos a partir do argumento dado; como testar? fibos!
    n_data            = gen_table_data(f_data)
    storage, hash, memo, tm = min_param
    for ks in n_data:
        create_table(n_data[ks],ks)
        create_graph(n_data[ks],ks,graph_num)
        print(f"Done {ks}")
    print(f'Champion: {storage} {hash} {memo} time: {tm}') if memo != "no-cache" else print(f"Champion: --no-cache time {tm}")


if __name__ == '__main__':
    main()
