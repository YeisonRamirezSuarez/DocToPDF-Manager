Para usar:

1. Ejecutar el generatePDFs
2. Seleccionar el archivo de Word.
3. Iniciar conversión.

-- El resultado se va encontrar en la misma carpeta donde se eligió el documento de Word.




Developer:
    python -m PyInstaller --onefile --windowed --icon=pdf.ico --add-data "pdf.ico;." generatePDFs.py  ("Para generar el ejecutable")