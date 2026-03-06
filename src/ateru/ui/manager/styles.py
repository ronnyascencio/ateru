import flet as ft

# --- PALETA JAPONESA (CÓDIGOS HEX) ---
SUMI_BLACK = "#1C1C1C"
CARBON_GRAY = "#242424"
PAPER_WHITE = "#FFFEF7"
WARM_GRAY = "#B8B5A9"
BAMBOO_GREEN = "#C7D66D"
MOSS_GREEN = "#A9BF4F"
CARMINE_RED = "#B44949"
INK_BLUE = "#4F6D8C"
CARD_NORMAL_BG = "#242424"    # CARBON_GRAY
CARD_HOVER_BG = "#2B2B2B"     # Un gris apenas más claro para el feedback
CARD_BORDER_COLOR = "#333333"

# --- BOTÓN PRIMARIO (Launch, Publish) ---
PRIMARY_BUTTON = ft.ButtonStyle(
    color=SUMI_BLACK,
    bgcolor={
        ft.ControlState.DEFAULT: BAMBOO_GREEN,
        ft.ControlState.HOVERED: MOSS_GREEN,
    },
    shape=ft.RoundedRectangleBorder(radius=4),
)

# --- BOTÓN SECUNDARIO (Settings, Cancel) ---
SECONDARY_BUTTON = ft.ButtonStyle(
    color=PAPER_WHITE,
    bgcolor={
        ft.ControlState.DEFAULT: "#2A2A2A",
        ft.ControlState.HOVERED: "#303030",
    },
    side={ft.ControlState.DEFAULT: ft.BorderSide(1, "#3A3A3A")},
    shape=ft.RoundedRectangleBorder(radius=4),
)

# --- ESTILO DE SELECCIÓN (Regla 4) ---
def get_selection_style():
    return {
        "bgcolor": "rgba(199, 214, 109, 0.15)",
        "border": ft.border.only(left=ft.BorderSide(3, BAMBOO_GREEN)),
    }