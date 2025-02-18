#!/usr/bin/env python3





def get_max_length(data):
    max_length = 0

    max_length.isnumeric()
    for a_word in data:
        if not isinstance(a_word, str):
            return 0
        max_length = max(max_length, len(a_word))
    return max_length

words = ["this", "is", "a", "test", "of", "bla bla bla"]
longest = get_max_length(words)

for word in words:
    print(f"{word:>{longest}s}")
