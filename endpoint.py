# Standard
import sys
from io import StringIO
import logging

# Third party
from flask import Flask, request, jsonify
from lxml import etree
from nacl.encoding import HexEncoder, Base64Encoder
from nacl.public import PublicKey, SealedBox

# Logging setup
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

log: logging.Logger = logging.getLogger("nNGM Endpoint")


"""
As the system will be used with pyinstaller, having the xsd as a string in the
file makes life easier.

- The start of the string CAN NOT have any whitespace
- The string MUST be passed as bytes
"""
xsd_schema: bytes = b"""<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema" elementFormDefault="qualified">
  <xs:element name="patient">
    <xs:complexType mixed="true">
      <xs:sequence>
        <xs:element ref="vorname"/>
        <xs:element ref="nachname"/>
        <xs:element ref="geburtstag"/>
        <xs:element ref="geburtsmonat"/>
        <xs:element ref="geburtsjahr"/>
        <xs:element ref="versicherungsnummer"/>
        <xs:element ref="adresse.plz"/>
        <xs:element ref="adresse.stadt"/>
        <xs:element ref="adresse.strasse"/>
      </xs:sequence>
    </xs:complexType>
  </xs:element>
  <xs:element name="vorname">
    <xs:simpleType>
      <xs:restriction base="xs:string">
        <xs:minLength value="1"/>
      </xs:restriction>
    </xs:simpleType>
  </xs:element>
  <xs:element name="nachname">
    <xs:simpleType>
      <xs:restriction base="xs:string">
        <xs:minLength value="1"/>
      </xs:restriction>
    </xs:simpleType>
  </xs:element>
  <xs:element name="geburtstag">
    <xs:simpleType>
      <xs:restriction base="xs:integer">
        <xs:pattern value="[0-3][0-9]"/>
        <xs:maxInclusive value="31"/>
        <xs:minInclusive value="1"/>
      </xs:restriction>
    </xs:simpleType>
  </xs:element>
  <xs:element name="geburtsmonat">
    <xs:simpleType>
      <xs:restriction base="xs:integer">
        <xs:minInclusive value="1"/>
        <xs:maxInclusive value="12"/>
        <xs:pattern value="[0-1][0-9]"/>
      </xs:restriction>
    </xs:simpleType>
  </xs:element>
  <xs:element name="geburtsjahr">
    <xs:simpleType>
      <xs:restriction base="xs:integer">
        <xs:minInclusive value="1900"/>
        <xs:maxInclusive value="2045"/>
        <xs:pattern value="[1-2][0-9][0-9][0-9]"/>
      </xs:restriction>
    </xs:simpleType>
  </xs:element>
  <xs:element name="versicherungsnummer">
    <xs:simpleType>
      <xs:restriction base="xs:string">
        <xs:minLength value="1"/>
        <xs:maxLength value="32"/>
      </xs:restriction>
    </xs:simpleType>
  </xs:element>
  <xs:element name="adresse.plz">
    <xs:simpleType>
      <xs:restriction base="xs:string"> </xs:restriction>
    </xs:simpleType>
  </xs:element>
  <xs:element name="adresse.stadt">
    <xs:simpleType>
      <xs:restriction base="xs:string"> </xs:restriction>
    </xs:simpleType>
  </xs:element>
  <xs:element name="adresse.strasse">
    <xs:simpleType>
      <xs:restriction base="xs:string"> </xs:restriction>
    </xs:simpleType>
  </xs:element>
</xs:schema>
"""

"""
Setup 
"""
xml_schema: etree.XMLSchema = None

try:
    xml_schema = etree.XMLSchema(etree.fromstring(xsd_schema))
except etree.XMLSchemaError as err:  # Fatal
    log.critical(f"XSD Schema error - Exiting: {err}")
    sys.exit(1)

log.info("XSD Schema loaded")

api = Flask(__name__)

# Public Key provided by DKFZ
PUBLIC_KEY_HEX: bytes = b"e8553d8c6ffcf5d6418b215bd6f7286105d44ed537eacad7c80680650ef8540d"  # @TODO Replace DEV key
PUBLIC_KEY: PublicKey = PublicKey(PUBLIC_KEY_HEX, HexEncoder)
sealed_box: SealedBox = SealedBox(PUBLIC_KEY)

log.info(f"Public key: {PUBLIC_KEY_HEX}")


def encrypt_payload(payload: bytes, box: SealedBox = sealed_box) -> bytes:
    return box.encrypt(payload, Base64Encoder)


@api.route("/encrypt/xml", methods=["POST"])
def encrypt_xml():
    log.info(f"Received POST request from: {request.remote_addr}")
    payload: str = str(request.data.decode())

    if len(payload) == 0:
        log.debug("encrypt_xml(): Received empty payload. Returning 400.")
        return jsonify({"status": 400, "message": "Body empty"}), 400

    try:
        payload_xml: etree.Element = etree.parse(StringIO(payload))
    except etree.ParseError as xmlerror:
        log.debug("encrypt_xml(): Received corrupt XML payload. Returning 400.")
        return jsonify({"status": 400, "message": str(xmlerror)}), 400

    try:
        xml_schema.assertValid(payload_xml)
    except etree.DocumentInvalid as xmlerror:
        log.debug("encrypt_xml(): Received invalid XML payload. Returning 400.")
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
