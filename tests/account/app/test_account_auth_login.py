from urllib.parse import urljoin

import pytest
from tornado.httpclient import HTTPClientError


@pytest.mark.gen_test
async def test_account_auth_check_non_authenticated(http_client, base_url):
    url = urljoin(base_url, 'library/file/this_is_a_test')

    with pytest.raises(HTTPClientError) as context:
        yield http_client.fetch(url)
    assert context.value.code == 403


@pytest.mark.gen_test
def test_account_auth_get_auth_cookie(auth_cookie):
    auth_cookie = yield auth_cookie

    assert auth_cookie[0:4] == 'auth'


@pytest.mark.gen_test
def test_account_auth_get_data(http_client, base_url, auth_cookie):
    auth_cookie = yield auth_cookie

    url = urljoin(base_url, 'library/file/skuld.txt')
    headers = {'Cookie': auth_cookie}
    response = yield http_client.fetch(url, method='GET', headers=headers)
    assert response.body == b'El Psy Congroo'
