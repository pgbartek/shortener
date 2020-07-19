def test_redirects(test_client):
    create_response = test_client.post(
        "/redirects/", json={"url": "http://example.com"}
    )
    assert create_response.status_code == 200
    created = create_response.json()
    assert created["url"] == "http://example.com"
    assert "url_id" in created

    get_response = test_client.get(
        f'/redirects/{created["url_id"]}', allow_redirects=False
    )
    assert get_response.status_code == 307
    assert get_response.headers["location"] == "http://example.com"
