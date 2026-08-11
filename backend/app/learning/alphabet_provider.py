"""
alphabet_provider.py

Provides alphabet navigation (A-Z) for the learning module.
"""

from typing import List


class AlphabetProvider:
    """Manages the alphabet sequence for sign language practice."""

    def __init__(self):
        self._alphabets: List[str] = [chr(i) for i in range(ord("A"), ord("Z") + 1)]
        self._current_index: int = 0

    def get_all_letters(self) -> List[str]:
        """Return all available alphabets."""
        return self._alphabets.copy()

    def get_current_letter(self) -> str:
        """Return the current alphabet."""
        return self._alphabets[self._current_index]

    def get_next_letter(self) -> str:
        """
        Move to the next alphabet.
        If already at Z, remain at Z.
        """
        if self._current_index < len(self._alphabets) - 1:
            self._current_index += 1
        return self.get_current_letter()

    def get_previous_letter(self) -> str:
        """Move back one alphabet."""
        if self._current_index > 0:
            self._current_index -= 1
        return self.get_current_letter()

    def select_letter(self, letter: str) -> str:
        """
        Select a specific alphabet (A-Z).
        """
        letter = letter.upper()

        if letter not in self._alphabets:
            raise ValueError(f"Invalid alphabet: {letter}")

        self._current_index = self._alphabets.index(letter)
        return self.get_current_letter()

    def reset(self) -> str:
        """Reset back to A."""
        self._current_index = 0
        return self.get_current_letter()

    def is_last_letter(self) -> bool:
        """Return True if current alphabet is Z."""
        return self._current_index == len(self._alphabets) - 1