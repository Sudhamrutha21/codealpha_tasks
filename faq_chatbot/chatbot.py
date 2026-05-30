import json
import tkinter as tk
from tkinter import scrolledtext
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# Load FAQ Data
# -----------------------------
with open("faq_data.json", "r") as file:
    faq_data = json.load(file)

questions = [item["question"] for item in faq_data]
answers = [item["answer"] for item in faq_data]

# -----------------------------
# NLP Vectorizer
# -----------------------------
vectorizer = TfidfVectorizer()

question_vectors = vectorizer.fit_transform(questions)

# -----------------------------
# Chatbot Response Function
# -----------------------------
def get_response(user_input):
    user_vector = vectorizer.transform([user_input])

    similarity = cosine_similarity(user_vector, question_vectors)

    best_match_index = similarity.argmax()

    best_score = similarity[0][best_match_index]

    # Prevent irrelevant answers
    if best_score < 0.2:
        return "Sorry, I couldn't understand that."

    return answers[best_match_index]

# -----------------------------
# Send Message Function
# -----------------------------
def send_message(event=None):

    user_message = entry_box.get().strip()

    if user_message == "":
        return

    # Show user message
    chat_area.config(state=tk.NORMAL)

    chat_area.insert(tk.END, f"You: {user_message}\n")

    # Generate response
    response = get_response(user_message)

    # Show bot response
    chat_area.insert(tk.END, f"Bot: {response}\n\n")

    # Disable editing again
    chat_area.config(state=tk.DISABLED)

    # Auto-scroll
    chat_area.yview(tk.END)

    # Clear input box
    entry_box.delete(0, tk.END)

# -----------------------------
# GUI Window
# -----------------------------
root = tk.Tk()

root.title("FAQ Chatbot")

root.geometry("650x550")

root.configure(bg="#1e1e1e")

# -----------------------------
# Heading
# -----------------------------
title_label = tk.Label(
    root,
    text="FAQ Chatbot",
    font=("Arial", 20, "bold"),
    bg="#1e1e1e",
    fg="white"
)

title_label.pack(pady=10)

# -----------------------------
# Chat Area
# -----------------------------
chat_area = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    font=("Arial", 12),
    bg="#2b2b2b",
    fg="white",
    insertbackground="white"
)

chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

chat_area.config(state=tk.DISABLED)

# -----------------------------
# Bottom Frame
# -----------------------------
bottom_frame = tk.Frame(root, bg="#1e1e1e")

bottom_frame.pack(fill=tk.X, padx=10, pady=10)

# -----------------------------
# Input Box
# -----------------------------
entry_box = tk.Entry(
    bottom_frame,
    font=("Arial", 14),
    bg="#3b3b3b",
    fg="white",
    insertbackground="white"
)

entry_box.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

# Press Enter to Send
entry_box.bind("<Return>", send_message)

# -----------------------------
# Send Button
# -----------------------------
send_button = tk.Button(
    bottom_frame,
    text="Send",
    font=("Arial", 12, "bold"),
    bg="#4CAF50",
    fg="white",
    padx=20,
    command=send_message
)

send_button.pack(side=tk.RIGHT)

# -----------------------------
# Start GUI
# -----------------------------
root.mainloop()