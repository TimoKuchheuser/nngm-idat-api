# Third party
import pytest
from nacl.public import PublicKey, PrivateKey, SealedBox
from nacl.encoding import HexEncoder, Base64Encoder


# Test key pair provided by DKFZ
PUBLIC_KEY: bytes = b"fac5bac92c40adb0abe85b1159a03856bd9641c7e3bc65f29e011e42681d5e24"
PRIVATE_KEY: bytes = b"a5c7c055fc1087610ed131aa8413d4d87c879127272cba587c3b16f14dcec65c"


XML_TEST_VALID: str = (
    "<patient>"
    "<vorname>Test</vorname>)"
    "<nachname>Test</nachname>"
    "<geburtstag>01</geburtstag>"
    "<geburtsmonat>01</geburtsmonat>"
    "<geburtsjahr>2001</geburtsjahr>"
    "<versicherungsnummer>X234567890</versicherungsnummer>"
    "<adresse.plz>99999</adresse.plz>"
    "<adresse.stadt>Testhausen</adresse.stadt>"
    "<adresse.strasse>Teststr. 21</adresse.strasse>"
    "</patient>"
)


@pytest.fixture
def box_encrypt():
    return SealedBox(PublicKey(PUBLIC_KEY, HexEncoder))


@pytest.fixture()
def box_decrypt():
    return SealedBox(PrivateKey(PRIVATE_KEY, HexEncoder))


def test_encryption(box_encrypt, box_decrypt):
    plain: str = "Text to be encrypted 123 !ß%@"
    cipher: bytes = box_encrypt.encrypt(str.encode(plain), Base64Encoder)
    decrypted: str = box_decrypt.decrypt(cipher, Base64Encoder).decode()
    assert plain == decrypted


def test_encrypt_xml(box_encrypt, box_decrypt):
    cipher: bytes = box_encrypt.encrypt(str.encode(XML_TEST_VALID), Base64Encoder)
    decrypted: str = box_decrypt.decrypt(cipher, Base64Encoder).decode()
    assert XML_TEST_VALID == decrypted
