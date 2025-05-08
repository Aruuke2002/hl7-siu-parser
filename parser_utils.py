import datetime
import re

def parse_h17_message(h17_str):

    segments = re.split(r'\r|\n', h17_str.strip())
    data = {}

    for segment in segments:
        fields = segment.split('|')


        if fields[0] == 'SCH':
            data.update(parse_sch(fields))
        elif fields[0] == 'PID':
            data['patient'] = parse_pid(fields)
        elif fields[0] == 'PV1':
            data['provider'] = parse_pv1(fields)


    validate_required_fields(data)
    return data

def parse_sch(fields):

    if len(fields) > 1:
        appointment_id = fields[1].split('^')[0]

    else:
        print("Error: SCH segment doesn't contain enough fields.")
        appointment_id = None  # Or handle appropriately

    dt_str = fields[4] if len(fields) > 4 else None  # Ensure there is a field 4
    if dt_str:
        try:
            appointment_dt = datetime.datetime.strptime(dt_str, '%Y%m%d%H%M')
            appointment_dt_iso = appointment_dt.isoformat() + 'Z'
        except ValueError:
            print(f"Error parsing date: {dt_str}")
            appointment_dt_iso = None
    else:
        appointment_dt_iso = None

    location = fields[6] if len(fields) > 6 else None
    reason = fields[7] if len(fields) > 7 else "Unknown"

    return {
        "appointment_id": appointment_id,
        "appointment_datetime": appointment_dt_iso,
        "location": location,
        "reason": reason
    }

def parse_pid(fields):
    patient_id = fields[3].split('^')[0] if len(fields) > 3 else None
    name_parts = fields[5].split('^') if len(fields) > 5 else []
    name = f"{name_parts[1]} {name_parts[0]}" if len(name_parts) >= 2 else name_parts[0] if name_parts else None
    dob = fields[7] if len(fields) > 7 else None
    gender = fields[8] if len(fields) > 8 else None

    return {
        "patient_id": patient_id,
        "name": name,
        "dob": dob,
        "gender": gender
    }

def parse_pv1(fields):
    if len(fields) > 3:
        provider_info = fields[3].split('^')
        provider_id = provider_info[0] if len(provider_info) > 0 else None
        provider_name = f"{provider_info[2]} {provider_info[1]}" if len(provider_info) > 2 else None
    else:
        provider_id = None
        provider_name = None

    return {
        "provider_id": provider_id,
        "provider_name": provider_name
    }
def validate_required_fields(data):
    required_keys = ['appointment_id', 'appointment_datetime', 'patient', 'provider', 'location']
    for key in required_keys:
        if key not in data or data[key] in [None, ""]:
            raise ValueError(f"Missing required field: {key}")
