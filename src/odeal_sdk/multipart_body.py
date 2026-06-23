"""multipart/form-data istek gövdesi.

Düz veri (metin alanları + dosya parçaları) tutar; gövde baytları bir kez üretilir
ve retry denemeleri arasında yeniden gönderilebilir (immutable bytes).
"""
import uuid
from typing import List, Tuple


class MultipartBody:
    """Dosya yükleyen endpoint'ler için multipart/form-data gövdesi (fluent API)."""

    def __init__(self) -> None:
        self._fields: List[Tuple[str, str]] = []
        self._files: List[Tuple[str, str, bytes, str]] = []

    def add_field(self, name: str, value: str) -> "MultipartBody":
        """Metin form alanı ekler."""
        self._fields.append((name, str(value)))
        return self

    def add_file(self, name: str, filename: str, content: bytes,
                 content_type: str = "application/octet-stream") -> "MultipartBody":
        """Dosya parçası ekler."""
        self._files.append((name, filename, content, content_type))
        return self

    def build(self) -> Tuple[str, bytes]:
        """(content_type, body_bytes) döndürür. content_type boundary içerir."""
        boundary = "----OdealBoundary" + uuid.uuid4().hex
        crlf = b"\r\n"
        bsep = ("--" + boundary).encode("utf-8")
        buf = bytearray()
        for name, value in self._fields:
            buf += bsep + crlf
            buf += f'Content-Disposition: form-data; name="{name}"'.encode("utf-8") + crlf + crlf
            buf += value.encode("utf-8") + crlf
        for name, filename, content, ctype in self._files:
            buf += bsep + crlf
            buf += f'Content-Disposition: form-data; name="{name}"; filename="{filename}"'.encode("utf-8") + crlf
            buf += f"Content-Type: {ctype}".encode("utf-8") + crlf + crlf
            buf += content + crlf
        buf += bsep + b"--" + crlf
        return f"multipart/form-data; boundary={boundary}", bytes(buf)
