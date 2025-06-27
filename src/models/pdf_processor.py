"""
Modelo para el procesamiento de archivos PDF.
Contiene la lógica para dividir PDFs y extraer información.
"""

import os
import re
import fitz
from typing import Optional, Tuple
from PyPDF2 import PdfReader, PdfWriter
from .exceptions import PDFProcessingError, FileNotFoundError
from src.utils import get_logger

logger = get_logger("pdf_processor")


class PDFProcessor:
    """Clase responsable del procesamiento de archivos PDF."""
    
    def extract_name_and_registration(self, pdf_filename: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Extrae el número de registro y nombre del estudiante de un PDF.
        
        Args:
            pdf_filename: Ruta del archivo PDF
            
        Returns:
            Tupla con (número_registro, nombre) o (None, None) si no se encuentra
            
        Raises:
            PDFProcessingError: Si hay un error procesando el PDF
        """
        try:
            # Abrir el archivo PDF con PyMuPDF
            doc = fitz.open(pdf_filename)
            
            # Extraer el texto de la primera página
            page = doc[0]
            text = page.get_text()
            doc.close()
            
            # Usar expresiones regulares para encontrar el "Registro No." y el nombre
            registration_number = self._extract_registration_number(text)
            name = self._extract_student_name(text)
            
            return registration_number, name
            
        except Exception as e:
            raise PDFProcessingError(f"Error al procesar PDF {pdf_filename}: {str(e)}")
    
    def _extract_registration_number(self, text: str) -> Optional[str]:
        """Extrae el número de registro del texto."""
        match = re.search(r"Registro No\.\s*(\d+)", text)
        return match.group(1) if match else None
    
    def _extract_student_name(self, text: str) -> Optional[str]:
        """Extrae el nombre del estudiante del texto."""
        match = re.search(r"HACE CONSTAR QUE:\s*(.*?)(\n|$)", text)
        return match.group(1).strip() if match else None
    
    def split_pdf_by_page(self, input_pdf_filename: str, output_folder: str) -> None:
        """
        Divide un PDF en páginas individuales y las renombra según el contenido.
        
        Args:
            input_pdf_filename: Ruta del archivo PDF a dividir
            output_folder: Carpeta donde guardar las páginas individuales
            
        Raises:
            PDFProcessingError: Si hay un error dividiendo el PDF
            FileNotFoundError: Si el archivo PDF no existe
        """
        try:
            if not os.path.exists(input_pdf_filename):
                raise FileNotFoundError(f"El archivo PDF {input_pdf_filename} no existe.")
            
            # Crear directorio de salida
            os.makedirs(output_folder, exist_ok=True)
            
            with open(input_pdf_filename, 'rb') as input_pdf_file:
                reader = PdfReader(input_pdf_file)
                num_pages = len(reader.pages)
                
                for page_num in range(num_pages):
                    self._process_single_page(reader, page_num, output_folder)
            
            # Eliminar el archivo PDF original
            self._cleanup_original_file(input_pdf_filename)
            
        except Exception as e:
            if isinstance(e, (PDFProcessingError, FileNotFoundError)):
                raise
            raise PDFProcessingError(f"Error al dividir PDF: {str(e)}")
    
    def _process_single_page(self, reader: PdfReader, page_num: int, output_folder: str) -> None:
        """Procesa una página individual del PDF."""
        writer = PdfWriter()
        writer.add_page(reader.pages[page_num])
        
        # Crear archivo temporal
        temp_pdf_filename = os.path.join(output_folder, f"temp_page_{page_num + 1}.pdf")
        
        with open(temp_pdf_filename, 'wb') as temp_pdf_file:
            writer.write(temp_pdf_file)
        
        # Renombrar según el contenido
        self._rename_pdf_file(temp_pdf_filename, output_folder, page_num)
    
    def _rename_pdf_file(self, temp_pdf_filename: str, output_folder: str, page_num: int) -> None:
        """Renombra el archivo PDF según su contenido."""
        registration_number, name = self.extract_name_and_registration(temp_pdf_filename)
        
        if registration_number and name:
            new_filename = f"{registration_number} - {name}.pdf"
            new_pdf_filename = os.path.join(output_folder, new_filename)
            os.rename(temp_pdf_filename, new_pdf_filename)
            logger.info(f"Página {page_num + 1} guardada como: {new_filename}")
        else:
            fallback_filename = os.path.join(output_folder, f"page_{page_num + 1}.pdf")
            os.rename(temp_pdf_filename, fallback_filename)
            logger.warning(f"Error al extraer datos de la página {page_num + 1}. Guardado como page_{page_num + 1}.pdf")
    
    def _cleanup_original_file(self, filename: str) -> None:
        """Elimina el archivo PDF original de forma segura."""
        try:
            if os.path.exists(filename):
                os.remove(filename)
                logger.info(f"Archivo PDF original eliminado: {filename}")
        except Exception as e:
            logger.warning(f"No se pudo eliminar el archivo {filename}: {str(e)}")
