# EcoCollect – Smart Waste Collection & Recycling Platform
> **FIT-FEST 2026 HACKATHON MVP**  
> *"Smart Waste Collection for a Cleaner Tomorrow"*

---

## 📖 Table of Contents
1. [Project Overview](#-project-overview)
2. [Problem Statement](#-problem-statement)
3. [The Solution](#-the-solution)
4. [Key Features](#-key-features)
5. [Tech Stack](#-tech-stack)
6. [Project Structure](#-project-structure)
7. [Local Setup Instructions](#-local-setup-instructions)
8. [Testing Instructions (All Features)](#-testing-instructions-all-features)
9. [Docker Instructions](#-docker-instructions)
10. [Google Cloud Run Deployment](#-google-cloud-run-deployment)
11. [Troubleshooting & Common Fixes](#-troubleshooting--common-fixes)
12. [How to Upload to GitHub](#-how-to-upload-to-github)
13. [Future Scope](#-future-scope)

---

## 🌿 Project Overview
**EcoCollect** is a modern, lightweight, full-stack web application designed for municipal waste management, recycling hubs, and residents. It simplifies how people sort and request doorstep pickups for recyclable materials and provides collection services with a centralized operational dashboard to manage, track, and analyze collection requests.

---

## 🚨 Problem Statement
- **Sorting Uncertainty:** Most households are unsure where and how to dispose of non-standard waste such as e-waste, hazardous materials, and mixed plastics.
- **Unreliable Logistics:** Bulky recyclables often pile up at home because municipal municipal garbage trucks reject them or regular recycling schedules are inaccessible.
- **Lack of Tracking & Operations:** Collection crews operate on fragmented paperwork or unstructured messages without real-time request tracking, statuses, or recovery metrics.

---

## 💡 The Solution
EcoCollect provides a single, unified digital platform that:
1. **Educates Instantly:** Features an instant **Smart Waste Guide** that identifies items (e.g. *"old mobile phone"*, *"plastic bottle"*, *"aluminium can"*) and recommends the right disposal stream.
2. **Streamlines Pickups:** Enables citizens to schedule doorstep pickups in under 60 seconds and assigns an automated sequential tracking ID (e.g. `EC-1001`).
3. **Provides Real-time Visibility:** Offers visual multi-stage timeline tracking for citizens from *Pending* to *Completed*.
4. **Empowers Dispatchers:** Provides administrators with a high-visibility dashboard with filters, search, one-click status transitions, and diversion statistics.

---

## ✨ Key Features

| Feature | Description |
| :--- | :--- |
| **1. Modern Home Portal** | Highlights the mission, problem & solution, quick category navigation, and live activity metrics. |
| **2. Waste Categorization** | Dedicated support for **7 streams**: Plastic, Paper, Glass, Metal, E-Waste, Organic Waste, and Other. |
| **3. Request Pickup Engine** | Responsive booking form capturing resident details, address, volume estimate, date, and preferred time slot. Generates unique IDs (e.g. `EC-1001`). |
| **4. Live Progress Tracker** | Visual step-by-step progress timeline displaying stages: *Pending* &rarr; *Scheduled* &rarr; *Picked Up* &rarr; *Completed* (with cancellation handling). |
| **5. Operations Dashboard** | Admin portal with 5 live KPI metric cards, material/status filters, keyword search, inline status updates, and deletion. |
| **6. Pickup History Log** | Audit log of fulfilled recycling requests with print-friendly report view. |
| **7. Smart Waste Guide** | Fast keyword-based classifier that maps everyday household items to their proper category, bin color, and disposal tips with one-click booking. |
| **8. Real-time Analytics** | Interactive Chart.js visualizations for waste stream volume distributions, status pipelines, and recycling diversion percentages. |

---

## 🛠 Tech Stack
- **Backend:** Python 3.12+, Flask 3.0+
- **Database:** SQLite3 (`ecocollect.db`) with automatic table creation & demo data seeding
- **Production Server:** Gunicorn WSGI
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla ES6), Bootstrap 5.3, FontAwesome 6
- **Data Visualization:** Chart.js 4.4
- **Containerization & Cloud:** Docker, Google Cloud Run (Linux `0.0.0.0`, dynamic `$PORT`)

---

## 📂 Project Structure
```text
ecocollect/
├── app.py                 # Main Flask application (routes, validation, API endpoints)
├── database.py            # SQLite database schema, CRUD helper methods, demo data seeder
├── smart_guide.py         # Smart Waste Guide categorization dictionary and matching engine
├── requirements.txt       # Python package dependencies
├── Dockerfile             # Container configuration for Google Cloud Run
├── .dockerignore          # Docker build exclusions
├── .gitignore             # Git repository exclusions
├── README.md              # Comprehensive documentation and hackathon submission guide
├── static/
│   ├── css/
│   │   └── style.css      # Custom eco-green theme, timeline styles, responsive cards
│   └── js/
│       ├── main.js        # Form validation, copy-to-clipboard, client-side table search
│       └── charts.js      # Chart.js initialization for category & status breakdown
└── templates/
    ├── base.html          # Main layout template with responsive navbar & alerts
    ├── index.html         # Landing page (hero, problem/solution, categories grid)
    ├── request_pickup.html# Doorstep pickup booking form
    ├── request_success.html# Submission confirmation receipt with unique ID & copy button
    ├── track.html         # Live request tracking with progress timeline
    ├── guide.html         # Smart Waste Guide item classifier & recycling guide
    ├── admin.html         # Admin dashboard with 5 KPI cards & operations table
    ├── history.html       # Completed pickups audit trail
    └── stats.html         # Impact analytics & interactive charts
```

---

## 💻 Local Setup Instructions

### 1. Prerequisites
- Python 3.9 or higher (tested on Python 3.12)
- Git (optional, for cloning)

### 2. Setup Step-by-Step
```bash
# 1. Navigate to the project directory
cd ecocollect

# 2. (Recommended) Create and activate a virtual environment
# Windows (PowerShell):
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS / Linux:
python3 -m venv venv
source venv/bin/activate

# 3. Install required dependencies
pip install -r requirements.txt

# 4. Run the application
python app.py
```

### 3. Open in Browser
Open your browser and navigate to:
```text
http://127.0.0.1:5000
```
> **Note:** The SQLite database (`ecocollect.db`) and realistic demo records (`EC-1001` through `EC-1007`) are automatically created and initialized on the very first run!

---

## 🧪 Testing Instructions (All Features)

Follow this 5-minute walkthrough to verify every feature for judges:

### Test 1: Home Page & Navigation
1. Visit `http://127.0.0.1:5000`.
2. Verify project name **EcoCollect** and tagline *"Smart Waste Collection for a Cleaner Tomorrow"*.
3. Verify the **Problem vs Solution** cards.
4. Click on any waste category card (e.g. **Plastic** or **E-Waste**) — notice it redirects to the pickup form with that category preselected!

### Test 2: Request Pickup & Unique ID Generation
1. Click **"Request Pickup"** in the navigation bar.
2. Select **E-Waste**.
3. Fill in:
   - Full Name: `Test Resident`
   - Mobile: `+1 555-0199`
   - Email: `resident@test.com`
   - Quantity: `3 Old Keyboards & 1 Laptop`
   - Address: `Suite 101, Green Tech Park`
   - Pickup Date: *(Pick any future date)*
   - Time Slot: `09:00 AM - 12:00 PM`
4. Click **"Submit Pickup Request"**.
5. **Expected Result:** You will see the green confirmation page displaying your newly generated unique Request ID (e.g. `EC-1008`).
6. Click the **"Copy Request ID"** button to verify the clipboard feedback.

### Test 3: Live Progress Tracking
1. Click **"Track Progress Now"** (or click **"Track Request"** in the top navbar).
2. Enter `EC-1001` (or your new ID `EC-1008`) and click **Track**.
3. **Expected Result:** A visual progress timeline appears showing the status (*Pending*, *Scheduled*, *Picked Up*, or *Completed*).
4. Try clicking the quick demo pill `EC-1007` to see the **Cancelled** status view.

### Test 4: Smart Waste Guide
1. Navigate to **"Smart Guide"** in the navbar.
2. Type `old mobile phone` and click **Classify**.
   - **Expected Result:** Suggests **E-Waste**, shows the purple badge, designated e-waste drop box, and eco-facts.
3. Test other items using the quick test chips:
   - `plastic bottle` &rarr; **Plastic**
   - `newspaper` &rarr; **Paper**
   - `glass bottle` &rarr; **Glass**
   - `food waste` &rarr; **Organic Waste**
   - `aluminium can` &rarr; **Metal**
4. Click **"Request Pickup for This"** to ensure it carries through to the booking form seamlessly.

### Test 5: Admin Operations Dashboard
1. Click **"Admin Dashboard"** in the top navigation bar.
2. Check the 5 KPI summary cards (**Total**, **Pending**, **Scheduled**, **Completed**, **Cancelled**).
3. In the search box, type a resident's name or address (e.g., `Aarav` or `Springfield`) — notice the table filters instantly.
4. Select the **Status filter** dropdown to filter by `Pending` or `Scheduled`.
5. Change a request's status using the inline dropdown (e.g., change `Pending` &rarr; `Scheduled`). Notice the status updates immediately in the database and reflects in the tracking view!
6. Click the trash icon to test request deletion (with confirmation modal).

### Test 6: Pickup History & Statistics
1. Click **"Pickup History"** in the navbar &rarr; displays all requests with status `Completed`.
2. Click **"Statistics"** in the navbar &rarr; displays Chart.js interactive **Doughnut chart** (Waste Categories) and **Bar chart** (Request Pipeline).

---

## 🐳 Docker Instructions

### 1. Build Docker Image
```bash
docker build -t ecocollect:latest .
```

### 2. Run Container Locally
```bash
docker run -p 8080:8080 -e PORT=8080 ecocollect:latest
```

### 3. Verify
Open `http://localhost:8080` in your web browser.

---

## ☁️ Google Cloud Run Deployment

Google Cloud Run executes containerized applications in a fully managed serverless environment. EcoCollect is fully configured for Cloud Run:
- Binds to `0.0.0.0`
- Reads port dynamically from `$PORT`
- Includes optimized Dockerfile with Gunicorn WSGI

### Step-by-Step Cloud Run Deployment:

#### 1. Install & Initialize Google Cloud SDK
```bash
# Login to your Google Cloud account
gcloud auth login

# Set your active project ID
gcloud config set project YOUR_PROJECT_ID
```

#### 2. Enable Required Google Cloud APIs
```bash
gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com
```

#### 3. Build & Deploy Directly via Cloud Build
Run this single command from inside the `ecocollect` folder:
```bash
gcloud run deploy ecocollect \
    --source . \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --port 8080
```

#### 4. Access Your Live Deployment
Cloud Run will output the live public URL:
```text
Service [ecocollect] revision [ecocollect-00001-abc] has been deployed and is serving 100 percent of traffic.
Service URL: https://ecocollect-xyz-uc.a.run.app
```

---

## 🔧 Troubleshooting & Common Fixes

| Issue | Cause | Solution |
| :--- | :--- | :--- |
| `Port already in use` | Another service is using port 5000 | Run on a different port: `python -c "import os; os.environ['PORT']='5050'; import app; app.app.run(port=5050)"` or set `PORT=5050 python app.py`. |
| `ModuleNotFoundError: No module named 'flask'` | Virtual environment not activated or dependencies not installed | Run `pip install -r requirements.txt`. |
| Changes to database not appearing | SQLite locks or caching | Ensure previous Python processes running the app are terminated before restarting. |
| Container fails to start on Cloud Run | Application didn't bind to `0.0.0.0` or dynamic `$PORT` | `app.py` and `Dockerfile` are already configured with `0.0.0.0` and `${PORT}`. |

---

## 🚀 How to Upload to GitHub

Follow these simple commands to push your project to GitHub:

```bash
# 1. Initialize git in the project directory
git init

# 2. Add all files
git add .

# 3. Commit the changes
git commit -m "Initial release of EcoCollect MVP for FIT-FEST 2026"

# 4. Rename default branch to main
git branch -M main

# 5. Link to your GitHub repository (replace URL with your repository)
git remote add origin https://github.com/YOUR_USERNAME/ecocollect.git

# 6. Push to GitHub
git push -u origin main
```

---

## 🔮 Future Scope
For future production scale and post-hackathon enhancements:

1. **AI Image-Based Waste Classification:**
   - Integrate Google Gemini Flash multimodal vision to allow residents to snap a photo of any waste item and auto-detect category and contamination status.
2. **Google Maps & Dynamic Route Optimization:**
   - Integrate Google Maps Routes API to automatically calculate the shortest multi-stop collection route for drivers, reducing fuel consumption and emissions.
3. **Automated Citizen Notifications:**
   - Integrate Twilio / Firebase Cloud Messaging for instant SMS and WhatsApp notifications when the driver is on the way or pickup is completed.
4. **Recycling Center Locator:**
   - Interactive map showing the nearest municipal drop-off hubs, hazardous collection depots, and bottle return deposit kiosks.
5. **Mobile Application (Flutter / React Native):**
   - Cross-platform mobile app enabling offline queueing, push notifications, and driver barcode scanning.
6. **Eco-Reward Loyalty Points:**
   - Gamification engine awarding green reward points for every kilogram recycled, redeemable for local public transit vouchers or discounts.

---

## 👥 Hackathon Team & Acknowledgments
- **Project:** EcoCollect
- **Event:** FIT-FEST 2026 HACKATHON
- **Theme:** Clean Tech & Smart Urban Waste Management
