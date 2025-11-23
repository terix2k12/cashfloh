from app.transformers.transformer_dkb import DkbTransformer
from app.transformers.transformer_voba import VobaTransformer


def test_dkb_filename_matchers():
    dkb_2025_filename = (
        "2025-09-05_Kontoauszug_9_2025_vom_05.09.2025_zu_Konto_1088888883.pdf"
    )
    assert DkbTransformer().checkFilename(dkb_2025_filename) == True


def test_voba_filename_matcher():
    voba_2025_filename = (
        "888888015_2025_Nr.008_Kontoauszug_vom_2025.08.30_20250909122452.pdf"
    )
    assert VobaTransformer().checkFilename(voba_2025_filename) == True
