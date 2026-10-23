def test_learning_index_lists_guides_and_is_public(client):
    response = client.get("/learning/")

    assert response.status_code == 200
    assert b"Learning" in response.data
    assert b"Python" in response.data
    assert b"HTML &amp; CSS" in response.data
    assert b"TypeScript" in response.data
    assert b"Log in" in response.data


def test_language_guide_has_all_levels_and_code(client):
    response = client.get("/learning/python")

    assert response.status_code == 200
    assert b"Basics" in response.data
    assert b"Intermediate" in response.data
    assert b"Advanced" in response.data
    assert b"def even_squares" in response.data
    assert b"Examples are for learning" not in response.data


def test_every_language_guide_renders(client):
    slugs = (
        "python", "javascript", "html-css", "java", "c", "cpp",
        "csharp", "rust", "php", "sql", "typescript",
    )

    for slug in slugs:
        response = client.get(f"/learning/{slug}")
        assert response.status_code == 200, slug
        assert b"Basics" in response.data
        assert b"Advanced" in response.data


def test_unknown_language_returns_not_found(client):
    response = client.get("/learning/not-a-language")

    assert response.status_code == 404


def test_learning_link_is_available_from_homepage(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Explore Learning" in response.data
