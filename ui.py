import argparse

from datetime import datetime

from exceptions import CoinExceptionAPI
from manager import Manager


def format_date(date):
    try:
        return datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        pass
    try:
        return datetime.strptime(date, '%Y-%m')
    except ValueError:
        CoinExceptionAPI({"type": "Invalid_date_format"}).handle()


def arg_parser():
    # noinspection PyTypeChecker
    parser = argparse.ArgumentParser(description='Parse orders and arguments',
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('main_command', default='help',
                        help='consecutive-increase : Finds longest consecutive period in which price '
                             'was increasing, within the user-specified range.  Usage example: ui.py '
                             '-ci ''1990-01-01 1991-01-02 \n' +
                             'average-price-by-month : Return average price in every month, within the user-specified '
                             'range. Usage example: '
                             'ui.py average-price-by-month --start-date=2021-01 --end-date=2021-03 \n' +
                             'export : Export data for given period in one of selected format csv or '
                             'json. Usage example: export --start-date=2021-01-01 '
                             '--end-date=2021-01-03 --format=csv --file=exported_data.csv '
                        )

    parser.add_argument('-f=', '--format=', dest='data_format', choices=['csv', 'json'], default='json',
                        help='Format of exporting file')

    parser.add_argument('-c=', '--coin=', dest='coin', default='btc-bitcoin',
                        help='Specify other type of cryptocurrency. Default btc-bitcoin. ')

    parser.add_argument('-sd=', '--start-date=', dest='start_date', type=format_date, required=True,
                        help='Start date format Year-mont-day', )

    parser.add_argument('-ed=', '--end-date=', dest='end_date', type=format_date, required=True,
                        help='End date format Year-mont-day')

    parser.add_argument('-fn=', '--file=', dest='file', action='store',
                        help='Provide name of file to export data.')

    return parser


def console_interface(parser=arg_parser()):
    # For testing with argparse purpose
    try:
        args = parser.parse_args()
    except AttributeError:
        args = parser

    if args.main_command == "consecutive-increase":
        return Manager(coin=args.coin, end_date=args.end_date, start_date=args.start_date, file_name=args.file,
                       data_format=args.data_format).consecutive_increase()
    elif args.main_command == "average-price-by-month":
        return Manager(coin=args.coin, end_date=args.end_date, start_date=args.start_date, file_name=args.file,
                       data_format=args.data_format).average_price_by_month()
    elif args.main_command == "export":
        return Manager(coin=args.coin, end_date=args.end_date, start_date=args.start_date, file_name=args.file,
                       data_format=args.data_format).export()
    else:
        return "bad argument"


if __name__ == "__main__":
    print(console_interface())
