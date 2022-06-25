class FourDigitYearConverter:
    regex = '[0-9]{4}'

    @staticmethod
    def to_python(value: str) -> int:
        return int(value)

    @staticmethod
    def to_url(value: str) -> str:
        return '%04d' % value
