from core.models import configuration
from core import secret, contract
from core.constants import ENVIRONMENT

import os
import tempfile
from core.logging import LoggerMixin

class InitialInjestTransform(LoggerMixin):

    def __init__(self, input_s3_path, delimiter=',', quote_char='"', skip_rows=0, encoding="utf-8"):
