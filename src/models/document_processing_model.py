"""
Modelo principal que coordina las operaciones de conversión y procesamiento.
"""

import os
from typing import Optional
from .document_converter import DocumentConverter
from .pdf_processor import PDFProcessor
from .exceptions import DocumentConversionError, PDFProcessingError
from src.utils import get_logger

logger = get_logger("document_processing")


class DocumentProcessingModel:
    """Modelo principal que coordina todas las operaciones de procesamiento de documentos."""
    
    def __init__(self):
        self.document_converter = DocumentConverter()
        self.pdf_processor = PDFProcessor()
        self.selected_file: Optional[str] = None
    
    def set_selected_file(self, file_path: str) -> None:
        """Establece el archivo seleccionado para procesar."""
        self.selected_file = file_path
    
    def get_selected_file(self) -> Optional[str]:
        """Obtiene el archivo actualmente seleccionado."""
        return self.selected_file
    
    def has_selected_file(self) -> bool:
        """Verifica si hay un archivo seleccionado."""
        return self.selected_file is not None
    
    def clear_selected_file(self) -> None:
        """Limpia el archivo seleccionado."""
        self.selected_file = None
        logger.info("Archivo seleccionado limpiado del modelo")
    
    def process_document(self) -> None:
        """
        Procesa el documento seleccionado: convierte a PDF y divide en páginas.
        
        Raises:
            DocumentConversionError: Si no hay archivo seleccionado o error en conversión
            PDFProcessingError: Si hay error procesando el PDF
        """
        if not self.has_selected_file():
            raise DocumentConversionError("No se ha seleccionado ningún archivo.")
        
        # Generar nombres de archivos y carpetas
        output_pdf_filename = self._get_output_pdf_filename()
        output_folder = self._get_output_folder()
        
        try:
            # Convertir Word a PDF
            self.document_converter.convert_word_to_pdf(
                self.selected_file, 
                output_pdf_filename
            )
            
            # Dividir PDF en páginas individuales
            self.pdf_processor.split_pdf_by_page(
                output_pdf_filename, 
                output_folder
            )
            
        finally:
            # Limpiar archivo temporal si existe
            self._cleanup_temp_file(output_pdf_filename)
    
    def _get_output_pdf_filename(self) -> str:
        """Genera el nombre del archivo PDF temporal."""
        return os.path.splitext(self.selected_file)[0] + ".pdf"
    
    def _get_output_folder(self) -> str:
        """Genera el nombre de la carpeta de salida."""
        base_name = os.path.splitext(os.path.basename(self.selected_file))[0]
        return os.path.join(os.path.dirname(self.selected_file), base_name)
    
    def _cleanup_temp_file(self, filename: str) -> None:
        """Elimina el archivo temporal de forma segura."""
        try:
            if os.path.exists(filename):
                os.remove(filename)
                logger.info(f"Archivo temporal eliminado: {filename}")
        except Exception as e:
            logger.warning(f"No se pudo eliminar archivo temporal {filename}: {str(e)}")
