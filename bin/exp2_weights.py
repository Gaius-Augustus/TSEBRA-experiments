#!/usr/bin/env python3
# ==============================================================
# author: Lars Gabriel
#
# exp2_weights.py: Create directory and weights for Experiment 2.
# ==============================================================
import os
import csv
import argparse
import sys

evm_label = [['ABINITIO_PREDICTION', 'braker1'], ['ABINITIO_PREDICTION', 'braker2'], \
    ['TRANSCRIPT', 'PASA'], ['PROTEIN', 'Spaln_scorer']]
tsebra_label = ['P', 'E', 'intron_support', 'stasto_support', 'e_1', 'e_2',
    'e_3', 'e_4']

def main():
    args = parseCmd()
    bin_dir = os.path.dirname(os.path.realpath(__file__))

    # create EVM dir
    path_out = '{}/../{}/EVM/{}/'.format(bin_dir, args.species, args.test_level)
    if not os.path.exists(path_out):
        os.makedirs(path_out)

    test_key = '{};{}'.format(args.species, args.test_level)

    # get EVM weights
    evm_weights = csv_read("{}/exp2_weights/evm_weights.tab".format(bin_dir))
    print(evm_weights)
    print(test_key)
    weights = []
    for w in evm_weights:
        if w[0] == test_key:
            weights = w[1:]
            break
    print(weights)
    for i in range(0, len(evm_label)):
        weights[i] = evm_label[i] + [weights[i]]
    csv_write(weights, '{}/EVM.weights.tab'.format(path_out), '\t')

    # get TSEBRA weights
    tsebra_weights = csv_read("{}/exp2_weights/tsebra_weights.tab".format(bin_dir))
    weights = []
    for w in tsebra_weights:
        if w[0] == test_key:
            weights = w[1:]
            break
    csv_write(zip(tsebra_label, weights), '{}/tsebra.cfg'.format(path_out), ' ')
    
    sys.stderr.write('### Finished, weights are located in {}.\n'.format(path_out))

def csv_write(tab, out_path, d):
    with open(out_path, 'w+') as file:
        table = csv.writer(file, delimiter=d)
        for line in tab:
            print(line)
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
    parser = argparse.ArgumentParser(description='Create directory and weights for Experiment 2.')
    parser.add_argument('--species', type=str,
        help='Species name for the experiment, e.g. Drosophila_melanogaster')
    parser.add_argument('--test_level', type=str,
        help='One of "species_excluded", "family_excluded" or "order_excluded"')
    return parser.parse_args()

if __name__ == '__main__':
    main()
