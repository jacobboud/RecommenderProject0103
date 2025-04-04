# get_content_recs.py
import sys
import pickle
from sklearn.metrics.pairwise import cosine_similarity

# Input args
input_id = int(sys.argv[1])
k = int(sys.argv[2]) if len(sys.argv) > 2 else 5
input_type = sys.argv[3].lower() if len(sys.argv) > 3 else "item"

# Load the model
with open('PythonModels/content_model.sav', 'rb') as f:
    model = pickle.load(f)

tfidf = model["tfidf_vectorizer"]
tfidf_matrix = model["tfidf_matrix"]
title_to_index = model["title_to_index"]
index_to_id = model["index_to_id"]
content_ids = model["content_ids"]
content_titles = model["content_titles"]
df_users = model["df_users"]

# Helper: Recommend for one article index
def get_recs_for_index(index, seen_ids):
    article_vector = tfidf_matrix[index:index+1]
    sim_scores = cosine_similarity(article_vector, tfidf_matrix).flatten()
    sim_indices = sim_scores.argsort()[::-1]

    recs = []
    for i in sim_indices:
        rec_id = index_to_id[i]
        if i != index and rec_id not in seen_ids and rec_id not in recs:
            recs.append(rec_id)
        if len(recs) >= k:
            break
    return recs

# Gather all recommendations (deduplicated after collection)
seen_ids = set()
all_recs = []

if input_type == "item":
    try:
        index = content_ids.index(input_id)
        seen_ids.add(input_id)
        all_recs.extend(get_recs_for_index(index, seen_ids))
    except ValueError:
        pass

elif input_type == "user":
    # Get user's strongly rated content (LIKE or higher)
    strong_interactions = df_users[
        (df_users['personId'] == input_id) &
        (df_users['eventType'].isin(['LIKE', 'BOOKMARK', 'COMMENT CREATED']))
    ]

    seen_ids.update(strong_interactions['contentId'])

    for cid in seen_ids:
        if cid in content_ids:
            try:
                index = content_ids.index(cid)
                recs = get_recs_for_index(index, seen_ids.union(all_recs))
                all_recs.extend(recs)
            except ValueError:
                continue

# Deduplicate and get final top-k
final_recs = []
unique_ids = set()

for rec in all_recs:
    if rec not in unique_ids:
        final_recs.append(rec)
        unique_ids.add(rec)
    if len(final_recs) == k:
        break

# Output
for rec_id in final_recs:
    print(rec_id)
