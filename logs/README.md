# Sistema de Logs - DocToPDF Manager

Este directorio contiene los archivos de log generados automáticamente por la aplicación.

## Archivos de Log

### `document_converter.log`
- **Descripción**: Log principal de la aplicación que registra toda la actividad
- **Contenido**: 
  - Eventos de inicio y cierre de la aplicación
  - Procesos de conversión (método utilizado, éxito/fallo)
  - Errores y advertencias
  - Información de depuración
  - Logs de bibliotecas externas (comtypes, etc.)

### Rotación Automática
- **Tamaño máximo**: 5MB por archivo
- **Archivos mantenidos**: 5 versiones anteriores
- **Formato**: `document_converter.log.1`, `document_converter.log.2`, etc.

## Niveles de Log

| Nivel | Descripción | Mostrado en Consola |
|-------|-------------|-------------------|
| `DEBUG` | Información detallada para depuración | ❌ |
| `INFO` | Eventos normales de la aplicación | ❌ |
| `WARNING` | Advertencias que no impiden el funcionamiento | ✅ |
| `ERROR` | Errores que afectan funcionalidad específica | ✅ |
| `CRITICAL` | Errores graves que pueden cerrar la aplicación | ✅ |

## Configuración

El sistema de logging se configura automáticamente en `src/utils/file_utils.py`:
- Logs detallados se guardan en archivo
- Solo WARNING y superiores se muestran en consola
- Formato incluye timestamp, módulo, nivel y ubicación del código

## Limpieza

- **Automática**: Los logs se rotan automáticamente cuando alcanzan 5MB
- **Manual**: Puedes eliminar estos archivos de forma segura, se regenerarán automáticamente
- **Recomendación**: Conservar para diagnóstico de problemas

## Uso para Depuración

Si experimentas problemas con la aplicación:
1. Revisa `document_converter.log` para ver el último error
2. Busca mensajes de nivel `ERROR` o `CRITICAL`
3. Los logs incluyen la línea de código exacta donde ocurrió el problema
4. Proporciona estos logs al soporte técnico si es necesario
