"""Apache log parser implemented for CDL"""
from argparse import ArgumentParser
from parser import LogParser
from pattern import expand


def main():
    parser = ArgumentParser(
        description=__doc__
    )

    parser.add_argument("log_file", type=str, help="The log file to be processed")

    parser.add_argument("--interval", type=int, default=1,
                        help="The duration of an interval, in minutes")

    parser.add_argument("--start", type=str, default="1970-01-01T00:00",
                        help="The start time for considering log entries")

    parser.add_argument("--end", type=str, default="2099-01-01T00:00",
                        help="The end time for considering log entries")

    parser.add_argument("--success", type=str, default="2xx",
                        help="The patterns of the status codes that will be "
                             "considered successful")

    args = parser.parse_args()

    success_codes = list()

    for pattern in args.success.split(','):
        success_codes += expand(pattern)

    parser = LogParser(args.log_file,
                       args.start,
                       args.end,
                       args.interval,
                       success_codes)

    parser.parse()

    parser.print_stats()


if __name__ == '__main__':
    main()
