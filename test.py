import tkinter as tk
from tkinter import *
from tkinter import ttk
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from heapq import nlargest

def summarize_text(text, num_sentences=3):
    # Your existing summarization function remains unchanged
    # Tokenize the text into sentences and words
    sentences = sent_tokenize(text)
    words = word_tokenize(text)

    # Filter out stopwords
    stop_words = set(stopwords.words("english"))
    words = [word.lower() for word in words if word.lower() not in stop_words]

    # Calculate word frequency
    word_frequencies = {}
    for word in words:
        if word not in word_frequencies:
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1

    # Calculate sentence scores based on word frequencies
    sentence_scores = {}
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in word_frequencies:
                if len(sentence.split(" ")) < 30:
                    if sentence not in sentence_scores:
                        sentence_scores[sentence] = word_frequencies[word]
                    else:
                        sentence_scores[sentence] += word_frequencies[word]

    # Get the top N sentences with highest scores
    summarized_sentences = nlargest(
        num_sentences, sentence_scores, key=sentence_scores.get)
    summarized_text = " ".join(summarized_sentences)
    return summarized_text

def get_summary():
    # Get text from the input Text widget
    input_text = entry.get("1.0", END)

    # Perform text summarization using the summarize_text function
    summarized_text = summarize_text(input_text)

    # Clear the previous result
    result_text.delete("1.0", END)

    # Display the summarized text in the result Text widget
    result_text.insert(END, summarized_text)


nltk.download('punkt')
nltk.download('stopwords')

window = Tk()
window.title("Summarizer GUI")
window.geometry('700x500')

# Create GUI components
style = ttk.Style(window)
style.configure('lefttab.TNotebook', tabposition="wn")

# ... Your existing code for tabs, labels, and frames ...
tab_control = ttk.Notebook(window, style='lefttab.TNotebook')

tab1 = ttk.Frame(tab_control)
#tab2 = ttk.Frame(tab_control)
#tab3 = ttk.Frame(tab_control)
#tab4 = ttk.Frame(tab_control)
#tab5 = ttk.Frame(tab_control)

tab_control.add(tab1, text=f'{"Home":^20s}')
#tab_control.add(tab2, text=f'{"file":^20s}')
#tab_control.add(tab3, text=f'{"URL":^20s}')
#tab_control.add(tab4, text=f'{"Compare":^20s}')
#tab_control.add(tab5, text=f'{"About":^20s}')

Label1 = Label(tab1, text='Summaryzer', padx=5, pady=5)
Label1.grid(column=0, row=0)

#Label2 = Label(tab2, text='file processing ', padx=5, pady=5)
#Label2.grid(column=0, row=0)

#Label3 = Label(tab3, text='URL', padx=5, pady=5)
#Label3.grid(column=0, row=0)

#Label4 = Label(tab4, text='compare', padx=5, pady=5)
#Label4.grid(column=0, row=0)

#Label5 = Label(tab5, text='About', padx=5, pady=5)
#Label5.grid(column=0, row=0)

l1 = Label(tab1, text='Enter Text to summarize', padx=5, pady=5)
l1.grid(row=1, column=0)

# Input Text widget
l1 = Label(tab1, text='Enter Text to summarize', padx=5, pady=5)
l1.grid(row=1, column=0)
entry = Text(tab1, height=10)
entry.grid(row=2, column=0, columnspan=4, pady=5, padx=5)

# Button to trigger summarization
button2 = Button(tab1, text='Summarize', command=get_summary, width=12, bg='#25d366', fg='#fff')
button2.grid(row=4, column=0, pady=10, padx=10)

# Result Text widget to display the summarized text
result_text = Text(tab1, height=10)
result_text.grid(row=5, column=0, columnspan=4, pady=5, padx=5)

tab_control.pack(expand=1, fill='both')

window.mainloop()
