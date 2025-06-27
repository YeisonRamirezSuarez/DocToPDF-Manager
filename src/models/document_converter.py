"""
Modelo para la conversión de documentos Word a PDF.
Contiene la lógica de negocio para la conversión y procesamiento de documentos.
Implementa múltiples métodos de conversión para máxima compatibilidad.
"""

import os
import subprocess
import sys
from typing import Optional, Tuple
from .exceptions import DocumentConversionError, FileNotFoundError
from src.utils import get_logger

logger = get_logger("document_converter")


class DocumentConverter:
    """Clase responsable de convertir documentos Word a PDF con múltiples métodos."""
    
    def __init__(self):
        self._conversion_method = None
        self._check_available_methods()
    
    def _check_available_methods(self) -> None:
        """Verifica qué métodos de conversión están disponibles."""
        # Método 1: Comprobar si Microsoft Word está disponible (PRIORIDAD MÁXIMA - mantiene formato e imágenes)
        try:
            import comtypes.client
            import comtypes
            import pythoncom
            
            # Test rápido de Word con timeout
            pythoncom.CoInitialize()
            try:
                # Intentar crear Word con timeout implícito
                word_app = comtypes.client.CreateObject('Word.Application')
                word_app.Visible = False
                word_app.Quit()
                pythoncom.CoUninitialize()
                
                self._conversion_method = "word"
                logger.info("Usando método de conversión: Microsoft Word (mantiene formato e imágenes)")
                return
            except:
                pythoncom.CoUninitialize()
                raise
        except Exception as e:
            logger.warning(f"Word no disponible: {str(e)[:100]}...")
        
        # Método 2: Comprobar si LibreOffice está disponible (SEGUNDA PRIORIDAD - mantiene formato e imágenes)
        try:
            subprocess.run(['soffice', '--version'], 
                         capture_output=True, check=True, timeout=5)
            self._conversion_method = "libreoffice"
            logger.info("Usando método de conversión: LibreOffice (mantiene formato e imágenes)")
            return
        except Exception as e:
            logger.warning(f"LibreOffice no disponible: {str(e)[:50]}...")
        
        # Método 3: Comprobar si docx2txt está disponible (TERCERA PRIORIDAD - solo texto plano)
        try:
            import docx2txt
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            self._conversion_method = "docx2txt"
            logger.warning("Usando método de conversión: docx2txt + reportlab (SOLO TEXTO PLANO, SIN FORMATO NI IMÁGENES)")
            return
        except ImportError as e:
            logger.error(f"docx2txt no disponible: {str(e)[:50]}...")
        
        # Si no hay métodos disponibles, usar el método básico
        self._conversion_method = "basic"
        print("⚠️ Usando método de conversión: básico (fallback - texto plano)")
        print("   Recomendación: Instale Microsoft Word o LibreOffice para mejor calidad")
    
    def convert_word_to_pdf(self, docx_filename: str, output_pdf_filename: str) -> None:
        """
        Convierte un documento de Word a PDF usando el mejor método disponible.
        
        Args:
            docx_filename: Ruta del archivo Word
            output_pdf_filename: Ruta del archivo PDF de salida
            
        Raises:
            DocumentConversionError: Si hay un error durante la conversión
            FileNotFoundError: Si el archivo Word no existe
        """
        try:
            # Obtener rutas absolutas
            docx_filename = os.path.abspath(docx_filename)
            output_pdf_filename = os.path.abspath(output_pdf_filename)
            
            # Verificar si el archivo de Word existe
            if not os.path.exists(docx_filename):
                raise FileNotFoundError(f"El archivo de Word no existe: {docx_filename}")
            
            # Crear directorio de salida si no existe
            os.makedirs(os.path.dirname(output_pdf_filename), exist_ok=True)
            
            # Usar el método de conversión disponible
            if self._conversion_method == "word":
                self._convert_with_word(docx_filename, output_pdf_filename)
            elif self._conversion_method == "libreoffice":
                self._convert_with_libreoffice(docx_filename, output_pdf_filename)
            elif self._conversion_method == "docx2txt":
                self._convert_with_docx2txt(docx_filename, output_pdf_filename)
            else:
                self._convert_basic(docx_filename, output_pdf_filename)
            
            # Verificar que el PDF fue creado
            if not os.path.exists(output_pdf_filename):
                raise DocumentConversionError("No se pudo generar el archivo PDF.")
                
        except Exception as e:
            if isinstance(e, (DocumentConversionError, FileNotFoundError)):
                raise
            raise DocumentConversionError(f"Error al convertir documento: {str(e)}")
    
    def _convert_with_word(self, docx_filename: str, output_pdf_filename: str) -> None:
        """Convierte usando Microsoft Word (mantiene formato e imágenes)."""
        import comtypes.client
        import comtypes
        import pythoncom
        import os
        
        word_app = None
        doc = None
        
        try:
            # Inicializar COM en el thread actual
            pythoncom.CoInitialize()
            
            # Crear aplicación de Word
            word_app = comtypes.client.CreateObject('Word.Application')
            word_app.Visible = False
            word_app.DisplayAlerts = False
            
            # Convertir rutas a formato absoluto
            docx_filename = os.path.abspath(docx_filename)
            output_pdf_filename = os.path.abspath(output_pdf_filename)
            
            # Abrir el documento
            doc = word_app.Documents.Open(docx_filename, ReadOnly=True)
            
            # Exportar a PDF con configuración optimizada (7 argumentos exactos)
            doc.ExportAsFixedFormat(
                OutputFileName=output_pdf_filename,
                ExportFormat=17,  # wdExportFormatPDF
                OptimizeFor=0,    # wdExportOptimizeForMinimumSize
                BitmapMissingFonts=True,
                DocStructureTags=True,
                CreateBookmarks=0  # wdExportCreateNoBookmarks
            )
            
            print(f"Conversión exitosa usando Microsoft Word (con formato e imágenes): {output_pdf_filename}")
            
        finally:
            # Cerrar documento y aplicación de forma segura
            try:
                if doc:
                    doc.Close(SaveChanges=False)
            except:
                pass
                
            try:
                if word_app:
                    word_app.Quit()
            except:
                pass
            
            # Limpiar COM
            try:
                pythoncom.CoUninitialize()
            except:
                pass
    
    def _convert_with_libreoffice(self, docx_filename: str, output_pdf_filename: str) -> None:
        """Convierte usando LibreOffice."""
        output_dir = os.path.dirname(output_pdf_filename)
        
        cmd = [
            'soffice',
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', output_dir,
            docx_filename
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            raise DocumentConversionError(f"LibreOffice falló: {result.stderr}")
        
        # LibreOffice genera el PDF con el mismo nombre base
        generated_pdf = os.path.join(output_dir, 
                                   os.path.splitext(os.path.basename(docx_filename))[0] + '.pdf')
        
        # Si el nombre es diferente, renombrar
        if generated_pdf != output_pdf_filename:
            os.rename(generated_pdf, output_pdf_filename)
    
    def _convert_with_docx2txt(self, docx_filename: str, output_pdf_filename: str) -> None:
        """Convierte usando docx2txt + reportlab (SOLO TEXTO PLANO - SIN FORMATO NI IMÁGENES)."""
        import docx2txt
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.utils import simpleSplit
        
        print("⚠️  ADVERTENCIA: Usando conversión básica que SOLO conserva texto plano")
        print("   Las imágenes, formato, tablas y estilos se perderán")
        print("   Para conservar formato instale Microsoft Word o LibreOffice")
        
        # Extraer texto del documento Word
        text = docx2txt.process(docx_filename)
        
        if not text.strip():
            raise DocumentConversionError("No se pudo extraer texto del documento Word.")
        
        # Crear PDF usando reportlab
        c = canvas.Canvas(output_pdf_filename, pagesize=letter)
        width, height = letter
        
        # Configurar fuente y tamaño
        c.setFont("Helvetica", 12)
        
        # Dividir texto en líneas
        lines = text.split('\n')
        y_position = height - 50  # Empezar desde arriba
        
        for line in lines:
            if not line.strip():
                y_position -= 15  # Línea vacía
                continue
            
            # Dividir líneas largas
            wrapped_lines = simpleSplit(line, "Helvetica", 12, width - 100)
            
            for wrapped_line in wrapped_lines:
                if y_position < 50:  # Nueva página si no hay espacio
                    c.showPage()
                    c.setFont("Helvetica", 12)
                    y_position = height - 50
                
                c.drawString(50, y_position, wrapped_line)
                y_position -= 15
        
        c.save()
    
    def _convert_basic(self, docx_filename: str, output_pdf_filename: str) -> None:
        """Método básico de conversión como fallback."""
        # Este método crea un PDF básico indicando que se necesita conversión manual
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        c = canvas.Canvas(output_pdf_filename, pagesize=letter)
        width, height = letter
        
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 100, "DocToPDF Manager")
        
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 150, "Conversión automática no disponible")
        c.drawString(50, height - 180, f"Archivo original: {os.path.basename(docx_filename)}")
        c.drawString(50, height - 210, "")
        c.drawString(50, height - 240, "Para convertir este documento, necesitas:")
        c.drawString(70, height - 270, "• Microsoft Word instalado, o")
        c.drawString(70, height - 300, "• LibreOffice instalado")
        c.drawString(50, height - 340, "Alternativamente, puedes instalar las dependencias:")
        c.drawString(70, height - 370, "pip install docx2txt reportlab")
        
        c.save()
        
        raise DocumentConversionError(
            "No se encontró un método de conversión disponible.\n"
            "Instala Microsoft Word, LibreOffice, o las dependencias de Python:\n"
            "pip install docx2txt reportlab"
        )
