from fastapi import FastAPI, HTTPException, Query
from typing import List, Dict, Optional
import json
import os
import random

app = FastAPI()

# Define the path to the blogs.json file
BLOGS_FILE_PATH = os.path.join(os.path.dirname(__file__), 'blogs.json')

# Function to load blogs from JSON file
def load_blogs_data():
    with open(BLOGS_FILE_PATH, 'r') as file:
        return json.load(file)

# Load blogs data at startup
blogs_data = load_blogs_data()
total_items = len(blogs_data)

@app.get("/blogs", response_model=Dict)
async def get_blogs(page: int = Query(1, ge=1), limit: int = Query(total_items, ge=1)):
    """
    Returns a paginated list of blogs along with pagination metadata.

    - `page`: The page number.
    - `limit`: The number of blogs to return per page.
    """
    
    total_pages = (total_items + limit - 1) // limit  # Calculate the total number of pages
    print(total_items, " " ,total_pages)

    # Ensure the requested page number is within valid range
    if page > total_pages or page < 1:
        raise HTTPException(status_code=402, detail="Invalid request")

    # Pagination logic
    start = (page - 1) * limit
    end = start + limit
    paginated_blogs = blogs_data[start:end]

    next_page = page + 1 if page < total_pages else None
    prev_page = page - 1 if page > 1 else None

    # Return paginated results and pagination details
    return {
        "page": page,
        "pages": total_pages,
        "next": next_page,
        "prev": prev_page,
        "count": total_items,
        "blogs": paginated_blogs
    }

@app.get("/blogs/top-ten", response_model=Dict)
async def get_random_news():
    # Select 10 random news items
    random_news = random.sample(blogs_data, 10)
    
    return {
        "page": 1,
        "pages": 1,
        "next": None,
        "prev": None,
        "count": len(random_news),
        "blogs": random_news
        }


@app.get("/blogs/{id}", response_model=dict)
async def get_blog_by_id(id: int):
    """
    Returns a single blog by its ID.
    
    - `id`: The blog ID.
    """
    for blog in blogs_data:
        if blog.get('id') == id:
            return blog

    raise HTTPException(status_code=404, detail="Blog not found")


# If you want to run the app, use the following:
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
