from abc import ABC, abstractmethod

from core.output.dispatcher import dispatch


class BaseCommand(ABC):

    @abstractmethod
    def build_table(self):
        pass

    @abstractmethod
    def build_json(self):
        pass

    def run(self, output):

        dispatch(
            output,
            table_data=self.build_table(),
            json_data=self.build_json(),
        )