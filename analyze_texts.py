#!/usr/bin/env python3
"""
Distant Reading Analysis of Plant Lore Texts
Analyzes two historical texts about plant folklore and generates visualizations.
"""

import json
import re
from collections import Counter
from pathlib import Path
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

# Download required NLTK data
print("Downloading NLTK data...")
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('punkt_tab', quiet=True)

class TextAnalyzer:
    """Analyzes historical texts for distant reading."""

    def __init__(self, filepath, title, author):
        self.filepath = filepath
        self.title = title
        self.author = author
        self.raw_text = ""
        self.clean_text = ""
        self.tokens = []
        self.bag_of_words = Counter()
        self.sentiment = {}
        self.stop_words = set(stopwords.words('english'))

    def load_text(self):
        """Load text file handling UTF-8 BOM."""
        print(f"Loading {self.title}...")
        with open(self.filepath, 'r', encoding='utf-8-sig') as f:
            self.raw_text = f.read()

    def strip_gutenberg_metadata(self):
        """Remove Project Gutenberg headers and footers."""
        # Find start marker
        start_match = re.search(r'\*\*\* START OF [^\*]+\*\*\*', self.raw_text)
        # Find end marker
        end_match = re.search(r'\*\*\* END OF [^\*]+\*\*\*', self.raw_text)

        if start_match and end_match:
            self.clean_text = self.raw_text[start_match.end():end_match.start()]
        else:
            # Fallback: use entire text
            self.clean_text = self.raw_text

        print(f"  Stripped metadata. Text length: {len(self.clean_text)} characters")

    def preprocess(self):
        """Clean and tokenize text."""
        print(f"Preprocessing {self.title}...")

        # Convert to lowercase
        text = self.clean_text.lower()

        # Remove special formatting markers (underscores, plus signs, brackets)
        text = re.sub(r'[_+=\[\]{}]', ' ', text)

        # Tokenize
        self.tokens = word_tokenize(text)

        # Filter: keep only alphabetic tokens, remove stopwords
        filtered_tokens = [
            token for token in self.tokens
            if token.isalpha() and token not in self.stop_words and len(token) > 2
        ]

        # Build bag of words
        self.bag_of_words = Counter(filtered_tokens)

        print(f"  Total tokens: {len(self.tokens)}")
        print(f"  Filtered tokens: {len(filtered_tokens)}")
        print(f"  Unique words: {len(self.bag_of_words)}")

    def analyze_sentiment(self):
        """Conduct VADER sentiment analysis on entire text."""
        print(f"Analyzing sentiment for {self.title}...")
        analyzer = SentimentIntensityAnalyzer()

        # VADER works better on smaller chunks, but we'll analyze the whole text
        # as requested, using a representative sample if too large
        text_sample = self.clean_text[:1000000]  # First ~1MB

        scores = analyzer.polarity_scores(text_sample)
        self.sentiment = {
            'positive': scores['pos'],
            'negative': scores['neg'],
            'neutral': scores['neu'],
            'compound': scores['compound']
        }

        print(f"  Compound sentiment: {self.sentiment['compound']:.3f}")

    def generate_wordcloud(self, output_path, colors):
        """Generate word cloud image with Victorian botanical palette."""
        print(f"Generating word cloud for {self.title}...")

        # Create word cloud
        wc = WordCloud(
            width=1200,
            height=800,
            background_color='#F5F5DC',  # Beige/cream background
            colormap=colors,
            max_words=200,
            relative_scaling=0.5,
            min_font_size=10
        ).generate_from_frequencies(self.bag_of_words)

        # Save to file
        plt.figure(figsize=(15, 10))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout(pad=0)
        plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='#F5F5DC')
        plt.close()

        print(f"  Saved word cloud to {output_path}")

    def get_top_words(self, n=50):
        """Get top N most common words."""
        return self.bag_of_words.most_common(n)

    def to_dict(self):
        """Convert analysis to dictionary for JSON export."""
        return {
            'title': self.title,
            'author': self.author,
            'total_words': len(self.tokens),
            'unique_words': len(self.bag_of_words),
            'lexical_diversity': len(self.bag_of_words) / len(self.tokens) if self.tokens else 0,
            'sentiment': self.sentiment,
            'top_words': [{'word': word, 'count': count} for word, count in self.get_top_words(100)],
            'bag_of_words': dict(self.get_top_words(500))  # Top 500 for word cloud data
        }


def compare_texts(analyzer1, analyzer2):
    """Compare two texts and find overlapping vocabulary."""
    print("\nComparing texts...")

    words1 = set(analyzer1.bag_of_words.keys())
    words2 = set(analyzer2.bag_of_words.keys())

    shared_words = words1.intersection(words2)
    unique_to_1 = words1 - words2
    unique_to_2 = words2 - words1

    # Get top shared words by combined frequency
    shared_word_freq = {
        word: analyzer1.bag_of_words[word] + analyzer2.bag_of_words[word]
        for word in shared_words
    }
    top_shared = sorted(shared_word_freq.items(), key=lambda x: x[1], reverse=True)[:50]

    overlap_percentage = len(shared_words) / len(words1.union(words2)) * 100 if words1.union(words2) else 0

    comparison = {
        'total_shared_words': len(shared_words),
        'unique_to_folkard': len(unique_to_1),
        'unique_to_shakespeare': len(unique_to_2),
        'overlap_percentage': overlap_percentage,
        'top_shared_words': [{'word': word, 'combined_count': count} for word, count in top_shared],
        'top_unique_folkard': [word for word in list(unique_to_1)[:30]],
        'top_unique_shakespeare': [word for word in list(unique_to_2)[:30]]
    }

    print(f"  Shared words: {len(shared_words)}")
    print(f"  Unique to Folkard: {len(unique_to_1)}")
    print(f"  Unique to Shakespeare: {len(unique_to_2)}")
    print(f"  Overlap: {overlap_percentage:.2f}%")

    return comparison


def main():
    """Main analysis pipeline."""
    print("=" * 60)
    print("Plant Lore Distant Reading Analysis")
    print("=" * 60)

    # Initialize analyzers
    folkard = TextAnalyzer(
        'Plant Lore Legends and Lyrics Text File.txt',
        'Plant Lore, Legends, and Lyrics',
        'Richard Folkard, Jun.'
    )

    shakespeare = TextAnalyzer(
        'Plant Lore and Garden Craft of Shakespeare.txt',
        'The Plant-Lore & Garden-Craft of Shakespeare',
        'Henry Nicholson Ellacombe'
    )

    # Process Folkard text
    print("\n--- Processing Folkard Text ---")
    folkard.load_text()
    folkard.strip_gutenberg_metadata()
    folkard.preprocess()
    folkard.analyze_sentiment()
    folkard.generate_wordcloud('wordcloud_folkard.png', 'YlGn')  # Yellow-Green for botanical

    # Process Shakespeare text
    print("\n--- Processing Shakespeare Text ---")
    shakespeare.load_text()
    shakespeare.strip_gutenberg_metadata()
    shakespeare.preprocess()
    shakespeare.analyze_sentiment()
    shakespeare.generate_wordcloud('wordcloud_shakespeare.png', 'RdPu')  # Red-Purple for Victorian

    # Compare texts
    comparison = compare_texts(folkard, shakespeare)

    # Create comprehensive JSON output
    print("\n--- Creating JSON Output ---")
    analysis_data = {
        'texts': [
            folkard.to_dict(),
            shakespeare.to_dict()
        ],
        'comparison': comparison,
        'metadata': {
            'analysis_type': 'distant_reading',
            'sentiment_method': 'VADER',
            'stopwords_removed': True,
            'wordcloud_images': {
                'folkard': 'wordcloud_folkard.png',
                'shakespeare': 'wordcloud_shakespeare.png'
            }
        }
    }

    with open('analysis.json', 'w', encoding='utf-8') as f:
        json.dump(analysis_data, f, indent=2, ensure_ascii=False)

    print("  Saved analysis.json")
    print("\n" + "=" * 60)
    print("Analysis complete!")
    print("=" * 60)
    print(f"\nGenerated files:")
    print("  - analysis.json")
    print("  - wordcloud_folkard.png")
    print("  - wordcloud_shakespeare.png")


if __name__ == '__main__':
    main()
