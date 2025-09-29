from crewai.tools import tool

@tool
def count_letters(sentence: str):
    """Counts the number of letters in a sentence."""
    print("tool called with input:", sentence)
    return len(sentence)