"""
Excepciones personalizadas para el manejo de errores en la aplicación.
"""


class DocumentConversionError(Exception):
    """Excepción lanzada cuando hay un error durante la conversión de documentos."""
    pass


class FileNotFoundError(Exception):
    """Excepción lanzada cuando un archivo no se encuentra."""
    pass


class PDFProcessingError(Exception):
    """Excepción lanzada cuando hay un error procesando archivos PDF."""
    pass
