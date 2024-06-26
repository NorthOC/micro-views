from supabase import Client, create_client

#init supabase client
def init_supabase_client(url, key):
    supabase: Client = create_client(url, key)
    return supabase

# check if url is already in count
def url_exists(supabase: Client, value: str, key:str = "url"):
    try:
        url = supabase.from_("views_count").select("*").eq(key, value.lower()).limit(1).execute()
        return url
    except Exception as e:
            return {"error": e,
                    "helper": "url adding no1 error"}

# check if user already viewed the page
def unique_view_exists(supabase:Client, url_value:str, uuid_value: str, url_key:str = "url", uuid_key:str = "client_uuid"):
    unique_view = supabase.from_("views_detailed").select("*").eq(url_key, url_value.lower()).eq(url_key, url_value.lower()).eq(uuid_key, uuid_value).execute()
    return len(unique_view.data) > 0
    