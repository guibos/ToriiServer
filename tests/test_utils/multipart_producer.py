import mimetypes
from typing import List, Dict, Any

from tornado import gen


@gen.coroutine
def multipart_producer(
        boundary: str,
        files: List[Dict[str, str]],
        fields: List[Dict[str, str]],
        objects: List[Dict[str, Any]],
        write):
    boundary_bytes = boundary.encode()

    for field in fields:
        field_bytes = field['name'].encode()
        buf = (
            (b"--%s\r\n" % boundary_bytes) + (b'Content-Disposition: form-data; name="%s"\r\n' % field_bytes) +
            b"\r\n" + field['value'].encode() + b"\r\n")
        yield write(buf)

    for file in files:
        mime_type = mimetypes.guess_type(file['path'])[0] or "application/octet-stream"
        buf = (
            (b"--%s\r\n" % boundary_bytes) +
            (b'Content-Disposition: form-data; name="%s"; filename="%s"\r\n' %
             (file['field'].encode(),
              file['filename'].encode())) + (b"Content-Type: %s\r\n" % mime_type.encode()) + b"\r\n")
        yield write(buf)
        with open(file['path'], "rb") as f:
            while True:
                # 16k at a time.
                chunk = f.read(16 * 1024)
                if not chunk:
                    break
                yield write(chunk)

        yield write(b"\r\n")

    for obj_dict in objects:
        buf = (
            (b"--%s\r\n" % boundary_bytes) +
            (b'Content-Disposition: form-data; name="%s"; filename="%s"\r\n' %
             (obj_dict['field'].encode(),
              obj_dict['filename'].encode())) + (b"Content-Type: %s\r\n" % obj_dict['mime'].encode()) + b"\r\n")
        yield write(buf)
        while True:
            # 16k at a time.
            chunk = obj_dict['obj'].read(16 * 1024)
            if not chunk:
                break
            yield write(chunk)

        yield write(b"\r\n")

    yield write(b"--%s--\r\n" % (boundary_bytes, ))
