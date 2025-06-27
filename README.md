# DocToPDF Manager

**Conversión Profesional de Documentos Word a PDF**

Una aplicación de escritorio moderna y elegante para convertir documentos Word (.docx) a PDF manteniendo el formato original, imágenes y estilos.

## ✨ Características

- **🎯 Interfaz Moderna**: Diseño profesional con arrastrar y soltar
- **🔄 Múltiples Métodos**: Prioriza calidad usando Word, LibreOffice o fallback
- **📄 Mantiene Formato**: Conserva imágenes, estilos y estructura original
- **🚀 Procesamiento Asíncrono**: No bloquea la interfaz durante conversión
- **⚡ Auto-limpieza**: Limpia selección después de conversión exitosa
- **📁 División Automática**: Separa páginas y renombra automáticamente

## 🛠️ Métodos de Conversión

### 1. **Microsoft Word** (Prioridad Máxima)
- ✅ Mantiene **formato completo**
- ✅ Conserva **imágenes y gráficos**
- ✅ Preserva **estilos y tablas**
- ✅ **Calidad profesional**

### 2. **LibreOffice** (Segunda Prioridad)
- ✅ Mantiene **formato e imágenes**
- ✅ Alternativa gratuita a Word
- ✅ **Buena calidad**

### 3. **docx2txt + ReportLab** (Fallback)
- ⚠️ **Solo texto plano**
- ❌ Se pierden imágenes y formato
- ✅ Siempre disponible

## 📋 Requisitos

### Dependencias Python
```bash
pip install -r config/requirements.txt
```

### Software Recomendado
- **Microsoft Word** (óptimo) O
- **LibreOffice** (alternativa gratuita)

## 🚀 Instalación

1. **Clonar el repositorio**
```bash
git clone <repositorio>
cd DocToPDF-Manager
```

2. **Instalar dependencias**
```bash
pip install -r config/requirements.txt
```

3. **Ejecutar la aplicación**
```bash
python main.py
```

## 💼 Uso

1. **Iniciar la aplicación**
   ```bash
   python main.py
   ```

2. **Seleccionar archivo**
   - Arrastra un archivo .docx al área designada, O
   - Haz clic en "Seleccionar Archivo"

3. **Iniciar conversión**
   - Clic en "Iniciar Conversión"
   - La aplicación automáticamente:
     - Convierte el Word a PDF
     - Divide en páginas individuales
     - Renombra con datos del documento

4. **Archivo procesado**
   - La selección se limpia automáticamente
   - Listo para procesar el siguiente documento

## 📁 Estructura del Proyecto

```
DocToPDF-Manager/
├── main.py                     # Punto de entrada principal
├── install_dependencies.bat    # Script de instalación Windows
├── config/                     # Archivos de configuración
│   └── requirements.txt        # Dependencias Python
├── resources/                  # Recursos de la aplicación
│   └── pdf.ico                 # Icono de la aplicación
├── logs/                       # Archivos de log (generados automáticamente)
│   ├── document_converter.log  # Log principal de la aplicación
│   └── README.md               # Documentación del sistema de logs
├── formatos/                   # Archivos de ejemplo
└── src/                        # Código fuente
    ├── models/                 # Lógica de negocio
    │   ├── document_converter.py
    │   ├── document_processing_model.py
    │   ├── pdf_processor.py
    │   └── exceptions.py
    ├── views/                  # Interfaz de usuario
    │   └── main_view.py
    ├── presenters/            # Lógica de presentación
    │   └── main_presenter.py
    └── utils/                 # Utilidades
        ├── file_utils.py
        └── styles.py
```

## 🎨 Características Técnicas

- **Arquitectura**: Patrón MVP (Model-View-Presenter)
- **Interfaz**: PyQt5 con diseño moderno y gradientes
- **Threading**: Procesamiento asíncrono con QThread
- **COM Integration**: API nativa de Microsoft Word
- **Error Handling**: Manejo robusto de errores y fallbacks
- **Auto-cleanup**: Limpieza automática de recursos COM

## 🔧 Configuración Avanzada

### Método de Conversión
La aplicación automáticamente detecta y prioriza:
1. Microsoft Word (mejor calidad)
2. LibreOffice (buena alternativa)
3. docx2txt (fallback básico)

### Mensajes Informativos
- ✅ **Verde**: Conversión con formato completo
- ⚠️ **Amarillo**: Advertencia de calidad reducida
- ❌ **Rojo**: Error en la conversión

## 📝 Notas

- **Formato óptimo**: Para mejores resultados instala Microsoft Word
- **Alternativa gratuita**: LibreOffice mantiene buena calidad
- **Fallback**: docx2txt solo conserva texto plano
- **Archivos grandes**: El procesamiento puede tomar varios minutos
- **Permisos**: Asegúrate de tener permisos de escritura en la carpeta

## � Depuración y Logs

### Sistema de Logs Profesional
La aplicación mantiene logs detallados para facilitar la depuración:

- **Ubicación**: `logs/document_converter.log`
- **Rotación automática**: Máximo 5MB por archivo, mantiene 5 versiones
- **Niveles**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Contenido**: Eventos de conversión, errores, información de depuración

### Diagnóstico de Problemas
Si experimentas problemas:
1. Revisa `logs/document_converter.log` para ver el último error
2. Busca mensajes de nivel `ERROR` o `CRITICAL`
3. Los logs incluyen la línea de código exacta del problema

## �🔄 Actualizaciones Recientes

- ✅ **Sistema de logging profesional** con rotación automática
- ✅ **Organización mejorada** de archivos en carpetas dedicadas
- ✅ Corrección de argumentos en ExportAsFixedFormat
- ✅ Auto-limpieza después de conversión exitosa
- ✅ Mejoras en el layout y espaciado de botones
- ✅ Manejo robusto de errores COM
- ✅ Optimización de la interfaz de usuario

## 📞 Soporte

Para reportar problemas o sugerencias:
1. **Revisa los logs**: Consulta `logs/document_converter.log` para información detallada
2. **Verifica requisitos**: 
   - Microsoft Word o LibreOffice instalados
   - Archivo no abierto en otra aplicación
   - Permisos de escritura en la carpeta
   - Dependencias correctamente instaladas
3. **Proporciona logs**: Incluye el contenido del log al reportar problemas

---

**DocToPDF Manager** - Conversión profesional de documentos con calidad garantizada.
