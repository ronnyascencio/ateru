import flet as ft
from pathlib import Path
from ateru.core.api import scan_shots, scan_projects
import ateru.ui.manager.styles as st


class ShotCard(ft.Container):
    def __init__(self, shot_name, on_select):
        super().__init__()
        self.shot_name = shot_name
        self.on_select = on_select

        self.content = ft.Text(
            shot_name,
            weight=ft.FontWeight.W_500,
            color=st.PAPER_WHITE,
        )
        self.bgcolor = st.CARBON_GRAY
        self.padding = 20
        self.border_radius = 5
        # Corregido: ft.Border.all en minúsculas
        self.border = ft.Border.all(1, st.BAMBOO_GREEN)
        self.on_click = self.handle_click

    def handle_click(self, e):
        self.on_select(self)


class ShotsView(ft.Column):
    def __init__(self):
        super().__init__(expand=True)
        self.selected_card = None

        # 1. Obtener proyectos para el Dropdown
        projects = scan_projects()

        self.project_dd = ft.Dropdown(
            label="Select Project",
            width=300,
            bgcolor=st.CARBON_GRAY,  # Fondo sutil (Gris Carbón)
            border_color=st.WARM_GRAY,  # Borde discreto (Gris Cálido)
            border_width=1,
            border_radius=4,  # Menos redondeado, más técnico
            focused_border_color=st.BAMBOO_GREEN,  # Solo brilla al hacer clic
            label_style=ft.TextStyle(color=st.WARM_GRAY),
            color=st.PAPER_WHITE,
            options=[ft.dropdown.Option(p) for p in projects],
            on_select=self.on_project_changed, 
        )
        
        

        self.header = ft.Container(
            content=ft.Column(
                controls=[

                    ft.Row(
                        controls=[
                            ft.Text(
                                "SHOTS",
                                size=30,
                                weight=ft.FontWeight.W_500,
                                color=st.PAPER_WHITE,
                            ),
                            ft.Button(
                                content="new shot",  
                                style=st.PRIMARY_BUTTON, 
                                on_click=self.create_shot_action,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),

                    ft.Container(height=10),
                    ft.Divider(color="white10"),

                    ft.Row(
                        controls=[
                            self.project_dd,
                        ],
                    ),
                ],
                spacing=0,
            ),
            padding=ft.Padding.only(bottom=10),
        )


        self.grid = ft.GridView(
            expand=True,
            runs_count=3,
            max_extent=250,
            spacing=10,
            run_spacing=10,
        )

        self.controls = [
            self.header,
            self.grid,
        ]

    def on_project_changed(self, e):
        project_name = self.project_dd.value
        if not project_name:
            return

        self.grid.controls.clear()

        shots = scan_shots(project_name=project_name)

        for shot in shots:
            card = ShotCard(shot_name=shot, on_select=self.handle_card_selection)
            self.grid.controls.append(card)

        self.update()

    def handle_card_selection(self, card):
        if self.selected_card:
            self.selected_card.Border = ft.Border.all(1, "transparent")
            self.selected_card.bgcolor = "white10"

        self.selected_card = card
        card.border = ft.Border.all(2, "#C7D66D")
        card.bgcolor = "white24"
        self.update()

    def create_shot_action(self, e):
        if not self.project_dd.value:
            print("Error: Selecciona un proyecto primero")
            return
        print(f"Creando shot en: {self.project_dd.value}")
