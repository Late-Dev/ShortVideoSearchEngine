import asyncio
import csv
from app.videos_db import add_video_data

from dotenv import load_dotenv

load_dotenv()

async def load_csv_to_mongodb(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        tasks = []
        for row in csv_reader:
            tasks.append(add_video_data(row))
        
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    file_path = 'static/yappy_hackaton_2024_400k.csv'
    asyncio.run(load_csv_to_mongodb(file_path))
