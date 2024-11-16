import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_file_upload(client):
    with open('test.pdf', 'rb') as pdf_file:
        response = client.post(reverse('upload_file'), {'file': pdf_file})
    assert response.status_code == 200
