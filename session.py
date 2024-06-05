import uuid

def generate_session_id():
    unique_id = uuid.uuid4()
    hex_id = unique_id.hex
    formatted_id = f"{hex_id[:6]}-{hex_id[6:9]}-{hex_id[9:12]}-{hex_id[12:15]}-{hex_id[15:]}"
    return formatted_id
