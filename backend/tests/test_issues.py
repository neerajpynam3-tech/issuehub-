from tests.conftest import signup_and_login


def setup_project(client, headers, key="WEB"):
    return client.post(
        "/api/projects",
        json={"name": "Web App", "key": key, "description": "Demo"},
        headers=headers,
    ).json()["id"]


def create_issue(client, headers, project_id, title="Bug", priority="high"):
    return client.post(
        f"/api/projects/{project_id}/issues",
        json={"title": title, "description": "Something broke", "priority": priority},
        headers=headers,
    )


def test_create_and_get_issue(client):
    headers = signup_and_login(client, "Alice", "alice@example.com")
    project_id = setup_project(client, headers)

    created = create_issue(client, headers, project_id)
    assert created.status_code == 201
    issue_id = created.json()["id"]

    fetched = client.get(f"/api/issues/{issue_id}", headers=headers)
    assert fetched.status_code == 200
    assert fetched.json()["title"] == "Bug"
    assert fetched.json()["reporter"]["email"] == "alice@example.com"


def test_non_member_cannot_create_issue(client):
    alice = signup_and_login(client, "Alice", "alice@example.com")
    bob = signup_and_login(client, "Bob", "bob@example.com")
    project_id = setup_project(client, alice)

    response = create_issue(client, bob, project_id)
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "not_a_member"


def test_filter_and_search_issues(client):
    headers = signup_and_login(client, "Alice", "alice@example.com")
    project_id = setup_project(client, headers)
    create_issue(client, headers, project_id, title="Login bug", priority="high")
    create_issue(client, headers, project_id, title="Slow page", priority="low")

    # Text search in title.
    response = client.get(
        f"/api/projects/{project_id}/issues?q=login", headers=headers
    )
    body = response.json()
    assert body["total"] == 1
    assert body["items"][0]["title"] == "Login bug"

    # Filter by priority.
    response = client.get(
        f"/api/projects/{project_id}/issues?priority=low", headers=headers
    )
    assert response.json()["total"] == 1


def test_only_maintainer_can_change_status(client):
    alice = signup_and_login(client, "Alice", "alice@example.com")
    bob = signup_and_login(client, "Bob", "bob@example.com")
    project_id = setup_project(client, alice)
    client.post(
        f"/api/projects/{project_id}/members",
        json={"email": "bob@example.com", "role": "member"},
        headers=alice,
    )
    issue_id = create_issue(client, bob, project_id).json()["id"]

    # Bob (reporter, member) cannot close the issue.
    denied = client.patch(
        f"/api/issues/{issue_id}", json={"status": "closed"}, headers=bob
    )
    assert denied.status_code == 403
    assert denied.json()["error"]["code"] == "not_maintainer"

    # Alice (maintainer) can.
    allowed = client.patch(
        f"/api/issues/{issue_id}", json={"status": "closed"}, headers=alice
    )
    assert allowed.status_code == 200
    assert allowed.json()["status"] == "closed"


def test_reporter_can_edit_own_issue_description(client):
    headers = signup_and_login(client, "Alice", "alice@example.com")
    project_id = setup_project(client, headers)
    issue_id = create_issue(client, headers, project_id).json()["id"]

    response = client.patch(
        f"/api/issues/{issue_id}", json={"title": "Updated title"}, headers=headers
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated title"


def test_maintainer_can_delete_issue(client):
    headers = signup_and_login(client, "Alice", "alice@example.com")
    project_id = setup_project(client, headers)
    issue_id = create_issue(client, headers, project_id).json()["id"]

    response = client.delete(f"/api/issues/{issue_id}", headers=headers)
    assert response.status_code == 204
    assert client.get(f"/api/issues/{issue_id}", headers=headers).status_code == 404


def test_enhance_endpoint_returns_structured_text(client):
    headers = signup_and_login(client, "Alice", "alice@example.com")
    response = client.post(
        "/api/issues/enhance",
        json={"title": "Login failing", "description": "Users cannot login"},
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["provider"] == "mock"
    assert "Steps to Reproduce" in response.json()["enhanced_description"]
