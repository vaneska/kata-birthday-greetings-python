import os
import csv
from datetime import date
from typing import Protocol, Iterator, Iterable, TextIO
from dataclasses import dataclass
from optparse import OptionParser

@dataclass()
class Friend:
    """
    Слой сущностей доменной логики.
    """
    first_name: str
    last_name: str
    birthday: date
    email: str


class Repository(Protocol):
    """
    Протокол, предоставляющий инфраструктурный слой.
    Занимается получением данных из внешних источников
    """

    def all(self) -> Iterator:
        raise NotImplementedError

class CSVFriendRepository(Repository):
    """
    Получение данных о друзьях из CSV-файла
    """
    _file: TextIO

    def __init__(self, file: TextIO):
        self._file = file

    def all(self) -> Iterator:
        return CSVFriendsIterator(file=self._file)


class CSVFriendsIterator(Iterator):
    """
    Обертка-итератор для выдачи записи в виде сущности Friend
    """
    _csv_reader: Iterable
    _file: TextIO

    def __init__(self, file: TextIO) -> None:
        self._file = file
        self.csv_reader = csv.reader(self._file, delimiter=",", quotechar="|")

    def __iter__(self): return self

    def __next__(self):
        item = next(self.csv_reader)
        return Friend(
            last_name=item[0],
            first_name=item[1],
            birthday=date.fromisoformat(item[2]),
            email=item[3]
        )


class Notifier(Protocol):
    """
    Протокол для нотификаторов
    """

    def notify(self, friends: Iterable[Friend]) -> bool:
        """
        Уведомить друзей каким-либо способом
        :param friends:
        :return:
        """
        raise NotImplementedError


class ConsoleNotifier(Notifier):
    """
    Консольный нотификатор
    """

    def notify(self, friends: Iterable[Friend]) -> bool:
        for friend in friends:
            print("Happy birthday, dear {first_name}!".format(first_name=friend.first_name))
        return True


class DomainService(Protocol):
    """
    Протокол для слоя сервиса доменной логики
    """

    def execute(self) -> bool:
        """
        Выполнить действие
        :return: bool
        """
        raise NotImplementedError


class NotifyFriendBirthdaysService(DomainService):
    """
    Доменный сервис нотификатор о днях рождений
    """
    _repository: Repository
    _notifier: Notifier
    current_date: date

    def __init__(
            self,
            repository: Repository,
            notifier: Notifier,
            current_date: date = date.today()
    ) -> None:
        self._repository = repository
        self._notifier = notifier
        self.current_date = current_date

    def execute(self) -> bool:
        filtered_friends = []
        for friend in self._repository.all():
            if friend.birthday.month == self.current_date.month and friend.birthday.day == self.current_date.day:
                filtered_friends.append(friend)

        return self._notifier.notify(filtered_friends)


class ConsoleApp:
    """
    Объект приложения.
    Инфраструктурный слой. Соединяет бизнес-логику и внешний мир
    """
    CSV_FRIENDS_PATH = os.path.dirname(__file__) + "/../friends.csv"

    def _get_current_date(self) -> date:
        parser = OptionParser()
        parser.add_option(
            "-d", "--date",
            default=date.today().isoformat(),
            dest="current_date",
            help="Current date"
        )
        (options, args) = parser.parse_args()
        return date.fromisoformat(options.current_date)

    def run(self) -> None:
        with open(self.CSV_FRIENDS_PATH, newline='') as file:
            NotifyFriendBirthdaysService(
                current_date=self._get_current_date(),
                repository=CSVFriendRepository(file=file),
                notifier=ConsoleNotifier()
            ).execute()



if __name__ == "__main__":
    ConsoleApp().run()
