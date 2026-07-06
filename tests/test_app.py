from fastapi.testclient import TestClient

from src.app import activities, app


client = TestClient(app)


def test_duplicate_signup_is_rejected():
    activity_name = "Chess Club"
    email = "duplicate@example.com"
    activity = activities[activity_name]
    initial_count = len(activity["participants"])

    first_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert first_response.status_code == 200

    second_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student is already signed up"

    assert len(activity["participants"]) == initial_count + 1
    assert activity["participants"].count(email) == 1
