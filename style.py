import customtkinter as ctk

# Aparência global (modo claro estilo macOS)
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Paleta inspirada no macOS
COLORS = {
    "bg_main": "#f5f5f7",
    "bg_card": "#ffffff",
    "primary": "#007aff",   # azul Apple
    "success": "#34c759",
    "danger": "#ff3b30",
    "warning": "#ff9f0a",
    "text": "#1c1c1e",
    "subtext": "#6e6e73",
    "border": "#d1d1d6"
}

FONT_TITLE = ("SF Pro Display", 18, "bold")
FONT_LABEL = ("SF Pro Text", 12)
FONT_INPUT = ("SF Pro Text", 12)


def card(master):
    """Frame estilo 'card'"""
    return ctk.CTkFrame(
        master,
        fg_color=COLORS["bg_card"],
        corner_radius=12,
        border_width=1,
        border_color=COLORS["border"]
    )


def primary_button(master, text, command):
    return ctk.CTkButton(
        master,
        text=text,
        command=command,
        fg_color=COLORS["primary"],
        hover_color="#005ecb",
        corner_radius=8
    )


def danger_button(master, text, command):
    return ctk.CTkButton(
        master,
        text=text,
        command=command,
        fg_color=COLORS["danger"],
        hover_color="#d9362b",
        corner_radius=8
    )


def success_button(master, text, command):
    return ctk.CTkButton(
        master,
        text=text,
        command=command,
        fg_color=COLORS["success"],
        hover_color="#28a745",
        corner_radius=8
    )
