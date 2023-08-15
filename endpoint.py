# Standard
import sys
from io import StringIO

# Third party
from flask import Flask, request, jsonify
from lxml import etree

from nacl.public import PublicKey, SealedBox
from nacl.encoding import HexEncoder, Base64Encoder

"""
Setup 
"""
schema_xml: etree.Element = None
xml_schema: etree.XMLSchema = None
try:
    schema_xml = etree.parse("schema.xsd")
except FileNotFoundError as err:  # Fatal
    print("ERROR - XSD Schema file not found - Exiting")
    sys.exit(1)

try:
    xml_schema = etree.XMLSchema(schema_xml)
except etree.XMLSchemaError as err:  # Fatal
    print(f"ERROR - XSD Schema error - Exiting: {err}")
    sys.exit(1)


api = Flask(__name__)

# Public Key provided by DKFZ
PUBLIC_KEY_HEX: bytes = b"fac5bac92c40adb0abe85b1159a03856bd9641c7e3bc65f29e011e42681d5e24"  # @TODO REPLACE TEST KEY!!!
PUBLIC_KEY: PublicKey = PublicKey(PUBLIC_KEY_HEX, HexEncoder)
sealed_box: SealedBox = SealedBox(PUBLIC_KEY)


def encrypt_payload(payload: bytes, box: SealedBox = sealed_box) -> bytes:
    return box.encrypt(payload, Base64Encoder)


@api.route("/encrypt/xml", methods=["POST"])
def encrypt_xml():
    payload: str = str(request.data.decode())

    if len(payload) == 0:
        return jsonify({"status": 400, "message": "Body empty"}), 400

    try:
        payload_xml: etree.Element = etree.parse(StringIO(payload))
    except etree.ParseError as xmlerror:
        return jsonify({"status": 400, "message": str(xmlerror)}), 400

    try:
        xml_schema.assertValid(payload_xml)
    except etree.DocumentInvalid as xmlerror:
        return jsonify({"status": 400, "message": str(xmlerror)}), 400

    payload_encrypted: str = encrypt_payload(str.encode(payload)).decode()

    response: dict = {
        "status": 200,
        "message": "OK",
        "payload_encrypted": payload_encrypted,
    }

    return jsonify(response), 200


if __name__ == "__main__":
    api.run()
