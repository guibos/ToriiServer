from functools import partial
from urllib.parse import urljoin
from uuid import uuid4

import pytest

from tests.test_utils.fake_data_generator import FakeDataGenerator
from tests.test_utils.multipart_producer import multipart_producer


@pytest.mark.gen_test
def test_multipart_upload(http_client, base_url, auth_cookie):
    auth_cookie = yield auth_cookie
    url = urljoin(base_url, 'graph')
    boundary = uuid4().hex
    headers = {'Cookie': auth_cookie, "Content-Type": "multipart/form-data; boundary=%s" % boundary}
    file_names = [{'path': 'tests/graph/fixture_file.epub', 'field': 'file', 'filename': 'fixture_file.epub'}]
    graph = '''
    query {
      users {
        name,
        lastName
      }
    }
    '''
    fields = []
    objects = []
    body_producer = partial(multipart_producer, boundary, file_names, fields, objects)

    response = yield http_client.fetch(url, method='POST', headers=headers, body_producer=body_producer)


@pytest.mark.stress
@pytest.mark.gen_test(timeout=50000)
def test_multipart_upload_stress(http_client, base_url, auth_cookie):
    auth_cookie = yield auth_cookie
    url = urljoin(base_url, 'graph')
    boundary = uuid4().hex
    headers = {'Cookie': auth_cookie, "Content-Type": "multipart/form-data; boundary=%s" % boundary}
    file_names = []
    fields = [{'name': 'graph', 'value': 'whats app!'}]
    objects = [{'field': 'file', 'filename': 'fixture_file.epub', 'obj': FakeDataGenerator(20 * 1024 * 1024 * 1024), 'mime': 'plain/text'}]  # 20GiB
    body_producer = partial(multipart_producer, boundary, file_names, fields, objects)

    response = yield http_client.fetch(
        url,
        method='POST',
        headers=headers,
        body_producer=body_producer,
        request_timeout=55555)
