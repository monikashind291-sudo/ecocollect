import sqlite3
import os
import re
from datetime import datetime

DATABASE_NAME = os.environ.get("DATABASE_PATH", "ecocollect.db")

def get_db_connection():
    """Create and return a database connection with dict-like row access."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the SQLite database with the requests table and demo data."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            waste_category TEXT NOT NULL,
            quantity TEXT NOT NULL,
            address TEXT NOT NULL,
            pickup_date TEXT NOT NULL,
            time_slot TEXT NOT NULL,
            notes TEXT,
            status TEXT NOT NULL DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    
    # Check if demo data needs to be seeded
    cursor.execute("SELECT COUNT(*) FROM requests")
    count = cursor.fetchone()[0]
    if count == 0:
        seed_demo_data(cursor)
        conn.commit()
        
    conn.close()

def generate_next_request_id():
    """Generate a clean sequential unique Request ID (e.g., EC-1001, EC-1002)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT request_id FROM requests ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    
    highest_num = 1000
    for row in rows:
        match = re.search(r'EC-(\d+)', row['request_id'])
        if match:
            num = int(match.group(1))
            if num > highest_num:
                highest_num = num
                
    next_num = highest_num + 1
    return f"EC-{next_num}"

def seed_demo_data(cursor):
    """Seed initial realistic demo data for presentation and hackathon evaluation."""
    demo_records = [
        (
            "EC-1001", "Aarav Sharma", "+91 98765 43210", "aarav.sharma@example.com",
            "Plastic", "3 Large Sacks (PET Bottles & Containers)",
            "Flat 402, Green Meadows, Sector 14, Gurugram",
            "2026-10-02", "09:00 AM - 12:00 PM",
            "Please call upon arrival at the security gate.",
            "Pending", "2026-09-26 10:15:00"
        ),
        (
            "EC-1002", "Sophia Martinez", "+1 (555) 234-5678", "sophia.m@example.com",
            "E-Waste", "2 Broken Laptops, 4 Keyboards, 10 Chargers",
            "742 Evergreen Terrace, Springfield",
            "2026-10-01", "01:00 PM - 04:00 PM",
            "Batteries are already removed and securely packaged.",
            "Scheduled", "2026-09-25 14:30:00"
        ),
        (
            "EC-1003", "Rahul Patel", "+91 91234 56789", "rahul.patel@example.com",
            "Glass", "25 Glass Beverage Bottles & Broken Jars",
            "Villa 12, Palm Residency, Whitefield, Bengaluru",
            "2026-09-30", "10:00 AM - 01:00 PM",
            "Stored safely in cardboard crate with bubble wrap.",
            "Picked Up", "2026-09-25 09:00:00"
        ),
        (
            "EC-1004", "Emma Watson", "+44 7700 900123", "emma.watson@example.co.uk",
            "Paper", "30 kg Newspapers, Magazines & Shipping Boxes",
            "18 Primrose Gardens, Camden, London",
            "2026-09-24", "02:00 PM - 05:00 PM",
            "Tied securely with natural hemp twine.",
            "Completed", "2026-09-23 11:20:00"
        ),
        (
            "EC-1005", "Michael Chen", "+1 (555) 890-1234", "mchen@example.com",
            "Metal", "15 Aluminium Beverage Cans & 2 Steel Pots",
            "305 Beacon Street, Boston, MA",
            "2026-09-22", "09:00 AM - 12:00 PM",
            "Clean and crushed metal items.",
            "Completed", "2026-09-21 16:45:00"
        ),
        (
            "EC-1006", "Priyanka Verma", "+91 99887 76655", "priyanka.v@example.com",
            "Organic Waste", "12 kg Kitchen Compost & Dry Leaves",
            "House 88, Rosewood Enclave, HSR Layout, Bengaluru",
            "2026-09-20", "08:00 AM - 11:00 AM",
            "Biodegradable compostable bags used.",
            "Completed", "2026-09-19 18:10:00"
        ),
        (
            "EC-1007", "David Miller", "+1 (555) 432-8765", "david.miller@example.com",
            "Other", "Hazardous Paint Buckets & Varnish Cans",
            "1204 Pine Ridge Road, Austin, TX",
            "2026-09-18", "01:00 PM - 04:00 PM",
            "Resident cancelled - transferred to hazardous city drop-off.",
            "Cancelled", "2026-09-17 13:00:00"
        )
    ]
    
    cursor.executemany("""
        INSERT INTO requests (
            request_id, name, phone, email, waste_category, quantity,
            address, pickup_date, time_slot, notes, status, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, demo_records)

def create_request(data):
    """Insert a new pickup request into the database and return the assigned request_id."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    req_id = generate_next_request_id()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute("""
        INSERT INTO requests (
            request_id, name, phone, email, waste_category, quantity,
            address, pickup_date, time_slot, notes, status, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Pending', ?)
    """, (
        req_id,
        data['name'].strip(),
        data['phone'].strip(),
        data['email'].strip(),
        data['waste_category'],
        data['quantity'].strip(),
        data['address'].strip(),
        data['pickup_date'],
        data['time_slot'],
        data.get('notes', '').strip(),
        now_str
    ))
    
    conn.commit()
    conn.close()
    return req_id

def get_request_by_id(request_id):
    """Retrieve a single request by its case-insensitive request ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM requests WHERE UPPER(request_id) = UPPER(?)", (request_id.strip(),))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_all_requests(category=None, status=None, search=None):
    """Fetch all requests with optional filtering and search."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM requests WHERE 1=1"
    params = []
    
    if category and category != 'All':
        query += " AND waste_category = ?"
        params.append(category)
        
    if status and status != 'All':
        query += " AND status = ?"
        params.append(status)
        
    if search:
        search_term = f"%{search.strip()}%"
        query += " AND (request_id LIKE ? OR name LIKE ? OR phone LIKE ? OR address LIKE ? OR notes LIKE ?)"
        params.extend([search_term, search_term, search_term, search_term, search_term])
        
    query += " ORDER BY id DESC"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_completed_requests():
    """Fetch all completed pickup requests for history log."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM requests WHERE status = 'Completed' ORDER BY pickup_date DESC, id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def update_request_status(request_id, new_status):
    """Update status of a given request."""
    valid_statuses = ['Pending', 'Scheduled', 'Picked Up', 'Completed', 'Cancelled']
    if new_status not in valid_statuses:
        return False
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE requests SET status = ? WHERE UPPER(request_id) = UPPER(?)", (new_status, request_id.strip()))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0

def delete_request(request_id):
    """Delete a request by its request ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM requests WHERE UPPER(request_id) = UPPER(?)", (request_id.strip(),))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0

def get_dashboard_stats():
    """Compute aggregate counts and breakdown metrics for admin and statistics views."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Total counts
    cursor.execute("SELECT COUNT(*) FROM requests")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM requests WHERE status = 'Pending'")
    pending = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM requests WHERE status = 'Scheduled'")
    scheduled = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM requests WHERE status = 'Picked Up'")
    picked_up = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM requests WHERE status = 'Completed'")
    completed = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM requests WHERE status = 'Cancelled'")
    cancelled = cursor.fetchone()[0]
    
    # Category breakdown
    cursor.execute("""
        SELECT waste_category, COUNT(*) as count 
        FROM requests 
        GROUP BY waste_category 
        ORDER BY count DESC
    """)
    category_counts = {row['waste_category']: row['count'] for row in cursor.fetchall()}
    
    # Status breakdown
    status_counts = {
        'Pending': pending,
        'Scheduled': scheduled,
        'Picked Up': picked_up,
        'Completed': completed,
        'Cancelled': cancelled
    }
    
    conn.close()
    
    return {
        'total': total,
        'pending': pending,
        'scheduled': scheduled,
        'picked_up': picked_up,
        'completed': completed,
        'cancelled': cancelled,
        'category_counts': category_counts,
        'status_counts': status_counts
    }
