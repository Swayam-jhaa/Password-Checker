# =============================================================
# Password Strength Checker + Breach Detection Tool
# Uses: Have I Been Pwned API (k-anonymity model)
# Author: You | Level: Beginner-Friendly
# =============================================================

import hashlib       # For SHA-1 hashing
import getpass       # For hidden password input (doesn't echo to terminal)
import re            # For regex pattern matching
import requests      # For making HTTP API calls
import sys           # For clean program exit


# ─────────────────────────────────────────────
# SECTION 1: Password Strength Checker
# ─────────────────────────────────────────────

def check_length(password):
    """
    Check if the password meets minimum length requirements.
    Returns a tuple: (passed: bool, feedback: str)
    """
    length = len(password)
    if length < 8:
        return False, f"❌ Too short ({length} chars). Use at least 8 characters."
    elif length < 12:
        return True, f"⚠️  Acceptable length ({length} chars). 12+ is recommended."
    else:
        return True, f"✅ Good length ({length} chars)."


def check_uppercase(password):
    """Check if password contains at least one uppercase letter (A-Z)."""
    if re.search(r'[A-Z]', password):
        return True, "✅ Contains uppercase letters."
    return False, "❌ Missing uppercase letters (A-Z)."


def check_lowercase(password):
    """Check if password contains at least one lowercase letter (a-z)."""
    if re.search(r'[a-z]', password):
        return True, "✅ Contains lowercase letters."
    return False, "❌ Missing lowercase letters (a-z)."


def check_digits(password):
    """Check if password contains at least one numeric digit (0-9)."""
    if re.search(r'[0-9]', password):
        return True, "✅ Contains numbers."
    return False, "❌ Missing numbers (0-9)."


def check_special_chars(password):
    """Check if password contains at least one special character."""
    # Common special characters that add entropy to a password
    if re.search(r'[!@#$%^&*(),.?":{}|<>_\-\[\]\/\\]', password):
        return True, "✅ Contains special characters."
    return False, "❌ Missing special characters (!@#$%^&* etc.)."


def evaluate_strength(password):
    """
    Run all checks and compute an overall strength score.
    
    Scoring system:
      - Each check contributes 1 point (max 5 points)
      - Length check is weighted more (contributes up to 2 points)
      
    Returns:
      score (int), rating (str), all feedback messages (list)
    """
    feedback = []
    score = 0

    # Run each individual check
    checks = [
        check_length(password),
        check_uppercase(password),
        check_lowercase(password),
        check_digits(password),
        check_special_chars(password),
    ]

    for passed, message in checks:
        feedback.append(message)
        if passed:
            score += 1

    # Bonus point for being extra long (16+ characters)
    if len(password) >= 16:
        score += 1
        feedback.append("🌟 Bonus: Very long password (16+ chars)!")

    # Classify based on total score
    if score <= 2:
        rating = "🔴 WEAK"
    elif score <= 4:
        rating = "🟡 MODERATE"
    else:
        rating = "🟢 STRONG"

    return score, rating, feedback


# ─────────────────────────────────────────────
# SECTION 2: Have I Been Pwned Breach Check
# ─────────────────────────────────────────────

def hash_password(password):
    """
    Convert the password into a SHA-1 hash string.
    
    SHA-1 produces a 40-character hexadecimal string.
    Example: "hello" → "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d"
    
    We use .upper() to match the format HIBP returns.
    """
    # Encode password to bytes, then apply SHA-1
    sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    return sha1_hash


def query_hibp_api(hash_prefix):
    """
    Send the first 5 characters of the SHA-1 hash to the HIBP API.
    
    HIBP API endpoint: https://api.pwnedpasswords.com/range/{prefix}
    
    Returns a list of (suffix, count) tuples if successful.
    Returns None if the request fails.
    """
    url = f"https://api.pwnedpasswords.com/range/{hash_prefix}"
    
    # Add a User-Agent header — good practice for API calls
    headers = {"User-Agent": "PasswordStrengthChecker-Learning-Project"}
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        
        # HTTP 200 means success
        if response.status_code == 200:
            # Response looks like:
            # "SUFFIX1:COUNT1\nSUFFIX2:COUNT2\n..."
            # We split by line, then by colon
            entries = []
            for line in response.text.splitlines():
                parts = line.split(':')
                if len(parts) == 2:
                    suffix, count = parts
                    entries.append((suffix.strip(), int(count.strip())))
            return entries
        else:
            print(f"⚠️  API returned status code: {response.status_code}")
            return None

    except requests.exceptions.ConnectionError:
        print("❌ No internet connection. Skipping breach check.")
        return None
    except requests.exceptions.Timeout:
        print("❌ API request timed out. Try again later.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ API request failed: {e}")
        return None


def check_breach(password):
    """
    Main breach-check function.
    
    Steps:
      1. Hash the password with SHA-1
      2. Split into prefix (first 5 chars) and suffix (rest)
      3. Send only the prefix to HIBP
      4. Search the response for our suffix
      5. Return breach count (0 if not found)
    """
    print("\n🔍 Checking against known data breaches...")
    
    # Step 1: Get SHA-1 hash
    full_hash = hash_password(password)
    
    # Step 2: Split the hash
    prefix = full_hash[:5]   # First 5 chars → sent to API
    suffix = full_hash[5:]   # Remaining 35 chars → checked locally
    
    # Step 3: Query the API
    results = query_hibp_api(prefix)
    
    if results is None:
        print("⚠️  Could not complete breach check.")
        return
    
    # Step 4: Search for our suffix in the returned list
    for returned_suffix, count in results:
        if returned_suffix == suffix:
            # Found a match → password was in a breach
            print(f"\n🚨 BREACH ALERT! This password has appeared in {count:,} known data breaches!")
            print("   You should NEVER use this password anywhere.")
            return
    
    # Step 5: Suffix not found → password is clean
    print("✅ Great news! This password was NOT found in any known data breaches.")


# ─────────────────────────────────────────────
# SECTION 3: Display & Main Program
# ─────────────────────────────────────────────

def print_divider(char="─", length=50):
    """Print a visual divider line."""
    print(char * length)


def display_results(password):
    """
    Orchestrate the full analysis and display results cleanly.
    """
    print_divider("═")
    print("        🔐 PASSWORD STRENGTH ANALYSIS")
    print_divider("═")

    # --- Strength Evaluation ---
    score, rating, feedback = evaluate_strength(password)

    print(f"\n📊 Overall Rating: {rating}  (Score: {score}/6)\n")
    print_divider()
    print("📋 Detailed Breakdown:")
    print_divider()
    for line in feedback:
        print(f"  {line}")

    # --- Breach Check ---
    print_divider()
    check_breach(password)
    print_divider("═")


def main():
    """
    Entry point of the program.
    Uses getpass so the password doesn't appear on screen while typing.
    """
    print("\n" + "═" * 50)
    print("   🛡️  Password Strength Checker + Breach Detector")
    print("═" * 50)
    print("  Your password is hashed locally and never sent")
    print("  to any server in full. (k-Anonymity model) ✅")
    print("═" * 50 + "\n")

    try:
        # getpass hides the input — it won't show on screen
        password = getpass.getpass("Enter a password to analyze: ")
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\n\n👋 Exited. No password was stored or transmitted.")
        sys.exit(0)

    # Don't allow empty input
    if not password.strip():
        print("❌ No password entered. Exiting.")
        sys.exit(1)

    display_results(password)
    print("\n💡 Tip: Use a password manager to generate and store strong passwords.")
    print()


# Standard Python entry point guard
if __name__ == "__main__":
    main()