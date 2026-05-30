import tkinter as tk
from tkinter import ttk, messagebox
from googletrans import Translator, LANGUAGES
import pyttsx3

# -----------------------------
# Translator setup
# -----------------------------
translator = Translator()

# Text-to-speech engine
engine = pyttsx3.init()

# -----------------------------
# Translate Function
# -----------------------------
def translate_text():

    input_text = input_box.get("1.0", tk.END).strip()

    if input_text == "":
        messagebox.showwarning(
            "Warning",
            "Please enter some text!"
        )
        return

    source_lang = source_combo.get()
    target_lang = target_combo.get()

    source_code = language_dict[source_lang]
    target_code = language_dict[target_lang]

    try:
        translated = translator.translate(
            input_text,
            src=source_code,
            dest=target_code
        )

        output_box.config(state=tk.NORMAL)

        output_box.delete("1.0", tk.END)

        output_box.insert(
            tk.END,
            translated.text
        )

        output_box.config(state=tk.DISABLED)

    except Exception as e:
        messagebox.showerror(
            "Error",
            f"Translation failed!\n{e}"
        )

# -----------------------------
# Copy Function
# -----------------------------
def copy_text():

    translated_text = output_box.get("1.0", tk.END).strip()

    if translated_text:
        root.clipboard_clear()
        root.clipboard_append(translated_text)

        messagebox.showinfo(
            "Copied",
            "Translated text copied!"
        )

# -----------------------------
# Speak Function
# -----------------------------
def speak_text():

    translated_text = output_box.get("1.0", tk.END).strip()

    if translated_text:
        engine.say(translated_text)
        engine.runAndWait()

# -----------------------------
# Swap Languages
# -----------------------------
def swap_languages():

    source = source_combo.get()
    target = target_combo.get()

    source_combo.set(target)
    target_combo.set(source)

# -----------------------------
# GUI Window
# -----------------------------
root = tk.Tk()

root.title("Language Translator")

root.geometry("750x600")

root.config(bg="#1f1f2e")

# -----------------------------
# Heading
# -----------------------------
title_label = tk.Label(
    root,
    text="Language Translator",
    font=("Arial", 24, "bold"),
    bg="#1f1f2e",
    fg="#ffffff"
)

title_label.pack(pady=15)

# -----------------------------
# Language Dictionary
# -----------------------------
language_dict = {
    language.title(): code
    for code, language in LANGUAGES.items()
}

language_names = sorted(language_dict.keys())

# -----------------------------
# Dropdown Frame
# -----------------------------
dropdown_frame = tk.Frame(
    root,
    bg="#1f1f2e"
)

dropdown_frame.pack(pady=10)

# Source Language
source_combo = ttk.Combobox(
    dropdown_frame,
    values=language_names,
    width=20,
    font=("Arial", 12)
)

source_combo.set("English")

source_combo.grid(row=0, column=0, padx=10)

# Swap Button
swap_button = tk.Button(
    dropdown_frame,
    text="🔄",
    font=("Arial", 16),
    bg="#ffcc70",
    command=swap_languages
)

swap_button.grid(row=0, column=1, padx=5)

# Target Language
target_combo = ttk.Combobox(
    dropdown_frame,
    values=language_names,
    width=20,
    font=("Arial", 12)
)

target_combo.set("Hindi")

target_combo.grid(row=0, column=2, padx=10)

# -----------------------------
# Input Label
# -----------------------------
input_label = tk.Label(
    root,
    text="📝 Enter Text",
    font=("Arial", 14, "bold"),
    bg="#1f1f2e",
    fg="white"
)

input_label.pack(anchor="w", padx=20)

# -----------------------------
# Input Box
# -----------------------------
input_box = tk.Text(
    root,
    height=8,
    font=("Arial", 13),
    bg="#2d2d44",
    fg="white",
    insertbackground="white",
    relief=tk.FLAT
)

input_box.pack(
    padx=20,
    pady=10,
    fill=tk.BOTH
)

# -----------------------------
# Translate Button
# -----------------------------
translate_button = tk.Button(
    root,
    text="✨Translate✨",
    font=("Arial", 14, "bold"),
    bg="#6c63ff",
    fg="white",
    padx=20,
    pady=10,
    command=translate_text
)

translate_button.pack(pady=15)

# -----------------------------
# Output Label
# -----------------------------
output_label = tk.Label(
    root,
    text="🌍 Translated Text",
    font=("Arial", 14, "bold"),
    bg="#1f1f2e",
    fg="white"
)

output_label.pack(anchor="w", padx=20)

# -----------------------------
# Output Box
# -----------------------------
output_box = tk.Text(
    root,
    height=8,
    font=("Arial", 13),
    bg="#2d2d44",
    fg="#00ffcc",
    relief=tk.FLAT
)

output_box.pack(
    padx=20,
    pady=10,
    fill=tk.BOTH
)

output_box.config(state=tk.DISABLED)

# -----------------------------
# Bottom Buttons
# -----------------------------
button_frame = tk.Frame(
    root,
    bg="#1f1f2e"
)

button_frame.pack(pady=10)

# Copy Button
copy_button = tk.Button(
    button_frame,
    text="📋 Copy",
    font=("Arial", 12, "bold"),
    bg="#ff7b54",
    fg="white",
    padx=15,
    command=copy_text
)

copy_button.grid(row=0, column=0, padx=10)

# Speak Button
speak_button = tk.Button(
    button_frame,
    text="🔊 Speak",
    font=("Arial", 12, "bold"),
    bg="#00c897",
    fg="white",
    padx=15,
    command=speak_text
)

speak_button.grid(row=0, column=1, padx=10)

# -----------------------------
# Run App
# -----------------------------
root.mainloop()