import argparse

from datetime import datetime

from exceptions import (
    BadCoinIdError,
    DatesOutOfRange,
    DividingByZeroError,
    NotMatchingFileFormats,
    InvalidDateFormat,
)
from manager import Manager


def format_date(date):
    try:
        return datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        pass
    try:
        return datetime.strptime(date, "%Y-%m")
    except ValueError:
        raise InvalidDateFormat()


def arg_parser():
    # noinspection PyTypeChecker
    parser = argparse.ArgumentParser(
        description="Parse orders and arguments",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "main_command",
        default="help",
        help="consecutive-increase : Finds longest consecutive period in which price "
        "was increasing, within the user-specified range.  Usage example: ui.py "
        "-ci "
        "1990-01-01 1991-01-02 \n"
        + "average-price-by-month : Return average price in every month, within the user-specified "
        "range. Usage example: "
        "ui.py average-price-by-month --start-date=2021-01 --end-date=2021-03 \n"
        + "export : Export data for given period in one of selected format csv or "
        "json. Usage example: export --start-date=2021-01-01 "
        "--end-date=2021-01-03 --format=csv --file=exported_data.csv ",
    )

    parser.add_argument(
        "-f=",
        "--format=",
        dest="data_format",
        choices=["csv", "json"],
        default="json",
        help="Format of exporting file",
    )

    parser.add_argument(
        "-c=",
        "--coin=",
        dest="coin",
        default="btc-bitcoin",
        help="Specify other type of cryptocurrency. Default btc-bitcoin. ",
    )

    parser.add_argument(
        "-sd=",
        "--start-date=",
        dest="start_date",
        type=format_date,
        required=True,
        help="Start date format Year-mont-day",
    )

    parser.add_argument(
        "-ed=",
        "--end-date=",
        dest="end_date",
        type=format_date,
        required=True,
        help="End date format Year-mont-day",
    )

    parser.add_argument(
        "-fn=",
        "--file=",
        dest="file",
        action="store",
        help="Provide name of file to export data.",
    )

    return parser


def console_interface(parser=arg_parser()):
    # For testing with argparse purpose
    args = parser.parse_args() if hasattr(parser, "parse_args") else parser
    manager = Manager(
        coin=args.coin,
        end_date=args.end_date,
        start_date=args.start_date,
        file_name=args.file,
        data_format=args.data_format,
    )
    if args.main_command == "consecutive-increase":
        return manager.consecutive_increase()
    elif args.main_command == "average-price-by-month":
        return manager.average_price_by_month()
    elif args.main_command == "export":
        return manager.export()
    else:
        return "bad argument"


if __name__ == "__main__":
    try:
        print(console_interface())
    except BadCoinIdError:
        raise SystemExit(1)
    except DatesOutOfRange:
        raise SystemExit(1)
    except DividingByZeroError:
        raise SystemExit(1)
    except NotMatchingFileFormats:
        raise SystemExit(1)
    except InvalidDateFormat():
        raise SystemExit(1)
