import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')

def detect_text_plagiarism(text1, text2):
    vectorizer = TfidfVectorizer().fit_transform([text1, text2])
    vectors = vectorizer.toarray()
    similarity = cosine_similarity(vectors)
    return similarity[0][1]  # Similarity between the two texts

# # Example usage
# text1 = "This is a sample text."
# text2 = "This is another text."
# similarity_score = detect_text_plagiarism(text1, text2)
# print(f"Text Similarity: {similarity_score}")
