"""
Archivo principal para iniciar la aplicación de conversión de documentos.
Punto de entrada principal que sigue el patrón MVP con PyQt5.
"""

import sys
import os
from PyQt5.QtWidgets import QApplication

# Agregar el directorio src al path para las importaciones
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.presenters import MainPresenter
from src.utils import setup_logging, get_logger, get_app_icon


def main():
    """Función principal de la aplicación."""
    try:
        # Configurar logging
        setup_logging()
        logger = get_logger("main")
        logger.info("Iniciando DocToPDF Manager...")
        
        # Crear aplicación Qt
        app = QApplication(sys.argv)
        
        # Configurar icono de la aplicación
        icon_path = get_app_icon()
        if icon_path:
            from PyQt5.QtGui import QIcon
            app.setWindowIcon(QIcon(icon_path))
            logger.info(f"Icono de aplicación configurado globalmente: {icon_path}")
        
        # Configurar estilo de la aplicación
        app.setStyle('Fusion')  # Estilo moderno
        
        # Crear y mostrar el presentador principal
        presenter = MainPresenter()
        presenter.run()
        logger.info("Aplicación mostrada exitosamente")
        
        # Ejecutar la aplicación
        exit_code = app.exec_()
        logger.info(f"Aplicación cerrada con código: {exit_code}")
        return exit_code
        
    except KeyboardInterrupt:
        logger = get_logger("main")
        logger.info("Aplicación interrumpida por el usuario")
        return 0
    except Exception as e:
        logger = get_logger("main")
        logger.critical(f"Error inesperado: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
