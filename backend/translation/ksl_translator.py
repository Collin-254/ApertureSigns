def translate_to_ksl(text: str) -> dict:
    """
    Temporary KSL translation layer.
    Later this will connect to the trained Aperture Signs model.
    """
    return {
        "input_text": text,
        "language": "KSL",
        "status": "translation_pending",
        "sign_sequence": []
    }
