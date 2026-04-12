import customtkinter as ctk

# Aparência global (modo automático)
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

# 🎨 Paleta moderna
COLORS = {
    "bg_main": "#eef1f5",
    "bg_card": "#ffffff",
    "primary": "#0a84ff",
    "primary_hover": "#0066cc",
    "success": "#30d158",
    "success_hover": "#28b94f",
    "danger": "#ff453a",
    "danger_hover": "#d9362b",
    "text": "#1c1c1e",
    "subtext": "#8e8e93",
    "border": "#e5e5ea",
    "input_bg": "#f2f2f7"
}

# 🧾 Fontes
FONT_TITLE = ("SF Pro Display", 20, "bold")
FONT_LABEL = ("SF Pro Text", 13)
FONT_INPUT = ("SF Pro Text", 13)


# 🧊 Card com efeito de profundidade (simulação de sombra)
def card(master):
    outer = ctk.CTkFrame(master, fg_color="transparent")

    shadow = ctk.CTkFrame(
        outer,
        fg_color="#d1d1d6",
        corner_radius=14
    )
    shadow.pack(padx=2, pady=2)

    inner = ctk.CTkFrame(
        shadow,
        fg_color=COLORS["bg_card"],
        corner_radius=12
    )
    inner.pack(padx=2, pady=2)

    return inner


# ✏️ Input moderno
def input_field(master, textvariable=None, width=300, placeholder=""):
    return ctk.CTkEntry(
        master,
        textvariable=textvariable,
        width=width,
        placeholder_text=placeholder,
        fg_color=COLORS["input_bg"],
        border_color=COLORS["border"],
        corner_radius=8,
        height=34,
        font=FONT_INPUT
    )


# 🔵 Botão principal
def primary_button(master, text, command):
    return ctk.CTkButton(
        master,
        text=text,
        command=command,
        fg_color=COLORS["primary"],
        hover_color=COLORS["primary_hover"],
        text_color="#ffffff",
        corner_radius=10,
        height=36,
        font=("SF Pro Text", 13, "bold")
    )


# 🟢 Botão sucesso
def success_button(master, text, command):
    return ctk.CTkButton(
        master,
        text=text,
        command=command,
        fg_color=COLORS["success"],
        hover_color=COLORS["success_hover"],
        text_color="#ffffff",
        corner_radius=10,
        height=36,
        font=("SF Pro Text", 13, "bold")
    )


# 🔴 Botão perigo
def danger_button(master, text, command):
    return ctk.CTkButton(
        master,
        text=text,
        command=command,
        fg_color=COLORS["danger"],
        hover_color=COLORS["danger_hover"],
        text_color="#ffffff",
        corner_radius=10,
        height=36,
        font=("SF Pro Text", 13, "bold")
    )


# ⚪ Botão secundário (ideal para ações neutras como "Limpar")
def secondary_button(master, text, command):
    return ctk.CTkButton(
        master,
        text=text,
        command=command,
        fg_color="#e5e5ea",
        hover_color="#d1d1d6",
        text_color="#1c1c1e",
        corner_radius=10,
        height=36,
        font=("SF Pro Text", 13)
    )
