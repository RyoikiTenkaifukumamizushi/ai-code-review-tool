def to_camel_case(text):
    words = text.split('_')
    return words[0] + ''.join(word.capitalize() for word in words[1:])

def count_vowels(text):
    return sum(1 for char in text.lower() if char in 'aeiou')
