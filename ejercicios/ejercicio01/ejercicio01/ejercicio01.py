import reflex as rx


class State(rx.State):
    mostrar_solo_pendientes: bool = False

    def mostrar_pendientes(self):
        self.mostrar_solo_pendientes = not self.mostrar_solo_pendientes



tareas_pendientes = [
    {"titulo": "Tarea 1", "estado": "Pendiente"},
    {"titulo": "Tarea 3", "estado": "Pendiente"},
    {"titulo": "Tarea 5", "estado": "Pendiente"},
]
tareas_completas = [
    {"titulo": "Tarea 2", "estado": "Completado"},
    {"titulo": "Tarea 4", "estado": "Completado"},
]


def tarjeta_tarea(tarea):
    return rx.table.row(
        rx.table.cell(tarea["titulo"]),
        rx.table.cell(tarea["estado"]),
    )


def columna_kanban(nombre, tareas):
    return (
        rx.hstack(
            rx.heading(nombre),
            rx.table.root(
                rx.table.body(
                    rx.foreach(
                        tareas,
                        tarjeta_tarea,
                    )
                ),
            ),
        ),
    )


def index():
    return rx.cond(
        State.mostrar_solo_pendientes,
        rx.flex(
            rx.button("Ver Tareas Completadas", on_click=State.mostrar_pendientes),
            columna_kanban("En Progreso", tareas_pendientes),
            width="100%",
            justify="center",
            margin="20px"
        ),
        rx.hstack(
            rx.button("Ver Tareas Pendientes", on_click=State.mostrar_pendientes),
            columna_kanban("Completadas", tareas_completas),
                        width="100%",
            justify="center",
            margin="20px"
            
        ),
    )


app = rx.App()
app.add_page(index)
