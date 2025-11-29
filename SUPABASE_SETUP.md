# Supabase Setup & RLS Configuration Guide

## Problem
The error `new row violates row-level security policy for table "candidates"` occurs when RLS is enabled but no policies allow inserts.

## Solutions

### Option 1: Use Service Role Key (RECOMMENDED)
This is the most secure approach for your Streamlit app.

1. **Get your Service Role Key**:
   - Go to Supabase Dashboard → Project Settings → API
   - Copy the `service_role` key (NOT the `anon` key)
   - ⚠️ **Keep this secret!** Never commit it to version control.

2. **Update `.streamlit/secrets.toml`**:
   ```toml
   GEMINI_API_KEY = "your_google_api_key"
   SUPABASE_URL = "https://your-project.supabase.co"
   SUPABASE_KEY = "your_anon_key"
   SUPABASE_SERVICE_ROLE_KEY = "your_service_role_key"
   ```

3. **The code is already updated** to use `supabase_admin` with the service role key for database inserts.

---

### Option 2: Disable RLS (FOR DEVELOPMENT ONLY)
If you want to test without setting up the service role key:

1. Go to Supabase Dashboard
2. Select `candidates` table
3. Click the **RLS toggle** to **disable** it
4. ⚠️ **Not recommended for production!**

---

### Option 3: Create RLS Policies (FOR PRODUCTION)
To keep RLS enabled with proper policies:

1. Go to Supabase Dashboard → SQL Editor
2. Run this SQL:
   ```sql
   -- Enable RLS
   ALTER TABLE candidates ENABLE ROW LEVEL SECURITY;

   -- Allow anyone to insert
   CREATE POLICY "Allow anyone to insert" 
   ON candidates FOR INSERT 
   WITH CHECK (true);

   -- Allow anyone to read
   CREATE POLICY "Allow anyone to read" 
   ON candidates FOR SELECT 
   USING (true);
   ```

---

## Recommended Setup
- **Development**: Option 2 (Disable RLS) for quick testing
- **Production**: Option 1 (Service Role Key) or Option 3 (RLS Policies)

The app code now supports Option 1 out of the box!
