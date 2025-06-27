"""
Módulo de utilidades para la aplicación de conversión de documentos.
"""

from .file_utils import (
    setup_logging,
    get_logger,
    validate_file_extension,
    create_output_directory,
    safe_file_removal,
    get_file_size_mb,
    get_resource_path,
    get_app_icon
)

try:
    from .styles import COLORS, MAIN_STYLE, BUTTON_STYLE_PRIMARY, BUTTON_STYLE_SECONDARY
    STYLES_AVAILABLE = True
except ImportError:
    STYLES_AVAILABLE = False

__all__ = [
    'setup_logging',
    'get_logger',
    'validate_file_extension', 
    'create_output_directory',
    'safe_file_removal',
    'get_file_size_mb',
    'get_resource_path',
    'get_app_icon'
]

if STYLES_AVAILABLE:
    __all__.extend(['COLORS', 'MAIN_STYLE', 'BUTTON_STYLE_PRIMARY', 'BUTTON_STYLE_SECONDARY'])
