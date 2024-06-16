import os
import json

from pymilvus import MilvusClient
import pandas as pd
from thefuzz import fuzz, process


class SearchEngine:
    def __init__(self, use_reranker=False, distance_threshold = 0.3):

        self.collection_name = "search"
        self.search_db_file = "./search.db"
        self.row_data_path = 'data.json'
        self.distance_threshold = distance_threshold
        self.df_user_name = pd.read_csv('users.csv')
        self.users_name = self.df_user_name['user_name'].tolist()

        do_build_index = not os.path.exists(self.search_db_file) and os.path.exists(self.row_data_path)

        self.client = MilvusClient(self.search_db_file)

        if do_build_index:
            self._build_index(self.row_data_path)
        else:
            self.client.create_collection(
                collection_name=self.collection_name,
                dimension=512,
                auto_id=True
            )

        
    def _build_index(self, data_path: str):
        print('INDEX BUILDING')
        with open(data_path, 'r') as data:
            corpus = json.load(data)

        data = [
            {
                "link": doc['link'], 
                "vector": vec, 
                "text": '',
                "description": doc['description'],

            }
            for doc in corpus for vec in doc['video_face_embeddings']
        ]

        self.client.create_collection(
            collection_name=self.collection_name,
            dimension=512,
            auto_id=True
        )

        self.client.insert(collection_name=self.collection_name, data=data)

    def search(self, query: str):

        results = process.extractBests(query, self.users_name, scorer=fuzz.ratio, score_cutoff=70)
        
        if results:
            results = results[0][0]
        else:
            return []

        query_embeddings = self.df_user_name[self.df_user_name['user_name'] == results]['embedding'].tolist()
        query_embeddings = [json.loads(emb) for emb in query_embeddings]

        result = self.client.search(
            collection_name=self.collection_name,
            data=query_embeddings,
            limit=100,
            output_fields=["link", "text", 'description'],
        )[0]

        result = [
            {
                'link':res['entity']['link'], 
                'description':  res['entity']['description']
            }
            for res in result 
            if res['distance'] > self.distance_threshold
        ]

        return result

    def add_video(self, video):
        data = [
            {
                "link": video.link, 
                "vector": vec, 
                "text": '',
                "description": video.description,

            } for vec in video.video_face_embeddings
        ]

        self.client.insert(collection_name=self.collection_name, data=data)
        return {'success': True}
