import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import hashlib
import itertools
import string
import threading

# Thread-safe insert into output text widget
def safe_insert(text_widget, content):
    text_widget.configure(state='normal')
    text_widget.insert(tk.END, content)
    text_widget.see(tk.END)
    text_widget.configure(state='disabled')

def load_wordlist():
    filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if filepath:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
            wordlist = file.read()
        wordlist_text.configure(state='normal')
        wordlist_text.delete(1.0, tk.END)
        wordlist_text.insert(tk.END, wordlist)
        wordlist_text.configure(state='disabled')

def start_brute_force():
    target = hash_entry.get().strip().lower()
    if len(target) != 64 or not all(c in string.hexdigits for c in target):
        messagebox.showerror("Invalid Hash", "Please enter a valid SHA-256 hash (64 hex characters).")
        return
    
    try:
        max_len = int(max_length_entry.get())
        if not (1 <= max_len <= 12):
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Length", "Max length must be an integer between 1 and 12.")
        return
    
    use_wordlist = use_wordlist_var.get()

    output_text.configure(state='normal')
    output_text.delete(1.0, tk.END)
    output_text.configure(state='disabled')

    def brute_force():
        charset = string.ascii_lowercase + string.digits
        
        if use_wordlist:
            words = wordlist_text.get(1.0, tk.END).splitlines()
            safe_insert(output_text, f"[*] Loaded {len(words)} words from wordlist...\n")
            for i, word in enumerate(words, 1):
                hashed_word = hashlib.sha256(word.encode()).hexdigest()
                if hashed_word == target:
                    safe_insert(output_text, f"[+] Password found: {word}\n")
                    return
                if i % 1000 == 0:
                    safe_insert(output_text, f"Checked {i} words...\n")
            safe_insert(output_text, "[-] Password not found in wordlist.\n")
        else:
            total_attempts = sum(len(charset)**l for l in range(1, max_len+1))
            safe_insert(output_text, f"[*] Starting brute force: max length {max_len}, charset size {len(charset)}\n")
            attempts_done = 0
            for length in range(1, max_len + 1):
                for attempt in itertools.product(charset, repeat=length):
                    password = ''.join(attempt)
                    hashed_attempt = hashlib.sha256(password.encode()).hexdigest()
                    attempts_done += 1
                    if hashed_attempt == target:
                        safe_insert(output_text, f"[+] Password found: {password}\n")
                        return
                    if attempts_done % 10000 == 0:
                        safe_insert(output_text, f"Checked {attempts_done} / {total_attempts} attempts...\n")
            safe_insert(output_text, "[-] Password not found.\n")

    threading.Thread(target=brute_force, daemon=True).start()

# Hacker-style colors and fonts
BG_COLOR = "black"
FG_COLOR = "#00FF00"
FONT = ("Consolas", 12)

root = tk.Tk()
root.title("Brute Force Password Cracker")
root.configure(bg=BG_COLOR)

label_style = {"bg": BG_COLOR, "fg": FG_COLOR, "font": FONT}
entry_style = {"bg": "#003300", "fg": FG_COLOR, "insertbackground": FG_COLOR, "font": FONT, "highlightbackground": FG_COLOR, "highlightcolor": FG_COLOR}
button_style = {"bg": "#003300", "fg": FG_COLOR, "activebackground": "#005500", "activeforeground": FG_COLOR, "font": FONT}

tk.Label(root, text="Target SHA-256 Hash:", **label_style).pack(pady=(10,0))
hash_entry = tk.Entry(root, width=70, **entry_style)
hash_entry.pack(pady=(0,10))

tk.Label(root, text="Max Password Length (1-12):", **label_style).pack()
max_length_entry = tk.Entry(root, width=5, **entry_style)
max_length_entry.insert(0, "4")
max_length_entry.pack(pady=(0,10))

use_wordlist_var = tk.BooleanVar()
tk.Checkbutton(root, text="Use Wordlist", variable=use_wordlist_var, bg=BG_COLOR, fg=FG_COLOR, selectcolor=BG_COLOR, font=FONT).pack()

tk.Button(root, text="Load Wordlist", command=load_wordlist, **button_style).pack(pady=(5,10))

wordlist_text = scrolledtext.ScrolledText(root, width=70, height=10, bg=BG_COLOR, fg=FG_COLOR, insertbackground=FG_COLOR, font=FONT)
wordlist_text.configure(state='disabled')
wordlist_text.pack()

tk.Button(root, text="Start Brute Force", command=start_brute_force, **button_style).pack(pady=(10,10))

output_text = scrolledtext.ScrolledText(root, width=70, height=12, bg=BG_COLOR, fg=FG_COLOR, insertbackground=FG_COLOR, font=FONT)
output_text.configure(state='disabled')
output_text.pack(pady=(0,10))

# Blinking cursor effect in output text
def blink_cursor():
    try:
        content = output_text.get("end-2c", "end-1c")
        if content == "|":
            output_text.configure(state='normal')
            output_text.delete("end-2c")
            output_text.configure(state='disabled')
        else:
            output_text.configure(state='normal')
            output_text.insert(tk.END, "|")
            output_text.configure(state='disabled')
        output_text.see(tk.END)
    except tk.TclError:
        pass  # widget might be closed
    root.after(500, blink_cursor)

blink_cursor()

root.mainloop()