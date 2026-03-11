from turtle import bgcolor
import flet as ft
import ateru.ui.manager.styles as st
from ateru.core.api import list_projects
from ateru.ui.manager.views.projects_view import ProjectsView
from ateru.ui.manager.views.shots_view import ShotsView


def main(page: ft.Page):
    page.title = "Ateru Pipeline Manager"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.spacing = 0
    page.window.width = 1100
    page.window.height = 600
    page.window.icon = "assets/icons/ateru_icon.png"
    page.window.title_bar_hidden = False
    page.bgcolor = st.SUMI_BLACK

    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=st.BAMBOO_GREEN,
            surface=st.CARBON_GRAY,
            on_surface=st.PAPER_WHITE,
            outline=st.WARM_GRAY,
        )
    )

    def view_assets():
        # CORRECCIÓN: Usamos 'label' en lugar de 'text' para los Tabs
        return ft.Column(
            controls=[
                ft.Text("ASSETS", size=30, weight="bold", color="green700"),
                ft.Tabs(
                    length=3,
                    selected_index=1,
                    content=ft.Column(spacing=8, controls=["tab_bar", "tab_view"]),
                ),
                ft.Container(
                    content=ft.Text(
                        "Explorador de libreria de assets...",
                    ),
                    padding=20,
                ),
            ],
            expand=True,
        )

    # --- LÓGICA DE NAVEGACIÓN ---

    def change_view(view_name):
        central_container.content = None  # Limpiamos memoria
        if view_name == "PROJECTS":
            central_container.content = ProjectsView()
        elif view_name == "SHOTS":
            central_container.content = ShotsView()
        elif view_name == "ASSETS":
            central_container.content = view_assets()
        page.update()

    def show_settings(e):
        central_container.content = ft.Column(
            controls=[
                ft.Text("settings", size=30, weight="bold", color="blue400"),
                ft.Text("Configuracion global del pipeline Ateru", color="grey"),
                ft.Divider(height=20, color="white10"),
                ft.TextField(
                    label="Ruta de Proyectos", value="X:/Dropbox/pipeline/ateru"
                ),
            ]
        )
        page.update()

    # --- COLUMNA 1: SIDEBAR (Botones Manuales) ---

    # Creamos botones simples. Usamos lambda para pasar el nombre de la vista.
    btn_projects = ft.TextButton(
        content="projects", on_click=lambda _: change_view("PROJECTS")
    )
    btn_shots = ft.TextButton(content="shots", on_click=lambda _: change_view("SHOTS"))
    btn_assets = ft.TextButton(
        content="assets", on_click=lambda _: change_view("ASSETS")
    )

    sidebar = ft.Container(
        content=ft.Column(
            controls=[
                ft.Image(
                    src="icons/ateru.svg",
                    width=20,
                    height=20,
                ),
                # Lista de botones de navegación
                ft.Column(
                    controls=[
                        btn_projects,
                        btn_shots,
                        btn_assets,
                    ],
                    spacing=10,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(expand=True, bgcolor="242424"),  # Espacio intermedio
                # Parte inferior: Settings + Usuario
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.TextButton(
                                content="SETTINGS",
                                on_click=show_settings,
                                icon_color="#FFFEF7",
                            ),
                            ft.Divider(color="white10"),
                            ft.Container(
                                content=ft.Text(
                                    "USER: RONNY", size=10, weight=ft.FontWeight.W_600
                                ),
                                padding=10,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=10,
                    bgcolor="#242424",
                ),
            ],
            spacing=0,
        ),
        width=150,  # Aumentado un poco para que los botones quepan bien
        bgcolor="#1C1C1C",
    )

    # --- COLUMNA 2: CONTENIDO CENTRAL ---
    central_container = ft.Container(
        content=ProjectsView(),
        expand=True,
        padding=30,
        bgcolor="#1C1C1C",
    )

    # --- COLUMNA 3: INFO BAR ---
    info_bar = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Details", weight="bold", color="#FFFEF7", size=14),
                ft.Divider(color="white10"),
                ft.Text("Domi info", italic=True, color="grey400"),
            ]
        ),
        width=250,
        bgcolor="#242424",
        padding=20,
    )

    # --- COMPOSICIÓN FINAL ---
    layout = ft.Row(
        controls=[sidebar, central_container, info_bar], expand=True, spacing=0
    )

    page.add(layout)
    page.add(ft.Text("Bienvenido a Ateru"))


if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
