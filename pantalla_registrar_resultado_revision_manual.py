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
        # Estilo y encabezado
        style = ttk.Style(self.root)
        try:
            style.theme_use('clam')
        except Exception:
            pass
        header = tk.Frame(self.root, bg="#1f4e79")
        header.pack(fill=tk.X)
        tk.Label(header, text="Registrar Solicitud de Revisión Manual", font=("Segoe UI", 18, "bold"), bg="#1f4e79", fg="white", pady=10).pack()

        # Contenedor principal: panel izquierdo (lista) y derecho (detalles)
        main = tk.Frame(self.root)
        main.pack(fill=tk.BOTH, expand=True, padx=12, pady=10)

        # Panel izquierdo: búsqueda y dos listas de eventos
        left = tk.Frame(main, bd=1, relief=tk.FLAT)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,10))
        toolbar = tk.Frame(left)
        toolbar.pack(fill=tk.X, pady=4)
        self.btn_iniciar = ttk.Button(toolbar, text="Cargar Sismos", command=self.mostrarSismos)
        self.btn_iniciar.pack(side=tk.LEFT)
        self.var_autodetectado = tk.BooleanVar(value=True)
        
        # Lista superior: Todos los eventos
        tk.Label(left, text="Eventos Pendientes de Revision:", anchor='w').pack(fill=tk.X)
        list_frame = tk.Frame(left)
        list_frame.pack(fill=tk.BOTH, expand=True)
        self.lst_eventos = tk.Listbox(list_frame, width=46, height=10, selectmode=tk.SINGLE, activestyle='none')
        self.lst_eventos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.lst_eventos.yview)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.lst_eventos.config(yscrollcommand=scrollbar.set)
        self.lst_eventos.bind('<<ListboxSelect>>', self.solicitaSeleccionarSismo)

        self.btn_confirmar_seleccion = ttk.Button(left, text="Confirmar Selección", command=self.tomarSeleccionSismo)
        self.btn_confirmar_seleccion.pack(pady=6, fill=tk.X)

        # Lista inferior: Evento bloqueado (confirmado)
        tk.Label(left, text="Evento Seleccionado:", anchor='w').pack(fill=tk.X, pady=(8,0))
        list_frame_bloqueado = tk.Frame(left)
        list_frame_bloqueado.pack(fill=tk.BOTH, expand=True)
        self.lst_evento_bloqueado = tk.Listbox(list_frame_bloqueado, width=46, height=6, selectmode=tk.NONE, activestyle='none', bg="#f0f0f0")
        self.lst_evento_bloqueado.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_bloqueado = tk.Scrollbar(list_frame_bloqueado, orient=tk.VERTICAL, command=self.lst_evento_bloqueado.yview)
        scrollbar_bloqueado.pack(side=tk.LEFT, fill=tk.Y)
        self.lst_evento_bloqueado.config(yscrollcommand=scrollbar_bloqueado.set)

        # Panel derecho: detalles del evento, muestras y acciones
        right = tk.Frame(main)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Estación y visualización
        frame_estacion = tk.Frame(right)
        frame_estacion.pack(fill=tk.X, pady=(0,8))
        tk.Label(frame_estacion, text="Estación:").pack(side=tk.LEFT)
        self.cmb_estaciones = ttk.Combobox(frame_estacion, state="readonly")
        self.cmb_estaciones.pack(side=tk.LEFT, padx=6)
        self.cmb_estaciones.bind('<<ComboboxSelected>>', self.on_estacion_select)
        ttk.Button(frame_estacion, text="Visualizar en Mapa").pack(side=tk.LEFT, padx=6)

        # Tabla de muestras
        tk.Label(right, text="Muestras (Estación seleccionada):").pack(anchor='w')
        self.tree_muestras = ttk.Treeview(right, columns=("instante", "vel", "frec", "long"), show="headings", height=6)
        for col, txt in zip(["instante", "vel", "frec", "long"], ["Instante", "Vel. Onda", "Freq. Onda", "Long. Onda"]):
            self.tree_muestras.heading(col, text=txt)
            self.tree_muestras.column(col, width=100, anchor='center')
        self.tree_muestras.pack(fill=tk.X, pady=6)

        # Datos del evento
        frame_datos = ttk.LabelFrame(right, text="Datos del Evento Seleccionado")
        frame_datos.pack(fill=tk.BOTH, expand=False, pady=6)
        self.vars = {}
        labels = ["Ubicación:", "Fecha:", "Clasificación Sismo:", "Magnitud:", "Origen Sismo:", "Alcance Sismo:"]
        for i, label in enumerate(labels):
            ttk.Label(frame_datos, text=label).grid(row=i, column=0, sticky=tk.W, padx=6, pady=3)
            var = tk.StringVar()
            
            entry = ttk.Entry(frame_datos, textvariable=var, state="disabled", width=40)
            entry.grid(row=i, column=1, sticky=tk.W, padx=6, pady=3)
            self.vars[label] = (var, entry)

        # Botones de acción (editar/guardar/generar)
        frame_accion = tk.Frame(right)
        frame_accion.pack(fill=tk.X, pady=6)
        self.btn_modificar = ttk.Button(frame_accion, text="Modificar", command=self.habilitarOpcionEditarValores, state="disabled")
        self.btn_modificar.pack(side=tk.LEFT, padx=6)
        self.btn_guardar = ttk.Button(frame_accion, text="Guardar", command=self.guardarCambios, state="disabled")
        self.btn_guardar.pack(side=tk.LEFT, padx=6)
        ttk.Button(frame_accion, text="Generar Sismograma").pack(side=tk.LEFT, padx=6)

        # Botones de resultado alineados al final
        frame_resultado = tk.Frame(self.root)
        frame_resultado.pack(fill=tk.X, padx=12, pady=(6,12))
        self.btn_confirmar = ttk.Button(frame_resultado, text="Confirmar Evento", command=self.confirmarEvento)
        self.btn_confirmar.pack(side=tk.RIGHT, padx=6)
        self.btn_rechazar = ttk.Button(frame_resultado, text="Rechazar Evento", command=self.rechazarEvento)
        self.btn_rechazar.pack(side=tk.RIGHT, padx=6)
        self.btn_derivar = ttk.Button(frame_resultado, text="Derivar a Experto", command=self.derivarEvento)
        self.btn_derivar.pack(side=tk.RIGHT, padx=6)
        self.btn_cancelar = ttk.Button(frame_resultado, text="Cancelar", command=self.cancelar)
        self.btn_cancelar.pack(side=tk.LEFT)

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
        self.mostrarDatosEventoSismico(evento)
        

    def tomarSeleccionSismo(self):
        idx = self.lst_eventos.curselection()
        if not idx:
            messagebox.showwarning("Advertencia", "Por favor selecciona un sismo.")
            return
        evento = self.eventos_cargados[idx[0]]
        self.gestor.tomarSeleccionSismo(evento.id)
        muestras = self.gestor.obtenerValoresMuestras(evento)
        nombres_estaciones = list({muestra['Estacion Sismologica'] for muestra in muestras if muestra.get('Estacion Sismologica')})
        self.cmb_estaciones['values'] = nombres_estaciones
        if nombres_estaciones:
            self.cmb_estaciones.current(0)
            self.on_estacion_select(None)
        self.btn_modificar.config(state="normal")
        
        # Mostrar evento seleccionado en la lista bloqueada
        self.lst_evento_bloqueado.delete(0, tk.END)
        ubic = "Córdoba"
        fecha = evento.fechaHoraConcurrencia.strftime("%d/%m/%Y %H:%M")
        mag = evento.valorMagnitud
        evento_info = f"{fecha} | {ubic} | M {mag}"
        self.lst_evento_bloqueado.insert(tk.END, evento_info)
        
        # Eliminar de la lista superior
        self.lst_eventos.delete(idx[0])
        self.eventos_cargados.pop(idx[0])
        self.btn_confirmar_seleccion.config(state="disabled")
        

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
            self.vars[key][1].config(state="disabled")
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
        self.cmb_estaciones.config(state="readonly")

    def confirmarEvento(self):
        evento = self.gestor.evento_seleccionado
        if evento:
            # Obtener índice actual en la lista
            idx = self.lst_eventos.curselection()
            self.gestor.confirmarEvento()
            self.mostrarDatosEventoSismico(evento)
            messagebox.showinfo("Éxito", "Evento confirmado correctamente.")
            
            # Eliminar de la lista superior y actualizar
            if idx:
                self.lst_eventos.delete(idx[0])
                self.eventos_cargados.pop(idx[0])
            
            # El evento ya está en la lista bloqueada, mantenerlo ahí
            # (no limpiar, solo actualizar la lista superior)
            self.btn_confirmar_seleccion.config(state="enabled")

    def rechazarEvento(self):
        evento = self.gestor.evento_seleccionado
        if evento:
            # Obtener índice actual en la lista
            idx = self.lst_eventos.curselection()
            self.gestor.rechazarEvento()
            self.mostrarDatosEventoSismico(evento)
            messagebox.showinfo("Éxito", "Evento rechazado correctamente.")
            
            # Eliminar de la lista superior y actualizar
            if idx:
                self.lst_eventos.delete(idx[0])
                self.eventos_cargados.pop(idx[0])
            
            # Limpiar la lista bloqueada
            self.lst_evento_bloqueado.delete(0, tk.END)
            self.btn_confirmar_seleccion.config(state="enabled")

    def derivarEvento(self):
        evento = self.gestor.evento_seleccionado
        if evento:
            # Obtener índice actual en la lista
            idx = self.lst_eventos.curselection()
            self.gestor.derivarEvento()
            self.mostrarDatosEventoSismico(evento)
            messagebox.showinfo("Éxito", "Evento derivado a experto correctamente.")
            
            # Eliminar de la lista superior y actualizar
            if idx:
                self.lst_eventos.delete(idx[0])
                self.eventos_cargados.pop(idx[0])
            
            # Limpiar la lista bloqueada
            self.lst_evento_bloqueado.delete(0, tk.END)
            self.btn_confirmar_seleccion.config(state="enabled")

    def cancelar(self):
        if messagebox.askyesno("Confirmar", "¿Está seguro que desea cancelar y cerrar la pantalla?"):
            self.root.destroy()

if __name__ == "__main__":
    PantallaRegistrarResultadoRevisionManual() 