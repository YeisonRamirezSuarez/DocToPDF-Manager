"""
Presentador principal que coordina la vista y el modelo.
Implementa la lógica de presentación según el patrón MVP con PyQt5.
"""

import threading
from typing import Optional
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from ..models import DocumentProcessingModel, DocumentConversionError, PDFProcessingError
from ..views import MainView
from src.utils import get_logger

logger = get_logger("main_presenter")


class ConversionWorker(QObject):
    """Worker thread para manejar la conversión en segundo plano."""
    
    finished = pyqtSignal()
    error = pyqtSignal(str)
    success = pyqtSignal()
    
    def __init__(self, model: DocumentProcessingModel):
        super().__init__()
        self.model = model
    
    def process(self):
        """Procesa la conversión del documento."""
        try:
            self.model.process_document()
            self.success.emit()
        except (DocumentConversionError, PDFProcessingError) as e:
            self.error.emit(str(e))
        except Exception as e:
            self.error.emit(f"Error inesperado durante la conversión: {str(e)}")
        finally:
            self.finished.emit()


class MainPresenter(QObject):
    """Presentador principal que coordina la vista y el modelo."""
    
    def __init__(self):
        super().__init__()
        self.model = DocumentProcessingModel()
        self.view = MainView()
        self.worker_thread: Optional[QThread] = None
        self.worker: Optional[ConversionWorker] = None
        self._setup_view_callbacks()
    
    def _setup_view_callbacks(self) -> None:
        """Configura los callbacks de la vista."""
        self.view.on_file_select = self.handle_file_selection
        self.view.on_convert_start = self.handle_conversion_start
        self.view.on_close = self.shutdown
    
    def handle_file_selection(self, file_path: str) -> None:
        """
        Maneja la selección de un archivo.
        
        Args:
            file_path: Ruta del archivo seleccionado
        """
        if file_path:
            self.model.set_selected_file(file_path)
            self.view.update_selected_file(file_path)
            self.view.show_info_message("Archivo seleccionado correctamente.")
        else:
            self.view.show_warning_message("No se seleccionó ningún archivo.")
    
    def handle_conversion_start(self) -> None:
        """Maneja el inicio del proceso de conversión."""
        if not self.model.has_selected_file():
            self.view.show_error_message("No se ha seleccionado ningún archivo de Word.")
            return
        
        # Verificar método de conversión disponible
        try:
            converter = self.model.get_converter()
            method = converter._conversion_method
            
            # Mostrar información sobre el método que se usará
            if method == "word":
                self.view.show_info_message("Usando Microsoft Word - Se mantendrá formato e imágenes ✓")
            elif method == "libreoffice":
                self.view.show_info_message("Usando LibreOffice - Se mantendrá formato e imágenes ✓")
            elif method == "docx2txt":
                self.view.show_warning_message("⚠️ Conversión básica: Solo se conservará texto plano (sin formato ni imágenes)")
            else:
                self.view.show_warning_message("⚠️ Método de conversión limitado disponible")
        except:
            pass
        
        # Mostrar estado de carga
        self.view.show_loading()
        
        # Crear worker y thread
        self.worker = ConversionWorker(self.model)
        self.worker_thread = QThread()
        
        # Mover worker al thread
        self.worker.moveToThread(self.worker_thread)
        
        # Conectar señales
        self.worker_thread.started.connect(self.worker.process)
        self.worker.finished.connect(self.worker_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)
        self.worker_thread.finished.connect(lambda: setattr(self, 'worker_thread', None))
        self.worker_thread.finished.connect(lambda: setattr(self, 'worker', None))
        
        self.worker.success.connect(self._on_conversion_success)
        self.worker.error.connect(self._on_conversion_error)
        self.worker.finished.connect(self._on_conversion_finished)
        
        # Iniciar thread
        self.worker_thread.start()
    
    def _on_conversion_success(self) -> None:
        """Maneja el éxito de la conversión."""
        self.view.show_success_message(
            "🎉 ¡Conversión completada con éxito!\n\n"
            "Los archivos PDF individuales se han guardado en la carpeta correspondiente.\n"
            "Cada página ha sido renombrada automáticamente con el número de registro y nombre del estudiante."
        )
        # Limpiar el archivo seleccionado para evitar conversiones duplicadas
        self.model.clear_selected_file()
        self.view.clear_selected_file()
    
    def _on_conversion_error(self, error_message: str) -> None:
        """
        Maneja los errores de conversión.
        
        Args:
            error_message: Mensaje de error a mostrar
        """
        self.view.show_error_message(
            f"❌ Error durante la conversión:\n\n{error_message}\n\n"
            "Por favor, verifica que:\n"
            "• Microsoft Word esté instalado\n"
            "• El archivo no esté abierto en otra aplicación\n"
            "• Tengas permisos de escritura en la carpeta"
        )
    
    def _on_conversion_finished(self) -> None:
        """Limpia los recursos cuando termina la conversión."""
        self.view.hide_loading()
    
    def run(self) -> None:
        """Inicia la aplicación."""
        self.view.run()
    
    def shutdown(self) -> None:
        """Cierra la aplicación de forma limpia."""
        # Esperar a que termine el thread si está ejecutando
        if self.worker_thread and self.worker_thread.isRunning():
            self.worker_thread.quit()
            self.worker_thread.wait()
        
        self.view.close()
