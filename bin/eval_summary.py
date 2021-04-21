#!/usr/bin/env python3
# ==============================================================
# author: Lars Gabriel
#
# eval_exp2.py: Collect the evaluations of multiple species and test level
# ==============================================================
import argparse
import os
import csv
import sys

exp_bin = os.path.dirname(os.path.realpath(__file__))
measures = ['F1', 'Sn', 'Sp']
modes = ['cds', 'trans', 'gene']
test_level = ['species_excluded', 'family_excluded', 'order_excluded']
methods = ['BRAKER1', 'BRAKER2', 'EVM', 'TSEBRA_EVM', 'TESEBRA_default']
workdir = ''

def main():
    global workdir
    args = parseCmd()

    workdir = os.path.abspath(args.parent_dir)

    # read names of species and model_species
    species_list = csv_read('{}/../species.tab'.format(exp_bin))
    species_list = [s for s, in species_list if not s[0] == '#']

    # table header
    header = []
    line = ['# species']
    for mo in modes:
        line += [' ', ' ', mo, ' ', ' ']
    header.append(line)
    header.append(['#'] + methods*3)

    # table body
    for mea in measures:
        out_tab = header
        for species in species_list:
            for level in test_level:
                species_key = ['{}_{}'.format(species, level)]
                # check if exp2 has been conducted
                tab_path = '{}/{}/EVM/{}/evaluation/{}.eval.tab'.format(workdir, \
                    species, level, mea)
                if os.path.exists(tab_path):
                    tab = csv_read(tab_path)
                    out_tab.append(species_key + tab[-1])
                    continue

                # else check for results from exp1
                tab_path = '{}/{}/tsebra_default/{}/{}.eval.tab'.format(workdir, \
                    species, level, mea)
                if os.path.exists(tab_path):
                    tab = csv_read(tab_path)
                    line = species_key
                    for i in range(0, len(tab[-1])):
                        if i%3 == 2:
                            line += [' ', ' ']
                        line.append(tab[-1][i])
                    out_tab.append(line)

        csv_write(out_tab, '{}/{}.eval.tab'.format(workdir, mea))

def csv_write(tab, out_path):
    with open(out_path, 'w+') as file:
        table = csv.writer(file, delimiter='\t')
        for line in tab:
            table.writerow(line)

def csv_read(file_path):
    result = []
    with open(file_path, 'r') as file:
        lines = csv.reader(file, delimiter='\t')
        for line in lines:
            if line:
                result.append(line)
    return result

def parseCmd():
    """Parse command line arguments

    Returns:
        dictionary: Dictionary with arguments
    """
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--parent_dir', type=str,
        help='')
    return parser.parse_args()

if __name__ == '__main__':
    main()
