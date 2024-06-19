"# micro-views" 

env variables:
    - `SUPABASE_API_URL`
    - `SUPABASE_API_KEY`
    - `SUPABASE_DB_PASSWORD`

DB tables:
    - views_count
    - views_detailed

views_count table columns:
    - url (varchar, PRIMARY KEY)
    - views (int8)
    - created_at (timestamptz)

views_detailed table columns:
    - id (PRIMARY KEY)
    - created_at (timestamptz)
    - url (varchar, FOREIGN KEY)
    - country (varchar)
    - ip (varchar)
    - client_uuid (varchar uuid)