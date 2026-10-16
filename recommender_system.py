import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error
from scipy.sparse.linalg import svds

class RecommenderSystem:
    def __init__(self, ratings_df):
        self.ratings_df = ratings_df
        self.user_item_matrix = ratings_df.pivot(index='user_id', columns='item_id', values='rating').fillna(0)
        
    def collaborative_filtering_user(self, user_id, top_n=5):
        """User-based collaborative filtering using cosine similarity."""
        similarity_matrix = cosine_similarity(self.user_item_matrix)
        similarity_df = pd.DataFrame(similarity_matrix, index=self.user_item_matrix.index, columns=self.user_item_matrix.index)
        
        # Find similar users
        similar_users = similarity_df[user_id].sort_values(ascending=False).index[1:]
        
        user_ratings = self.user_item_matrix.loc[user_id]
        recommendations = {}
        
        for other_user in similar_users:
            other_ratings = self.user_item_matrix.loc[other_user]
            for item, rating in other_ratings.items():
                if user_ratings[item] == 0 and rating > 0:
                    if item not in recommendations:
                        recommendations[item] = rating
                        
        sorted_recs = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)[:top_n]
        return sorted_recs

    def matrix_factorization_svd(self, k=3):
        """Matrix Factorization using SVD."""
        matrix = self.user_item_matrix.values
        user_ratings_mean = np.mean(matrix, axis=1)
        matrix_demeaned = matrix - user_ratings_mean.reshape(-1, 1)
        
        U, sigma, Vt = svds(matrix_demeaned, k=k)
        sigma = np.diag(sigma)
        
        predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)
        preds_df = pd.DataFrame(predicted_ratings, index=self.user_item_matrix.index, columns=self.user_item_matrix.columns)
        return preds_df

if __name__ == "__main__":
    print("[INFO] Running Recommender System Pipeline...")
    # Sample ratings data
    data = {
        'user_id': [1, 1, 1, 2, 2, 3, 3, 3, 4, 4],
        'item_id': [101, 102, 103, 101, 104, 102, 103, 105, 101, 105],
        'rating': [5, 3, 4, 4, 2, 4, 5, 3, 2, 5]
    }
    df = pd.DataFrame(data)
    
    rec_sys = RecommenderSystem(df)
    print("\n[INFO] User-based recommendations for User 1:")
    print(rec_sys.collaborative_filtering_user(1))
    
    print("\n[INFO] Matrix Factorization SVD Predictions:")
    print(rec_sys.matrix_factorization_svd(k=2))
    print("\n[SUCCESS] Recommender System pipeline executed successfully!")