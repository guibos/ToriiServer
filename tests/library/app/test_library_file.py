from urllib.parse import urljoin

import pytest


@pytest.mark.gen_test
async def test_library_file(http_client, base_url, auth_cookie):
    auth_cookie = yield auth_cookie

    url = urljoin(base_url, 'library/file/skuld.txt')
    headers = {'Cookie': auth_cookie}
    response = yield http_client.fetch(url, method='GET', headers=headers)
    assert response.body == b'El Psy Congroo'
