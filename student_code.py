from collections import Counter, defaultdict
import time
from typing import Dict, List, Set, Tuple
import requests

def extract_binary_patterns(binary_text: str) -> List[str]:
    """Extract 8-bit patterns from binary text"""
    return [binary_text[i:i+8] for i in range(0, len(binary_text), 8) if len(binary_text[i:i+8]) == 8]

def analyze_pattern_frequencies(patterns: List[str]) -> Dict[str, float]:
    """Analyze pattern frequencies in the encrypted text"""
    total = len(patterns)
    return {pattern: count/total for pattern, count in Counter(patterns).items()}

def get_french_letter_frequencies() -> Dict[str, float]:
    """Get French language character frequencies"""
    return {
        'e': 0.1726, ' ': 0.1635, 's': 0.0798, 'a': 0.0784, 'i': 0.0757,
        't': 0.0732, 'n': 0.0728, 'r': 0.0658, 'l': 0.0554, 'u': 0.0527,
        'o': 0.0518, 'd': 0.0372, 'c': 0.0328, 'p': 0.0289, 'm': 0.0265,
        'é': 0.0228, 'v': 0.0132, 'q': 0.0138, 'f': 0.0108, 'b': 0.0092,
        'g': 0.0089, 'h': 0.0076, 'j': 0.0056, 'à': 0.0048, 'x': 0.0039,
        'y': 0.0033, 'z': 0.0016, 'w': 0.0011, 'k': 0.0002, 'è': 0.0025,
        'ê': 0.0024, 'â': 0.0016, 'î': 0.0007, 'ô': 0.0006, 'û': 0.0005,
        'ë': 0.0004, 'ï': 0.0003, 'ù': 0.0002, '\n': 0.0105, '\r': 0.0102,
        '.': 0.0065, ',': 0.0054, ';': 0.0022, ':': 0.0021, '!': 0.0012,
        '?': 0.0011, '-': 0.0010, '_': 0.0009, '"': 0.0008, "'": 0.0007,
        '(': 0.0006, ')': 0.0006
    }

def get_french_bigram_frequencies() -> Dict[str, float]:
    """Get French language bigram frequencies"""
    return {
        'es': 0.0324, 'le': 0.0318, 'de': 0.0296, 'en': 0.0288, 're': 0.0285,
        'nt': 0.0278, 'on': 0.0265, 'er': 0.0258, 'te': 0.0248, 'an': 0.0239,
        'in': 0.0229, 'qu': 0.0220, 'el': 0.0216, 'se': 0.0212, 'it': 0.0187,
        'ur': 0.0186, 'et': 0.0181, 'ai': 0.0180, 'em': 0.0178, 'ou': 0.0174,
        ' l': 0.0173, ' d': 0.0168, 'e ': 0.0163, 's ': 0.0158, ' p': 0.0153,
        'é ': 0.0148, ' é': 0.0143, 'à ': 0.0138, ' à': 0.0133, 'la': 0.0128
    }

def get_common_patterns() -> Set[str]:
    """Get common French language patterns"""
    return {
        'le ', 'la ', 'les ', 'de ', 'des ', 'du ', 'un ', 'une ',
        'et ', 'ou ', 'mais ', 'donc ', 'car ', 'que ', 'qui ',
        'quoi ', 'où ', 'quand ', 'comment ', 'pourquoi ',
        '. ', ', ', '; ', ': ', '? ', '! ',
        'tion', 'ement', 'ment', 'ant', 'ent', 'able', 'ible',
        'aux', 'eux', 'ouse', 'aine', 'elle', 'esse', 'ette'
    }

def score_mapping(pattern_freq: float, char: str, prev_char: str = None, next_char: str = None) -> float:
    """Score a potential mapping based on frequencies and context"""
    char_freqs = get_french_letter_frequencies()
    bigram_freqs = get_french_bigram_frequencies()
    
    # Base frequency score
    base_score = -abs(pattern_freq - char_freqs.get(char, 0))
    
    # Context score using bigrams
    context_score = 0
    if prev_char:
        bigram = prev_char + char
        if bigram in bigram_freqs:
            context_score += bigram_freqs[bigram]
    if next_char:
        bigram = char + next_char
        if bigram in bigram_freqs:
            context_score += bigram_freqs[bigram]
    
    return base_score + (context_score * 1.5)

def decrypt(C: str) -> str:
    """Decrypt French text using pattern analysis and frequency matching"""
    # Extract patterns
    patterns = extract_binary_patterns(C)
    pattern_freqs = analyze_pattern_frequencies(patterns)
    
    # Initialize mapping
    char_freqs = get_french_letter_frequencies()
    common_patterns = get_common_patterns()
    mapping = {}
    used_chars = set()
    
    # First pass: Map most frequent patterns to most frequent characters
    sorted_patterns = sorted(pattern_freqs.items(), key=lambda x: x[1], reverse=True)
    sorted_chars = sorted(char_freqs.items(), key=lambda x: x[1], reverse=True)
    
    # Initialize with high-confidence mappings
    for (pattern, p_freq), (char, c_freq) in zip(sorted_patterns[:10], sorted_chars[:10]):
        if abs(p_freq - c_freq) < 0.02:  # Only map if frequencies are close
            mapping[pattern] = char
            used_chars.add(char)
    
    # Second pass: Use context and patterns
    max_iterations = 100
    iteration = 0
    while len(mapping) < len(pattern_freqs) and iteration < max_iterations:
        iteration += 1
        changes_made = False
        
        # Try to map unmapped patterns
        for pattern in pattern_freqs:
            if pattern in mapping:
                continue
                
            best_score = float('-inf')
            best_char = None
            
            # Find position context
            pattern_positions = [i for i, p in enumerate(patterns) if p == pattern]
            for pos in pattern_positions:
                prev_char = mapping.get(patterns[pos-1]) if pos > 0 else None
                next_char = mapping.get(patterns[pos+1]) if pos < len(patterns)-1 else None
                
                # Try each unused character
                for char in char_freqs:
                    if char in used_chars:
                        continue
                        
                    score = score_mapping(pattern_freqs[pattern], char, prev_char, next_char)
                    
                    # Bonus for common patterns
                    if prev_char and next_char:
                        context = prev_char + char + next_char
                        if context in common_patterns:
                            score += 0.1
                    
                    if score > best_score:
                        best_score = score
                        best_char = char
            
            if best_char:
                mapping[pattern] = best_char
                used_chars.add(best_char)
                changes_made = True
        
        if not changes_made:
            break
    
    # Fill remaining patterns
    remaining_chars = set(char_freqs.keys()) - used_chars
    for pattern in pattern_freqs:
        if pattern not in mapping and remaining_chars:
            mapping[pattern] = remaining_chars.pop()
    
    # Map any unmapped patterns to underscore
    result = []
    for pattern in patterns:
        result.append(mapping.get(pattern, '_'))
    
    return ''.join(result)
