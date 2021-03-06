import argparse
import sys, csv
from open_fda_api import get_fda_info
from seer_api import get_rx_info


def parse_args(argv: list) -> argparse.Namespace:
    """Parse the inputs options
    Args:
        argv (list): list of arguments
    Returns:
        argparse.Namespace:
    """
    usage = "python drug_info.py OPTIONS"
    desc = (
        "Get info of the drugs from https://seer.cancer.gov/ and https://open.fda.gov/"
    )
    parser = argparse.ArgumentParser(
        description=desc,
        usage=usage,
    )
    parser.add_argument(
        "-i",
        "--input",
        dest="in_file",
        metavar="IN_FILE",
        help="input file name",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="out_name",
        metavar="OUT_NAME",
        help="Output file name",
        required=True,
    )
    args, _ = parser.parse_known_args(argv)
    return args


def save_data(data, out_file):
    with open(out_file, "w") as oF:
        header = data[0].keys()
        writer = csv.DictWriter(
            oF, fieldnames=list(header), delimiter="\t", quoting=csv.QUOTE_NONNUMERIC
        )
        writer.writeheader()
        writer.writerows(data)


def drug_info(args: list = None):
    if args is None:
        args = sys.argv

    argv = parse_args(args)
    with open(argv.in_file) as oF:
        drugList = [x.strip() for x in oF]

    FDA_info = []
    for entry in drugList:
        print(f"FDA searching for {entry}:")
        info = get_fda_info(entry)
        if not info["found_flag"]:
            print(f"OPEN FDA: Cannot find {entry}", file=sys.stderr)
        FDA_info.append(info)

    seer_info = []
    for entry in drugList:
        print(f"SEER searching for {entry}:")
        info = get_rx_info(entry)
        if not info["found_flag"]:
            print(f"SEER Cancer.gov: Cannot find {entry}", file=sys.stderr)
        seer_info.append(info)

    out_file_fda = argv.out_name + "_fda.tsv"
    save_data(FDA_info, out_file_fda)
    out_file_seer = argv.out_name + "_seer.tsv"
    save_data(seer_info, out_file_seer)


if __name__ == "__main__":
    args = "-i /Users/sbelkin/Broad/drug_info_portal/example.txt -o /Users/sbelkin/Broad/drug_info_portal/example"
    drug_info()
