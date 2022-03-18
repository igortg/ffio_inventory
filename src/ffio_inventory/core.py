import tempfile
from pathlib import Path

TEMP_PATH = Path(tempfile.gettempdir())
UPLOAD_FOLDER = TEMP_PATH / "ffio_inventory"
