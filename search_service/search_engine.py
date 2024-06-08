import os
import json

from pymilvus import MilvusClient
from pymilvus.model.hybrid import BGEM3EmbeddingFunction


class SearchEngine:
    def __init__(self):

        self.collection_name = "search"
        self.search_db_file = "./search.db"
        self.row_data_path = 'data.json'
        self.distance_threshold = 0.1

        self.embedding_fn = BGEM3EmbeddingFunction(
            model_name='BAAI/bge-m3', # Specify the model name
            device='cpu', # Specify the device to use, e.g., 'cpu' or 'cuda:0'
            use_fp16=False # Specify whether to use fp16. Set to `False` if `device` is `cpu`.
        )

        do_build_index = not os.path.exists(self.search_db_file) and os.path.exists(self.row_data_path)

        self.client = MilvusClient(self.search_db_file)

        if do_build_index:
            self._build_index(self.row_data_path)

        
    def _build_index(self, data_path: str):
        print('INDEX BUILDING')
        with open(data_path, 'r') as data:
            corpus = json.load(data)

        embeddings = self.embedding_fn.encode_documents([line['description'] for line in corpus])

        data = [
            {
                "link": doc['link'], 
                "vector": vec, 
                "text": doc['description']
            }
            for doc, vec in zip(corpus, embeddings['dense'])
        ]

        self.client.create_collection(
            collection_name=self.collection_name,
            dimension=1024,
            auto_id=True
        )

        self.client.insert(collection_name=self.collection_name, data=data)

    def search(self, query: str):
        query_embeddings = self.embedding_fn.encode_queries([query])['dense']

        result = self.client.search(
            collection_name=self.collection_name,
            data=query_embeddings,
            limit=100,
            output_fields=["link"],
        )[0]

        result = [
            res['entity']['link'] 
            for res in result 
            if res['distance'] > self.distance_threshold
        ]

        return result
