
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# FAQ data load karna
faq = pd.read_csv("faq_data.csv")

# Questions ko machine-readable banana
vectorizer = TfidfVectorizer()
question_vectors = vectorizer.fit_transform(faq["question"])

# User ke question ka answer khojna
def get_faq_answer(user_question):

    user_vector = vectorizer.transform([user_question])

    scores = cosine_similarity(
        user_vector,
        question_vectors
    )

    best_match = scores.argmax()
    confidence = scores[0][best_match]

    if confidence < 0.40:
    return "Sorry! I don't know the answer yet."
        return "Sorry, mujhe iska jawab abhi nahi pata."

    return faq.iloc[best_match]["answer"]
