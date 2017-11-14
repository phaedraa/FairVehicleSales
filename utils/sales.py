from enum import Enum


class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple((choice.name, choice.value) for choice in cls)


class TransactionEntityType(ChoiceEnum):
    dealer = 'dealer'
    individual = 'individual'

