"""
Utilidades y funciones auxiliares para la aplicación.
"""

import os
import logging
import logging.handlers
from typing import Optional
from datetime import datetime


def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """
    Configura el sistema de logging de la aplicación con rotación automática.
    
    Args:
        log_level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Returns:
        Logger configurado para la aplicación
    """
    # Crear directorio de logs si no existe
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Configurar el logger principal
    logger = logging.getLogger("DocToPDF-Manager")
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Evitar duplicar handlers si ya están configurados
    if not logger.handlers:
        # Formato detallado para logs
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
        )
        
        # Handler para archivo con rotación (máximo 5MB, mantener 5 archivos)
        log_file = os.path.join(log_dir, "document_converter.log")
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, 
            maxBytes=5*1024*1024,  # 5MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        
        # Handler para consola (más simple)
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        
        # Solo mostrar WARNING y superiores en consola
        console_handler.setLevel(logging.WARNING)
        
        # Agregar handlers
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        # Log inicial
        logger.info(f"=== DocToPDF Manager iniciado - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
    
    return logger


def get_logger(name: str = None) -> logging.Logger:
    """
    Obtiene un logger para un módulo específico.
    
    Args:
        name: Nombre del módulo (opcional)
        
    Returns:
        Logger configurado
    """
    if name:
        return logging.getLogger(f"DocToPDF-Manager.{name}")
    return logging.getLogger("DocToPDF-Manager")


def validate_file_extension(file_path: str, expected_extension: str) -> bool:
    """
    Valida que un archivo tenga la extensión esperada.
    
    Args:
        file_path: Ruta del archivo a validar
        expected_extension: Extensión esperada (ej: '.docx')
        
    Returns:
        True si la extensión es correcta, False en caso contrario
    """
    if not file_path:
        return False
    
    _, extension = os.path.splitext(file_path.lower())
    return extension == expected_extension.lower()


def create_output_directory(base_path: str, directory_name: str) -> str:
    """
    Crea un directorio de salida si no existe.
    
    Args:
        base_path: Ruta base donde crear el directorio
        directory_name: Nombre del directorio a crear
        
    Returns:
        Ruta completa del directorio creado
    """
    output_path = os.path.join(base_path, directory_name)
    os.makedirs(output_path, exist_ok=True)
    return output_path


def safe_file_removal(file_path: str) -> bool:
    """
    Elimina un archivo de forma segura.
    
    Args:
        file_path: Ruta del archivo a eliminar
        
    Returns:
        True si se eliminó correctamente, False en caso contrario
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception as e:
        logger = get_logger("file_utils")
        logger.warning(f"No se pudo eliminar el archivo {file_path}: {str(e)}")
        return False


def get_file_size_mb(file_path: str) -> Optional[float]:
    """
    Obtiene el tamaño de un archivo en megabytes.
    
    Args:
        file_path: Ruta del archivo
        
    Returns:
        Tamaño en MB o None si hay error
    """
    try:
        if os.path.exists(file_path):
            size_bytes = os.path.getsize(file_path)
            return size_bytes / (1024 * 1024)
        return None
    except Exception as e:
        logger = get_logger("file_utils")
        logger.warning(f"No se pudo obtener el tamaño del archivo {file_path}: {str(e)}")
        return None
