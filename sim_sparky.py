import numpy as np
import argparse
import nmrglue as ng
import sys

# Simulate 2D NMR spectra in SPARKY format from a peak list file.
#
# Written by: Daniel K. Weber
# Affiliation: University of Minnesota, MN, USA
# Funding sources: NIH R01GM064742 and NIH R01HL144130 (Gianluigi Veglia). AHA 19POST34420009 (DW).


def residue_letter(resname):
    '''Convert 3-letter amino acid code to 1-letter code.
    '''
    conversion = {
        "ALA": "A",
        "ARG": "R",
        "ASN": "N",
        "ASP": "D",
        "CYS": "C",
        "GLN": "Q",
        "GLU": "E",
        "GLY": "G",
        "HIS": "H",
        "HSE": "H",
        "HID": "H",
        "HSD": "H",
        "HSP": "H",
        "ILE": "I",
        "LEU": "L",
        "LYS": "K",
        "MET": "M",
        "PHE": "F",
        "PRO": "P",
        "SER": "S",
        "THR": "T",
        "TRP": "W",
        "TYR": "Y",
        "VAL": "V",
        "ASX": "B",
        "GLX": "Z"
    }
    try:
        return conversion[resname]
    except KeyError:
        print('WARNING! Unknown residue name \'{}\'. Single letter code \'U\' will be used.'.format(resname))
        return "U"


def split_correlations(correlations):
    #correlations = correlations.split()
    assert len(correlations) % 2 == 0, 'Odd number of correlations detected. Correlations must be paired'
    correlations = [correlations[i * 2:(i + 1) * 2] for i in range((len(correlations) + 2 - 1) // 2 )]
    return correlations


def read_csv(csv_file):
    r_ids = np.genfromtxt(csv_file,usecols=(0),dtype=int)
    r_names = np.genfromtxt(csv_file,usecols=(1),dtype=str)
    r_names = [ residue_letter(i) for i in r_names ]
    a_names = np.genfromtxt(csv_file,usecols=(2),dtype=str)
    shifts = np.genfromtxt(csv_file,usecols=(3),dtype=float)
    return zip(r_ids,r_names,a_names,shifts)


def parse_args():
    parser = argparse.ArgumentParser(description='Simulate spectra from peak list.',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        '-i', '--infile', type=str,
        help='Input file name with accepted format.'
    )
    parser.add_argument(
        '-o', '--out_prefix', type=str, default='hsqc',
        help='Output prefix for peak list (.list) and spectrum (.ucsf) file. Default: hsqc.'
    )
    parser.add_argument(
        '-t', '--file_type', type=str, choices=['csv'],
        help='Input file format. Default: CSV (r_id, r_name, a_name, shift)'
    )
    parser.add_argument(
        '-c', '--intra_corr', type=str, nargs='+', default=['H','N','HD21','ND2','HD22','ND2','HE21','NE2','HE22','NE2','HE1','NE1'],
        help='Pair-wise intra-residue peak correlations. Default: H N HD21 ND2 HD22 ND2 HE21 NE2 HE22 NE2 HE1 NE1. (I.e. H-N HSQC).'
    )
    parser.add_argument(
        '-s', '--inter_corr', type=int, nargs='+', default=[0],
        help='Sequential connectivities. Default: 0 (I.e. Intra-residue connections only, H-N HSQC.).'
    )
    parser.add_argument(
        '--nuc1_label', type=str,
        help='Label for nucleus 1 (direct dimension). Default: 1H.',
        default='1H'
    )
    parser.add_argument(
        '--nuc2_label', type=str,
        help='Label for nucleus 2 (indirect dimension). Default: 15N.',
        default='15N'
    )
    parser.add_argument(
        '--nuc1_freq', type=float,
        help='Frequency of nucleus 1 in MHz. Default: 600.00.',
        default=600.0000000
    )
    parser.add_argument(
        '--nuc2_freq', type=float,
        help='Frequency of nucleus 2 in MHz. Default: 60.7639142.',
        default=60.7639142
    )
    parser.add_argument(
        '--nuc1_center', type=float,
        help='Center position of nucleus 1 in PPM. Default: 8.30.',
        default=8.30
    )
    parser.add_argument(
        '--nuc2_center', type=float,
        help='Center position of nucleus 2 in PPM. Default: 120.00.',
        default=120.00
    )
    parser.add_argument(
        '--nuc1_sw', type=float,
        help='Spectral width of nucleus 1 in PPM. Default: 4.00.',
        default=4.00
    )
    parser.add_argument(
        '--nuc2_sw', type=float,
        help='Spectral width of nucleus 1 in PPM. Default: 20.00.',
        default=20.00
    )
    parser.add_argument(
        '--nuc1_size', type=int,
        help='Number of points in nucleus 1 dimension. Default: 4096.',
        default=4096
    )
    parser.add_argument(
        '--nuc2_size', type=int,
        help='Number of points in nucleus 2 dimension. Default: 4096.',
        default=4096
    )
    args = parser.parse_args()
    return args


def main():

    # Read args and assign parameters.
    args = parse_args()
    infile = args.infile
    out_prefix = args.out_prefix
    file_type = args.file_type
    intra_corr = split_correlations(args.intra_corr)
    inter_corr = args.inter_corr
    nuc1_label = args.nuc1_label
    nuc2_label = args.nuc2_label
    nuc1_freq = args.nuc1_freq
    nuc2_freq = args.nuc2_freq
    nuc1_center = args.nuc1_center
    nuc2_center = args.nuc2_center
    nuc1_sw = args.nuc1_sw
    nuc2_sw = args.nuc2_sw
    nuc1_size = args.nuc1_size
    nuc2_size = args.nuc2_size
    
    # Read in data from specified file format
    if file_type == 'csv':
        print('Reading CSV data from {}...'.format(infile))
        data = read_csv(infile)

    # Arrange data into dictionaries.
    data_shifts = {}
    data_rnames = {}
    data_atypes = {}
    for r_id, r_name, a_name, shift in data:
        try:
            data_shifts[r_id][a_name] = shift
        except KeyError:
            data_shifts[r_id] = {}
            data_shifts[r_id][a_name] = shift
        try:
            data_atypes[r_id][a_name] = a_name[0][:1]
        except KeyError:
            data_atypes[r_id] = {}
            data_atypes[r_id][a_name] = a_name[0][:1]
        data_rnames[r_id] = r_name           
    print('Read chemical shifts for {} residues.'.format(len(data_shifts.keys())))
        
    # Interate through each residue and find correlations. Output to Sparky peak list file.
    fo = open(out_prefix+'.list', 'w')
    fo.write('      Assignment         w1         w2  \n\n')
    num_intra = 0
    for r_id in data_shifts.keys():
        
        # Iterate through intra-residue correlations
        for c in intra_corr:
            try:
                shift1 = str(data_shifts[r_id][c[0]])
                shift1 = shift1.rjust(11,' ')
                shift2 = str(data_shifts[r_id][c[1]])
                shift2 = shift2.rjust(11,' ')
                assignment = data_rnames[r_id]+str(r_id)+c[1]+'-'+c[0]
                assignment = assignment.rjust(17)
                fo.write('{}{}{}\n'.format(assignment,shift2,shift1))
                num_intra += 1
            except KeyError:
                pass
    fo.close()
    print('List of {} peaks output to {}.list.'.format(num_intra,out_prefix))
    # Iterate through inter-residue connections
    # Mirror for homonuclear spectra

    
    # Simulate Sparky spectrum file from peak list
    # Make NMRGlue universal dictionary
    nuc1_center_hz = nuc1_freq*nuc1_center
    nuc2_center_hz = nuc2_freq*nuc2_center
    nuc1_sw_hz = nuc1_freq*nuc1_sw
    nuc2_sw_hz = nuc2_freq*nuc2_sw
    
    udic = {
        'ndim': 2,
        0: {'car': nuc2_center_hz,
            'complex': False,
            'encoding': 'states',
            'freq': True,
            'label': nuc2_label,
            'obs': nuc2_freq,
            'size': nuc2_size,
            'sw': nuc2_sw_hz,
            'time': False},
        1: {'car': nuc1_center_hz,
            'complex': False,
            'encoding': 'direct',
            'freq': True,
            'label': nuc1_label,
            'obs': nuc1_freq,
            'size': nuc1_size,
            'sw': nuc1_sw_hz,
            'time': False}
    }
    dic = ng.sparky.create_dic(udic)
    data = np.empty((nuc1_size, nuc2_size), dtype='float32')

    # read in the peak list
    peak_list = np.recfromtxt(out_prefix+'.list', names=True)
    npeaks = len(peak_list)

    # convert the peak list from PPM to points
    uc_nuc2 = ng.sparky.make_uc(dic, None, 0)
    uc_nuc1 = ng.sparky.make_uc(dic, None, 1)

    nuc1_lw = 20
    nuc2_lw = 20
    lw_nuc1 = (nuc1_lw/nuc1_sw_hz)*nuc1_size    # Nuc1 dimension linewidth in points
    lw_nuc2 = (nuc2_lw/nuc2_sw_hz)*nuc2_size    # Nuc2 dimension linewidth in points

    params = []
    for name, ppm_nuc2, ppm_nuc1 in peak_list:
        pts_nuc1 = uc_nuc1.f(ppm_nuc1, 'ppm')
        pts_nuc2 = uc_nuc2.f(ppm_nuc2, 'ppm')
        params.append([(pts_nuc2, lw_nuc2), (pts_nuc1, lw_nuc1)])

    # simulate the spectrum
    shape = (nuc2_size, nuc1_size)      # size should match the dictionary size
    lineshapes = ('g', 'g')  # gaussian in both dimensions
    amps = [100.0] * npeaks
    data = ng.linesh.sim_NDregion(shape, lineshapes, params, amps)

    # save the spectrum
    ng.sparky.write(out_prefix+'.ucsf', dic, data.astype('float32'), overwrite=True)
    
if __name__ == '__main__':
    main()

