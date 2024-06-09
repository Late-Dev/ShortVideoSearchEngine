import os
import json

from pymilvus import MilvusClient
from pymilvus.model.hybrid import BGEM3EmbeddingFunction
from pymilvus.model.reranker import BGERerankFunction


class SearchEngine:
    def __init__(self, use_reranker=False, distance_threshold = 0.1):

        self.collection_name = "search"
        self.search_db_file = "./search.db"
        self.row_data_path = 'data.json'
        self.distance_threshold = distance_threshold
        self.use_reranker = use_reranker

        self.embedding_fn = BGEM3EmbeddingFunction(
            model_name='BAAI/bge-m3', # Specify the model name
            device='cpu', # Specify the device to use, e.g., 'cpu' or 'cuda:0'
            use_fp16=False # Specify whether to use fp16. Set to `False` if `device` is `cpu`.
        )

        # Define the rerank function
        self.reranker = BGERerankFunction(
            model_name="BAAI/bge-reranker-v2-m3",  # Specify the model name. Defaults to `BAAI/bge-reranker-v2-m3`.
            device="cpu" # Specify the device to use, e.g., 'cpu' or 'cuda:0'
        )

        do_build_index = not os.path.exists(self.search_db_file) and os.path.exists(self.row_data_path)

        self.client = MilvusClient(self.search_db_file)

        if do_build_index:
            self._build_index(self.row_data_path)

        
    def _build_index(self, data_path: str):
        print('INDEX BUILDING')
        with open(data_path, 'r') as data:
            corpus = json.load(data)

        embeddings = self.embedding_fn.encode_documents([line['video_caption'] for line in corpus if line['video_caption']])

        data = [
            {
                "link": doc['link'], 
                "vector": vec, 
                "text": doc['video_caption'],
                "description": doc['description'],

            }
            for doc, vec in zip([line for line in corpus if line['video_caption']], embeddings['dense'])
        ]

        # embeddings = self.embedding_fn.encode_documents([line['speech'] for line in corpus if line['speech']])
        # data += [
        #     {
        #         "link": doc['link'], 
        #         "vector": vec, 
        #         "text": doc['speech'],
        #         "description": doc['description'],

        #     }
        #     for doc, vec in zip([line for line in corpus if line['speech']], embeddings['dense'])
        # ]

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
            output_fields=["link", "text", 'description'],
        )[0]

        if self.use_reranker:
            reranker_result = self.reranker(
                query=query,
                documents=[i['entity']['text'] for i in result],
                top_k=100
            )

            result = [result[i.index] for i in reranker_result]

        result = [
            {
                'link':res['entity']['link'], 
                'description':  res['entity']['description']
            }
            for res in result 
            if res['distance'] > self.distance_threshold
        ]

        return result
