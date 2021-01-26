from dataclasses import dataclass

@dataclass
class TimeStamp():
    day: int
    month: int
    year: int

    def get_date(self):
        return f"{self.year:04d}-{self.month:02d}-{self.day:02d}"
