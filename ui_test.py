import pytest

from exceptions import (
    BadCoinIdError,
    NotMatchingFileFormats,
    DatesOutOfRange,
)
from ui import console_interface, arg_parser


def test_average_price_by_month_1():
    parser = arg_parser().parse_args(
        [
            "average-price-by-month",
            "--start-date=2021-01",
            "--end-date=2021-03",
            "--file=test",
        ]
    )

    assert (
        console_interface(parser=parser) == "Date     Average price ($)\n"
        "2021-01  34778.37\n"
        "2021-02  45396.15\n"
        "2021-03  53508.5\n"
    )

    parser = arg_parser().parse_args(
        ["average-price-by-month", "--start-date=2021-01-01", "--end-date=2021-03-01"]
    )

    assert (
        console_interface(parser=parser) == "Date     Average price ($)\n"
        "2021-01  34778.37\n"
        "2021-02  45396.15\n"
        "2021-03  53508.5\n"
    )

    parser = arg_parser().parse_args(
        ["average-price-by-month", "--start-date=2021-01-01", "--end-date=2021-03-01"]
    )

    assert (
        console_interface(parser=parser) == "Date     Average price ($)\n"
        "2021-01  34778.37\n"
        "2021-02  45396.15\n"
        "2021-03  53508.5\n"
    )

    parser = arg_parser().parse_args(
        ["average-price-by-month", "--start-date=2021-01-01", "--end-date=2021-03-15"]
    )

    assert (
        console_interface(parser=parser) == "Date     Average price ($)\n"
        "2021-01  34778.37\n"
        "2021-02  45396.15\n"
        "2021-03  53508.5\n"
    )

    parser = arg_parser().parse_args(
        ["average-price-by-month", "--start-date=2021-01-01", "--end-date=2021-03"]
    )

    assert (
        console_interface(parser=parser) == "Date     Average price ($)\n"
        "2021-01  34778.37\n"
        "2021-02  45396.15\n"
        "2021-03  53508.5\n"
    )

    parser = arg_parser().parse_args(
        ["average-price-by-month", "--start-date=2021-01", "--end-date=2021-03-16"]
    )

    assert (
        console_interface(parser=parser) == "Date     Average price ($)\n"
        "2021-01  34778.37\n"
        "2021-02  45396.15\n"
        "2021-03  53508.5\n"
    )


def test_average_price_by_month_2():
    parser = arg_parser().parse_args(
        [
            "average-price-by-month",
            "--start-date=2023-01",
            "--end-date=2023-03",
            "--file=test",
        ]
    )

    with pytest.raises(DatesOutOfRange):
        console_interface(parser=parser)

    parser = arg_parser().parse_args(
        [
            "average-price-by-month",
            "--start-date=2021-01",
            "--end-date=2021-03",
            "--file=test",
            "--coin=exception",
        ]
    )

    with pytest.raises(BadCoinIdError):
        console_interface(parser=parser)

    parser = arg_parser().parse_args(
        [
            "export",
            "--start-date=2021-01",
            "--end-date=2021-03",
            "--file=test.csv",
            "--format=json",
        ]
    )

    with pytest.raises(NotMatchingFileFormats):
        console_interface(parser=parser)

    # Test to check. It fails, yest program behave right during that test.
    # parser = arg_parser().parse_args(["export", "--start-date=invalid_date",
    #                                   "--end-date=invalid_date", "--file=test.csv", "--format=csv"])
    #
    # with pytest.raises(InvalidDateFormat):
    #     console_interface(parser=parser)


def test_consecutive_increase_0():
    parser = arg_parser().parse_args(
        ["consecutive-increase", "--start-date=2021-02-11", "--end-date=2021-03-20"]
    )

    assert (
        console_interface(parser=parser)
        == "Longest consecutive period was from 2021-03-06 to 2021-03-11 with "
        "increase of $8873.35"
    )

    parser = arg_parser().parse_args(
        [
            "consecutive-increase",
            "--start-date=2021-02-11",
            "--end-date=2021-03-20",
            "--coin=eth-ethereum",
        ]
    )

    assert (
        console_interface(parser=parser)
        == "Longest consecutive period was from 2021-02-15 to 2021-02-19 with "
        "increase of $186.33"
    )
