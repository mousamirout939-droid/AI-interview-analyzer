"""
test_upload.py
=================
Tests upload endpoint access control and validation-layer rejection of
disallowed file types, without depending on real media processing.
"""

import io


def test_upload_requires_login(client, db):
    response = client.get("/upload/", follow_redirects=True)
    assert b"Log in" in response.data or b"Log In" in response.data


def _register_and_login(client, email="uploader@example.com"):
    client.post("/auth/register", data={
        "full_name": "Uploader Test",
        "email": email,
        "password": "Password1",
        "confirm_password": "Password1",
    }, follow_redirects=True)


def test_upload_rejects_disallowed_extension(client, db):
    _register_and_login(client)
    data = {
        "title": "Bad Upload",
        "question": "Test",
        "media_file": (io.BytesIO(b"not a real file"), "malware.exe"),
    }
    response = client.post("/upload/", data=data, content_type="multipart/form-data", follow_redirects=True)
    assert b"Unsupported file type" in response.data
