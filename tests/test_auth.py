"""
認証APIのテスト

面接で「テストはどう書きましたか？」と聞かれた時に
「正常系と異常系を両方書きました」と言えるようにする
"""


# ===== ユーザー登録のテスト =====

def test_register_success(client):
    """正常系: ユーザー登録が成功する"""
    response = client.post("/auth/register", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "password123",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "password" not in data  # パスワードがレスポンスに含まれないことを確認


def test_register_duplicate_email(client):
    """異常系: 同じメールアドレスで登録しようとしたら400エラー"""
    # 1回目は成功
    client.post("/auth/register", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "password123",
    })
    # 2回目は同じメールなので失敗
    response = client.post("/auth/register", json={
        "email": "test@example.com",
        "username": "anotheruser",
        "password": "password123",
    })
    assert response.status_code == 400


def test_register_duplicate_username(client):
    """異常系: 同じユーザー名で登録しようとしたら400エラー"""
    client.post("/auth/register", json={
        "email": "test1@example.com",
        "username": "testuser",
        "password": "password123",
    })
    response = client.post("/auth/register", json={
        "email": "test2@example.com",
        "username": "testuser",
        "password": "password123",
    })
    assert response.status_code == 400


# ===== ログインのテスト =====

def test_login_success(client):
    """正常系: ログインが成功してJWTトークンが返る"""
    # まずユーザーを登録
    client.post("/auth/register", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "password123",
    })
    # ログイン
    response = client.post("/auth/login", data={
        "username": "test@example.com",
        "password": "password123",
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    """異常系: パスワードが違ったら401エラー"""
    client.post("/auth/register", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "password123",
    })
    response = client.post("/auth/login", data={
        "username": "test@example.com",
        "password": "wrongpassword",
    })
    assert response.status_code == 401


def test_login_not_exist_user(client):
    """異常系: 存在しないユーザーでログインしたら401エラー"""
    response = client.post("/auth/login", data={
        "username": "notexist@example.com",
        "password": "password123",
    })
    assert response.status_code == 401
