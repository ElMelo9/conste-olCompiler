# Importar el modelo y la vista
from models.tokenizer_models import Tokenizer
from models.tokens_models import TOKENS
from view.main_view import MainView

class MainController:
    def __init__(self, master=None):
        self.tokenizer = Tokenizer(TOKENS)
        self.view = MainView(master)
        self.view.set_compilar_command(self.procesar_texto)

    def procesar_texto(self):
        texto = self.view.get_codigo()
        resultados = self.tokenizer.analizar_declaraciones(texto, TOKENS)

        # Limpiar resaltados previos
        self.view.limpiar_resaltados()

        compilacion_exitosa = True

        for resultado in resultados:
            linea = resultado["linea"]
            resultado_linea = resultado["resultado"]
            logs = resultado_linea["logs"]
            consola = resultado_linea["consola"]

            self.view.registrar_log(f"Línea {linea}: {logs}")
            if "Error" in logs:
                self.view.resaltar_linea_error(linea)
                compilacion_exitosa = False
            if consola:
                self.view.imprimir_en_consola(consola)

        # Mensaje final de compilación
        mensaje_final = " ----- Compilado correctamente ----- " if compilacion_exitosa else " ----- Hubo un error al compilar ----- "
        self.view.imprimir_en_consola(mensaje_final)