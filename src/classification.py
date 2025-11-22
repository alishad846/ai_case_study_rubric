from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def semantic_score(text, criterion):
    transcript_embedding = model.encode(text)
    criterion_embedding = model.encode(criterion)
    
    similarity = util.cos_sim(transcript_embedding, criterion_embedding)
    return float(similarity)
