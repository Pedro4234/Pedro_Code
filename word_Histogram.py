"""🔹 3. Hard – Word Histogram (7–10 mins)
Problem:
Write a function word_histogram(text) that takes a string and returns a dictionary with each word (case-insensitive) as keys and their count as values. Ignore punctuation.

💡 Example:


word_histogram("Hello, hello! How are you? Are you okay?")  
# → {'hello': 2, 'how': 1, 'are': 2, 'you': 2, 'okay': 1}

d = {"a": 1, "b": 2}
d["a"]         # 1
d.get("c", 0)  # 0 (default if key doesn't exist)

for key, val in d.items():
    print(key, val)

You'll want to normalize the text:

Convert it all to lowercase.
Remove punctuation so only words remain.
Then, split the text into words (using .split()).

Loop through each word:

If it's already in your dictionary, increase its count.
If not, add it with a count of 1."""

d={}
Ntext = input("PLease input the text: ")
def word_histogram(text):
    words = []
    text = text.lower()
    nText = ""
    for char in text:
        if char.isalpha() or char==" ":
            nText = nText + char #I think this is the concatinate but i am not sure
    words= nText.split() #IDK how to use this function
    for word in words:
        if word in d:
            d[word] +=1  #if the word is new add it to dictionary, if it is already there +1 to count
        else:
            d[word] = 1
    print(d)


word_histogram(Ntext)