from app.models import User

PASSWORD = "Str0ngPass1"


def register(client, org="DIU", email="admin@diu.edu", password=PASSWORD):
    return client.post("/api/auth/register-organization", json={
        "org_name": org, "admin_name": "Asif Raihan", "email": email, "password": password,
    })


def login(client, email="admin@diu.edu", password=PASSWORD):
    return client.post("/api/auth/login", json={"email": email, "password": password})


def auth_header(client, email="admin@diu.edu", password=PASSWORD):
    token = login(client, email, password).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_register_creates_org_and_admin(client):
    r = register(client)
    assert r.status_code == 201
    body = r.json()
    assert body["admin"]["role"] == "admin"
    assert body["organization"]["type"] == "educational_institution"
    assert "password" not in str(body)


def test_password_is_hashed_in_database(client):
    register(client)
    with client.session_factory() as db:
        user = db.query(User).one()
        assert user.password_hash != PASSWORD
        assert user.password_hash.startswith("$2")  # bcrypt


def test_duplicate_org_and_email_rejected(client):
    register(client)
    assert register(client, org="diu", email="other@diu.edu").status_code == 409
    assert register(client, org="Other Uni", email="ADMIN@diu.edu").status_code == 409


def test_weak_password_rejected(client):
    for bad in ["short1A", "alllowercase1", "ALLUPPERCASE1", "NoDigitsHere"]:
        assert register(client, password=bad).status_code == 422


def test_invalid_email_rejected(client):
    assert register(client, email="not-an-email").status_code == 422


def test_login_success_and_me(client):
    register(client)
    r = login(client)
    assert r.status_code == 200
    me = client.get("/api/users/me", headers=auth_header(client))
    assert me.status_code == 200
    assert me.json()["email"] == "admin@diu.edu"


def test_login_is_case_insensitive_for_email(client):
    register(client)
    assert login(client, email="Admin@DIU.edu").status_code == 200


def test_login_wrong_password_and_unknown_email_same_error(client):
    register(client)
    a = login(client, password="WrongPass1")
    b = login(client, email="nobody@diu.edu")
    assert a.status_code == b.status_code == 401
    assert a.json() == b.json()


def test_protected_endpoint_needs_valid_token(client):
    assert client.get("/api/users/me").status_code == 401
    assert client.get("/api/users/me", headers={"Authorization": "Bearer garbage"}).status_code == 401


def test_swagger_form_login(client):
    register(client)
    r = client.post("/api/auth/token", data={"username": "admin@diu.edu", "password": PASSWORD})
    assert r.status_code == 200


def test_admin_creates_staff_and_staff_can_login(client):
    register(client)
    r = client.post("/api/users", headers=auth_header(client), json={
        "name": "Store Person", "email": "store@diu.edu", "password": PASSWORD, "role": "store_officer",
    })
    assert r.status_code == 201
    assert r.json()["role"] == "store_officer"
    assert login(client, email="store@diu.edu").status_code == 200


def test_non_admin_cannot_create_or_list_users(client):
    register(client)
    client.post("/api/users", headers=auth_header(client), json={
        "name": "Store Person", "email": "store@diu.edu", "password": PASSWORD, "role": "store_officer",
    })
    staff = auth_header(client, email="store@diu.edu")
    payload = {"name": "X Y", "email": "x@diu.edu", "password": PASSWORD, "role": "manager"}
    assert client.post("/api/users", headers=staff, json=payload).status_code == 403
    assert client.get("/api/users", headers=staff).status_code == 403


def test_organizations_are_isolated(client):
    register(client, org="DIU", email="admin@diu.edu")
    register(client, org="Other University", email="admin@other.edu")
    users_a = client.get("/api/users", headers=auth_header(client, "admin@diu.edu")).json()
    assert [u["email"] for u in users_a] == ["admin@diu.edu"]


def test_deactivated_user_cannot_use_token(client):
    register(client)
    headers = auth_header(client)
    with client.session_factory() as db:
        user = db.query(User).one()
        user.is_active = False
        db.commit()
    assert client.get("/api/users/me", headers=headers).status_code == 401
    assert login(client).status_code == 401
