import tkinter as tk
from tkinter import *
from tkinter import ttk
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from heapq import nlargest

# Download NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

def summarize_text(text, num_sentences=3):
    # Tokenize the text into sentences and words
    sentences = sent_tokenize(text)
    words = word_tokenize(text)

    # Filter out stopwords and non-alphabetic words
    stop_words = set(stopwords.words("english"))
    words = [word.lower() for word in words if word.isalpha() and word.lower() not in stop_words]

    # Calculate word frequency
    word_frequencies = {}
    for word in words:
        word_frequencies[word] = word_frequencies.get(word, 0) + 1

    # Calculate sentence scores
    sentence_scores = {}
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in word_frequencies:
                if len(sentence.split(" ")) < 30:
                    sentence_scores[sentence] = sentence_scores.get(sentence, 0) + word_frequencies[word]

    # Get the top N sentences with highest scores
    summarized_sentences = nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
    return " ".join(summarized_sentences)

def get_summary():
    input_text = entry.get("1.0", END).strip()
    if not input_text:
        result_text.delete("1.0", END)
        result_text.insert(END, "Please enter text to summarize!")
        return
    num_sentences = int(summary_length.get())
    summarized_text = summarize_text(input_text, num_sentences)
    result_text.delete("1.0", END)
    result_text.insert(END, summarized_text)

# GUI Setup
window = Tk()
window.title("Summarizer GUI")
window.geometry('700x500')

# Notebook Style
style = ttk.Style(window)
style.configure('lefttab.TNotebook', tabposition="wn")

tab_control = ttk.Notebook(window, style='lefttab.TNotebook')
tab1 = ttk.Frame(tab_control)
tab_control.add(tab1, text=f'{"Home":^20s}')

Label(tab1, text='Summaryzer', font=("Arial", 16), padx=5, pady=5).grid(column=0, row=0)

# Input Text widget
Label(tab1, text='Enter Text to summarize:', padx=5, pady=5).grid(row=1, column=0)
entry = Text(tab1, height=10, font=("Arial", 12))
entry.grid(row=2, column=0, columnspan=4, pady=5, padx=5)

# Summary Length Spinner
Label(tab1, text='Number of Sentences:', padx=5, pady=5).grid(row=3, column=0)
summary_length = ttk.Spinbox(tab1, from_=1, to=10, width=5)
summary_length.set(3)
summary_length.grid(row=3, column=1)

# Summarize Button
Button(tab1, text='Summarize', command=get_summary, width=12, bg='#25d366', fg='#fff').grid(row=4, column=0, pady=10, padx=10)

# Result Text widget
result_text = Text(tab1, height=10, font=("Arial", 12), bg="#f4f4f4")
result_text.grid(row=5, column=0, columnspan=4, pady=5, padx=5)

tab_control.pack(expand=1, fill='both')
window.mainloop()
