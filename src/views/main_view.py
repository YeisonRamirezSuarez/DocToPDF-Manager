"""
Vista principal de la aplicación usando PyQt5.
Implementa una interfaz moderna y profesional según el patrón MVP.
"""

import sys
import os
from typing import Callable, Optional
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QProgressBar, QMessageBox,
    QFrame, QSizePolicy, QSpacerItem, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve, QUrl
from PyQt5.QtGui import QFont, QPixmap, QIcon, QPalette, QColor, QLinearGradient, QDragEnterEvent, QDropEvent
from src.utils import get_logger

logger = get_logger("main_view")


class ModernButton(QPushButton):
    """Botón personalizado con estilo moderno y efectos de animación."""
    
    def __init__(self, text: str, primary: bool = False, icon: str = ""):
        super().__init__(text)
        self.primary = primary
        self.icon_text = icon
        self.setup_style()
        self.setup_shadow()
    
    def setup_style(self):
        """Configura el estilo del botón con gradientes y sombras."""
        if self.primary:
            style = """
                QPushButton {
                    background: qlineargradient(
                        x1: 0, y1: 0, x2: 0, y2: 1,
                        stop: 0 #667eea,
                        stop: 1 #764ba2
                    );
                    color: white;
                    border: none;
                    padding: 12px 24px;
                    border-radius: 10px;
                    font-size: 13px;
                    font-weight: 600;
                    min-width: 150px;
                    min-height: 40px;
                    letter-spacing: 0.3px;
                }
                QPushButton:hover {
                    background: qlineargradient(
                        x1: 0, y1: 0, x2: 0, y2: 1,
                        stop: 0 #5a67d8,
                        stop: 1 #6b46c1
                    );
                }
                QPushButton:pressed {
                    background: qlineargradient(
                        x1: 0, y1: 0, x2: 0, y2: 1,
                        stop: 0 #4c51bf,
                        stop: 1 #553c9a
                    );
                }
                QPushButton:disabled {
                    background: #e2e8f0;
                    color: #a0aec0;
                }
            """
        else:
            style = """
                QPushButton {
                    background: qlineargradient(
                        x1: 0, y1: 0, x2: 0, y2: 1,
                        stop: 0 #48bb78,
                        stop: 1 #38a169
                    );
                    color: white;
                    border: none;
                    padding: 12px 24px;
                    border-radius: 10px;
                    font-size: 13px;
                    font-weight: 600;
                    min-width: 150px;
                    min-height: 40px;
                    letter-spacing: 0.3px;
                }
                QPushButton:hover {
                    background: qlineargradient(
                        x1: 0, y1: 0, x2: 0, y2: 1,
                        stop: 0 #38a169,
                        stop: 1 #2f855a
                    );
                }
                QPushButton:pressed {
                    background: qlineargradient(
                        x1: 0, y1: 0, x2: 0, y2: 1,
                        stop: 0 #2f855a,
                        stop: 1 #276749
                    );
                }
                QPushButton:disabled {
                    background: #e2e8f0;
                    color: #a0aec0;
                }
            """
        self.setStyleSheet(style)
    
    def setup_shadow(self):
        """Agrega efecto de sombra al botón."""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.setGraphicsEffect(shadow)


class ModernProgressBar(QProgressBar):
    """Barra de progreso personalizada con estilo moderno y animaciones."""
    
    def __init__(self):
        super().__init__()
        self.setup_style()
        self.setup_shadow()
    
    def setup_style(self):
        """Configura el estilo de la barra de progreso con gradientes."""
        style = """
            QProgressBar {
                border: none;
                border-radius: 10px;
                text-align: center;
                font-weight: 600;
                font-size: 12px;
                min-height: 25px;
                background-color: #f7fafc;
                color: #2d3748;
            }
            QProgressBar::chunk {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #667eea,
                    stop: 1 #764ba2
                );
                border-radius: 10px;
                margin: 2px;
            }
        """
        self.setStyleSheet(style)
    
    def setup_shadow(self):
        """Agrega efecto de sombra a la barra de progreso."""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, 40))
        self.setGraphicsEffect(shadow)


class DropArea(QLabel):
    """Área personalizada para arrastrar y soltar archivos."""
    
    file_dropped = pyqtSignal(str)
    
    def __init__(self, text: str):
        super().__init__(text)
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignCenter)
        self.setWordWrap(True)
        self.default_style = """
            QLabel {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #f8fafc,
                    stop: 1 #e2e8f0
                );
                border: 2px dashed #cbd5e0;
                border-radius: 12px;
                padding: 15px;
                margin: 8px 0;
                color: #718096;
                min-height: 50px;
                font-weight: 500;
            }
        """
        self.hover_style = """
            QLabel {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #e6fffa,
                    stop: 1 #b2f5ea
                );
                border: 2px dashed #38a169;
                border-radius: 12px;
                padding: 15px;
                margin: 8px 0;
                color: #276749;
                min-height: 50px;
                font-weight: 600;
            }
        """
        self.setStyleSheet(self.default_style)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Maneja el evento cuando un archivo es arrastrado sobre el área."""
        try:
            if event.mimeData().hasUrls():
                urls = event.mimeData().urls()
                if len(urls) == 1:
                    file_path = urls[0].toLocalFile()
                    if file_path.lower().endswith('.docx'):
                        self.setStyleSheet(self.hover_style)
                        self.setText("📥  ¡Suelta aquí tu archivo!\nPerfecto, es un archivo .docx")
                        event.acceptProposedAction()
                    else:
                        self.setText("❌  Solo archivos .docx\nEste tipo de archivo no es compatible")
                        event.ignore()
                else:
                    self.setText("❌  Solo un archivo a la vez\nPor favor selecciona un solo archivo")
                    event.ignore()
            else:
                event.ignore()
        except Exception as e:
            logger.error(f"Error en dragEnterEvent: {e}")
            event.ignore()
    
    def dragLeaveEvent(self, event):
        """Maneja el evento cuando el archivo sale del área."""
        try:
            self.setStyleSheet(self.default_style)
            self.setText("🎯  Arrastra tu archivo aquí\no haz clic en 'Seleccionar Archivo'")
        except Exception as e:
            logger.error(f"Error en dragLeaveEvent: {e}")
    
    def dropEvent(self, event: QDropEvent):
        """Maneja el evento cuando un archivo es soltado en el área."""
        try:
            if event.mimeData().hasUrls():
                urls = event.mimeData().urls()
                if len(urls) == 1:
                    file_path = urls[0].toLocalFile()
                    if file_path.lower().endswith('.docx'):
                        self.file_dropped.emit(file_path)
                        event.acceptProposedAction()
                    else:
                        event.ignore()
                else:
                    event.ignore()
            else:
                event.ignore()
            
            # Restaurar estilo original
            self.setStyleSheet(self.default_style)
        except Exception as e:
            logger.error(f"Error en dropEvent: {e}")
            event.ignore()
            # Intentar restaurar el estilo por si acaso
            try:
                self.setStyleSheet(self.default_style)
            except:
                pass


class MainView(QMainWindow):
    """Vista principal de la aplicación con PyQt5."""
    
    def __init__(self):
        super().__init__()
        
        # Callbacks que serán asignados por el Presenter
        self.on_file_select: Optional[Callable[[str], None]] = None
        self.on_convert_start: Optional[Callable[[], None]] = None
        self.on_close: Optional[Callable[[], None]] = None
        
        # Widgets principales
        self.central_widget: Optional[QWidget] = None
        self.select_button: Optional[ModernButton] = None
        self.convert_button: Optional[ModernButton] = None
        self.progress_bar: Optional[ModernProgressBar] = None
        self.progress_label: Optional[QLabel] = None
        self.file_label: Optional[DropArea] = None
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Configura la interfaz de usuario."""
        self._setup_window()
        self._create_widgets()
        self._arrange_widgets()
        self._apply_modern_theme()
    
    def _setup_window(self) -> None:
        """Configura la ventana principal con diseño profesional."""
        self.setWindowTitle("DocToPDF Manager • Conversión Profesional de Documentos")
        self.setFixedSize(650, 620)
        self._center_window()
        
        # Configurar icono si existe
        try:
            icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'resources', 'pdf.ico')
            if os.path.exists(icon_path):
                self.setWindowIcon(QIcon(icon_path))
        except:
            pass
        
        # Aplicar estilo de ventana con gradiente
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #f8fafc,
                    stop: 0.5 #e2e8f0,
                    stop: 1 #cbd5e0
                );
            }
        """)
    
    def _center_window(self) -> None:
        """Centra la ventana en la pantalla."""
        from PyQt5.QtWidgets import QDesktopWidget
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )
    
    def _create_widgets(self) -> None:
        """Crea todos los widgets de la interfaz con diseño profesional."""
        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Header con logo y título
        self.header_frame = QFrame()
        self.header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #667eea,
                    stop: 1 #764ba2
                );
                border: none;
                border-radius: 15px;
                margin: 8px;
                min-height: 90px;
                max-height: 90px;
            }
        """)
        
        # Sombra para el header
        header_shadow = QGraphicsDropShadowEffect()
        header_shadow.setBlurRadius(15)
        header_shadow.setXOffset(0)
        header_shadow.setYOffset(6)
        header_shadow.setColor(QColor(0, 0, 0, 30))
        self.header_frame.setGraphicsEffect(header_shadow)
        
        # Título principal con estilo elegante
        self.title_label = QLabel("DocToPDF Manager")
        self.title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont("Segoe UI", 22, QFont.Bold)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet("""
            color: white; 
            margin: 10px 0 5px 0;
            background: transparent;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        """)
        
        # Subtítulo elegante
        self.subtitle_label = QLabel("Conversión profesional de Word a PDF • Rápido y confiable")
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_font = QFont("Segoe UI", 11, QFont.Normal)
        self.subtitle_label.setFont(subtitle_font)
        self.subtitle_label.setStyleSheet("""
            color: rgba(255, 255, 255, 0.9); 
            margin-bottom: 10px;
            background: transparent;
            font-style: italic;
        """)
        
        # Marco principal para el contenido
        self.content_frame = QFrame()
        self.content_frame.setFrameStyle(QFrame.NoFrame)
        self.content_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: none;
                border-radius: 15px;
                padding: 25px;
                margin: 8px;
            }
        """)
        
        # Sombra para el contenido principal
        content_shadow = QGraphicsDropShadowEffect()
        content_shadow.setBlurRadius(20)
        content_shadow.setXOffset(0)
        content_shadow.setYOffset(8)
        content_shadow.setColor(QColor(0, 0, 0, 15))
        self.content_frame.setGraphicsEffect(content_shadow)
        
        # Sección de instrucciones con icono
        self.instruction_label = QLabel("📄  Selecciona un archivo Word (.docx)\npara comenzar la conversión")
        self.instruction_label.setAlignment(Qt.AlignCenter)
        instruction_font = QFont("Segoe UI", 13, QFont.Normal)
        self.instruction_label.setFont(instruction_font)
        self.instruction_label.setStyleSheet("""
            color: #4a5568; 
            margin: 10px 0 15px 0;
            background: transparent;
            font-weight: 500;
            line-height: 1.4;
        """)
        
        # Área de archivo con diseño de drop zone
        self.file_label = DropArea("🎯  Arrastra tu archivo aquí\no haz clic en 'Seleccionar Archivo'")
        file_font = QFont("Segoe UI", 11)
        self.file_label.setFont(file_font)
        
        # Botones con nuevos estilos
        self.select_button = ModernButton("📁  Seleccionar Archivo", primary=False)
        self.convert_button = ModernButton("🚀  Iniciar Conversión", primary=True)
        
        # Configurar callbacks
        self.select_button.clicked.connect(self._handle_file_selection)
        self.convert_button.clicked.connect(self._handle_conversion_start)
        self.file_label.file_dropped.connect(self._handle_file_dropped)
        
        # Elementos de progreso con mejor diseño
        self.progress_label = QLabel("⚡  Procesando documento...")
        self.progress_label.setAlignment(Qt.AlignCenter)
        progress_font = QFont("Segoe UI", 12, QFont.Bold)
        self.progress_label.setFont(progress_font)
        self.progress_label.setStyleSheet("""
            color: #667eea; 
            margin: 15px 0 10px 0;
            background: transparent;
        """)
        self.progress_label.hide()
        
        self.progress_bar = ModernProgressBar()
        self.progress_bar.setRange(0, 0)  # Modo indeterminado
        self.progress_bar.hide()
        
        # Etiqueta de estado con mejor diseño
        self.status_label = QLabel("✨  Todo listo para convertir tus documentos")
        self.status_label.setAlignment(Qt.AlignCenter)
        status_font = QFont("Segoe UI", 11, QFont.Medium)
        self.status_label.setFont(status_font)
        self.status_label.setStyleSheet("""
            color: #48bb78; 
            margin-top: 15px;
            background: transparent;
            font-weight: 500;
        """)
    
    def _arrange_widgets(self) -> None:
        """Organiza los widgets en layouts con mejor espaciado."""
        # Layout principal
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Layout del header
        header_layout = QVBoxLayout(self.header_frame)
        header_layout.setContentsMargins(20, 15, 20, 15)
        header_layout.addWidget(self.title_label)
        header_layout.addWidget(self.subtitle_label)
        
        # Agregar header al layout principal
        main_layout.addWidget(self.header_frame)
        
        # Layout del contenido principal
        content_layout = QVBoxLayout(self.content_frame)
        content_layout.setSpacing(15)
        content_layout.setContentsMargins(30, 30, 30, 30)
        
        # Agregar widgets al contenido
        content_layout.addWidget(self.instruction_label)
        content_layout.addWidget(self.file_label)
        
        # Espacio mucho más grande entre file_label y botones para bajarlos considerablemente más
        content_layout.addItem(QSpacerItem(20, 160, QSizePolicy.Minimum, QSizePolicy.Fixed))
        
        # Layout para botones con mejor espaciado
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        button_layout.addWidget(self.select_button)
        button_layout.addWidget(self.convert_button)
        button_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        content_layout.addLayout(button_layout)
        
        # Espacio mayor entre botones y elementos de progreso para evitar superposición
        content_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed))
        
        # Elementos de progreso
        content_layout.addWidget(self.progress_label)
        content_layout.addWidget(self.progress_bar)
        
        # Agregar el marco de contenido al layout principal
        main_layout.addWidget(self.content_frame)
        main_layout.addWidget(self.status_label)
    
    def _apply_modern_theme(self) -> None:
        """Aplica un tema moderno con gradientes y sombras profesionales."""
        pass  # El tema ya se aplica en _setup_window()
    
    def _handle_file_selection(self) -> None:
        """Maneja la selección de archivo."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo Word",
            "",
            "Archivos Word (*.docx);;Todos los archivos (*.*)"
        )
        
        if file_path and self.on_file_select:
            self.on_file_select(file_path)
    
    def _handle_conversion_start(self) -> None:
        """Maneja el inicio de la conversión."""
        if self.on_convert_start:
            self.on_convert_start()
    
    def _handle_file_dropped(self, file_path: str) -> None:
        """Maneja el archivo arrastrado y soltado."""
        try:
            # Actualizar la interfaz
            self._update_file_display(file_path)
            
            # Notificar al presenter si el callback está configurado
            if self.on_file_select:
                self.on_file_select(file_path)
                
        except Exception as e:
            logger.error(f"Error en _handle_file_dropped: {e}")
            self._show_file_error()

    def _update_file_display(self, file_path: str) -> None:
        """Actualiza solo la visualización del archivo sin causar recursión."""
        try:
            filename = os.path.basename(file_path)
            # Si el nombre es muy largo, cortarlo y agregar "..."
            if len(filename) > 40:
                filename = filename[:37] + "..."
            
            self.file_label.setText(f"✅  {filename}")
            
            # Usar el estilo de éxito personalizado para DropArea
            self.file_label.setStyleSheet("""
                QLabel {
                    background: qlineargradient(
                        x1: 0, y1: 0, x2: 0, y2: 1,
                        stop: 0 #f0fff4,
                        stop: 1 #c6f6d5
                    );
                    border: 2px solid #48bb78;
                    border-radius: 12px;
                    padding: 15px;
                    margin: 8px 0;
                    color: #276749;
                    min-height: 50px;
                    font-weight: 600;
                }
            """)
            
            self.status_label.setText("📁  Archivo cargado correctamente • Listo para convertir")
            self.status_label.setStyleSheet("""
                color: #667eea; 
                margin-top: 15px;
                background: transparent;
                font-weight: 500;
            """)
            
        except Exception as e:
            logger.error(f"Error en _update_file_display: {e}")
            self._show_file_error()
    
    def _show_file_error(self) -> None:
        """Muestra un error en la interfaz de archivo."""
        try:
            self.status_label.setText("❌  Error al procesar el archivo")
            self.status_label.setStyleSheet("""
                color: #f56565; 
                margin-top: 15px;
                background: transparent;
                font-weight: 500;
            """)
        except Exception as e:
            logger.critical(f"Error crítico en _show_file_error: {e}")

    def update_selected_file(self, file_path: str) -> None:
        """Actualiza la etiqueta del archivo seleccionado con animación."""
        self._update_file_display(file_path)
    
    def clear_selected_file(self) -> None:
        """Limpia la selección de archivo y restaura el estado inicial."""
        try:
            # Restaurar el texto y estilo inicial del DropArea
            self.file_label.setText("🎯  Arrastra tu archivo aquí\no haz clic en 'Seleccionar Archivo'")
            self.file_label.setStyleSheet("""
                QLabel {
                    background: qlineargradient(
                        x1: 0, y1: 0, x2: 0, y2: 1,
                        stop: 0 #f7fafc,
                        stop: 1 #edf2f7
                    );
                    border: 2px dashed #a0aec0;
                    border-radius: 12px;
                    padding: 15px;
                    margin: 8px 0;
                    color: #4a5568;
                    min-height: 50px;
                    font-weight: 500;
                }
                QLabel:hover {
                    border-color: #667eea;
                    background: qlineargradient(
                        x1: 0, y1: 0, x2: 0, y2: 1,
                        stop: 0 #ffffff,
                        stop: 1 #f0f4ff
                    );
                }
            """)
            
            # Restaurar el mensaje de estado inicial
            self.status_label.setText("✨  Todo listo para convertir tus documentos")
            self.status_label.setStyleSheet("""
                color: #48bb78; 
                margin-top: 15px;
                background: transparent;
                font-weight: 500;
            """)
            
            logger.info("Archivo seleccionado limpiado, listo para nueva conversión")
            
        except Exception as e:
            logger.error(f"Error al limpiar archivo seleccionado: {e}")

    def show_loading(self) -> None:
        """Muestra el estado de carga con mejor diseño."""
        self.select_button.setEnabled(False)
        self.convert_button.setEnabled(False)
        self.progress_label.show()
        self.progress_bar.show()
        self.status_label.setText("⚡  Conversión en progreso • Por favor espera...")
        self.status_label.setStyleSheet("""
            color: #ed8936; 
            margin-top: 15px;
            background: transparent;
            font-weight: 500;
        """)
    
    def hide_loading(self) -> None:
        """Oculta el estado de carga y restaura la interfaz."""
        self.progress_label.hide()
        self.progress_bar.hide()
        self.select_button.setEnabled(True)
        self.convert_button.setEnabled(True)
        self.status_label.setText("✨  Todo listo para convertir tus documentos")
        self.status_label.setStyleSheet("""
            color: #48bb78; 
            margin-top: 15px;
            background: transparent;
            font-weight: 500;
        """)
    
    def show_success_message(self, message: str) -> None:
        """Muestra un mensaje de éxito con diseño moderno."""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("✅ ¡Conversión Exitosa!")
        msg_box.setText(message)
        msg_box.setStyleSheet("""
            QMessageBox {
                font-size: 14px;
                background-color: white;
                border-radius: 12px;
            }
            QMessageBox QPushButton {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #48bb78,
                    stop: 1 #38a169
                );
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: 600;
                min-width: 100px;
            }
            QMessageBox QPushButton:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #38a169,
                    stop: 1 #2f855a
                );
            }
        """)
        msg_box.exec_()
        self.status_label.setText("🎉  ¡Conversión completada exitosamente!")
        self.status_label.setStyleSheet("""
            color: #48bb78; 
            margin-top: 25px;
            background: transparent;
            font-weight: 500;
        """)
    
    def show_error_message(self, message: str) -> None:
        """Muestra un mensaje de error con diseño moderno."""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("❌ Error en la Conversión")
        msg_box.setText(message)
        msg_box.setStyleSheet("""
            QMessageBox {
                font-size: 14px;
                background-color: white;
                border-radius: 12px;
            }
            QMessageBox QPushButton {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #f56565,
                    stop: 1 #e53e3e
                );
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: 600;
                min-width: 100px;
            }
            QMessageBox QPushButton:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #e53e3e,
                    stop: 1 #c53030
                );
            }
        """)
        msg_box.exec_()
        self.status_label.setText("❌  Error durante la conversión")
        self.status_label.setStyleSheet("""
            color: #f56565; 
            margin-top: 25px;
            background: transparent;
            font-weight: 500;
        """)
    
    def show_warning_message(self, message: str) -> None:
        """Muestra un mensaje de advertencia con diseño moderno."""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("⚠️ Advertencia")
        msg_box.setText(message)
        msg_box.setStyleSheet("""
            QMessageBox {
                font-size: 14px;
                background-color: white;
                border-radius: 12px;
            }
            QMessageBox QPushButton {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #ed8936,
                    stop: 1 #dd6b20
                );
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: 600;
                min-width: 100px;
            }
            QMessageBox QPushButton:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #dd6b20,
                    stop: 1 #c05621
                );
            }
        """)
        msg_box.exec_()
    
    def show_info_message(self, message: str) -> None:
        """Muestra un mensaje informativo con diseño moderno."""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("ℹ️ Información")
        msg_box.setText(message)
        msg_box.setStyleSheet("""
            QMessageBox {
                font-size: 14px;
                background-color: white;
                border-radius: 12px;
            }
            QMessageBox QPushButton {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #667eea,
                    stop: 1 #764ba2
                );
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: 600;
                min-width: 100px;
            }
            QMessageBox QPushButton:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #5a67d8,
                    stop: 1 #6b46c1
                );
            }
        """)
        msg_box.exec_()
    
    def closeEvent(self, event):
        """Maneja el evento de cierre de la ventana."""
        # Notificar al presenter si hay un callback configurado
        if hasattr(self, 'on_close') and self.on_close:
            self.on_close()
        event.accept()
    
    def run(self) -> None:
        """Muestra la ventana."""
        self.show()
    
    def close(self) -> None:
        """Cierra la aplicación."""
        super().close()
