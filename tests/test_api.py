from app.models.user import User


def register_user(client, name, email, password, role):
    return client.post(
        "/auth/register",
        json={"name": name, "email": email, "password": password, "role": role},
    )


def login_user(client, email, password):
    return client.post(
        "/auth/login",
        json={"email": email, "password": password},
    )


def auth_header(token: str):
    return {"Authorization": f"Bearer {token}"}


def test_register_login_and_profile(client):
    response = register_user(client, "Alice Student", "alice@example.com", "password123", "student")
    assert response.status_code == 200
    body = response.json()
    assert body["email"] == "alice@example.com"
    assert body["role"] == "student"
    assert body["is_active"] is True

    login_response = login_user(client, "alice@example.com", "password123")
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    profile = client.get("/auth/me", headers=auth_header(token))
    assert profile.status_code == 200
    assert profile.json()["email"] == "alice@example.com"


def test_admin_course_management_and_public_course_listing(client):
    admin_register = register_user(client, "Admin User", "admin@example.com", "adminpass", "admin")
    assert admin_register.status_code == 200

    login_response = login_user(client, "admin@example.com", "adminpass")
    assert login_response.status_code == 200
    admin_token = login_response.json()["access_token"]
    headers = auth_header(admin_token)

    create_response = client.post(
        "/courses/",
        headers=headers,
        json={"title": "Math 101", "code": "MATH101", "capacity": 2},
    )
    assert create_response.status_code == 200
    assert create_response.json()["code"] == "MATH101"

    create_response2 = client.post(
        "/courses/",
        headers=headers,
        json={"title": "Physics 101", "code": "PHYS101", "capacity": 1},
    )
    assert create_response2.status_code == 200

    course_id = create_response.json()["id"]
    update_response = client.put(
        f"/courses/{course_id}",
        headers=headers,
        json={"capacity": 1, "is_active": False},
    )
    assert update_response.status_code == 200
    assert update_response.json()["is_active"] is False

    public_courses = client.get("/courses/")
    assert public_courses.status_code == 200
    course_codes = [course["code"] for course in public_courses.json()]
    assert "PHYS101" in course_codes
    assert "MATH101" not in course_codes


def test_course_pagination_and_filtering(client):
    admin_register = register_user(client, "Admin Pager", "pager@example.com", "adminpass", "admin")
    assert admin_register.status_code == 200

    login_response = login_user(client, "pager@example.com", "adminpass")
    assert login_response.status_code == 200
    admin_token = login_response.json()["access_token"]
    admin_headers = auth_header(admin_token)

    for i in range(1, 12):
        response = client.post(
            "/courses/",
            headers=admin_headers,
            json={"title": f"Page Course {i}", "code": f"PAGE{i}", "capacity": 5},
        )
        assert response.status_code == 200

    page_two = client.get("/courses/?page=2&limit=5")
    assert page_two.status_code == 200
    assert len(page_two.json()) == 5

    search_response = client.get("/courses/?q=PAGE11")
    assert search_response.status_code == 200
    assert len(search_response.json()) == 1
    assert search_response.json()[0]["code"] == "PAGE11"


def test_auth_rate_limiting(client):
    response = None
    for _ in range(25):
        response = login_user(client, "notfound@example.com", "wrongpass")
        if response.status_code == 429:
            break

    assert response is not None
    assert response.status_code == 429


def test_student_enrollment_and_admin_oversight(client, db):
    student_response = register_user(client, "Bob Student", "bob@example.com", "studentpass", "student")
    assert student_response.status_code == 200

    admin_login = login_user(client, "admin@example.com", "adminpass")
    admin_token = admin_login.json()["access_token"]
    admin_headers = auth_header(admin_token)

    public_courses = client.get("/courses/")
    assert public_courses.status_code == 200
    assert len(public_courses.json()) >= 1
    course_id = public_courses.json()[0]["id"]

    enroll_response = client.post(
        "/enrollments/",
        headers=auth_header(login_user(client, "bob@example.com", "studentpass").json()["access_token"]),
        json={"course_id": course_id},
    )
    assert enroll_response.status_code == 200

    duplicate_response = client.post(
        "/enrollments/",
        headers=auth_header(login_user(client, "bob@example.com", "studentpass").json()["access_token"]),
        json={"course_id": course_id},
    )
    assert duplicate_response.status_code == 400

    admin_enrollments = client.get("/enrollments/", headers=admin_headers)
    assert admin_enrollments.status_code == 200
    assert len(admin_enrollments.json()) >= 1

    course_enrollments = client.get(f"/enrollments/course/{course_id}", headers=admin_headers)
    assert course_enrollments.status_code == 200
    assert len(course_enrollments.json()) >= 1

    enrollment_id = course_enrollments.json()[0]["id"]
    remove_response = client.delete(f"/enrollments/{enrollment_id}", headers=admin_headers)
    assert remove_response.status_code == 200

    # Ensure deregistration works for student
    re_enroll = client.post(
        "/enrollments/",
        headers=auth_header(login_user(client, "bob@example.com", "studentpass").json()["access_token"]),
        json={"course_id": course_id},
    )
    assert re_enroll.status_code == 200

    deregister_response = client.delete(
        f"/enrollments/self/{course_id}",
        headers=auth_header(login_user(client, "bob@example.com", "studentpass").json()["access_token"]),
    )
    assert deregister_response.status_code == 200


def test_inactive_user_cannot_authenticate(client, db):
    inactive = register_user(client, "Inactive User", "inactive@example.com", "nopass", "student")
    assert inactive.status_code == 200

    user = db.query(User).filter(User.email == "inactive@example.com").first()
    user.is_active = False
    db.commit()

    login_response = login_user(client, "inactive@example.com", "nopass")
    assert login_response.status_code == 401


def test_get_course_by_id_and_delete_by_admin(client):
    # create an admin and a course
    admin_register = register_user(client, "Delete Admin", "deladmin@example.com", "adminpass", "admin")
    assert admin_register.status_code == 200

    login_response = login_user(client, "deladmin@example.com", "adminpass")
    assert login_response.status_code == 200
    admin_token = login_response.json()["access_token"]
    headers = auth_header(admin_token)

    create_response = client.post(
        "/courses/",
        headers=headers,
        json={"title": "Temp Course", "code": "TEMP101", "capacity": 1},
    )
    assert create_response.status_code == 200
    course = create_response.json()
    course_id = course["id"]

    # retrieve by id
    get_response = client.get(f"/courses/{course_id}")
    assert get_response.status_code == 200
    assert get_response.json()["code"] == "TEMP101"

    # delete (deactivate) as admin
    del_response = client.delete(f"/courses/{course_id}", headers=headers)
    assert del_response.status_code == 200

    # ensure not present in public listing
    public = client.get("/courses/")
    codes = [c["code"] for c in public.json()]
    assert "TEMP101" not in codes


def test_student_cannot_manage_courses_and_admin_only_access(client):
    # register a student
    student_register = register_user(client, "Limited Student", "limited@example.com", "pass", "student")
    assert student_register.status_code == 200
    student_token = login_user(client, "limited@example.com", "pass").json()["access_token"]
    student_headers = auth_header(student_token)

    # student should be forbidden from creating courses (authenticated but not admin)
    resp = client.post(
        "/courses/",
        headers=student_headers,
        json={"title": "Bad Course", "code": "BAD1", "capacity": 1},
    )
    assert resp.status_code == 403

    # unauthenticated access to protected endpoints should be 401
    unauth_me = client.get("/auth/me")
    assert unauth_me.status_code == 401

    unauth_create = client.post(
        "/courses/",
        json={"title": "No Auth", "code": "NA1", "capacity": 1},
    )
    assert unauth_create.status_code == 401

    # student cannot access admin-only enrollments list
    resp = client.get("/enrollments/", headers=student_headers)
    assert resp.status_code == 403
