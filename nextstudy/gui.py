"""Moderne Desktop-Oberflaeche fuer NextStudy.

Die GUI nutzt nur `tkinter` aus der Python-Standardbibliothek. Abgerundete
Panels und Buttons werden bewusst selbst gezeichnet, damit das Projekt ohne
zusaetzliche Installation professionell aussieht und trotzdem ueberall laeuft.
"""

from __future__ import annotations

import platform
import tkinter as tk
from datetime import date
from pathlib import Path
from tkinter import filedialog, messagebox
from typing import Callable

from nextstudy.models import Difficulty, Status, StudyPlan, StudyUnit, Subject
from nextstudy.planner import StudyPlanner
from nextstudy.storage import DEFAULT_PLAN_PATH, JsonPlanStorage


ColorMap = dict[str, str]

COLORS: ColorMap = {
    "background": "#151719",
    "surface": "#202326",
    "surface_high": "#282C30",
    "field": "#111315",
    "border": "#3A3F44",
    "text": "#F4F1EA",
    "muted": "#A7ADA9",
    "primary": "#2F8F6B",
    "primary_hover": "#38A77E",
    "accent": "#D8A24A",
    "danger": "#C76E64",
    "done": "#63B179",
    "progress": "#C7A15C",
}


def font(size: int, weight: str = "normal") -> tuple[str, int, str]:
    family = ".AppleSystemUIFont" if platform.system() == "Darwin" else "Segoe UI"
    return family, size, weight


def draw_rounded_rect(
    canvas: tk.Canvas,
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    radius: int,
    *,
    fill: str,
    outline: str = "",
    width: int = 1,
    tags: str | tuple[str, ...] = (),
) -> None:
    """Zeichnet ein echtes Rechteck mit runden Ecken auf ein Canvas."""

    radius = max(0, min(radius, (x2 - x1) // 2, (y2 - y1) // 2))
    points = [
        x1 + radius,
        y1,
        x2 - radius,
        y1,
        x2,
        y1,
        x2,
        y1 + radius,
        x2,
        y2 - radius,
        x2,
        y2,
        x2 - radius,
        y2,
        x1 + radius,
        y2,
        x1,
        y2,
        x1,
        y2 - radius,
        x1,
        y1 + radius,
        x1,
        y1,
    ]
    canvas.create_polygon(
        points,
        smooth=True,
        splinesteps=18,
        fill=fill,
        outline=outline,
        width=width,
        tags=tags,
    )


class RoundedPanel(tk.Canvas):
    """Canvas-Panel mit abgerundetem Hintergrund und normalem Frame-Inhalt."""

    def __init__(
        self,
        master: tk.Misc,
        *,
        radius: int = 22,
        padding: int = 20,
        fill: str = COLORS["surface"],
        border: str = COLORS["border"],
        **kwargs: object,
    ) -> None:
        super().__init__(
            master,
            bg=COLORS["background"],
            bd=0,
            highlightthickness=0,
            relief="flat",
            **kwargs,
        )
        self.radius = radius
        self.padding = padding
        self.fill = fill
        self.border = border
        self.inner = tk.Frame(self, bg=fill)
        self._window = self.create_window(
            padding,
            padding,
            anchor="nw",
            window=self.inner,
        )
        self.bind("<Configure>", self._redraw)

    def _redraw(self, event: tk.Event) -> None:
        self.delete("panel")
        draw_rounded_rect(
            self,
            1,
            1,
            max(2, event.width - 1),
            max(2, event.height - 1),
            self.radius,
            fill=self.fill,
            outline=self.border,
            tags="panel",
        )
        self.tag_lower("panel")
        self.coords(self._window, self.padding, self.padding)
        self.itemconfigure(
            self._window,
            width=max(1, event.width - self.padding * 2),
            height=max(1, event.height - self.padding * 2),
        )


class RoundedButton(tk.Canvas):
    """Schlichter Button mit runden Ecken, Hover-Zustand und Tastaturfokus."""

    def __init__(
        self,
        master: tk.Misc,
        text: str,
        command: Callable[[], None],
        *,
        width: int = 150,
        height: int = 42,
        fill: str = COLORS["primary"],
        hover_fill: str = COLORS["primary_hover"],
        text_color: str = COLORS["text"],
        border: str = "",
        radius: int = 16,
        font_size: int = 11,
    ) -> None:
        super().__init__(
            master,
            width=width,
            height=height,
            bg=master.cget("bg"),
            bd=0,
            highlightthickness=0,
            cursor="hand2",
        )
        self.command = command
        self.normal_fill = fill
        self.hover_fill = hover_fill
        self.text_color = text_color
        self.border = border
        self.radius = radius
        self.label = text
        self.font_size = font_size
        self._active = True
        self._current_fill = fill

        self.bind("<Enter>", lambda _event: self._draw(self.hover_fill))
        self.bind("<Leave>", lambda _event: self._draw(self.normal_fill))
        self.bind("<Button-1>", self._handle_click)
        self.bind("<Return>", self._handle_click)
        self.bind("<space>", self._handle_click)
        self.bind("<Configure>", lambda _event: self._draw(self._current_fill))
        self.configure(takefocus=True)
        self._draw(self.normal_fill)

    def _draw(self, fill: str) -> None:
        self._current_fill = fill
        self.delete("all")
        width = max(self.winfo_width(), int(self.cget("width")))
        height = max(self.winfo_height(), int(self.cget("height")))
        draw_rounded_rect(
            self,
            1,
            1,
            width - 1,
            height - 1,
            self.radius,
            fill=fill if self._active else COLORS["surface_high"],
            outline=self.border,
            tags="shape",
        )
        self.create_text(
            width // 2,
            height // 2,
            text=self.label,
            fill=self.text_color if self._active else COLORS["muted"],
            font=font(self.font_size, "bold"),
        )

    def _handle_click(self, _event: tk.Event) -> None:
        if self._active:
            self.command()

    def set_enabled(self, enabled: bool) -> None:
        self._active = enabled
        self.configure(cursor="hand2" if enabled else "arrow")
        self._draw(self.normal_fill)

    def set_style(
        self,
        *,
        fill: str | None = None,
        hover_fill: str | None = None,
        text_color: str | None = None,
        border: str | None = None,
    ) -> None:
        if fill is not None:
            self.normal_fill = fill
        if hover_fill is not None:
            self.hover_fill = hover_fill
        if text_color is not None:
            self.text_color = text_color
        if border is not None:
            self.border = border
        self._draw(self.normal_fill)


class ScrollFrame(tk.Frame):
    """Scrollbarer Bereich fuer Tageskarten und Themenlisten."""

    def __init__(self, master: tk.Misc, *, bg: str = COLORS["background"]) -> None:
        super().__init__(master, bg=bg)
        self.canvas = tk.Canvas(self, bg=bg, bd=0, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(
            self,
            orient="vertical",
            command=self.canvas.yview,
            width=12,
            bg=COLORS["background"],
            troughcolor=COLORS["background"],
            activebackground=COLORS["primary"],
            relief="flat",
        )
        self.inner = tk.Frame(self.canvas, bg=bg)
        self.window = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.inner.bind("<Configure>", self._update_scroll_region)
        self.canvas.bind("<Configure>", self._resize_inner)
        self.canvas.bind("<Enter>", self._bind_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_mousewheel)

    def clear(self) -> None:
        for child in self.inner.winfo_children():
            child.destroy()

    def _update_scroll_region(self, _event: tk.Event) -> None:
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _resize_inner(self, event: tk.Event) -> None:
        self.canvas.itemconfigure(self.window, width=event.width)

    def _bind_mousewheel(self, _event: tk.Event) -> None:
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

    def _unbind_mousewheel(self, _event: tk.Event) -> None:
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def _on_mousewheel(self, event: tk.Event) -> None:
        if getattr(event, "num", None) == 4:
            self.canvas.yview_scroll(-1, "units")
        elif getattr(event, "num", None) == 5:
            self.canvas.yview_scroll(1, "units")
        else:
            delta = -1 if event.delta > 0 else 1
            self.canvas.yview_scroll(delta * 3, "units")


class NextStudyGui:
    """Grafische Anwendung fuer Fach, Themen, Planung und Fortschritt."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("NextStudy")
        self.root.geometry("1240x780")
        self.root.minsize(1040, 680)
        self.root.configure(bg=COLORS["background"])

        self.planner = StudyPlanner()
        self.storage = JsonPlanStorage()
        self.subject: Subject | None = None
        self.plan: StudyPlan | None = None
        self.topic_rows: list[tuple[str, Difficulty]] = []

        self.subject_var = tk.StringVar()
        self.topic_var = tk.StringVar()
        self.difficulty_var = tk.StringVar(value=Difficulty.MEDIUM.value)
        self.days_var = tk.StringVar(value="5")
        self.minutes_var = tk.StringVar(value="60")
        self.exam_date_var = tk.StringVar()
        self.difficulty_buttons: dict[Difficulty, RoundedButton] = {}

        self._configure_window_grid()
        self._build_sidebar()
        self._build_workspace()
        self._refresh_topics()
        self._refresh_plan()

    def _configure_window_grid(self) -> None:
        self.root.grid_columnconfigure(0, minsize=390, weight=0)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

    def _build_sidebar(self) -> None:
        sidebar = tk.Frame(self.root, bg=COLORS["background"], padx=24, pady=24)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_rowconfigure(2, weight=1)

        tk.Label(
            sidebar,
            text="NextStudy",
            bg=COLORS["background"],
            fg=COLORS["text"],
            font=font(28, "bold"),
        ).grid(row=0, column=0, sticky="w")
        tk.Label(
            sidebar,
            text="Lernplaner",
            bg=COLORS["background"],
            fg=COLORS["muted"],
            font=font(12),
        ).grid(row=1, column=0, sticky="w", pady=(0, 18))

        form_panel = RoundedPanel(sidebar, height=600, fill=COLORS["surface"], padding=18)
        form_panel.grid(row=2, column=0, sticky="nsew")
        form_panel.inner.grid_columnconfigure(0, weight=1)

        self._build_form(form_panel.inner)

    def _build_form(self, parent: tk.Frame) -> None:
        tk.Label(
            parent,
            text="Plan erstellen",
            bg=COLORS["surface"],
            fg=COLORS["text"],
            font=font(17, "bold"),
        ).grid(row=0, column=0, sticky="w")

        self._add_labeled_entry(parent, "Fach", self.subject_var, row=1)
        self._add_labeled_entry(parent, "Thema", self.topic_var, row=2)

        difficulty_row = tk.Frame(parent, bg=COLORS["surface"])
        difficulty_row.grid(row=3, column=0, sticky="ew", pady=(10, 8))
        for column in range(3):
            difficulty_row.grid_columnconfigure(column, weight=1)
        for index, difficulty in enumerate(Difficulty):
            button = RoundedButton(
                difficulty_row,
                difficulty.value.title(),
                command=lambda item=difficulty: self._set_difficulty(item),
                width=96,
                height=34,
                fill=COLORS["surface_high"],
                hover_fill=COLORS["border"],
                border=COLORS["border"],
                radius=14,
                font_size=10,
            )
            button.grid(row=0, column=index, sticky="ew", padx=(0 if index == 0 else 6, 0))
            self.difficulty_buttons[difficulty] = button
        self._refresh_difficulty_buttons()

        RoundedButton(
            parent,
            "Thema hinzufuegen",
            command=self._add_topic,
            width=310,
            height=42,
            fill=COLORS["primary"],
            hover_fill=COLORS["primary_hover"],
        ).grid(row=4, column=0, sticky="ew", pady=(4, 14))

        self.topic_list = ScrollFrame(parent, bg=COLORS["surface"])
        self.topic_list.grid(row=5, column=0, sticky="ew")
        self.topic_list.configure(height=118)
        self.topic_list.grid_propagate(False)

        details = tk.Frame(parent, bg=COLORS["surface"])
        details.grid(row=6, column=0, sticky="ew", pady=(18, 0))
        details.grid_columnconfigure(0, weight=1)
        details.grid_columnconfigure(1, weight=1)

        self._add_compact_entry(details, "Tage", self.days_var, row=0, column=0)
        self._add_compact_entry(details, "Minuten", self.minutes_var, row=0, column=1)
        self._add_labeled_entry(
            parent,
            "Pruefungstermin",
            self.exam_date_var,
            row=7,
        )

        actions = tk.Frame(parent, bg=COLORS["surface"])
        actions.grid(row=8, column=0, sticky="ew", pady=(18, 0))
        actions.grid_columnconfigure(0, weight=1)
        actions.grid_columnconfigure(1, weight=1)

        RoundedButton(
            actions,
            "Plan erstellen",
            command=self._create_plan,
            width=148,
            height=44,
            fill=COLORS["accent"],
            hover_fill="#E2B766",
            text_color="#151719",
        ).grid(row=0, column=0, sticky="ew", padx=(0, 8))
        RoundedButton(
            actions,
            "Zuruecksetzen",
            command=self._reset_form,
            width=148,
            height=44,
            fill=COLORS["surface_high"],
            hover_fill=COLORS["border"],
            border=COLORS["border"],
        ).grid(row=0, column=1, sticky="ew")

        file_actions = tk.Frame(parent, bg=COLORS["surface"])
        file_actions.grid(row=9, column=0, sticky="ew", pady=(12, 0))
        file_actions.grid_columnconfigure(0, weight=1)
        file_actions.grid_columnconfigure(1, weight=1)

        RoundedButton(
            file_actions,
            "Speichern",
            command=self._save_plan,
            width=148,
            height=38,
            fill=COLORS["surface_high"],
            hover_fill=COLORS["border"],
            border=COLORS["border"],
            font_size=10,
        ).grid(row=0, column=0, sticky="ew", padx=(0, 8))
        RoundedButton(
            file_actions,
            "Laden",
            command=self._load_plan,
            width=148,
            height=38,
            fill=COLORS["surface_high"],
            hover_fill=COLORS["border"],
            border=COLORS["border"],
            font_size=10,
        ).grid(row=0, column=1, sticky="ew")

    def _build_workspace(self) -> None:
        workspace = tk.Frame(self.root, bg=COLORS["background"], padx=(0, 24), pady=24)
        workspace.grid(row=0, column=1, sticky="nsew")
        workspace.grid_columnconfigure(0, weight=1)
        workspace.grid_rowconfigure(2, weight=0)

        self.title_label = tk.Label(
            workspace,
            text="Noch kein Lernplan",
            bg=COLORS["background"],
            fg=COLORS["text"],
            font=font(25, "bold"),
        )
        self.title_label.grid(row=0, column=0, sticky="w")

        self.subtitle_label = tk.Label(
            workspace,
            text="Fach und Themen eintragen, dann den Plan erstellen.",
            bg=COLORS["background"],
            fg=COLORS["muted"],
            font=font(12),
        )
        self.subtitle_label.grid(row=1, column=0, sticky="w", pady=(2, 16))

        self.stats_frame = tk.Frame(workspace, bg=COLORS["background"])
        self.stats_frame.grid(row=2, column=0, sticky="new")

        self.plan_scroll = ScrollFrame(workspace, bg=COLORS["background"])
        self.plan_scroll.grid(row=3, column=0, sticky="nsew", pady=(18, 0))
        workspace.grid_rowconfigure(3, weight=1)

    def _add_labeled_entry(
        self,
        parent: tk.Frame,
        label: str,
        variable: tk.StringVar,
        *,
        row: int,
    ) -> None:
        wrapper = tk.Frame(parent, bg=COLORS["surface"])
        wrapper.grid(row=row, column=0, sticky="ew", pady=(14, 0))
        wrapper.grid_columnconfigure(0, weight=1)

        tk.Label(
            wrapper,
            text=label,
            bg=COLORS["surface"],
            fg=COLORS["muted"],
            font=font(10, "bold"),
        ).grid(row=0, column=0, sticky="w", pady=(0, 6))

        entry = tk.Entry(
            wrapper,
            textvariable=variable,
            bg=COLORS["field"],
            fg=COLORS["text"],
            insertbackground=COLORS["text"],
            relief="flat",
            bd=0,
            font=font(12),
        )
        entry.grid(row=1, column=0, sticky="ew", ipady=10)

    def _add_compact_entry(
        self,
        parent: tk.Frame,
        label: str,
        variable: tk.StringVar,
        *,
        row: int,
        column: int,
    ) -> None:
        wrapper = tk.Frame(parent, bg=COLORS["surface"])
        wrapper.grid(row=row, column=column, sticky="ew", padx=(0 if column == 0 else 8, 0))
        wrapper.grid_columnconfigure(0, weight=1)

        tk.Label(
            wrapper,
            text=label,
            bg=COLORS["surface"],
            fg=COLORS["muted"],
            font=font(10, "bold"),
        ).grid(row=0, column=0, sticky="w", pady=(0, 6))
        tk.Entry(
            wrapper,
            textvariable=variable,
            bg=COLORS["field"],
            fg=COLORS["text"],
            insertbackground=COLORS["text"],
            relief="flat",
            bd=0,
            font=font(12),
        ).grid(row=1, column=0, sticky="ew", ipady=10)

    def _set_difficulty(self, difficulty: Difficulty) -> None:
        self.difficulty_var.set(difficulty.value)
        self._refresh_difficulty_buttons()

    def _refresh_difficulty_buttons(self) -> None:
        selected = Difficulty.parse(self.difficulty_var.get())
        for difficulty, button in self.difficulty_buttons.items():
            is_selected = difficulty == selected
            button.set_style(
                fill=COLORS["primary"] if is_selected else COLORS["surface_high"],
                hover_fill=COLORS["primary_hover"] if is_selected else COLORS["border"],
                text_color=COLORS["text"],
                border=COLORS["primary"] if is_selected else COLORS["border"],
            )

    def _add_topic(self) -> None:
        name = self.topic_var.get().strip()
        if not name:
            self._show_error("Bitte gib zuerst ein Thema ein.")
            return

        try:
            difficulty = Difficulty.parse(self.difficulty_var.get())
        except ValueError as error:
            self._show_error(str(error))
            return

        self.topic_rows.append((name, difficulty))
        self.topic_var.set("")
        self._refresh_topics()

    def _remove_topic(self, index: int) -> None:
        del self.topic_rows[index]
        self._refresh_topics()

    def _refresh_topics(self) -> None:
        for child in self.topic_list.inner.winfo_children():
            child.destroy()

        if not self.topic_rows:
            tk.Label(
                self.topic_list.inner,
                text="Noch keine Themen angelegt.",
                bg=COLORS["surface"],
                fg=COLORS["muted"],
                font=font(10),
            ).pack(anchor="w")
            return

        for index, (name, difficulty) in enumerate(self.topic_rows):
            row = tk.Frame(self.topic_list.inner, bg=COLORS["surface_high"], padx=10, pady=8)
            row.pack(fill="x", pady=(0, 8))
            row.grid_columnconfigure(0, weight=1)

            tk.Label(
                row,
                text=name,
                bg=COLORS["surface_high"],
                fg=COLORS["text"],
                font=font(11, "bold"),
                anchor="w",
            ).grid(row=0, column=0, sticky="ew")
            tk.Label(
                row,
                text=difficulty.value,
                bg=COLORS["surface_high"],
                fg=COLORS["muted"],
                font=font(9),
            ).grid(row=1, column=0, sticky="w")
            tk.Button(
                row,
                text="Entfernen",
                command=lambda item_index=index: self._remove_topic(item_index),
                bg=COLORS["surface_high"],
                fg=COLORS["danger"],
                activebackground=COLORS["surface_high"],
                activeforeground=COLORS["danger"],
                relief="flat",
                bd=0,
                cursor="hand2",
                font=font(9, "bold"),
            ).grid(row=0, column=1, rowspan=2, sticky="e")

    def _create_plan(self) -> None:
        try:
            subject = self._build_subject_from_form()
            days = self._read_positive_int(self.days_var.get(), "Lerntage", minimum=1)
            minutes = self._read_positive_int(self.minutes_var.get(), "Minuten pro Tag", minimum=15)
            exam_date = self._read_exam_date()
            self.plan = self.planner.create_plan(subject, days, minutes, exam_date)
            self.subject = subject
        except ValueError as error:
            self._show_error(str(error))
            return

        self._refresh_plan()

    def _build_subject_from_form(self) -> Subject:
        name = self.subject_var.get().strip()
        if not name:
            raise ValueError("Bitte gib ein Fach ein.")
        if not self.topic_rows:
            raise ValueError("Bitte fuege mindestens ein Thema hinzu.")

        subject = Subject(name)
        for topic_name, difficulty in self.topic_rows:
            subject.add_topic(topic_name, difficulty)
        return subject

    def _read_positive_int(self, value: str, label: str, *, minimum: int) -> int:
        try:
            number = int(value.strip())
        except ValueError as exc:
            raise ValueError(f"{label} muss eine ganze Zahl sein.") from exc

        if number < minimum:
            raise ValueError(f"{label} muss mindestens {minimum} sein.")
        return number

    def _read_exam_date(self) -> date | None:
        raw_value = self.exam_date_var.get().strip()
        if not raw_value:
            return None
        try:
            return date.fromisoformat(raw_value)
        except ValueError as exc:
            raise ValueError("Der Pruefungstermin muss im Format JJJJ-MM-TT sein.") from exc

    def _refresh_plan(self) -> None:
        self._refresh_header()
        self._refresh_stats()
        self._refresh_day_cards()

    def _refresh_header(self) -> None:
        if self.plan is None:
            self.title_label.configure(text="Noch kein Lernplan")
            self.subtitle_label.configure(text="Fach und Themen eintragen, dann den Plan erstellen.")
            return

        self.title_label.configure(text=f"Lernplan fuer {self.plan.subject.name}")
        exam_text = f"Pruefung: {self.plan.exam_date.isoformat()}" if self.plan.exam_date else "Kein Termin"
        self.subtitle_label.configure(
            text=f"{self.plan.days} Tage - {self.plan.minutes_per_day} Minuten pro Tag - {exam_text}"
        )

    def _refresh_stats(self) -> None:
        for child in self.stats_frame.winfo_children():
            child.destroy()

        for column in range(4):
            self.stats_frame.grid_columnconfigure(column, weight=1)
        if self.plan is None:
            values = [
                ("Themen", str(len(self.topic_rows))),
                ("Tage", self.days_var.get()),
                ("Minuten", self.minutes_var.get()),
                ("Fortschritt", "0 %"),
            ]
        else:
            stats = self.plan.statistics()
            values = [
                ("Einheiten", str(stats["total"])),
                ("Abgeschlossen", str(stats["done"])),
                ("Offen", str(stats["open"])),
                ("Fortschritt", f"{stats['progress']} %"),
            ]

        for column, (label, value) in enumerate(values):
            card = RoundedPanel(
                self.stats_frame,
                height=94,
                fill=COLORS["surface"],
                padding=16,
                radius=18,
            )
            card.grid(row=0, column=column, sticky="ew", padx=(0 if column == 0 else 12, 0))
            tk.Label(
                card.inner,
                text=label,
                bg=COLORS["surface"],
                fg=COLORS["muted"],
                font=font(10, "bold"),
            ).pack(anchor="w")
            tk.Label(
                card.inner,
                text=value,
                bg=COLORS["surface"],
                fg=COLORS["text"],
                font=font(20, "bold"),
            ).pack(anchor="w", pady=(8, 0))

    def _refresh_day_cards(self) -> None:
        self.plan_scroll.clear()

        if self.plan is None:
            empty = RoundedPanel(
                self.plan_scroll.inner,
                height=220,
                fill=COLORS["surface"],
                padding=22,
                radius=22,
            )
            empty.pack(fill="x")
            tk.Label(
                empty.inner,
                text="Dein Lernplan erscheint hier.",
                bg=COLORS["surface"],
                fg=COLORS["text"],
                font=font(18, "bold"),
            ).pack(anchor="w")
            tk.Label(
                empty.inner,
                text="Sobald du den Plan erstellst, werden die Lerntage als Karten angezeigt.",
                bg=COLORS["surface"],
                fg=COLORS["muted"],
                font=font(12),
                wraplength=640,
                justify="left",
            ).pack(anchor="w", pady=(10, 0))
            return

        unit_number = 1
        for day in range(1, self.plan.days + 1):
            day_units = self.plan.units_for_day(day)
            height = 90 + max(1, len(day_units)) * 100
            card = RoundedPanel(
                self.plan_scroll.inner,
                height=height,
                fill=COLORS["surface"],
                padding=18,
                radius=22,
            )
            card.pack(fill="x", pady=(0, 14))
            card.inner.grid_columnconfigure(0, weight=1)

            tk.Label(
                card.inner,
                text=f"Tag {day}",
                bg=COLORS["surface"],
                fg=COLORS["text"],
                font=font(17, "bold"),
            ).grid(row=0, column=0, sticky="w", pady=(0, 12))

            for row_index, unit in enumerate(day_units, start=1):
                self._add_unit_row(card.inner, unit_number, unit, row_index)
                unit_number += 1

    def _add_unit_row(
        self,
        parent: tk.Frame,
        unit_number: int,
        unit: StudyUnit,
        row_index: int,
    ) -> None:
        unit_frame = tk.Frame(parent, bg=COLORS["surface_high"], padx=12, pady=10)
        unit_frame.grid(row=row_index, column=0, sticky="ew", pady=(0, 10))
        unit_frame.grid_columnconfigure(0, weight=1)

        status_color = self._status_color(unit.status)
        tk.Label(
            unit_frame,
            text=f"{unit_number}. {unit.topic}",
            bg=COLORS["surface_high"],
            fg=COLORS["text"],
            font=font(12, "bold"),
            anchor="w",
        ).grid(row=0, column=0, sticky="ew")
        tk.Label(
            unit_frame,
            text=f"{unit.task} - {unit.duration_minutes} Min.",
            bg=COLORS["surface_high"],
            fg=COLORS["muted"],
            font=font(10),
            anchor="w",
            justify="left",
            wraplength=380,
        ).grid(row=1, column=0, sticky="ew", pady=(5, 0))
        tk.Label(
            unit_frame,
            text=unit.status.value,
            bg=COLORS["surface_high"],
            fg=status_color,
            font=font(10, "bold"),
        ).grid(row=0, column=1, sticky="e", padx=(12, 0))

        status_actions = tk.Frame(unit_frame, bg=COLORS["surface_high"])
        status_actions.grid(row=1, column=1, sticky="e", padx=(12, 0))
        for index, (label, status) in enumerate(
            [
                ("Offen", Status.OPEN),
                ("Arbeit", Status.IN_PROGRESS),
                ("Fertig", Status.DONE),
            ]
        ):
            RoundedButton(
                status_actions,
                label,
                command=lambda current=status, number=unit_number: self._set_unit_status(number, current),
                width=70,
                height=28,
                fill=self._status_button_fill(unit.status, status),
                hover_fill=COLORS["border"],
                border=COLORS["border"],
                radius=12,
                font_size=9,
            ).grid(row=0, column=index, padx=(0 if index == 0 else 6, 0))

    def _status_button_fill(self, current: Status, target: Status) -> str:
        if current != target:
            return COLORS["surface_high"]
        if target == Status.DONE:
            return COLORS["done"]
        if target == Status.IN_PROGRESS:
            return COLORS["progress"]
        return COLORS["border"]

    def _status_color(self, status: Status) -> str:
        if status == Status.DONE:
            return COLORS["done"]
        if status == Status.IN_PROGRESS:
            return COLORS["progress"]
        return COLORS["muted"]

    def _set_unit_status(self, unit_number: int, status: Status) -> None:
        if self.plan is None:
            return
        self.plan.update_status(unit_number, status)
        self._refresh_plan()

    def _save_plan(self) -> None:
        if self.plan is None:
            self._show_error("Erstelle zuerst einen Lernplan.")
            return

        path = filedialog.asksaveasfilename(
            title="Lernplan speichern",
            defaultextension=".json",
            initialfile=DEFAULT_PLAN_PATH.name,
            filetypes=[("JSON-Dateien", "*.json"), ("Alle Dateien", "*.*")],
        )
        if not path:
            return

        self.storage.save(self.plan, Path(path))
        messagebox.showinfo("Gespeichert", "Der Lernplan wurde erfolgreich gespeichert.")

    def _load_plan(self) -> None:
        path = filedialog.askopenfilename(
            title="Lernplan laden",
            filetypes=[("JSON-Dateien", "*.json"), ("Alle Dateien", "*.*")],
        )
        if not path:
            return

        try:
            self.plan = self.storage.load(Path(path))
        except (ValueError, OSError) as error:
            self._show_error(str(error))
            return

        self.subject = self.plan.subject
        self.subject_var.set(self.subject.name)
        self.topic_rows = [(topic.name, topic.difficulty) for topic in self.subject.topics]
        self.days_var.set(str(self.plan.days))
        self.minutes_var.set(str(self.plan.minutes_per_day))
        self.exam_date_var.set(self.plan.exam_date.isoformat() if self.plan.exam_date else "")
        self._refresh_topics()
        self._refresh_plan()

    def _reset_form(self) -> None:
        self.subject = None
        self.plan = None
        self.topic_rows.clear()
        self.subject_var.set("")
        self.topic_var.set("")
        self.difficulty_var.set(Difficulty.MEDIUM.value)
        self.days_var.set("5")
        self.minutes_var.set("60")
        self.exam_date_var.set("")
        self._refresh_difficulty_buttons()
        self._refresh_topics()
        self._refresh_plan()

    def _show_error(self, message: str) -> None:
        messagebox.showerror("NextStudy", message)


def main() -> None:
    root = tk.Tk()
    NextStudyGui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
