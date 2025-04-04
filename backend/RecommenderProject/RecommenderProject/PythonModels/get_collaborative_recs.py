# get_collaborative_recs.py
import sys
import pickle

# Load the saved model
with open('PythonModels/collaborative_model.sav', 'rb') as f:
    model_data = pickle.load(f)

model = model_data['model']
X = model_data['X']
item_mapper = model_data['item_mapper']
item_inv_mapper = model_data['item_inv_mapper']

# Read args
item_id = int(sys.argv[1])
k = int(sys.argv[2]) if len(sys.argv) > 2 else 5

# Recommend function
def recommend(itemId, X, model, item_mapper, item_inv_mapper, k):
    item_index = item_mapper.get(itemId)
    if item_index is None:
        return []

    item_vector = X[item_index]
    rec = model.kneighbors(item_vector.reshape(1, -1), return_distance=False)
    rec_indices = rec[0][1:k+1]  # Exclude the item itself
    rec_ids = [item_inv_mapper[i] for i in rec_indices]
    return rec_ids

# Run it
recommendations = recommend(item_id, X, model, item_mapper, item_inv_mapper, k)

# Print results (one per line)
for rec_id in recommendations:
    print(rec_id)
