import os
from dotenv import load_dotenv 
from fastapi import FastAPI
from utils.supabase import unique_view_exists, url_exists, init_supabase_client
from fastapi.middleware.cors import CORSMiddleware
from utils.models import Viewer, Url

load_dotenv()
app = FastAPI()
supabase = init_supabase_client(url=os.getenv("SUPABASE_API_URL"), key=os.getenv("SUPABASE_API_KEY"))

origins = [
    "http://localhost",
    "http://localhost:8000",
    "https://thefriendlyskies.net"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# add view
@app.post("/api/create_view", response_model=None)
def create_view(viewer_instance: Viewer, url_instance: Url):
    url_instance.url = url_instance.url.lower()
    url = url_exists(supabase, url_instance.url)
    
    if not url.data:
        try:
            url = supabase.from_("views_count").insert({"url": url_instance.url}).execute()
            if not url:
                return {"error": "Url adding failed"}
        except Exception as e:
            return {"error": e,
                    "helper": "url adding no2 error"}
        
    if not unique_view_exists(supabase, url_instance.url, viewer_instance.client_uuid):
        try:
            view = supabase.from_("views_detailed").insert({"url": url_instance.url,
            "country": viewer_instance.country,
            "ip": viewer_instance.ip,
            "client_uuid": viewer_instance.client_uuid}).execute()
        except Exception as e:
            return {"error": e,
                    "helper": "unique view adding error"}
        try:
            incremented = int(url.data[0]['views']) + 1
            _data, _count = supabase.from_("views_count").update({"views": incremented}).eq("url", url_instance.url).execute()
            
        except Exception as e:
            return {"error": e,
                    "helper": "increment error"}
    
    return {"message": "success"}
    

# get view counts for each url
@app.get("/api/views")
async def get_url_count():
    url = supabase.from_("views_count").select("url", "views").execute()

    if len(url.data) > 0:
        return url.data
    else:
        return {"error": "No urls currently in db"}