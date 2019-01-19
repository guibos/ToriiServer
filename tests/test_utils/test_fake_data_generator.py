from tests.test_utils.fake_data_generator import FakeDataGenerator


def test_fake_data_generator_total_bytes_exactly():
    n_bytes = 40
    fake = FakeDataGenerator(total_bytes=n_bytes)
    data = b''
    while True:
        chunk = fake.read(20)
        if not chunk:
            break
        data += chunk
    assert len(data) == n_bytes


def test_fake_data_generator_total_bytes_non_exactly():
    n_bytes = 50
    fake = FakeDataGenerator(total_bytes=n_bytes)
    data = b''
    while True:
        chunk = fake.read(20)
        if not chunk:
            break
        data += chunk
    assert len(data) == n_bytes


def test_fake_data_generator_total_bytes_non_exactly():
    n_bytes = 50
    fake = FakeDataGenerator(total_bytes=n_bytes)
    data = b''
    while True:
        chunk = fake.read(20)
        if not chunk:
            break
        data += chunk
    assert len(data) == n_bytes