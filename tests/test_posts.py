"""
記事APIのテスト
"""


def get_auth_header(client):
    """テスト用のヘルパー: ユーザー登録→ログイン→トークン取得"""
    client.post("/auth/register", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "password123",
    })
    response = client.post("/auth/login", data={
        "username": "test@example.com",
        "password": "password123",
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def create_tag(client, headers, name="Python"):
    response = client.post("/tags/", json={"name": name}, headers=headers)
    assert response.status_code == 201
    return response.json()["id"]


# ===== 記事作成のテスト =====

def test_create_post_success(client):
    """正常系: ログイン済みユーザーが記事を作成できる"""
    headers = get_auth_header(client)
    response = client.post("/posts/", json={
        "title": "テスト記事",
        "content": "テスト内容",
        "tag_ids": [],
    }, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "テスト記事"
    assert data["author"]["username"] == "testuser"


def test_create_post_unauthorized(client):
    """異常系: ログインしていないと記事を作成できない"""
    response = client.post("/posts/", json={
        "title": "テスト記事",
        "content": "テスト内容",
        "tag_ids": [],
    })
    assert response.status_code == 401


def test_create_post_with_invalid_tag_ids_returns_400(client):
    """異常系: 存在しないタグIDを指定したら400エラー"""
    headers = get_auth_header(client)

    response = client.post("/posts/", json={
        "title": "テスト記事",
        "content": "テスト内容",
        "tag_ids": [999],
    }, headers=headers)

    assert response.status_code == 400


# ===== 記事取得のテスト =====

def test_get_posts(client):
    """正常系: 記事一覧が取得できる"""
    headers = get_auth_header(client)
    # 記事を2つ作成
    client.post("/posts/", json={"title": "記事1", "content": "内容1", "tag_ids": []}, headers=headers)
    client.post("/posts/", json={"title": "記事2", "content": "内容2", "tag_ids": []}, headers=headers)

    response = client.get("/posts/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_post_not_found(client):
    """異常系: 存在しない記事を取得しようとしたら404エラー"""
    response = client.get("/posts/9999")
    assert response.status_code == 404


def test_update_post_with_invalid_tag_ids_returns_400(client):
    """異常系: 更新時に存在しないタグIDを指定したら400エラー"""
    headers = get_auth_header(client)
    tag_id = create_tag(client, headers)
    post_response = client.post(
        "/posts/",
        json={"title": "記事", "content": "内容", "tag_ids": [tag_id]},
        headers=headers,
    )
    post_id = post_response.json()["id"]

    response = client.put(
        f"/posts/{post_id}",
        json={"tag_ids": [tag_id, 999]},
        headers=headers,
    )

    assert response.status_code == 400


# ===== 記事削除のテスト =====

def test_delete_other_users_post(client):
    """異常系: 他のユーザーの記事は削除できない"""
    # ユーザー1で記事を作成
    headers1 = get_auth_header(client)
    post_response = client.post("/posts/", json={
        "title": "ユーザー1の記事",
        "content": "内容",
        "tag_ids": [],
    }, headers=headers1)
    post_id = post_response.json()["id"]

    # ユーザー2を作成してログイン
    client.post("/auth/register", json={
        "email": "user2@example.com",
        "username": "user2",
        "password": "password123",
    })
    login2 = client.post("/auth/login", data={
        "username": "user2@example.com",
        "password": "password123",
    })
    headers2 = {"Authorization": f"Bearer {login2.json()['access_token']}"}

    # ユーザー2がユーザー1の記事を削除しようとする → 403エラー
    response = client.delete(f"/posts/{post_id}", headers=headers2)
    assert response.status_code == 403