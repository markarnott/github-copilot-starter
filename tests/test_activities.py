import pytest
from urllib.parse import quote


@pytest.mark.asyncio
async def test_get_activities(async_client):
    resp = await async_client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Basic sanity check for a known activity
    assert "Chess Club" in data


@pytest.mark.asyncio
async def test_signup_duplicate_and_unregister_flow(async_client):
    activity = "Chess Club"
    email = "testuser@example.com"
    enc_activity = quote(activity, safe="")

    # Ensure clean state: try removing if already present
    await async_client.delete(f"/activities/{enc_activity}/participants", params={"email": email})

    # Sign up
    resp = await async_client.post(f"/activities/{enc_activity}/signup", params={"email": email})
    assert resp.status_code == 200

    # Verify participant appears
    resp = await async_client.get("/activities")
    participants = resp.json()[activity]["participants"]
    assert email in participants

    # Duplicate signup should return 400
    resp = await async_client.post(f"/activities/{enc_activity}/signup", params={"email": email})
    assert resp.status_code == 400

    # Unregister the participant
    resp = await async_client.delete(f"/activities/{enc_activity}/participants", params={"email": email})
    assert resp.status_code == 200
    body = resp.json()
    assert email not in body.get("participants", [])

    # Unregistering a missing participant returns 404
    resp = await async_client.delete(f"/activities/{enc_activity}/participants", params={"email": "noone@example.com"})
    assert resp.status_code == 404
