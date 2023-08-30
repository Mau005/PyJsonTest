import tkinter as tk
import importlib
import os
import threading
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog
from datetime import datetime
TITTLE = "PyJsonTest V{} Module: {}"
__version__ = "1.0.1"


class DynamicModuleExecutor:
    def __init__(self, module_name):
        self.module_name = module_name
        self.module = None
        self.thread = None
        self.result = None

    def import_module(self):
        self.module = importlib.import_module(self.module_name)

    def execute_function(self, function_name, *args, **kwargs):
        if self.module is None:
            self.import_module()

        if hasattr(self.module, function_name):
            function = getattr(self.module, function_name)
            self.result = function(*args, **kwargs)

            return self.result
        else:
            raise AttributeError(f"La función {function_name} no existe en el módulo {self.module_name}")

    def start_thread(self, function_name, *args, **kwargs):
        self.thread = threading.Thread(target=self.execute_function, args=(function_name, *args), kwargs=kwargs)
        self.thread.start()

    def join_thread(self, callback=None):
        if self.thread is not None:
            self.thread.join()
        if callback is not None:
            callback(self.result)
        return self.result

    def destroy_module(self):
        del self.module

class Console_Custom(ScrolledText):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.tag_configure("info", foreground="blue")
        self.tag_configure("warning", foreground="yellow")
        self.tag_configure("error", foreground="red")
        self.tag_configure("debug", foreground="green")

    def error(self, value):
        self.__msg("error", value)

    def warning(self, value):
        self.__msg("warning", value)

    def debug(self, value):
        self.__msg("debug", value)

    def information(self, value):
        self.__msg("info", value)

    def magenta(self, value):
        self.__msg("magenta", value)

    def cyan(self, value):
        self.__msg("cyan", value)

    def white(self, value):
        self.__msg("white", value)

    def __msg(self, level, message):
        formatted = f"{datetime.now()} [{level.upper()}]: {message}"
        self.configure(state="normal")
        self.insert("end", formatted + "\n", level)
        self.configure(state="disabled")



class GUIApp:
    def __init__(self, root):
        self.consult = None #consult
        self.result = None #consult

        self.consult_compare = None #compare default
        self.consult_preview = None #compare default

        self.logger = None

        self.consult_result = None
        self.console = None

        self.root = root
        self.root.title(TITTLE.format(__version__, "Sin Modulo Agregado"))
        self.create_menu()
        self.create_tabs()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Cargar Archivo", command=self.load_file)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)

    def create_tabs(self):
        tab_control = ttk.Notebook(self.root)
        tab1 = ttk.Frame(tab_control)
        tab2 = ttk.Frame(tab_control)
        tab3 = ttk.Frame(tab_control)
        tab4 = ttk.Frame(tab_control)
        tab5 = ttk.Frame(tab_control)
        tab_control.add(tab1, text="Consultar")
        tab_control.add(tab2, text="Comparar Default")
        tab_control.add(tab3, text="Comprar Basado en Test")
        tab_control.add(tab4, text="Comparar Primitivos")
        tab_control.add(tab5, text="Configuracion")
        tab_control.pack(expand=1, fill="both")

        self.View_Consult(tab1)
        self.View_Compare_Default(tab2)

        self.Configure_Console()
        self.configure_tab(tab1, tab2,tab3,tab4,tab5)

    def Configure_Console(self):
        self.console = Console_Custom(self.root, wrap="word", state="disabled", height=8, background="black")
        self.console.pack(fill="both", expand=True, padx=10, pady=10)


    def View_Consult(self, tab:ttk.Frame):
        consult_label = tk.Label(tab, text="Consulta de Calculator")
        consult_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.consult = ScrolledText(tab)
        self.consult.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        generate_button = ttk.Button(tab, text="Generar", command=self.generate)
        generate_button.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        result_label = tk.Label(tab, text="Resultado Calculator")
        result_label.grid(row=0, column=2, padx=10, pady=5, sticky="w")

        self.consult_result = ScrolledText(tab)
        self.consult_result.grid(row=1, column=2, padx=10, pady=5, sticky="nsew")

    def View_Compare_Default(self, tab:ttk.Frame):
        consult_label = tk.Label(tab, text="Json de Comparación")
        consult_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.consult_compare = ScrolledText(tab)
        self.consult_compare.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        generate_button = ttk.Button(tab, text="Generar", command=self.generate)
        generate_button.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        result_label = tk.Label(tab, text="Vista Previa de la estructura")
        result_label.grid(row=0, column=2, padx=10, pady=5, sticky="w")

        self.consult_preview = ScrolledText(tab)
        self.consult_preview.grid(row=1, column=2, padx=10, pady=5, sticky="nsew")
        self.consult_preview.configure(state="disabled")

    def configure_tab(self, *args:ttk.Frame):
        for elements in args:
            elements.grid_rowconfigure(1, weight=1)
            elements.grid_columnconfigure(0, weight=1)
            elements.grid_columnconfigure(2, weight=1)

    def load_file(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos Py", "*.py")])
        if archivo:
            nombre_modulo = os.path.splitext(os.path.basename(archivo))[0]
            if self.execute_function(nombre_modulo):
                self.console.debug("Se ha agregado el Módulo correctamente")

    def callback_consult_procesing(self, value:str, *args):
        self.consult_result.delete("1.0", "end")
        self.consult_result.insert("1.0", value)

    def execute_function(self, name_module, name_fun="main") -> bool:
        executor = DynamicModuleExecutor(name_module)
        executor.start_thread(name_fun, self.consult.get("1.0", "end-1c"))

        executor.join_thread(callback=self.callback_consult_procesing)

        executor.destroy_module()

    def generate(self):
        json_content = self.consult.get("1.0", "end")
        try:
            # Aquí puedes implementar la lógica para generar el resultado deseado a partir del JSON
            result = "Resultado de generación"
        except Exception as e:
            result = str(e)
        self.console.delete("1.0", "end")
        self.console.insert("1.0", result)

    def comparar_primitivos(self):
        # Implementa la lógica para comparar primitivos aquí
        result = "Resultado de comparación"
        self.console.delete("1.0", "end")
        self.console.insert("1.0", result)

    def Print_Console(self, value:str):
        self.console.configure(state="normal")
        self.console.insert("1.0", value+'\n')
        self.console.configure(state="disabled")




if __name__ == "__main__":
    root = tk.Tk()
    app = GUIApp(root)
    root.mainloop()
