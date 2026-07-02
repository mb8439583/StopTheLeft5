# Get Labour Out — Tactical Voting Site

A right-of-centre tactical voting site for UK general elections.
Only recommends voting Conservative or Reform UK — never Lib Dem or Green.

---

## Project structure

```
get-labour-out/
├── index.html          ← The entire site (one file)
├── data/
│   └── results.js      ← 2024 GE results (auto-generated, see below)
├── build_data.py       ← Script to (re)build results.js from HoC CSV
└── README.md
```

---

## Step 1 — Get the real 2024 data

1. Go to: https://commonslibrary.parliament.uk/research-briefings/cbp-10009/
2. Download **"Results by constituency"** CSV (look for the spreadsheet download link)
3. Place the CSV in this folder
4. Edit `build_data.py` — the top of the file has instructions for CSV import mode
5. Run: `python3 build_data.py --input <filename>.csv`
6. This regenerates `data/results.js`

The CSV has columns including ONS constituency code, constituency name, and vote
counts/shares for each party. The builder normalises party names to:
LAB, CON, REF, LD, SNP, PC, GRN, OTHER.

---

## Step 2 — Test locally

Just open `index.html` in a browser. Or run a local server (needed if your browser
blocks local file fetch):

```bash
python3 -m http.server 8080
# then open http://localhost:8080
```

---

## Step 3 — Put it on GitHub

1. Create a free account at github.com if you don't have one
2. Click "New repository" → name it `get-labour-out` → Public → Create
3. In your terminal (from the `get-labour-out/` folder):

```bash
git init
git add .
git commit -m "Initial build"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/get-labour-out.git
git push -u origin main
```

---

## Step 4 — Deploy (free hosting)

### Option A: GitHub Pages (simplest)
1. In your GitHub repo → Settings → Pages
2. Source: "Deploy from a branch" → branch: `main` → folder: `/ (root)`
3. Save. In ~60 seconds your site is live at:
   `https://YOUR_USERNAME.github.io/get-labour-out/`

### Option B: Netlify (nicer URLs, faster)
1. Go to netlify.com → "Add new site" → "Import an existing project"
2. Connect your GitHub repo
3. Build command: (leave blank) / Publish directory: `.`
4. Deploy. You get a URL like `https://random-name.netlify.app`
5. In Site settings → Domain management → add custom domain

### Option C: Cloudflare Pages (fastest, free)
Same as Netlify — connect repo, no build command, publish dir `.`

---

## Step 5 — Custom domain (optional, ~£8/yr)

1. Buy `getlabourout.co.uk` at Namecheap or Cloudflare Registrar
2. In your hosting dashboard → add custom domain
3. Update your domain's DNS records as instructed (usually just add a CNAME)
4. Takes up to 24h to propagate

---

## Step 6 — The recommendation algorithm (TODO)

The current algorithm in `index.html` (inside `getRecommendation()`) is a stub:
- Reform won → vote Reform
- Con won → vote Con
- Labour won → whoever of Con/Reform got more votes in 2024

**The real algorithm (to be built):**
We need to decide what to recommend in Labour-won seats where Con came 2nd but
Reform is surging. Key inputs:
- 2024 Con share vs Reform share
- A Reform surge multiplier (e.g. ×1.7 based on national polls: 14% → 24%)
- A "decisiveness threshold" — only recommend if one party is clearly ahead
- A "hopeless seat" cutoff — if even the leading right party is >25pts behind Labour

See the `getRecommendation()` function in index.html to add this logic.

---

## Updating recommendations

Since everything is baked into `results.js`, to update:
1. Edit `build_data.py` or `index.html`
2. Commit and push to GitHub
3. Site updates automatically within seconds

No server, no database, no ongoing costs beyond the domain name.
