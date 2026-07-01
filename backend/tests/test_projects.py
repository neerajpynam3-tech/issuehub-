from tests.conftest import signup_and_login


def create_project(client, headers, name="Web App", key="WEB"):
    return client.post(
        "/api/projects",
        json={"name": name, "key": key, "description": "Demo"},
        headers=headers,
    )


def test_create_project_makes_creator_maintainer(client):
    headers = signup_and_login(client, "Alice", "alice@example.com")
    response = create_project(client, headers)
    assert response.status_code == 201
    assert response.json()["my_role"] == "maintainer"


def test_duplicate_key_is_rejected(client):
    headers = signup_and_login(client, "Alice", "alice@example.com")
    create_project(client, headers, key="WEB")
    response = create_project(client, headers, name="Another", key="WEB")
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "key_taken"


def test_projects_list_is_scoped_to_membership(client):
    alice = signup_and_login(client, "Alice", "alice@example.com")
    bob = signup_and_login(client, "Bob", "bob@example.com")
    create_project(client, alice, key="WEB")

    # Bob is not a member, so he sees no projects.
    assert client.get("/api/projects", headers=bob).json() == []
    # Alice sees her own project.
    assert len(client.get("/api/projects", headers=alice).json()) == 1


def test_maintainer_can_add_member_by_email(client):
    alice = signup_and_login(client, "Alice", "alice@example.com")
    signup_and_login(client, "Bob", "bob@example.com")
    project_id = create_project(client, alice, key="WEB").json()["id"]

    response = client.post(
        f"/api/projects/{project_id}/members",
        json={"email": "bob@example.com", "role": "member"},
        headers=alice,
    )
    assert response.status_code == 201
    assert response.json()["role"] == "member"


def test_non_maintainer_cannot_add_member(client):
    alice = signup_and_login(client, "Alice", "alice@example.com")
    bob = signup_and_login(client, "Bob", "bob@example.com")
    signup_and_login(client, "Cara", "cara@example.com")
    project_id = create_project(client, alice, key="WEB").json()["id"]
    client.post(
        f"/api/projects/{project_id}/members",
        json={"email": "bob@example.com", "role": "member"},
        headers=alice,
    )

    # Bob is only a member, so he cannot add Cara.
    response = client.post(
        f"/api/projects/{project_id}/members",
        json={"email": "cara@example.com", "role": "member"},
        headers=bob,
    )
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "not_maintainer"
