from urllib.parse import urljoin

import pytest

from src.application.system.system_release_value_object import SystemReleaseValueObject


@pytest.mark.gen_test
def test_system_release(http_client, base_url, auth_cookie):
    auth_cookie = yield auth_cookie

    url = urljoin(base_url, 'system/release')
    headers = {'Cookie': auth_cookie}
    response = yield http_client.fetch(url, method='GET', headers=headers)

    system_release = SystemReleaseValueObject(release='0')

    assert system_release == SystemReleaseValueObject.from_json(response.body)
