# get_collaborative_recs_user.py
import sys
import pickle

user_id = int(sys.argv[1])
k = int(sys.argv[2]) if len(sys.argv) > 2 else 5

# Load model
with open('PythonModels/collaborative_model.sav', 'rb') as f:
    model_data = pickle.load(f)

model = model_data['model']
X = model_data['X']
item_mapper = model_data['item_mapper']
item_inv_mapper = model_data['item_inv_mapper']
user_mapper = model_data['user_mapper']
df_triple = model_data['df_triple']  # Save this when you update your .sav file

# Recommend logic
def recommend(itemId, X, model, item_mapper, item_inv_mapper, k):
    if itemId not in item_mapper:
        return []
    item_index = item_mapper[itemId]
    item_vector = X[item_index]
    rec = model.kneighbors(item_vector.reshape(1, -1), return_distance=False)
    rec_indices = rec[0][1:k+1]  # skip self
    return [item_inv_mapper[i] for i in rec_indices]

# Step 1: Get items this user interacted with (strong)
df_user = df_triple[(df_triple['personId'] == user_id) & (df_triple['eventType'] >= 2)]

# Step 2: Recommend based on each item
recommended = set()
for content_id in df_user['contentId']:
    recs = recommend(content_id, X, model, item_mapper, item_inv_mapper, k)
    recommended.update(recs)

# Step 3: Remove already-seen items
seen = set(df_user['contentId'])
final_recs = list(recommended - seen)[:k]

# Print result
for rec in final_recs:
    print(rec)
