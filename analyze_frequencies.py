import requests
from collections import Counter
from typing import Dict, List, Tuple

def load_text_from_web(url: str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error loading text from {url}: {e}")
        return ""

def analyze_text(text: str) -> Tuple[Dict[str, float], Dict[str, float], Dict[str, float]]:
    # Calculate character frequencies
    total_chars = len(text)
    char_counts = Counter(text)
    char_freqs = {char: count/total_chars for char, count in char_counts.items()}
    
    # Calculate bigram frequencies
    bigrams = [text[i:i+2] for i in range(len(text)-1)]
    total_bigrams = len(bigrams)
    bigram_counts = Counter(bigrams)
    bigram_freqs = {bigram: count/total_bigrams for bigram, count in bigram_counts.most_common(100)}
    
    # Calculate common word patterns (including spaces)
    words = text.split()
    patterns = []
    for word in words:
        if len(word) >= 2:
            patterns.extend([f" {word[:2]}", f"{word[-2:]} "])
    pattern_counts = Counter(patterns)
    total_patterns = len(patterns)
    pattern_freqs = {pattern: count/total_patterns for pattern, count in pattern_counts.most_common(50)}
    
    return char_freqs, bigram_freqs, pattern_freqs

def main():
    # Load texts from Project Gutenberg
    urls = [
        "https://www.gutenberg.org/ebooks/13846.txt.utf-8",  # Descartes
        "https://www.gutenberg.org/ebooks/4650.txt.utf-8"    # Voltaire
    ]
    
    combined_text = ""
    for url in urls:
        text = load_text_from_web(url)
        # Remove Project Gutenberg header/footer
        if text:
            start_idx = text.find("*** START OF")
            end_idx = text.find("*** END OF")
            if start_idx != -1 and end_idx != -1:
                text = text[start_idx:end_idx]
            combined_text += text
    
    # Analyze frequencies
    char_freqs, bigram_freqs, pattern_freqs = analyze_text(combined_text)
    
    # Print results for verification
    print("\nCharacter Frequencies:")
    for char, freq in sorted(char_freqs.items(), key=lambda x: x[1], reverse=True)[:50]:
        if char.isprintable():
            print(f"'{char}': {freq:.4f}, ", end='')
    
    print("\n\nBigram Frequencies:")
    for bigram, freq in sorted(bigram_freqs.items(), key=lambda x: x[1], reverse=True)[:50]:
        if all(c.isprintable() for c in bigram):
            print(f"'{bigram}': {freq:.4f}, ", end='')
    
    print("\n\nPattern Frequencies:")
    for pattern, freq in sorted(pattern_freqs.items(), key=lambda x: x[1], reverse=True)[:30]:
        if all(c.isprintable() for c in pattern):
            print(f"'{pattern}': {freq:.4f}, ", end='')

if __name__ == "__main__":
    main()
