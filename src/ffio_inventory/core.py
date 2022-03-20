import os
import tempfile
from os import getenv
from pathlib import Path

_default_upload_folder = os.path.join(tempfile.gettempdir(), "ffio_inventory")

UPLOAD_FOLDER = getenv("UPLOAD_FOLDER", _default_upload_folder)
UPLOAD_PATH = Path(UPLOAD_FOLDER)
