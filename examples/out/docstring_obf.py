from base64 import b64decode
class Foo:
    """
    IyBzb3VyY2UgZmlsZSB0aGF0IHdpbGwgYmUgb2JmdXNjYXRlZAppbXBvcnQgcmFuZG9tCmltcG
    9ydCBzdHJpbmcKCgpkZWYgZ2V0X3JhbmRvbV9sZXR0ZXIoKToKICAgICIiIlRoaXMgaXMgYSBk
    b2NzdHJpbmcuIiIiCiAgICByZXR1cm4gcmFuZG9tLmNob2ljZShzdHJpbmcuYXNjaWlfbG93ZX
    JjYXNlKQoKCmRlZiBnZXRfcmFuZG9tX25hbWUobmFtZV9sZW4pOgogICAgIyB0aGlzIGlzIGEg
    Y29tbWVudAogICAgbmFtZSA9IGdldF9yYW5kb21fbGV0dGVyKCkKICAgIGZvciBfIGluIHJhbm
    dlKG5hbWVfbGVuIC0gMSk6CiAgICAgICAgbmFtZSArPSBnZXRfcmFuZG9tX2xldHRlcigpCiAg
    ICByZXR1cm4gbmFtZQoKCmRlZiBwcmVzZW50X215X3BldCgpOgogICAgcGV0X25hbWUgPSBnZX
    RfcmFuZG9tX25hbWUoOCkKICAgIG1lc3NhZ2UgPSAiTXkgcGV0IGlzIG5hbWVkOiAiICsgcGV0
    X25hbWUKICAgIHByaW50KG1lc3NhZ2UpCgoKcHJlc2VudF9teV9wZXQoKQo=
    """
    pass


exec(b64decode(Foo.__doc__.replace('\\n','').replace(' ','')))
