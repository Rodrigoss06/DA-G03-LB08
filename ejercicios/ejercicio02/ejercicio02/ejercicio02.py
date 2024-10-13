import reflex as rx
from typing import List, Dict

class State(rx.State):
    mostrar_solo_pendientes: bool = False
    contadores: Dict[str, int] = {"Pendiente": 0, "Completado": 0}
    tareas: List[Dict[str, str]] = [
        {"titulo": "Tarea 1", "estado": "Pendiente"},
        {"titulo": "Tarea 3", "estado": "Pendiente"},
        {"titulo": "Tarea 5", "estado": "Pendiente"},
        {"titulo": "Tarea 2", "estado": "Completado"},
        {"titulo": "Tarea 4", "estado": "Completado"},
    ]

    def mostrar_pendientes(self):
        self.mostrar_solo_pendientes = not self.mostrar_solo_pendientes

    def contar_tareas_por_estado(self):
        self.contadores = {"Pendiente": 0, "Completado": 0}
        for tarea in self.tareas:
            estado = tarea["estado"]
            if estado in self.contadores:
                self.contadores[estado] += 1

    def on_load(self):
        self.contar_tareas_por_estado()

def tarjeta_tarea(tarea: Dict[str, str]):
    return rx.table.row(
        rx.table.cell(tarea["titulo"]), 
        rx.table.cell(tarea["estado"]),
    )

def columna_kanban(nombre: str, estado_filtro: str):
    return (
        rx.vstack(
            rx.heading(nombre),
            rx.table.root(
                rx.table.body(
                    rx.foreach(
                        State.tareas, 
                        lambda tarea: rx.cond(
                            tarea["estado"] == estado_filtro,
                            tarjeta_tarea(tarea),
                            None  
                        )
                    )
                ),
            ),
        )
    )

def mostrar_contador():
    return rx.cond(
        State.mostrar_solo_pendientes,
        rx.text(f"Tareas Pendientes: {State.contadores['Pendiente']}", font_size="20px", margin="10px"),
        rx.text(f"Tareas Completadas: {State.contadores['Completado']}", font_size="20px", margin="10px")
    )

def index():
    return rx.cond(
        State.mostrar_solo_pendientes,
        rx.vstack(
            mostrar_contador(), 
            rx.button("Ver Tareas Completadas", on_click=State.mostrar_pendientes),
            columna_kanban("Pendientes", "Pendiente"),
            width="100%",
            justify="center",
            margin="20px"
        ),
        rx.vstack(
            mostrar_contador(),  
            rx.button("Ver Tareas Pendientes", on_click=State.mostrar_pendientes),
            columna_kanban("Completadas", "Completado"),
            width="100%",
            justify="center",
            margin="20px"
        ),
    )

app = rx.App()
app.add_page(index, on_load=State.on_load) 
