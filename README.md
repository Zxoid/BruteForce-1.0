# Bruteforce 1.0

A simple **SHA-256 password brute force and wordlist cracker** with a hacker-style terminal UI built in Python using Tkinter.

---

## About

This tool demonstrates the basics of brute forcing SHA-256 hashes by either:

- Trying passwords from a user-loaded wordlist file, or  
- Attempting every possible combination of lowercase letters and digits up to a maximum length.

It’s designed for educational and ethical research purposes only — **never use it on accounts or systems you do not own or have explicit permission to test**.

---

## Features

- Load a custom wordlist (`.txt` file) to check password guesses  
- Brute force all lowercase letters + digits passwords up to a set max length  
- Real-time output of progress in a "hacker-style" UI  
- Multithreaded for UI responsiveness  

---

## Usage

Run the Python script using:

```bash
python bruteforce.py
Enter the target SHA-256 hash you want to crack.

Choose the max password length if using brute force mode (1-12).

(Optional) Check "Use Wordlist" and load your own .txt wordlist file.

Click Start Brute Force to begin.

Monitor the output window for progress and results.

Important Notes
You must provide your own wordlist file if you want to use the wordlist option. This project does not include any wordlists.

Brute forcing hashes is computationally expensive and slow; cracking complex passwords with this method can take a very long time or may be practically impossible.

This project is for learning and research purposes only.

Requirements
Python 3.x

Standard Python libraries (Tkinter, hashlib, etc.) included by default

License
This project is licensed under the MIT License - see the LICENSE file for details.

Thank you for using Bruteforce 1.0 — please use responsibly!
