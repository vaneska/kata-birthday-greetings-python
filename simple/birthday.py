import os
import csv
from datetime import date
from optparse import OptionParser

CSV_FRIENDS_PATH = os.path.dirname(__file__) + "/../friends.csv"


def process_friends(current_date):
    with open(CSV_FRIENDS_PATH, newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='|')
        for row in reader:
            birthday = date.fromisoformat(row[2])
            if birthday.month == current_date.month and birthday.day == current_date.day:
                print("Happy birthday, dear {first_name}!".format(first_name=row[1]))


def get_current_date():
    parser = OptionParser()
    parser.add_option("-d", "--date", default=date.today(), dest="current_date", help="Current date")
    (options, args) = parser.parse_args()
    return date.fromisoformat(options.current_date)


if __name__ == "__main__":
    process_friends(get_current_date())
