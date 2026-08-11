from app.learning.alphabet_provider import AlphabetProvider

provider = AlphabetProvider()

print("Current:", provider.get_current_letter())
print("Next:", provider.get_next_letter())
print("Select:", provider.select_letter("M"))
print("Reset:", provider.reset())
print("Last?", provider.is_last_letter())