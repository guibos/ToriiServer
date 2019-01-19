from urllib.parse import urljoin

import pytest
from tornado.escape import url_escape
from tornado.httpclient import HTTPClientError

from src.domain.entities.user_entity import UserEntity
from src.domain.value_object import UserNewValueObject
from src.facade.database.data import get_admin_user
from tests.account.data.user import test_user_okabe_rintarou


@pytest.mark.gen_test
def test_account_user_get(http_client, base_url, auth_cookie):
    auth_cookie = yield auth_cookie

    url = urljoin(base_url, 'account/user')
    headers = {'Cookie': auth_cookie}
    response = yield http_client.fetch(url, method='GET', headers=headers)

    admin_user = get_admin_user().visible_fields()

    data = UserEntity.schema().loads(response.body, many=True)
    assert len(data) == 1
    user = UserNewValueObject.from_user_entity(user_entity=data[0])

    assert admin_user == user


@pytest.mark.gen_test
def test_account_user_get_filter(http_client, base_url, auth_cookie):
    auth_cookie = yield auth_cookie

    url = urljoin(base_url, 'account/user?username__in=admin')
    headers = {'Cookie': auth_cookie}
    response = yield http_client.fetch(url, method='GET', headers=headers)

    admin_user = get_admin_user().visible_fields()

    data = UserEntity.schema().loads(response.body, many=True)
    assert len(data) == 1
    user = UserNewValueObject.from_user_entity(user_entity=data[0])

    assert admin_user == user


@pytest.mark.gen_test
def test_account_user_get_bad_key_filter(http_client, base_url, auth_cookie):
    auth_cookie = yield auth_cookie

    url = urljoin(base_url, 'account/user?cristina__equal=1')
    headers = {'Cookie': auth_cookie}

    with pytest.raises(HTTPClientError) as context:
        yield http_client.fetch(url, method='GET', headers=headers)
    assert context.value.code == 400


@pytest.mark.gen_test
def test_account_user_get_bad_operator(http_client, base_url, auth_cookie):
    auth_cookie = yield auth_cookie

    url = urljoin(base_url, 'account/user?id__bad=1')
    headers = {'Cookie': auth_cookie}

    with pytest.raises(HTTPClientError) as context:
        yield http_client.fetch(url, method='GET', headers=headers)
    assert context.value.code == 400


@pytest.mark.gen_test
def test_account_user_add(http_client, base_url, auth_cookie):
    auth_cookie = yield auth_cookie

    url = urljoin(base_url, 'account/user')
    headers = {'Cookie': auth_cookie}

    data = [
        test_user_okabe_rintarou,
    ]

    response = yield http_client.fetch(
        url,
        method='POST',
        headers=headers,
        body=UserNewValueObject.schema().dumps(data,
                                               many=True))
    assert response.code == 204

    url = urljoin(base_url, f'account/user?username__in={url_escape(test_user_okabe_rintarou.username)}')
    headers = {'Cookie': auth_cookie}
    response = yield http_client.fetch(url, method='GET', headers=headers)

    data = UserEntity.schema().loads(response.body, many=True)
    assert len(data) == 1
    user = UserNewValueObject.from_user_entity(user_entity=data[0])

    assert test_user_okabe_rintarou.visible_fields() == user
