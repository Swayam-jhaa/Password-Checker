# 🔐 Password Strength Checker + Breach Detector

A beginner-friendly CLI tool written in Python that evaluates password strength and checks if it has been exposed in known data breaches — **without ever sending your full password anywhere**.

> Built as a cybersecurity learning project. Uses the [Have I Been Pwned](https://haveibeenpwned.com/API/v3) API with the **k-Anonymity model** for safe breach detection.

---

## 📸 Preview

```
══════════════════════════════════════════════════
   🛡️  Password Strength Checker + Breach Detector
══════════════════════════════════════════════════
  Your password is hashed locally and never sent
  to any server in full. (k-Anonymity model) ✅
══════════════════════════════════════════════════

Enter a password to analyze: 

══════════════════════════════════════════════════
        🔐 PASSWORD STRENGTH ANALYSIS
══════════════════════════════════════════════════

📊 Overall Rating: 🟢 STRONG  (Score: 6/6)

──────────────────────────────────────────────────
📋 Detailed Breakdown:
──────────────────────────────────────────────────
  ✅ Good length (18 chars).
  ✅ Contains uppercase letters.
  ✅ Contains lowercase letters.
  ✅ Contains numbers.
  ✅ Contains special characters.
  🌟 Bonus: Very long password (16+ chars)!

──────────────────────────────────────────────────
🔍 Checking against known data breaches...
✅ Great news! This password was NOT found in any known data breaches.
══════════════════════════════════════════════════

💡 Tip: Use a password manager to generate and store strong passwords.
```

---

## ✨ Features

- 🔍 **Strength Analysis** — Checks length, uppercase, lowercase, digits, and special characters
- 🏷️ **Strength Rating** — Classifies passwords as 🔴 Weak, 🟡 Moderate, or 🟢 Strong
- 💬 **Detailed Feedback** — Tells you exactly what's missing or good
- 🌐 **Breach Detection** — Queries the Have I Been Pwned database to check if password was leaked
- 🔒 **k-Anonymity Model** — Only the first 5 characters of your SHA-1 hash are sent to the API. Your full password never leaves your machine.
- 🙈 **Hidden Input** — Password is never echoed to the terminal while typing

---

## 🛡️ How the Breach Check Works (k-Anonymity)

This tool never sends your password — or even its full hash — to any server. Here's the exact flow:

```
Your Password
      │
      ▼
  SHA-1 Hash  →  "AAF4C61DDCC5E8A2DABEDE0F3B482CD9AEA9434D"
      │
      ├──── PREFIX (first 5 chars): "AAF4C"  ──► Sent to HIBP API
      │
      └──── SUFFIX (remaining 35):  "61DDC..."  ──► Checked LOCALLY only

API returns ~500 hashes starting with "AAF4C"
      │
      ▼
Tool searches the list locally for your suffix
      │
      ├── Match found  →  🚨 Breached! (shows count)
      └── No match     →  ✅ Not found in any breach
```

The API server only ever sees `"AAF4C"` — it has no way to know your full hash or original password.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- Internet connection (for breach check)

Verify your Python version:
```bash
python --version
```

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/your-username/password-strength-checker.git
cd password-strength-checker
```

**2. Install dependencies**
```bash
pip install requests
```

> All other modules (`hashlib`, `getpass`, `re`, `sys`) are part of Python's standard library — no extra installs needed.

### Run the tool
```bash
python password_checker.py
```

On some systems you may need:
```bash
python3 password_checker.py
```

---

## 📁 Project Structure

```
password-strength-checker/
│
├── password_checker.py    # Main script (all logic lives here)
├── README.md              # You're reading this
└── requirements.txt       # Python dependencies
```

---

## 📦 Dependencies

| Package | Version | Purpose |
|---|---|---|
| `requests` | ≥ 2.28.0 | HTTP calls to the HIBP API |

To generate a `requirements.txt`:
```bash
pip freeze > requirements.txt
```

Or create it manually with just:
```
requests
```

---

## 🧠 How the Strength Scoring Works

| Check | Points | Condition |
|---|---|---|
| Length | 1 | 8+ characters |
| Uppercase | 1 | At least one A–Z |
| Lowercase | 1 | At least one a–z |
| Digits | 1 | At least one 0–9 |
| Special Characters | 1 | At least one `!@#$%^&*` etc. |
| Bonus | 1 | 16+ characters |

| Score | Rating |
|---|---|
| 0 – 2 | 🔴 WEAK |
| 3 – 4 | 🟡 MODERATE |
| 5 – 6 | 🟢 STRONG |

---

## ⚠️ Troubleshooting

| Problem | Solution |
|---|---|
| `ModuleNotFoundError: No module named 'requests'` | Run `pip install requests` |
| Password is visible while typing | Use a standard terminal (CMD on Windows, Terminal on Mac/Linux). Avoid Git Bash or some IDEs |
| API timeout or connection error | Check your internet connection. The breach check is skipped gracefully if the API is unreachable |
| `python` command not found | Use `python3` instead |
| `Permission denied` | On Linux/macOS, try `chmod +x password_checker.py` then `./password_checker.py` |

---

## 🔭 Roadmap / Planned Improvements

- [ ] Color output using `colorama`
- [ ] Check multiple passwords from a file with `--file` flag
- [ ] Built-in strong password generator
- [ ] Detect common weak patterns (`password123`, `qwerty`, keyboard walks)
- [ ] Offline mode that skips API call (`--offline` flag)
- [ ] Flask web app wrapper with HTML UI
- [ ] zxcvbn integration (Dropbox's advanced strength estimator)

---

## 📚 What I Learned Building This

- How SHA-1 hashing works and why it's one-way
- What the k-Anonymity model is and why it's important for privacy
- How to make HTTP requests in Python using `requests`
- Using `getpass` for secure terminal input
- Defensive error handling with `try/except`
- Writing modular, readable Python code
- How the Have I Been Pwned API protects user privacy

---

## 📖 Resources

- [Have I Been Pwned API Docs](https://haveibeenpwned.com/API/v3#SearchingPwnedPasswordsByRange)
- [k-Anonymity Explained](https://en.wikipedia.org/wiki/K-anonymity)
- [Python hashlib docs](https://docs.python.org/3/library/hashlib.html)
- [Python getpass docs](https://docs.python.org/3/library/getpass.html)
- [Requests library docs](https://requests.readthedocs.io/)

---

## ⚖️ License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙌 Acknowledgements

- [Troy Hunt](https://www.troyhunt.com/) for creating and maintaining the Have I Been Pwned service
- The cybersecurity community for promoting k-Anonymity as a privacy standard

---

> **Disclaimer:** This tool is for educational purposes. Never enter real passwords you actively use into any tool you didn't write yourself. Use a password manager for real password generation and storage.
