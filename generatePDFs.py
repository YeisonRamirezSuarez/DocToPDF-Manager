import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import threading
import os
import comtypes.client
import fitz
import re
from PyPDF2 import PdfReader, PdfWriter
import shutil

# Variable global para almacenar el archivo seleccionado
selected_docx_filename = None

# Función para convertir el documento de Word a PDF
def word_to_pdf(docx_filename, output_pdf_filename):
    try:
        # Obtener la ruta absoluta
        docx_filename = os.path.abspath(docx_filename)
        output_pdf_filename = os.path.abspath(output_pdf_filename)
        
        # Verificar si el archivo de Word existe
        if not os.path.exists(docx_filename):
            raise FileNotFoundError(f"El archivo de Word no existe: {docx_filename}")
        
        # Crear una instancia de la aplicación Word
        word = comtypes.client.CreateObject('Word.Application')
        word.Visible = False  # No mostrar la interfaz de Word
        doc = word.Documents.Open(docx_filename)
        
        # Exportar el documento completo a un solo archivo PDF
        doc.SaveAs(output_pdf_filename, FileFormat=17)  # 17 es el formato PDF
        
        # Cerrar el documento y la aplicación de Word
        doc.Close()
        word.Quit()
        
        # Verificar si el archivo PDF fue creado correctamente
        if os.path.exists(output_pdf_filename):
            print(f"Documento exportado a PDF: {output_pdf_filename}")
        else:
            print(f"Error: El archivo PDF no se generó correctamente.")
            raise Exception("No se pudo generar el archivo PDF.")
        
    except Exception as e:
        print(f"Error al convertir el documento de Word a PDF: {e}")
        word.Quit()

def extract_name_and_registration(pdf_filename):
    # Abrir el archivo PDF con PyMuPDF
    doc = fitz.open(pdf_filename)

    # Extraer el texto de la primera página (puedes cambiar esto si necesitas más páginas)
    page = doc[0]
    text = page.get_text()

    # Usar expresiones regulares para encontrar el "Registro No." y el nombre
    # Buscar "Registro No." seguido de números y capturar lo que sigue
    match_registration = re.search(r"Registro No\.\s*(\d+)", text)
    if match_registration:
        registration_number = match_registration.group(1)
    else:
        registration_number = None

    # Buscar el texto después de "HACE CONSTAR QUE:" y capturar lo que sigue después de un salto de línea
    match_name = re.search(r"HACE CONSTAR QUE:\s*(.*?)(\n|$)", text)
    if match_name:
        name = match_name.group(1).strip()  # Limpiar espacios extra
    else:
        name = None

    return registration_number, name

# Función para dividir el PDF por páginas
def split_pdf_by_page(input_pdf_filename, output_folder):
    try:
        if not os.path.exists(input_pdf_filename):
            print(f"Error: El archivo PDF {input_pdf_filename} no existe.")
            raise Exception(f"El archivo PDF {input_pdf_filename} no existe.")
        
        with open(input_pdf_filename, 'rb') as input_pdf_file:
            reader = PdfReader(input_pdf_file)
            num_pages = len(reader.pages)

            # Crear el directorio de salida si no existe
            os.makedirs(output_folder, exist_ok=True)

            for page_num in range(num_pages):
                writer = PdfWriter()
                writer.add_page(reader.pages[page_num])

                # Guardar la página en un archivo temporal
                temp_pdf_filename = os.path.join(output_folder, f"temp_page_{page_num + 1}.pdf")
                with open(temp_pdf_filename, 'wb') as temp_pdf_file:
                    writer.write(temp_pdf_file)
                
                # Renombrar el archivo PDF con "Registro No. + Nombre de alumno"
                registration_number, name = extract_name_and_registration(temp_pdf_filename)
                
                if registration_number and name:
                    new_pdf_filename = os.path.join(output_folder, f"{registration_number} - {name}.pdf")
                    os.rename(temp_pdf_filename, new_pdf_filename)
                    print(f"Página {page_num + 1} guardada y renombrada como: {new_pdf_filename}")
                else:
                    print(f"Error al extraer datos de la página {page_num + 1}. El archivo se guardará como está.")
                    os.rename(temp_pdf_filename, os.path.join(output_folder, f"page_{page_num + 1}.pdf"))

        # Eliminar el archivo PDF completo después de procesar (NO ELIMINAR EL DIRECTORIO)
        if os.path.exists(input_pdf_filename):
            os.remove(input_pdf_filename)
            print(f"Archivo PDF completo eliminado: {input_pdf_filename}")
    except Exception as e:
        print(f"Error al dividir el PDF: {e}")

# Función para manejar la selección de archivo
def select_file():
    global selected_docx_filename
    selected_docx_filename = filedialog.askopenfilename(filetypes=[("Word Files", "*.docx")])
    if selected_docx_filename:
        messagebox.showinfo("Archivo seleccionado", f"Se seleccionó el archivo: {selected_docx_filename}")
    else:
        messagebox.showwarning("Advertencia", "No se seleccionó ningún archivo.")

# Función para manejar la generación del PDF y división
def start_conversion():
    if selected_docx_filename is None:
        messagebox.showerror("Error", "No se ha seleccionado ningún archivo de Word.")
        return

    # Deshabilitar los botones para evitar interacciones mientras se ejecuta el proceso
    select_button.config(state=tk.DISABLED)
    convert_button.config(state=tk.DISABLED)
    progress_label.grid(row=4, column=0, columnspan=2)
    progress_bar.grid(row=5, column=0, columnspan=2)
    progress_bar.start()

    output_pdf_filename = os.path.splitext(selected_docx_filename)[0] + ".pdf"  # Cambiado a .pdf
    # Crear una carpeta con el mismo nombre que el archivo seleccionado
    output_folder = os.path.join(
        os.path.dirname(selected_docx_filename),  # Directorio del archivo seleccionado
        os.path.splitext(os.path.basename(selected_docx_filename))[0]  # Nombre del archivo sin extensión
    )

    # Iniciar el proceso en un hilo separado
    threading.Thread(target=process_conversion, args=(selected_docx_filename, output_pdf_filename, output_folder)).start()

# Función para realizar la conversión y dividir el PDF
def process_conversion(docx_filename, output_pdf_filename, output_folder):
    try:
        word_to_pdf(docx_filename, output_pdf_filename)
        split_pdf_by_page(output_pdf_filename, output_folder)
        messagebox.showinfo("Éxito", "La conversión se completó con éxito.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error durante la conversión: {e}")
    finally:
        # Asegurarse de eliminar el archivo PDF generado al final
        if os.path.exists(output_pdf_filename):
            try:
                os.remove(output_pdf_filename)
                print(f"Archivo temporal eliminado: {output_pdf_filename}")
            except Exception as e:
                print(f"Error al intentar eliminar el archivo temporal {output_pdf_filename}: {e}")

        # Rehabilitar los botones y ocultar la barra de progreso
        progress_bar.stop()
        progress_label.grid_forget()
        progress_bar.grid_forget()
        select_button.config(state=tk.NORMAL)
        convert_button.config(state=tk.NORMAL)

# Crear la ventana principal
root = tk.Tk()
root.title("Conversión de Word a PDF")

# Obtener el tamaño de la pantalla y centrar la ventana
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = 400
window_height = 300
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Cambiar el icono de la ventana (asegúrate de tener un archivo .ico)
# Si tienes un archivo de icono de pluma, reemplázalo en la ruta
root.iconbitmap('pdf.ico')  # Asegúrate de tener un archivo .ico de tu pluma

# Configuración del color de fondo para la ventana
root.config(bg='#f0f0f0')  # Fondo gris claro

# Etiquetas y botones con colores
label = tk.Label(root, text="Selecciona un archivo Word para convertir a PDF:", font=("Arial", 12), bg='#f0f0f0')
label.grid(row=0, column=0, columnspan=2, pady=20, sticky="nsew")

select_button = tk.Button(root, text="Seleccionar archivo", command=select_file, width=20, height=2, font=("Arial", 14), 
                          bg='#4CAF50', fg='white', bd=2, relief="raised")
select_button.grid(row=1, column=0, pady=10, sticky="nsew")

convert_button = tk.Button(root, text="Iniciar Conversión", command=start_conversion, width=20, height=2, font=("Arial", 14),
                           bg='#008CBA', fg='white', bd=2, relief="raised")
convert_button.grid(row=2, column=0, pady=20, sticky="nsew")

# Barra de progreso y etiqueta de carga
progress_label = tk.Label(root, text="Generando el PDF, por favor espera...", font=("Arial", 12), bg='#f0f0f0')
progress_bar = ttk.Progressbar(root, mode="indeterminate")

# Configuración del grid para centrar los botones y texto
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)

# Iniciar la interfaz
root.mainloop()
