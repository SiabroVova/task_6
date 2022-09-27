from datetime import datetime
import click
from pathlib import Path

global report_difference_dict
global abb_dict  # dictionary for list_for_abb
global list_for_result
abb_dict = {}

def build_report(folder='docs', param=None):
    """
    Function for building report from files with start and end data.
    Func opens two files, read it, create lists, sort it and then create dicts from lists.
    :return: sorted dictionary with abbreviations in keys and time difference in values and dict with full names and cars.
    """
    report_start_list, report_end_list = [], []  # lists for strings from start & end logs

    prog_folder = Path.cwd()

    """Creates dict from START data file with abbreviation in keys and time in values """
    with open(Path(prog_folder) / str(folder) / 'start.log', 'r') as f_start:
        [report_start_list.append(line.rstrip()) for line in f_start]
        report_start_list.sort()
    report_start_dict = {string[0:3]: string[14:26] for string in report_start_list}

    """Creates dict from END data file with time format in values """
    with open(Path(prog_folder) / str(folder) / 'end.log', 'r') as f_end:
        [report_end_list.append(line.rstrip()) for line in f_end]
        report_end_list.sort()
    report_end_dict = {string[0:3]: string[14:26] for string in report_end_list}

    """Filling third dict for results"""
    report_difference_dict = {keys: 0 for keys in report_start_dict.keys()}  # collecting keys
    for key in report_difference_dict.keys():
        report_difference_dict[key] = str(
            datetime.strptime(
                report_end_dict[key], '%H:%M:%S.%f') - datetime.strptime(report_start_dict[key], '%H:%M:%S.%f')
        )[:-3]  # collecting values

    """Sorting difference dict by time, which depends from parameter: asc - sorted, desc - reversed"""
    if param==None or param == "asc":
        report_difference_dict = dict(sorted(report_difference_dict.items(), key=lambda item: item[1]))
    elif param == "desc":
        report_difference_dict = dict(sorted(report_difference_dict.items(), key=lambda item: item[1], reverse=True))

    list_for_abb = []  # list for names and cars from abbreviations file
    with open(Path(prog_folder) / str(folder) / 'abbreviations.txt', 'r', encoding="utf-8") as f_abb:
        [list_for_abb.append(line.rstrip()) for line in f_abb]

    for string in list_for_abb:
        index_for_cut = string.find('_', 4)
        abb_dict.update({string[0:3]: [string[4:index_for_cut], string[index_for_cut + 1:]]})

    return report_difference_dict


def print_report(diff, name=None):
    """
    Function for printing report according to requirements.
    Printing with sequence numbers, full names, car details and time difference.
    :return: None, just organizing appropriate output of results.
    """

    if name!=None:
        for key in diff.keys():
            if abb_dict[key][0] == name:
                return abb_dict[key][0], " | ", abb_dict[key][1], " | ", diff[key]

    else:
        number = 1
        list_for_result = []
        for key in diff.keys():
            term_dict_for_results = {'number': number, 'name': abb_dict[key][0], 'car': abb_dict[key][1], 'time': diff[key]}
            list_for_result.append(term_dict_for_results)
            number += 1
            # if number == 16:
            #     list_for_result.append("-" * 70)
        return list_for_result

@click.command()
@click.option('--files', '-f', type=str, default=None, help='input the folder in which storing all docs')
@click.option('--driver', '-d', type=str, default=None, help='input driver name to see statistic for him')
@click.option('--sort', '-p', type=str, default=None, help='input type of sorting the data')

def main(files, driver, sort):
    print_report(build_report(folder=files, param=sort), name=driver)


if __name__ == '__main__':
    main()
