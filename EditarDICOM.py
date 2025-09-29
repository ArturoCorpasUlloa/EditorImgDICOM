from datetime import datetime
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pydicom

CAMPOS = {
    "PatientName": "Nombre",
    "PatientID": "Documento",
    "PatientBirthDate": "Fecha de Nacimiento",
    "PatientSex": "Sexo",
    "StudyDate": "Fecha de Estudio",
    "StudyTime": "Hora de Estudio"
}

class DicomEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Imágenes DICOM")
        self.root.geometry("650x500")
        self.root.configure(bg="#f5f6fa")

        self.folder_src = tk.StringVar()
        self.folder_dst = tk.StringVar()
        self.entries = {}
        self.selected_patient = None
        self.pacientes = {}  # pacientes cargados
        self.remaining_patients = []  # pacientes pendientes por editar

        # UI
        frame = tk.Frame(root, padx=15, pady=15, bg="#f5f6fa")
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Carpeta con Imágenes:", bg="#f5f6fa", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.folder_src, width=50).grid(row=0, column=1, padx=5)
        tk.Button(frame, text="Buscar", command=self.select_src).grid(row=0, column=2, padx=5)

        tk.Label(frame, text="Carpeta Destino:", bg="#f5f6fa", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", pady=5)
        tk.Entry(frame, textvariable=self.folder_dst, width=50).grid(row=1, column=1, padx=5)
        tk.Button(frame, text="Buscar", command=self.select_dst).grid(row=1, column=2, padx=5)

        # Campos de edición
        row = 2
        tk.Label(frame, text="Datos del Paciente y Estudio", bg="#f5f6fa", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=3, pady=10)

        for tag, label in CAMPOS.items():
            row += 1
            tk.Label(frame, text=f"{label}:", bg="#f5f6fa", font=("Arial", 10)).grid(row=row, column=0, sticky="e", pady=3)
            var = tk.StringVar()
            entry = tk.Entry(frame, textvariable=var, width=40)
            entry.grid(row=row, column=1, columnspan=2, pady=3, sticky="w")
            self.entries[tag] = var

        # Barra de progreso
        row += 1
        tk.Label(frame, text="Progreso:", bg="#f5f6fa", font=("Arial", 10, "italic")).grid(row=row, column=0, sticky="w", pady=10)
        self.progress = ttk.Progressbar(frame, length=400, mode="determinate")
        self.progress.grid(row=row, column=1, columnspan=2, pady=10, sticky="w")

        # Botones
        row += 1
        tk.Button(frame, text="Cargar Datos", bg="#0984e3", fg="white", width=15, command=self.load_dicom).grid(row=row, column=0, pady=15)
        tk.Button(frame, text="Copiar con Cambios", bg="#00b894", fg="white", width=20, command=self.copy_with_edits).grid(row=row, column=1, pady=15)
        tk.Button(frame, text="Salir", bg="#d63031", fg="white", width=10, command=root.quit).grid(row=row, column=2, pady=15)

    def select_src(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_src.set(folder)

    def select_dst(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_dst.set(folder)

    def format_date(self, dicom_date):
        try:
            return datetime.strptime(dicom_date, "%Y%m%d").strftime("%d/%m/%Y")
        except:
            return dicom_date

    def format_time(self, dicom_time):
        try:
            return datetime.strptime(dicom_time.split(".")[0], "%H%M%S").strftime("%H:%M:%S")
        except:
            return dicom_time

    def unformat_date(self, user_date):
        try:
            return datetime.strptime(user_date, "%d/%m/%Y").strftime("%Y%m%d")
        except:
            return user_date

    def unformat_time(self, user_time):
        try:
            return datetime.strptime(user_time, "%H:%M:%S").strftime("%H%M%S")
        except:
            return user_time

    def load_dicom(self, reload=True):
        """Carga la lista de pacientes, o usa la lista guardada si reload=False"""
        if not self.folder_src.get():
            messagebox.showerror("Error", "Debe seleccionar carpeta origen.")
            return

        if reload:  # solo la primera vez
            self.pacientes.clear()
            for root, dirs, files in os.walk(self.folder_src.get()):
                for f in files:
                    if f.lower().endswith(".dcm"):
                        dcm_file = os.path.join(root, f)
                        try:
                            ds = pydicom.dcmread(dcm_file, stop_before_pixels=True)
                            nombre = str(getattr(ds, "PatientName", "DESCONOCIDO")).upper()
                            if nombre not in self.pacientes:
                                self.pacientes[nombre] = dcm_file
                        except:
                            continue
            self.remaining_patients = list(self.pacientes.keys())

        if not self.remaining_patients:
            messagebox.showinfo("Finalizado", "No quedan pacientes por editar.")
            return

        self.show_patient_selector()

    def show_patient_selector(self):
        """Ventana de selección de paciente"""
        top = tk.Toplevel(self.root)
        top.title("Seleccionar Paciente")
        tk.Label(top, text="Seleccione un paciente:", font=("Arial", 10, "bold")).pack(pady=5)
        lista = tk.Listbox(top, width=50, height=10)
        lista.pack(padx=10, pady=5)
        for nombre in self.remaining_patients:
            lista.insert(tk.END, nombre)

        def seleccionar():
            idx = lista.curselection()
            if not idx:
                messagebox.showerror("Error", "Debe seleccionar un paciente.")
                return
            nombre = lista.get(idx[0])
            self.selected_patient = nombre
            archivo = self.pacientes[nombre]

            ds = pydicom.dcmread(archivo, stop_before_pixels=True)
            for tag in CAMPOS.keys():
                value = getattr(ds, tag, "")
                if tag in ["StudyDate", "PatientBirthDate"]:
                    value = self.format_date(value)
                elif tag == "StudyTime":
                    value = self.format_time(value)
                self.entries[tag].set(value)

            top.destroy()
            messagebox.showinfo("Datos cargados", f"Se cargaron los datos de {nombre}.")

        tk.Button(top, text="Cargar", command=seleccionar).pack(pady=10)

    def copy_with_edits(self):
        if not self.folder_src.get() or not self.folder_dst.get():
            messagebox.showerror("Error", "Debe seleccionar carpetas de origen y destino.")
            return

        if not self.selected_patient:
            messagebox.showerror("Error", "Debe cargar primero un paciente.")
            return

        edits = {}
        for tag, var in self.entries.items():
            value = var.get()
            if tag in ["StudyDate", "PatientBirthDate"]:
                value = self.unformat_date(value)
            elif tag == "StudyTime":
                value = self.unformat_time(value)
            elif tag == "PatientName":
                value = value.upper()
            edits[tag] = value

        files_to_copy = []
        for root, dirs, files in os.walk(self.folder_src.get()):
            for f in files:
                if f.lower().endswith(".dcm"):
                    file_path = os.path.join(root, f)
                    try:
                        ds = pydicom.dcmread(file_path, stop_before_pixels=True)
                        nombre = str(getattr(ds, "PatientName", "")).upper()
                        if nombre == self.selected_patient:
                            files_to_copy.append(file_path)
                    except:
                        continue

        if not files_to_copy:
            messagebox.showerror("Error", "No se encontraron archivos del paciente seleccionado.")
            return

        self.progress["maximum"] = len(files_to_copy)
        count = 0

        for src_file in files_to_copy:
            rel_path = os.path.relpath(src_file, self.folder_src.get())
            dst_file = os.path.join(self.folder_dst.get(), rel_path)
            os.makedirs(os.path.dirname(dst_file), exist_ok=True)

            ds = pydicom.dcmread(src_file)
            for tag, value in edits.items():
                if hasattr(ds, tag):
                    setattr(ds, tag, value)
            ds.save_as(dst_file)

            count += 1
            self.progress["value"] = count
            self.root.update_idletasks()

        # marcar paciente como procesado
        if self.selected_patient in self.remaining_patients:
            self.remaining_patients.remove(self.selected_patient)

        # preguntar si se quiere otro paciente
        if self.remaining_patients:
            again = messagebox.askyesno("Otro paciente", "¿Desea editar otro paciente?")
            if again:
                self.load_dicom(reload=False)

        messagebox.showinfo("Finalizado", f"Se copiaron y editaron {count} archivos de {self.selected_patient}.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DicomEditorApp(root)
    root.mainloop()
