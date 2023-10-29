from app import db
from app.models import Article


def test_get_articles(client):
    test_article = Article(title='Test Title', description='Test Description')
    db.session.add(test_article)
    db.session.commit()

    response = client.get('/get')

    assert response.status_code == 200

    assert b'Test Title' in response.data
    assert b'Test Description' in response.data


def test_add_article(client):
    response = client.post('/add', json={'title': 'Test Title', 'description': 'Test Description'})

    assert response.status_code == 200
    assert b'Test Title' in response.data
    assert b'Test Description' in response.data


def test_update_article(client):
    test_article = Article(title='Old Title', description='Old Description')
    db.session.add(test_article)
    db.session.commit()

    response = client.put(f'/update/{test_article.id}', json={'title': 'New Title', 'description': 'New Description'})

    assert response.status_code == 200
    assert b'New Title' in response.data
    assert b'New Description' in response.data

    db.session.delete(test_article)
    db.session.commit()


def test_delete_article(client):
    test_article = Article(title='Test Title', description='Test Description')
    db.session.add(test_article)
    db.session.commit()

    response = client.delete(f'/delete/{test_article.id}')

    assert response.status_code == 200
    assert b'Test Title' in response.data
    assert b'Test Description' in response.data

    deleted_article = db.session.get(Article, test_article.id)

    assert deleted_article is None