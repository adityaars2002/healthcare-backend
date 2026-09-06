from django.urls import reverse
from rest_framework.test import APITestCase


class HealthcareFlowTests(APITestCase):
    """One end-to-end pass: register -> login -> patient -> doctor -> mapping -> isolation."""

    def setUp(self):
        self.client.post(
            reverse("register"),
            {"name": "Asha", "email": "asha@example.com", "password": "Str0ngPass!23"},
        )
        token = self.client.post(
            reverse("login"), {"email": "asha@example.com", "password": "Str0ngPass!23"}
        ).data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_flow(self):
        self.assertEqual(self.client.get("/api/patients/").status_code, 200)

        patient = self.client.post(
            "/api/patients/",
            {"name": "Ravi", "age": 34, "gender": "M", "phone": "+919812345678"},
        )
        self.assertEqual(patient.status_code, 201)

        doctor = self.client.post(
            "/api/doctors/",
            {
                "name": "Bose",
                "specialization": "Cardiology",
                "email": "bose@example.com",
                "phone": "9800000000",
                "experience_years": 12,
            },
        )
        self.assertEqual(doctor.status_code, 201)

        mapping = self.client.post(
            "/api/mappings/", {"patient": patient.data["id"], "doctor": doctor.data["id"]}
        )
        self.assertEqual(mapping.status_code, 201)
        # Duplicate assignment is rejected.
        self.assertEqual(
            self.client.post(
                "/api/mappings/", {"patient": patient.data["id"], "doctor": doctor.data["id"]}
            ).status_code,
            400,
        )
        # /mappings/<patient_id>/ lists that patient's doctors.
        by_patient = self.client.get(f"/api/mappings/{patient.data['id']}/")
        self.assertEqual(by_patient.data["count"], 1)
        self.assertEqual(by_patient.data["results"][0]["doctor_name"], "Bose")

        self.assertEqual(
            self.client.delete(f"/api/mappings/{mapping.data['id']}/").status_code, 204
        )

    def test_other_users_patients_are_invisible(self):
        mine = self.client.post(
            "/api/patients/",
            {"name": "Ravi", "age": 34, "gender": "M", "phone": "9812345678"},
        ).data["id"]

        self.client.credentials()
        self.client.post(
            reverse("register"),
            {"name": "Bikram", "email": "bikram@example.com", "password": "Str0ngPass!23"},
        )
        token = self.client.post(
            reverse("login"), {"email": "bikram@example.com", "password": "Str0ngPass!23"}
        ).data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        self.assertEqual(self.client.get(f"/api/patients/{mine}/").status_code, 404)
        self.assertEqual(self.client.get("/api/patients/").data["count"], 0)
        # Cannot assign a doctor to someone else's patient.
        self.assertEqual(self.client.post("/api/mappings/", {"patient": mine, "doctor": 1}).status_code, 400)

    def test_auth_required(self):
        self.client.credentials()
        self.assertEqual(self.client.get("/api/patients/").status_code, 401)
        self.assertEqual(self.client.get("/api/doctors/").status_code, 401)
