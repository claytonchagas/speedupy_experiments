import matplotlib.pyplot as plt
import numpy as np
from gen_data_from_raw import gen_data_from_raw

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


def create_graph(data, title):
    x = np.arange(len(labels))
    width = 0.2

    fig, ax = plt.subplots(figsize=(8,6))

    for i, set_label in enumerate(set_labels):
        ax.bar(x + i * width, data[:, i], width, label=set_label)
        for j, value in enumerate(data[:, i]):

            gp = value - max(data[:, i]) * 0.12 if value - max(data[:, i]) * 0.5 > 0 else value + max(data[:, i]) * 0.03
            #ax.text(x[j] + i * width, value + 0.2, f'{value:.4f}', ha='center', va='bottom', rotation=90, fontsize=8)
            #ax.text(x[j] + i * width, value + 0.2, f'{value:.2f}', ha='center', rotation=90, fontsize=8)
            ax.text(x[j] + i * width, gp, f'{value:.7f}', ha='center',rotation=90, fontsize=7)
            # bars = ax.bar(x + i * width, data[:, i], width, label=set_label)
            # ax.bar_label(bars, fmt='%.2f', label_type='edge')

    ax.set_xlabel('Memos')
    ax.set_ylabel('Tempo em Segundos')
    ax.set_title(title)
    ax.set_xticks(x + width)
    ax.set_xticklabels(labels)
    ax.legend()

    plt.xticks(rotation=22)
    plt.tight_layout()
    # plt.savefig(f'./results/{title}.png', bbox_inches='tight')
    # plt.clf()
    plt.show()


def main():
    f_data = gen_data_from_raw()
    n_data = gen_table_data(f_data)
    for ks in n_data:
        create_graph(n_data[ks], ks)
        #####
        break


if __name__ == '__main__':
    main()
