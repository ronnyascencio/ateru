import flet as ft
from pathlib import Path
from ateru.core.api import scan_projects
import ateru.ui.manager.styles as st

import flet as ft
from pathlib import Path
# Asumimos que list_projects devuelve una lista de objetos o strings
# de los proyectos encontrados en el disco.
# from ateru.core.api import list_projects


class ProjectCard(ft.Container):
    """Componente individual para cada proyecto en el Grid"""

    def __init__(self, project_name, on_select):
        super().__init__()
        self.project_name = project_name
        self.on_select = on_select  # Callback para avisar al padre

        self.content = ft.Text(
            f"{project_name}", weight=ft.FontWeight.W_500, color=st.PAPER_WHITE
        )
        self.bgcolor = st.CARBON_GRAY
        self.padding = 20
        self.border_radius = 5
        self.border = ft.Border.all(1, "#2A2A2A")
        self.on_click = self.handle_click

    def handle_click(self, e):
        self.on_select(self)


class ProjectsView(ft.Column):
    def __init__(
        self,
    ):
        super().__init__(expand=True)

        self.selected_card = None  # Para rastrear cuál está seleccionado

        # Simulación de carga (reemplazar con tu list_projects real)
        projects_path = Path("X:/projects")
        projects = scan_projects()

        # 1. Header
        self.header = ft.Row(
            controls=[
                ft.Text(
                    "PROJECTS",
                    size=30,
                    weight=ft.FontWeight.W_500,
                    color=st.PAPER_WHITE,
                ),
                ft.Button(
                    content="new",
                    style=st.PRIMARY_BUTTON,
                    on_click=self.create_project_dialog,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        # 2. Grid de Proyectos
        self.grid = ft.GridView(
            expand=True,
            runs_count=3,
            max_extent=250,
            spacing=10,
            run_spacing=10,
        )

        # Llenamos el grid usando nuestra clase ProjectCard
        #
        for project in projects:
            card = ProjectCard(
                project_name=project, on_select=self.handle_card_selection
            )
            self.grid.controls.append(card)

        self.controls = [
            self.header,
            ft.Divider(color="white10"),
            self.grid,
        ]

    def handle_card_selection(self, card):
        """Maneja el resaltado visual y actualiza el panel de info"""
        # Deseleccionar el anterior
        if self.selected_card:
            self.selected_card.border = ft.Border.all(1, "transparent")
            self.selected_card.bgcolor = "white10"

        # Seleccionar el nuevo
        self.selected_card = card
        card.border = ft.Border.all(2, "#C7D66D")  # Estilo Ateru
        card.bgcolor = "white24"

        # Actualizar el panel derecho (InfoBar)
        # Asumiendo que tu InfoBar tiene un método llamado 'display_info'
        # if self.info_panel:
        #     self.info_panel.display_info(
        #         title=card.project_name,
        #         details=f"Path: X:/projects/{card.project_name}\nStatus: Active",
        #     )

        self.update()

    def create_project_dialog(self, e):
        print(f"Abriendo diálogo para nuevo proyecto en la vista de Proyectos")
