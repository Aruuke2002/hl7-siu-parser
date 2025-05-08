import json
import sys
import argparse
from parser_utils import parse_h17_message

try:
    from jsonschema import validate, ValidationError
    SCHEMA_VALIDATION_AVAILABLE = True
except ImportError:
    SCHEMA_VALIDATION_AVAILABLE = False

def parse_file(filepath):
    with open(filepath, "r") as f:
        content = f.read()

    # Split multiple HL7 messages
    messages = content.strip().split("\nMSH")
    if len(messages) > 1:
        messages = ["MSH" + m if not m.startswith("MSH") else m for m in messages]
    else:
        messages = [content]

    results = []
    for message in messages:
        parsed = parse_h17_message(message)
        results.append(parsed)

    return results

def main():
    parser = argparse.ArgumentParser(description="HL7 SIU Parser")
    parser.add_argument("file", help="Path to the .hl7 input file")
    parser.add_argument("--validate", help="Path to JSON schema file", default=None)
    args = parser.parse_args()

    try:
        results = parse_file(args.file)

        if args.validate:
            if not SCHEMA_VALIDATION_AVAILABLE:
                print(" Install jsonschema to enable validation: pip install jsonschema")
                sys.exit(1)
            with open(args.validate) as schema_file:
                schema = json.load(schema_file)

            for idx, entry in enumerate(results):
                try:
                    validate(instance=entry, schema=schema)
                except ValidationError as e:
                    print(f"Validation failed for message {idx + 1}: {e.message}")
                    sys.exit(1)

            print(" All messages are valid against schema.")

        print(json.dumps(results, indent=2))

    except Exception as e:
        print(f" Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()



