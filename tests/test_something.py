

def author_payload(uid=1, name="Fred", email="sample@gmail.com", year_started="2000"):
    return {"author_id":uid, "name":name, "email": email, "year_started": year_started}

def test_create_author_ok(client):
    r= client.post("api/authors", json=author_payload())
    assert r.status_code = 201

def test_put_author_ok(client):
    r = client.post("api/authros", json=author_payload())
    r = client.put("api/authors/{1}", json=author_payload())
    assert r.status_code = 200

def test_patch_author_ok(client):
    r = client.post("api/authors")

