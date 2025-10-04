Free hosting guide (Supabase + Fly + Vercel)
=========================================

This guide walks through deploying the project on free tiers:
- Supabase (managed Postgres)
- Fly.io (Django backend as Docker)
- Vercel (Nuxt frontend static site)

1) Prepare repo
-----------------
- Remove local virtualenv from git tracking and commit a `.gitignore` (already included):

  git rm -r --cached backend/venv || true
  git add .gitignore
  git commit -m "chore: ignore venv and other local files"
  git push

2) Create a Supabase project
-----------------------------
- Sign up at https://supabase.com and create a free project.
- Get connection details (host, db, user, password) from Project → Settings → Database → Connection string.

3) Deploy backend to Fly.io
---------------------------
- Install `flyctl` (https://fly.io/docs/hands-on/install-flyctl/).
- From the `backend/` folder run:

  flyctl auth login
  flyctl launch --name protrack-backend --no-deploy

- Set secrets (replace placeholders):

  flyctl secrets set DB_HOST=<supabase_host> DB_PORT=5432 DB_NAME=<db> DB_USER=<user> DB_PASSWORD=<pw> SECRET_KEY=<your-secret> DEBUG=0 ALLOWED_HOSTS=<your-fly-host>.fly.dev CORS_ALLOWED_ORIGINS=https://<your-frontend-domain>

- Deploy and run migrations:

  flyctl deploy
  flyctl ssh run -a protrack-backend "python manage.py migrate"
  flyctl ssh run -a protrack-backend "python manage.py collectstatic --noinput"

4) Deploy frontend to Vercel
----------------------------
- Push repo to GitHub (already done).
- On https://vercel.com, Import Project → choose this repo.
- Build command: `npm run build`
- Output directory: `.output/public` (adjust if your Nuxt build differs)
- Add environment variable pointing to backend API:
  - key: `NUXT_PUBLIC_APIBASE`
  - value: `https://protrack-backend.fly.dev/api`

5) Final checks
---------------
- Ensure Django `CORS_ALLOWED_ORIGINS` contains your Vercel domain.
- Ensure `ALLOWED_HOSTS` contains your Fly app domain and (optionally) the Vercel domain.
- Test the frontend in browser; check browser devtools for network/CORS errors.

If you want I can run the cleanup commit that removes `backend/venv` from tracking and push it for you.
