import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import database
import smart_guide

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "ecocollect-hackathon-2026-secret-key")

# Initialize database and tables upon startup
with app.app_context():
    database.init_db()

CATEGORIES = [
    "Plastic",
    "Paper",
    "Glass",
    "Metal",
    "E-Waste",
    "Organic Waste",
    "Other"
]

TIME_SLOTS = [
    "09:00 AM - 12:00 PM",
    "12:00 PM - 03:00 PM",
    "03:00 PM - 06:00 PM"
]

@app.route("/")
def index():
    """Home Page: Overview, problem/solution, categories, and direct action triggers."""
    stats = database.get_dashboard_stats()
    return render_template("index.html", stats=stats, categories=CATEGORIES)

@app.route("/request-pickup", methods=["GET", "POST"])
def request_pickup():
    """Request Pickup: Form for residents/businesses to submit a waste pickup request."""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()
        waste_category = request.form.get("waste_category", "").strip()
        quantity = request.form.get("quantity", "").strip()
        address = request.form.get("address", "").strip()
        pickup_date = request.form.get("pickup_date", "").strip()
        time_slot = request.form.get("time_slot", "").strip()
        notes = request.form.get("notes", "").strip()

        # Validation
        if not (name and phone and email and waste_category and quantity and address and pickup_date and time_slot):
            flash("Please fill in all required fields marked with *.", "danger")
            return render_template("request_pickup.html", categories=CATEGORIES, time_slots=TIME_SLOTS, form_data=request.form)

        if waste_category not in CATEGORIES:
            flash("Invalid waste category selected.", "danger")
            return render_template("request_pickup.html", categories=CATEGORIES, time_slots=TIME_SLOTS, form_data=request.form)

        # Store in database and generate unique Request ID
        req_id = database.create_request({
            "name": name,
            "phone": phone,
            "email": email,
            "waste_category": waste_category,
            "quantity": quantity,
            "address": address,
            "pickup_date": pickup_date,
            "time_slot": time_slot,
            "notes": notes
        })

        flash(f"Pickup request submitted successfully! Your Request ID is {req_id}", "success")
        return redirect(url_for("request_success", request_id=req_id))

    # GET request with optional pre-selected category
    preselected_category = request.args.get("category", "")
    return render_template("request_pickup.html", categories=CATEGORIES, time_slots=TIME_SLOTS, preselected_category=preselected_category, form_data={})

@app.route("/request-success/<request_id>")
def request_success(request_id):
    """Success receipt page displaying Request ID and quick actions."""
    req = database.get_request_by_id(request_id)
    if not req:
        flash(f"Request ID '{request_id}' not found.", "warning")
        return redirect(url_for("index"))
    return render_template("request_success.html", request=req)

@app.route("/track", methods=["GET", "POST"])
def track():
    """Track Request: Lookup pickup request status and view visual progress timeline."""
    req_id = request.values.get("request_id", "").strip().upper()
    req = None
    searched = False

    if req_id:
        searched = True
        req = database.get_request_by_id(req_id)
        if not req:
            flash(f"No collection request found with ID '{req_id}'. Please verify and try again.", "warning")

    return render_template("track.html", request=req, search_query=req_id, searched=searched)

@app.route("/admin")
def admin():
    """Admin Dashboard: KPI cards, search, category & status filters, status updates, deletion."""
    category_filter = request.args.get("category", "All")
    status_filter = request.args.get("status", "All")
    search_query = request.args.get("search", "").strip()

    requests_list = database.get_all_requests(
        category=category_filter if category_filter != "All" else None,
        status=status_filter if status_filter != "All" else None,
        search=search_query if search_query else None
    )

    stats = database.get_dashboard_stats()

    return render_template(
        "admin.html",
        requests=requests_list,
        stats=stats,
        categories=CATEGORIES,
        selected_category=category_filter,
        selected_status=status_filter,
        search_query=search_query
    )

@app.route("/admin/update-status", methods=["POST"])
def update_status():
    """Admin action: Update status of a request."""
    request_id = request.form.get("request_id", "").strip()
    new_status = request.form.get("status", "").strip()

    success = database.update_request_status(request_id, new_status)
    if success:
        flash(f"Status for {request_id} updated to '{new_status}'.", "success")
    else:
        flash(f"Failed to update status for {request_id}.", "danger")

    return redirect(request.referrer or url_for("admin"))

@app.route("/admin/delete", methods=["POST"])
def delete_request_route():
    """Admin action: Remove a request."""
    request_id = request.form.get("request_id", "").strip()
    success = database.delete_request(request_id)
    if success:
        flash(f"Request {request_id} has been deleted.", "info")
    else:
        flash(f"Failed to delete request {request_id}.", "danger")

    return redirect(request.referrer or url_for("admin"))

@app.route("/history")
def history():
    """Pickup History: List of all successfully completed collections."""
    completed_requests = database.get_completed_requests()
    return render_template("history.html", requests=completed_requests)

@app.route("/guide", methods=["GET", "POST"])
def guide():
    """Smart Waste Guide: Instant waste item categorization and recycling instructions."""
    query = request.values.get("item", "").strip()
    result = None
    if query:
        result = smart_guide.classify_waste_item(query)

    return render_template(
        "guide.html",
        result=result,
        query=query,
        suggestions=smart_guide.POPULAR_SUGGESTIONS,
        metadata=smart_guide.CATEGORY_METADATA
    )

@app.route("/stats")
def stats():
    """Statistics: Visual analytics and waste recycling breakdown."""
    dashboard_stats = database.get_dashboard_stats()
    return render_template("stats.html", stats=dashboard_stats)

# --- JSON API Endpoints for interactive JS and mobile/external integration ---

@app.route("/api/classify")
def api_classify():
    """API endpoint for live Smart Waste Guide classification."""
    item = request.args.get("item", "").strip()
    if not item:
        return jsonify({"error": "Item query parameter is required"}), 400
    res = smart_guide.classify_waste_item(item)
    return jsonify(res)

@app.route("/api/stats")
def api_stats():
    """API endpoint for chart visualization data."""
    dashboard_stats = database.get_dashboard_stats()
    return jsonify(dashboard_stats)

@app.route("/api/requests/<request_id>")
def api_get_request(request_id):
    """API endpoint to get request details by ID."""
    req = database.get_request_by_id(request_id)
    if not req:
        return jsonify({"error": "Not found"}), 404
    return jsonify(req)


if __name__ == "__main__":
    # Google Cloud Run provides the PORT environment variable (defaults to 5000 locally or 8080 on Cloud Run)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
