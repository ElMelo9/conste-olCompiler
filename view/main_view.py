import tkinter as tk
from tkinter import scrolledtext, ttk
from models.reserved_models import RESERVED
import re

class MainView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self._create_widgets()
        self._layout_widgets()
        self._bind_events()

    def _create_widgets(self):
        """Crea los widgets que se utilizarán en la ventana."""
        self.text_area = scrolledtext.ScrolledText(self, width=70, height=20)
        self.line_numbers = tk.Text(self, width=4, height=20, state='disabled', bg='lightgrey')
        self.compilar_button = tk.Button(self, text="Compilar")

        # Crear el contenedor de pestañas
        self.tab_control = ttk.Notebook(self)

        # Crear pestañas
        self.tab_consola = tk.Frame(self.tab_control)
        self.tab_logs = tk.Frame(self.tab_control)

        # Agregar pestañas al contenedor
        self.tab_control.add(self.tab_consola, text='Consola')
        self.tab_control.add(self.tab_logs, text='Logs')

        # Widgets dentro de la pestaña Consola
        self.consola_text = tk.Text(self.tab_consola, height=10, state='disabled')

        # Widgets dentro de la pestaña Logs
        self.logs_text = tk.Text(self.tab_logs, height=10, state='disabled')
    
    def _layout_widgets(self):
        """Organiza los widgets en la ventana."""
        self.line_numbers.grid(row=0, column=0, sticky='nsw', pady=(10,10))
        self.text_area.grid(row=0, column=1, sticky='nsew', padx=(0,10), pady=(10,10))
        self.tab_control.grid(row=1, column=1, sticky='nsew', padx=10, pady=10)
        self.compilar_button.grid(row=2, column=1, sticky='ew', padx=10, pady=(0,10))

        # Posicionar widgets dentro de las pestañas
        self.consola_text.pack(expand=True, fill='both')
        self.logs_text.pack(expand=True, fill='both')

    def _bind_events(self):
        """Vincula eventos a los widgets."""
        self.text_area.bind('<KeyRelease>', self._update_line_numbers)
        self.text_area.bind('<MouseWheel>', self._on_text_scroll)
        self.text_area.bind('<KeyPress-Prior>', self._on_text_scroll)
        self.text_area.bind('<KeyPress-Next>', self._on_text_scroll)
        self.text_area.bind('<KeyRelease>', self._on_key_release)
        self.text_area.configure(yscrollcommand=self._on_text_scroll)
        self.line_numbers.configure(yscrollcommand=self._on_line_scroll)

    def _update_line_numbers(self, event=None):
        """Actualiza el número de línea al lado del área de texto."""
        self.line_numbers.config(state='normal')
        self.line_numbers.delete('1.0', 'end')

        line_count = int(self.text_area.index('end-1c').split('.')[0])
        line_number_content = "\n".join(str(i) for i in range(1, line_count + 1))
        self.line_numbers.insert('1.0', line_number_content)
        self.line_numbers.config(state='disabled')

    def _on_text_scroll(self, *args):
        """Sincroniza el desplazamiento del área de texto con el contador de líneas."""
        self.line_numbers.yview_moveto(self.text_area.yview()[0])

    def _on_line_scroll(self, *args):
        """Sincroniza el desplazamiento del contador de líneas con el área de texto."""
        self.text_area.yview_moveto(self.line_numbers.yview()[0])

    def set_compilar_command(self, command):
        """Establece el comando a ejecutar cuando se presiona el botón Compilar."""
        def compilar_command():
            self.limpiar_consola_logs()
            command()
        self.compilar_button.config(command=compilar_command)

    def get_codigo(self):
        """Obtiene el código del área de texto."""
        return self.text_area.get('1.0', tk.END)

    def imprimir_en_consola(self, texto):
        """Imprime texto en la consola."""
        self.consola_text.config(state='normal')
        self.consola_text.insert(tk.END, texto + '\n')
        self.consola_text.config(state='disabled')

    def registrar_log(self, mensaje):
        """Agrega un mensaje al log."""
        self.logs_text.config(state='normal')
        self.logs_text.insert(tk.END, mensaje + '\n')
        self.logs_text.config(state='disabled')

    def limpiar_consola_logs(self):
        """Limpia la consola y los logs."""
        self.consola_text.config(state='normal')
        self.consola_text.delete('1.0', tk.END)
        self.consola_text.config(state='disabled')

        self.logs_text.config(state='normal')
        self.logs_text.delete('1.0', tk.END)
        self.logs_text.config(state='disabled')

    def resaltar_palabras_reservadas(self):
        for palabra in RESERVED:
            start_index = '1.0'
            while True:
                start_index = self.text_area.search(r'\m' + re.escape(palabra) + r'\M', start_index, stopindex=tk.END, regexp=True)
                if not start_index:
                    break
                end_index = f"{start_index}+{len(palabra)}c"
                self.text_area.tag_add("reservada", start_index, end_index)
                start_index = end_index
            self.text_area.tag_config("reservada", foreground="blue")

    def _on_key_release(self, event=None):
        """Maneja el evento de liberación de tecla."""
        self._update_line_numbers()
        self.resaltar_palabras_reservadas()

    def limpiar_resaltados(self):
        """Limpia cualquier resaltado de error previo."""
        self.text_area.tag_remove("error", "1.0", tk.END)
        self.line_numbers.tag_remove("error", "1.0", tk.END)

    def resaltar_linea_error(self, numero_linea):
        """Resalta la línea especificada debido a un error."""
        self.text_area.tag_add("error", f"{numero_linea}.0", f"{numero_linea}.0 lineend")
        self.text_area.tag_config("error", background="red")

        self.line_numbers.tag_add("error", f"{numero_linea}.0", f"{numero_linea}.0 lineend")
        self.line_numbers.tag_config("error", background="red")        