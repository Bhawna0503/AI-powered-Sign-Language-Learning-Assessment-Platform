from dataclasses import dataclass


@dataclass
class FeedbackResult:
    status: str
    messages: list