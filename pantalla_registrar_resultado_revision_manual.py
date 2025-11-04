import tkinter as tk
from tkinter import ttk, messagebox
from gestor_registrar_resultado_revision_manual import GestorRegistrarResultadoRevisionManual

class PantallaRegistrarResultadoRevisionManual:
    def __init__(self):
        self.gestor = GestorRegistrarResultadoRevisionManual()
        self.gestor.registrarResultadoRevisionManual()
        self.root = tk.Tk()
        self.root.title("Registrar Solicitud de Revisión Manual")
        self.root.geometry("1000x600")
        self._crear_widgets()
        self.root.mainloop()

    def _crear_widgets(self):
        tk.Label(self.root, text="Registrar Solicitud de Revisión Manual", font=("Arial", 20, "bold"), bg="#b71c1c", fg="white").pack(fill=tk.X)
        frame_top = tk.Frame(self.root)
        frame_top.pack(pady=10)
        self.btn_iniciar = tk.Button(frame_top, text="Solicitar Iniciar Revisión", command=self.mostrarSismos)
        self.btn_iniciar.pack(side=tk.LEFT, padx=5)
        self.var_autodetectado = tk.BooleanVar(value=True)
        tk.Radiobutton(frame_top, text="AutoDetectado", variable=self.var_autodetectado, value=True, command=self.mostrarSismos).pack(side=tk.LEFT)
        self.lst_eventos = tk.Listbox(self.root, width=80, height=6, selectmode=tk.SINGLE)
        self.lst_eventos.pack(pady=5)
        self.lst_eventos.bind('<<ListboxSelect>>', self.solicitaSeleccionarSismo)
        self.btn_confirmar_seleccion = tk.Button(self.root, text="Confirmar Selección Evento", command=self.tomarSeleccionSismo)
        self.btn_confirmar_seleccion.pack(pady=5)
        frame_estacion = tk.Frame(self.root)
        frame_estacion.pack(pady=5)
        tk.Label(frame_estacion, text="Estación:").pack(side=tk.LEFT)
        self.cmb_estaciones = ttk.Combobox(frame_estacion, state="readonly")
        self.cmb_estaciones.pack(side=tk.LEFT, padx=5)
        self.cmb_estaciones.bind('<<ComboboxSelected>>', self.on_estacion_select)
        tk.Button(frame_estacion, text="Visualizar en Mapa").pack(side=tk.LEFT, padx=5)
        self.tree_muestras = ttk.Treeview(self.root, columns=("instante", "vel", "frec", "long"), show="headings", height=5)
        for col, txt in zip(["instante", "vel", "frec", "long"], ["Instante", "Velocidad de Onda", "Frecuencia de Onda", "Longitud de Onda"]):
            self.tree_muestras.heading(col, text=txt)
        self.tree_muestras.pack(pady=5)
        frame_datos = tk.LabelFrame(self.root, text="Datos del Evento Sismico Seleccionado:")
        frame_datos.pack(fill=tk.X, padx=10, pady=5)
        self.vars = {}
        labels = ["Ubicación:", "Fecha:", "Clasificación Sismo:", "Magnitud:", "Origen Sismo:", "Alcance Sismo:"]
        for i, label in enumerate(labels):
            tk.Label(frame_datos, text=label).grid(row=i, column=0, sticky=tk.W)
            var = tk.StringVar()
            entry = tk.Entry(frame_datos, textvariable=var, state="readonly")
            entry.grid(row=i, column=1, sticky=tk.W)
            self.vars[label] = (var, entry)
        frame_accion = tk.Frame(self.root)
        frame_accion.pack(pady=5)
        self.btn_modificar = tk.Button(frame_accion, text="Modificar Evento Sismico", command=self.habilitarOpcionEditarValores, state="disabled")
        self.btn_modificar.pack(side=tk.LEFT, padx=5)
        self.btn_guardar = tk.Button(frame_accion, text="Guardar Cambios", command=self.guardarCambios, state="disabled")
        self.btn_guardar.pack(side=tk.LEFT, padx=5)
        tk.Button(frame_accion, text="Generar Sismograma").pack(side=tk.LEFT, padx=5)
        # Botones de resultado
        frame_resultado = tk.Frame(self.root)
        frame_resultado.pack(pady=20)
        self.btn_confirmar = tk.Button(frame_resultado, text="Confirmar Evento", width=18, command=self.confirmarEvento)
        self.btn_confirmar.pack(side=tk.LEFT, padx=10)
        self.btn_rechazar = tk.Button(frame_resultado, text="Rechazar Evento", width=18, command=self.rechazarEvento)
        self.btn_rechazar.pack(side=tk.LEFT, padx=10)
        self.btn_derivar = tk.Button(frame_resultado, text="Derivar a Experto", width=18, command=self.derivarEvento)
        self.btn_derivar.pack(side=tk.LEFT, padx=10)
        self.btn_cancelar = tk.Button(frame_resultado, text="Cancelar", width=18, command=self.cancelar)
        self.btn_cancelar.pack(side=tk.LEFT, padx=10)

    def mostrarSismos(self):
        self.lst_eventos.delete(0, tk.END)
        eventos = self.gestor.buscarSismosAutodetectados()
        for evento in eventos:
            ubic = "Córdoba"
            fecha = evento.fechaHoraConcurrencia.strftime("%d/%m/%Y %H:%M")
            mag = evento.valorMagnitud
            self.lst_eventos.insert(tk.END, f"{fecha} | {ubic} (Epicentro: {evento.latitudEpicentro} | Hipocentro: {evento.latitudHipocentro}) | M {mag}")
        self.eventos_cargados = eventos

    def solicitaSeleccionarSismo(self, event):
        idx = self.lst_eventos.curselection()
        if not idx:
            return
        evento = self.eventos_cargados[idx[0]]
        self.gestor.tomarSeleccionSismo(evento.id)
        self.mostrarDatosEventoSismico(evento)

    def tomarSeleccionSismo(self):
        evento = self.gestor.evento_seleccionado
        if not evento:
            return
        muestras = self.gestor.obtenerValoresMuestras(evento)
        nombres_estaciones = list({muestra['Estacion Sismologica'] for muestra in muestras if muestra.get('Estacion Sismologica')})
        self.cmb_estaciones['values'] = nombres_estaciones
        if nombres_estaciones:
            self.cmb_estaciones.current(0)
            self.on_estacion_select(None)
        self.btn_modificar.config(state="normal")

    def on_estacion_select(self, event):
        evento = self.gestor.evento_seleccionado
        if not evento:
            return
        idx = self.cmb_estaciones.current()
        nombres_estaciones = list(self.cmb_estaciones['values'])
        if idx < 0 or idx >= len(nombres_estaciones):
            return
        estacion_nombre = nombres_estaciones[idx]
        muestras = self.gestor.obtenerValoresMuestras(evento)
        self.tree_muestras.delete(*self.tree_muestras.get_children())
        for muestra in muestras:
            if muestra.get('Estacion Sismologica', '') == estacion_nombre:
                instante = muestra.get('Instante', '')
                if instante:
                    instante = instante.strftime("%d/%m/%Y %H:%M")
                longi = muestra.get('Longitud de Onda', '')
                frec = muestra.get('Frecuencia de Onda', '')
                vel = muestra.get('Velocidad de Onda', '')
                self.tree_muestras.insert("", tk.END, values=(instante, vel, frec, longi))

    def mostrarDatosEventoSismico(self, evento):
        self.vars["Ubicación:"][0].set("Córdoba")
        self.vars["Fecha:"][0].set(evento.fechaHoraConcurrencia.strftime("%d/%m/%Y %H:%M"))
        self.vars["Clasificación Sismo:"][0].set(evento.getClasificacion())
        self.vars["Magnitud:"][0].set(str(evento.valorMagnitud))
        self.vars["Origen Sismo:"][0].set(evento.getOrigen())
        self.vars["Alcance Sismo:"][0].set(evento.getAlcance())
        for key in self.vars:
            self.vars[key][1].config(state="readonly")
        self.btn_guardar.config(state="disabled")
        self.btn_modificar.config(state="disabled")

    def habilitarOpcionEditarValores(self):
        for key in ["Magnitud:", "Origen Sismo:", "Alcance Sismo:"]:
            self.vars[key][1].config(state="normal")
        self.btn_guardar.config(state="normal")
        # Deshabilitar todos los demás botones de acción
        self.btn_confirmar.config(state="disabled")
        self.btn_rechazar.config(state="disabled")
        self.btn_derivar.config(state="disabled")
        self.btn_modificar.config(state="disabled")
        self.btn_confirmar_seleccion.config(state="disabled")
        self.cmb_estaciones.config(state="disabled")

    def guardarCambios(self):
        evento = self.gestor.evento_seleccionado
        if not evento:
            return
        mag = self.vars["Magnitud:"][0].get()
        origen_val = self.vars["Origen Sismo:"][0].get()
        alcance_val = self.vars["Alcance Sismo:"][0].get()
        if mag.strip() == "":
            messagebox.showerror("Error", "El campo Magnitud no puede estar vacío.")
            return
        try:
            float(mag)
        except ValueError:
            messagebox.showerror("Error", "El campo Magnitud debe ser un número válido.")
            return
        if not origen_val.replace(" ", "").isalpha():
            messagebox.showerror("Error", "El campo Origen Sismo debe contener solo letras.")
            return
        if not alcance_val.replace(" ", "").isalpha():
            messagebox.showerror("Error", "El campo Alcance Sismo debe contener solo letras.")
            return
        self.gestor.modificarEvento(evento, mag, alcance_val, origen_val)
        self.mostrarDatosEventoSismico(evento)
        messagebox.showinfo("Éxito", "Cambios guardados correctamente.")
        # Reactivar los botones
        self.btn_confirmar.config(state="normal")
        self.btn_rechazar.config(state="normal")
        self.btn_derivar.config(state="normal")
        self.btn_modificar.config(state="normal")
        self.btn_confirmar_seleccion.config(state="normal")
        self.cmb_estaciones.config(state="readonly")

    def confirmarEvento(self):
        evento = self.gestor.evento_seleccionado
        if evento:
            self.gestor.confirmarEvento(evento)
            self.mostrarDatosEventoSismico(evento)
            messagebox.showinfo("Éxito", "Evento confirmado correctamente.")
            self.mostrarSismos()

    def rechazarEvento(self):
        evento = self.gestor.evento_seleccionado
        if evento:
            self.gestor.rechazarEvento(evento)
            self.mostrarDatosEventoSismico(evento)
            messagebox.showinfo("Éxito", "Evento rechazado correctamente.")
            self.mostrarSismos()

    def derivarEvento(self):
        evento = self.gestor.evento_seleccionado
        if evento:
            self.gestor.derivarEvento(evento)
            self.mostrarDatosEventoSismico(evento)
            messagebox.showinfo("Éxito", "Evento derivado a experto correctamente.")
            self.mostrarSismos()

    def cancelar(self):
        if messagebox.askyesno("Confirmar", "¿Está seguro que desea cancelar y cerrar la pantalla?"):
            self.root.destroy()

if __name__ == "__main__":
    PantallaRegistrarResultadoRevisionManual() 