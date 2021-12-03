import argparse
import logging
import re
from sys import stdout

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler(stdout))
log.setLevel("INFO")

DEFAULT_LOG_PATH = "./HO_replace.log"

# Script created by Das Shelmer (https://github.com/DasShelmer)


def _replace_ho(src):
    log.info("Replacing HO clases with raw values...")  #
    pattern = re.compile(
        r"\=\s*(BooleanParameter|CategoricalParameter|DecimalParameter|IntParameter|RealParameter).*?((default=)(?P<value>.*?)|(default=)(?P<edge_value>.*?))\,.*?\)",
        re.DOTALL | re.VERBOSE,
    )

    def repl(matchobj):
        groupdict = matchobj.groupdict()
        return "= " + groupdict["value"] or groupdict["edge_value"]

    result = pattern.sub(repl, src)
    log.info("HO clases replaced.")  #
    return result


def _remove_ho_imports(src: str):
    pattern = re.compile(
        r"(\s*(BooleanParameter|CategoricalParameter|DecimalParameter|IntParameter|RealParameter)\,*)+"
    )
    remove_matchobj = lambda x: ""

    log.info("Searching for HO classes imports...")  #

    lines = src.splitlines(False)
    # filter only indexed lines contain ho classnames
    ho_lines = list(
        filter(lambda l: re.search(pattern, l[0]), zip(lines, range(len(lines))))
    )

    log.info(f"Found {len(ho_lines)} import lines.")  #
    log.info("Removing HO classes imports...")  #
    # remove ho classnames from import line
    ho_lines = map(lambda l: (pattern.sub(remove_matchobj, l[0]), l[1]), ho_lines)

    ho_empty_lines = []
    ho_update_lines = []
    for line, i in ho_lines:
        ho_empty_lines.append((line, i)) if line.endswith(
            "import"
        ) else ho_update_lines.append((line, i))

    # Updating lines with not only HO classnames
    for uline, i in ho_update_lines:
        lines[i] = uline
    log.info(f"Update {len(ho_update_lines)} lines.")  #

    # Remove lines with only HO classnames
    offset = 0
    for _, i in ho_empty_lines:
        del lines[i - offset]
        offset += 1
    log.info(f"Removed {len(ho_empty_lines)} lines.")  #

    log.info("Removing finished.")  #

    return "\n".join(lines)


def replace_ho(
    src: open,
    dist: open,
    on_error_copy_src: bool = False,
    log_filepath=DEFAULT_LOG_PATH,
):
    #
    # Module main function
    #
    """Script for replacing HO params in freqtrade strategy"""
    if log_filepath:
        log.addHandler(logging.FileHandler(log_filepath))  #

    src_file = src.read()
    log.info("Running HO replacement...")  #
    result = True
    try:
        raw = _replace_ho(src_file)
        no_imports = _remove_ho_imports(raw)
        dist.write(no_imports)
    except Exception as err:
        result = err
        log.error("Error: " + err)
        if on_error_copy_src:
            log.info("Enabled on_error_copy_src argument, copy src to dist...")
            dist.write(src_file)

    src.close()
    dist.close()

    log.info("Finish replacement succesfully.")  #
    return result


def _main():
    # Simple CLI
    parser = argparse.ArgumentParser(
        description="Script for replacing HO params in freqtrade strategias"
    )

    parser.add_argument(
        "-s",
        dest="src_file",
        required=True,
        type=open,
        help="strategy source file.",
    )
    parser.add_argument(
        "-d",
        dest="dist_file",
        required=True,
        type=argparse.FileType("w", encoding="utf-8"),
        help="strategy destination filepath.",
    )
    parser.add_argument(
        "-l", dest="log_file", type=str, help="log file path.", default=DEFAULT_LOG_PATH
    )
    parser.add_argument(
        "--on-error-copy-src",
        dest="on_error_copy_src",
        action="store_true",
        help="on error copy source file to destination path.",
    )

    args = parser.parse_args()

    replace_ho(args.src_file, args.dist_file, args.on_error_copy_src, args.log_file)


if __name__ == "__main__":
    _main()
