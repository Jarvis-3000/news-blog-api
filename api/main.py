from fastapi import FastAPI, HTTPException, Query
from typing import List
import json
import os

app = FastAPI()

# Define the path to the blogs.json file
BLOGS_FILE_PATH = os.path.join(os.path.dirname(__file__), 'blogs.json')

# Function to load blogs from JSON file
def load_blogs_data():
    with open(BLOGS_FILE_PATH, 'r') as file:
        return json.load(file)

# Load blogs data at startup
blogs_data = load_blogs_data()
blogs_length = len(blogs_data)

@app.get("/blogs", response_model=List[dict])
async def get_blogs(page: int = Query(1, ge=1), limit: int = Query(blogs_length, ge=1)):
    """
    Returns a paginated list of blogs based on page and limit query parameters.
    
    - `page`: The page number.
    - `limit`: The number of blogs to return per page.
    """
    start = (page - 1) * limit
    end = start + limit
    paginated_blogs = blogs_data[start:end]

    if not paginated_blogs:
        raise HTTPException(status_code=404, detail="No blogs found for this page.")

    return paginated_blogs


@app.get("/blogs/{id}", response_model=dict)
async def get_blog_by_id(id: int):
    """
    Returns a single blog by its ID.
    
    - `id`: The blog ID.
    """
    for blog in blogs_data:
        if blog['id'] == id:
            return blog

    raise HTTPException(status_code=404, detail="Blog not found")


# If you want to run the app, use the following:
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
