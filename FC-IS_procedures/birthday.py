import os
import csv
from datetime import date
from collections.abc import Iterator
from optparse import OptionParser

CSV_FRIENDS_PATH = os.path.dirname(__file__) + "/../friends.csv"


def get_current_date() -> date:
    parser = OptionParser()
    parser.add_option(
        "-d", "--date",
        default=date.today().isoformat(),
        dest="current_date",
        help="Current date"
    )
    (options, args) = parser.parse_args()
    return date.fromisoformat(options.current_date)


def process_friends(current_date: date, friends: Iterator) -> list:
    notify_friends = []
    for friend in friends:
        friend_date = date.fromisoformat(friend[2])
        if friend_date.month == current_date.month and friend_date.day == current_date.day:
            notify_friends.append(friend)

    return notify_friends


def notify(friends: list) -> bool:
    for friend in friends:
        print("Happy birthday, dear {first_name}!".format(first_name=friend[1]))

    return True


def run(current_date: date) -> bool:
    with open(CSV_FRIENDS_PATH, newline="") as file:
        friends = process_friends(current_date, csv.reader(file, delimiter=",", quotechar="|"))

    return notify(friends)


if __name__ == "__main__":
    run(get_current_date())
