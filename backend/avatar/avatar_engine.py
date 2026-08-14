def generate_avatar_sequence(sign_sequence: list) -> dict:
    """
    Temporary avatar layer.
    Later this will drive the signing avatar.
    """
    return {
        "status": "avatar_pending",
        "sign_sequence": sign_sequence,
        "animation": None
    }
