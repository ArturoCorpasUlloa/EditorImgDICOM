![Logo DICOM](./logo-dicom.svg)


# 🩺 Editor de Imágenes DICOM  

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)  
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-orange)  
![pydicom](https://img.shields.io/badge/pydicom-DICOM-red)  

Aplicación de escritorio en **Python** para **visualizar y editar metadatos de archivos DICOM (.dcm)** mediante una interfaz gráfica sencilla e intuitiva.  

---

## ✨ Características  

✅ Interfaz gráfica con **Tkinter**  
✅ Carga automática de pacientes desde archivos DICOM  
✅ Visualización y edición de datos clave:  
   - 🧑 Nombre del paciente  
   - 🆔 Documento / ID del paciente  
   - 🎂 Fecha de nacimiento  
   - ⚧ Sexo  
   - 📅 Fecha de estudio  
   - ⏰ Hora de estudio  
✅ Conversión automática de **fechas** (`dd/mm/yyyy`) y **horas** (`HH:MM:SS`)  
✅ Guardado de copias editadas en una carpeta destino  
✅ Progreso de edición mediante barra gráfica  
✅ Control de pacientes ya procesados (no se vuelven a cargar)  

---

## 🛠️ Requisitos  

- **Python 3.8+**  
- Librerías necesarias:  

```bash
pip install pydicom

🚀 Uso

1) Clona o descarga este repositorio.

2) Ejecuta el script principal:

python dicom_editor.py

3) En la ventana:

Selecciona la Carpeta Origen con archivos DICOM.
Selecciona la Carpeta Destino donde guardar los editados.
Carga un paciente y edita los campos deseados.
Haz clic en Copiar con Cambios para generar los archivos actualizados.


👨‍💻 Autor

📌 Desarrollado por Arturo Corpas
💼 Ingeniero en Desarrollo de Software y Datos








