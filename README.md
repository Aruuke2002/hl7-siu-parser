# HL7 SIU Parser

A Python-based parser for HL7 SIU^S12 appointment messages, converting them into structured JSON.

##  Features

- Parses `.hl7` SIU messages into JSON
- Extracts appointment, patient, provider, and location info
- Validates output against a JSON Schema
- Supports multiple messages in one file
- Command-line interface
- Dockerized

## 📂 Usage

### Run via CLI

```bash
python hl7_parser.py sample.hl7

### Docker 

docker build -t hl7-parser .
docker run --rm -v "$PWD":/app hl7-parser sample.hl7 --validate schema.json

## TEST
python -m unittest test_parser.py

## JSON OUTPUT EXAMPLE 

 All messages are valid against schema.
[
  {
    "appointment_id": "123456",
    "appointment_datetime": "2025-05-02T13:00:00Z",
    "location": "Clinic A - Room 203",
    "reason": "General Consultation",
    "patient": {
      "patient_id": "P12345",
      "name": "John Doe",
      "dob": "19850210",
      "gender": "M"
    },
    "provider": {
      "provider_id": "D67890",
      "provider_name": "Dr Smith"
    }
  }
]



