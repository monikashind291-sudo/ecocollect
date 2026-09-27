import unittest
import os
from app import app
import database
import smart_guide

class EcoCollectTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        cls.client = app.test_client()

    def test_01_database_initialization(self):
        """Test database connection and demo data presence."""
        stats = database.get_dashboard_stats()
        self.assertGreater(stats['total'], 0)
        self.assertGreater(stats['completed'], 0)
        print("PASS: Database initialized with demo data.")

    def test_02_home_page(self):
        """Test Home Page rendering and key contents."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"EcoCollect", response.data)
        self.assertIn(b"Smart Waste Collection for a Cleaner Tomorrow", response.data)
        self.assertIn(b"Request Pickup", response.data)
        self.assertIn(b"Track Request", response.data)
        self.assertIn(b"Admin Portal", response.data)
        print("PASS: Home page renders successfully.")

    def test_03_request_pickup_submission(self):
        """Test submitting a new pickup request and getting unique Request ID."""
        form_data = {
            "name": "Jane Test Doe",
            "phone": "+91 98989 89898",
            "email": "jane@example.com",
            "waste_category": "Plastic",
            "quantity": "5 Bags of Plastic Bottles",
            "address": "123 Green Avenue, Eco City",
            "pickup_date": "2026-10-05",
            "time_slot": "09:00 AM - 12:00 PM",
            "notes": "Gate code is 4321."
        }
        response = self.client.post("/request-pickup", data=form_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Pickup Request Confirmed!", response.data)
        self.assertIn(b"EC-", response.data)
        self.assertIn(b"Jane Test Doe", response.data)
        print("PASS: Request pickup submission and EC-ID generation verified.")

    def test_04_track_request(self):
        """Test tracking an existing request (EC-1001)."""
        response = self.client.get("/track?request_id=EC-1001")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"EC-1001", response.data)
        self.assertIn(b"Pending", response.data)
        self.assertIn(b"Aarav Sharma", response.data)
        print("PASS: Request tracking verified.")

    def test_05_admin_dashboard(self):
        """Test admin dashboard, filters, and KPI counts."""
        response = self.client.get("/admin")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Collection Management Dashboard", response.data)
        self.assertIn(b"Total Requests", response.data)
        self.assertIn(b"Pending", response.data)
        self.assertIn(b"Scheduled", response.data)
        self.assertIn(b"Completed", response.data)
        self.assertIn(b"Cancelled", response.data)
        print("PASS: Admin dashboard and metrics verified.")

    def test_06_admin_status_update(self):
        """Test updating status of a request via Admin action."""
        # Update EC-1001 to Scheduled
        response = self.client.post("/admin/update-status", data={
            "request_id": "EC-1001",
            "status": "Scheduled"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        req = database.get_request_by_id("EC-1001")
        self.assertEqual(req['status'], "Scheduled")
        print("PASS: Admin status update verified.")

    def test_07_smart_guide_classifications(self):
        """Test the Smart Waste Guide required examples."""
        test_cases = [
            ("old mobile phone", "E-Waste"),
            ("plastic bottle", "Plastic"),
            ("newspaper", "Paper"),
            ("glass bottle", "Glass"),
            ("food waste", "Organic Waste"),
            ("aluminium can", "Metal")
        ]
        for query, expected_cat in test_cases:
            res = smart_guide.classify_waste_item(query)
            self.assertIsNotNone(res)
            self.assertEqual(res['category'], expected_cat, f"Failed for {query}")
        
        # Test guide page rendering
        response = self.client.get("/guide?item=old+mobile+phone")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"E-Waste", response.data)
        print("PASS: Smart Waste Guide classifications verified for all required test items.")

    def test_08_pickup_history(self):
        """Test Pickup History page displaying completed requests."""
        response = self.client.get("/history")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Pickup History Log", response.data)
        self.assertIn(b"Completed", response.data)
        print("PASS: Pickup history page verified.")

    def test_09_statistics_page(self):
        """Test Statistics & Analytics page."""
        response = self.client.get("/stats")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Collection & Recycling Analytics", response.data)
        self.assertIn(b"categoryChart", response.data)
        self.assertIn(b"statusChart", response.data)
        print("PASS: Statistics page and chart canvas verified.")

    def test_10_api_endpoints(self):
        """Test JSON API endpoints."""
        res = self.client.get("/api/classify?item=plastic+bottle")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['category'], "Plastic")

        res_stats = self.client.get("/api/stats")
        self.assertEqual(res_stats.status_code, 200)
        self.assertIn("total", res_stats.get_json())
        print("PASS: JSON API endpoints verified.")

if __name__ == "__main__":
    unittest.main()
