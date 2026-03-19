import tkinter as tk
from tkinter import filedialog, messagebox
import whisper
import os
from docx import Document # 🚨 Nueva librería para manejar archivos .docx
import torch # Importamos la librería PyTorch para la gestión de dispositivos

# --- Lógica de Transcripción con Whisper ---
def transcribir_audio_whisper(ruta_audio):
    """
    Toma la ruta de un archivo de audio y lo transcribe usando el modelo Whisper de OpenAI.
    """
    try:
        # 1. Determinar el dispositivo de hardware
        # Usa 'cuda' si está disponible, de lo contrario, usa 'cpu'.
        dispositivo = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Usando el dispositivo: {dispositivo}")

        # 2. Cargar el modelo en el dispositivo especificado
        # El modelo se cargará directamente en la GPU si está disponible.
        # Usa 'tiny' o 'base' para probar la funcionalidad más rápido y "small", "medium", "large".
        modelo = whisper.load_model("medium").to(dispositivo)

        # 3. Transcribir el audio en el dispositivo seleccionado
        # El proceso de transcripción se ejecutará en la GPU para mayor velocidad.
        resultado = modelo.transcribe(ruta_audio, language='es')

        # 3. Devolver el texto transcrito.
        return resultado["text"]

    except Exception as e:
        messagebox.showerror("Error de Transcripción", f"Ocurrió un error con Whisper:\n\n{e}")
        return None

# --- Funciones de la Interfaz Gráfica ---
def seleccionar_archivo():
    """
    Abre un diálogo para seleccionar un archivo y llama a la función de transcripción.
    """
    global transcripcion_actual # 🚨 Usamos una variable global para guardar la transcripción

    ruta_archivo = filedialog.askopenfilename(
        title="Selecciona un archivo de audio",
        filetypes=(("Archivos de Audio", "*.mp3 *.wav *.m4a"), ("Todos los archivos", "*.*"))
    )

    if not ruta_archivo:
        return

    texto_resultado.delete("1.0", tk.END)
    texto_resultado.insert(tk.END, "Transcribiendo con Whisper, esto puede tardar un momento...")
    ventana.update()

    # Llamamos a la nueva función de transcripción
    transcripcion = transcribir_audio_whisper(ruta_archivo)
    transcripcion_actual = transcripcion # 🚨 Guardamos la transcripción en la variable global

    texto_resultado.delete("1.0", tk.END)
    if transcripcion:
        texto_resultado.insert(tk.END, transcripcion)
        boton_guardar_word.config(state=tk.NORMAL) # 🚨 Habilitamos el botón de guardar
    else:
        texto_resultado.insert(tk.END, "No se pudo transcribir el audio.")
        boton_guardar_word.config(state=tk.DISABLED) # 🚨 Deshabilitamos el botón de guardar

def guardar_como_word():
    """
    Guarda el texto transcrito en un archivo de Word (.docx).
    """
    global transcripcion_actual

    if not transcripcion_actual:
        messagebox.showwarning("Advertencia", "No hay transcripción para guardar.")
        return

    # Abre un diálogo para que el usuario elija dónde guardar el archivo
    ruta_guardado = filedialog.asksaveasfilename(
        defaultextension=".docx",
        filetypes=(("Archivos de Word", "*.docx"), ("Todos los archivos", "*.*")),
        title="Guardar transcripción como Word"
    )

    if not ruta_guardado:
        return

    try:
        # Crea un nuevo documento de Word
        documento = Document()
        # Agrega el texto transcrito al documento
        documento.add_paragraph(transcripcion_actual)
        # Guarda el documento
        documento.save(ruta_guardado)
        messagebox.showinfo("Éxito", "La transcripción se ha guardado correctamente como archivo de Word.")
    except Exception as e:
        messagebox.showerror("Error al Guardar", f"Ocurrió un error al guardar el archivo:\n\n{e}")

# --- Configuración de la Ventana Principal (con un nuevo botón) ---
ventana = tk.Tk()
ventana.title("Transcriptor de Audio con Whisper (IA Local)")
ventana.geometry("600x450") # 🚨 Aumentamos la altura de la ventana
ventana.config(bg="#f0f0f0")

# 🚨 Variable global para almacenar el texto transcrito
transcripcion_actual = ""

frame_principal = tk.Frame(ventana, padx=20, pady=20, bg="#f0f0f0")
frame_principal.pack(expand=True, fill=tk.BOTH)

etiqueta_titulo = tk.Label(frame_principal, text="Programa para Transcribir Audio (Whisper)", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
etiqueta_titulo.pack(pady=10)

boton_seleccionar = tk.Button(frame_principal, text="Seleccionar Archivo de Audio", command=seleccionar_archivo, font=("Helvetica", 12), bg="#007ACC", fg="white", relief="flat", padx=10, pady=5)
boton_seleccionar.pack(pady=20)

texto_resultado = tk.Text(frame_principal, height=10, width=60, font=("Helvetica", 11), wrap=tk.WORD, borderwidth=2, relief="groove")
texto_resultado.pack(pady=10, expand=True, fill=tk.BOTH)

# 🚨 Nuevo botón para guardar como Word
boton_guardar_word = tk.Button(frame_principal, text="Guardar como Word", command=guardar_como_word, font=("Helvetica", 12), bg="#28A745", fg="white", relief="flat", padx=10, pady=5, state=tk.DISABLED)
boton_guardar_word.pack(pady=10)

ventana.mainloop()
