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


def test_activities_include_participant_lists():
    response = client.get("/activities")
    assert response.status_code == 200

    activity_data = response.json()["Chess Club"]
    assert isinstance(activity_data["participants"], list)
    assert len(activity_data["participants"]) > 0


def test_unregister_participant_removes_them_from_activity():
    activity_name = "Chess Club"
    email = "temp@example.com"
    activity = activities[activity_name]
    original_participants = list(activity["participants"])

    activity["participants"].append(email)

    response = client.delete(f"/activities/{activity_name}/participants?email={email}")
    assert response.status_code == 200
    assert email not in activity["participants"]

    activity["participants"] = original_participants
