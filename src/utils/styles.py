"""
Estilos y recursos adicionales para la aplicación PyQt5.
"""

"""
Estilos y recursos adicionales para la aplicación PyQt5.
Diseño moderno con gradientes y efectos visuales profesionales.
"""

# Paleta de colores moderna y profesional
COLORS = {
    # Colores principales (gradientes púrpura-azul)
    'primary': '#667eea',
    'primary_dark': '#764ba2',
    'primary_light': '#a855f7',
    
    # Colores secundarios (gradientes verde)
    'secondary': '#48bb78',
    'secondary_dark': '#38a169',
    'secondary_light': '#68d391',
    
    # Colores de estado
    'accent': '#ed8936',
    'error': '#f56565',
    'warning': '#ed8936',
    'info': '#667eea',
    'success': '#48bb78',
    
    # Colores de fondo y superficie
    'background': '#f8fafc',
    'background_gradient_start': '#f8fafc',
    'background_gradient_end': '#e2e8f0',
    'surface': '#ffffff',
    'surface_elevated': '#ffffff',
    
    # Colores de texto
    'text_primary': '#2d3748',
    'text_secondary': '#4a5568',
    'text_muted': '#718096',
    'text_white': '#ffffff',
    
    # Colores de borde y división
    'border': '#e2e8f0',
    'border_focus': '#667eea',
    'divider': '#cbd5e0'
}

# Estilo principal de la aplicación con gradientes modernos
MAIN_STYLE = f"""
QMainWindow {{
    background: qlineargradient(
        x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 {COLORS['background_gradient_start']},
        stop: 0.5 {COLORS['background_gradient_end']},
        stop: 1 #cbd5e0
    );
}}

QFrame {{
    background-color: {COLORS['surface']};
    border: 1px solid {COLORS['border']};
    border-radius: 16px;
}}

QLabel {{
    color: {COLORS['text_primary']};
    background: transparent;
}}

QProgressBar {{
    border: none;
    border-radius: 12px;
    text-align: center;
    font-weight: 600;
    font-size: 13px;
    min-height: 30px;
    background-color: {COLORS['background']};
    color: {COLORS['text_primary']};
}}

QProgressBar::chunk {{
    background: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 0,
        stop: 0 {COLORS['primary']},
        stop: 1 {COLORS['primary_dark']}
    );
    border-radius: 12px;
    margin: 2px;
}}

QMessageBox {{
    background-color: {COLORS['surface']};
    color: {COLORS['text_primary']};
    border-radius: 12px;
}}

QMessageBox QPushButton {{
    background: qlineargradient(
        x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 {COLORS['primary']},
        stop: 1 {COLORS['primary_dark']}
    );
    color: {COLORS['text_white']};
    border: none;
    padding: 12px 24px;
    border-radius: 8px;
    font-weight: 600;
    min-width: 120px;
    min-height: 35px;
}}

QMessageBox QPushButton:hover {{
    background: qlineargradient(
        x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 #5a67d8,
        stop: 1 #6b46c1
    );
}}
"""

# Estilo para botones primarios con gradientes
BUTTON_STYLE_PRIMARY = f"""
QPushButton {{
    background: qlineargradient(
        x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 {COLORS['primary']},
        stop: 1 {COLORS['primary_dark']}
    );
    color: {COLORS['text_white']};
    border: none;
    padding: 16px 32px;
    border-radius: 12px;
    font-size: 15px;
    font-weight: 600;
    min-width: 180px;
    min-height: 50px;
    letter-spacing: 0.5px;
}}

QPushButton:hover {{
    background: qlineargradient(
        x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 #5a67d8,
        stop: 1 #6b46c1
    );
    transform: translateY(-2px);
}}

QPushButton:pressed {{
    background: qlineargradient(
        x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 #4c51bf,
        stop: 1 #553c9a
    );
    transform: translateY(0px);
}}

QPushButton:disabled {{
    background: {COLORS['border']};
    color: {COLORS['text_muted']};
}}
"""

# Estilo para botones secundarios con gradientes verdes
BUTTON_STYLE_SECONDARY = f"""
QPushButton {{
    background: qlineargradient(
        x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 {COLORS['secondary']},
        stop: 1 {COLORS['secondary_dark']}
    );
    color: {COLORS['text_white']};
    border: none;
    padding: 16px 32px;
    border-radius: 12px;
    font-size: 15px;
    font-weight: 600;
    min-width: 180px;
    min-height: 50px;
    letter-spacing: 0.5px;
}}

QPushButton:hover {{
    background: qlineargradient(
        x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 {COLORS['secondary_dark']},
        stop: 1 #2f855a
    );
    transform: translateY(-2px);
}}

QPushButton:pressed {{
    background: qlineargradient(
        x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 #2f855a,
        stop: 1 #276749
    );
    transform: translateY(0px);
}}

QPushButton:disabled {{
    background: {COLORS['border']};
    color: {COLORS['text_muted']};
}}
"""

# Función para obtener los colores
def get_colors():
    """Retorna el diccionario de colores."""
    return COLORS

# Función para aplicar tema oscuro (opcional)
def get_dark_theme():
    """Retorna estilos para tema oscuro."""
    dark_colors = COLORS.copy()
    dark_colors.update({
        'background': '#1a202c',
        'surface': '#2d3748',
        'text_primary': '#f7fafc',
        'text_secondary': '#e2e8f0',
        'border': '#4a5568'
    })
    return dark_colors
