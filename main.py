import os
import json
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    BASE_DIR = os.getcwd()
DATA_FILE = os.path.join(BASE_DIR, "homeschool_data.json")

BG = "#15151F"
CARD = "#23233A"
CARD_SOFT = "#2E2E4A"
PRIMARY = "#7C5CFC"
PRIMARY_DARK = "#5B3FD6"
GREEN = "#3DDC97"
ORANGE = "#FFB86B"
PINK = "#FF7EB6"
BLUE = "#69C0FF"
TEXT = "#F5F5F7"
MUTED = "#9A9AC0"
DARK_INK = "#15151F"

AREA_COLORS = {
    "Arte": PINK,
    "Ciencia": GREEN,
    "Mundo": ORANGE,
    "Logica": PRIMARY,
    "Palavras": BLUE,
    "Corpo": "#FF9E9E",
}

STATUS_FLOW = ["A fazer", "Fazendo", "Concluida"]
STATUS_COLORS = {"A fazer": MUTED, "Fazendo": ORANGE, "Concluida": GREEN}

DEFAULT_MISSIONS = [
    {"titulo": "Crie um animal imaginario", "area": "Arte", "dif": 1,
     "desc": "Desenhe e de nome a uma criatura que nao existe. Conte onde ela vive e o que come."},
    {"titulo": "Cientista por um dia", "area": "Ciencia", "dif": 2,
     "desc": "Misture agua, oleo e corante e observe o que acontece. Registre suas descobertas."},
    {"titulo": "Mapa do meu bairro", "area": "Mundo", "dif": 2,
     "desc": "Desenhe o caminho de casa ate um lugar que voce gosta, com os pontos importantes."},
    {"titulo": "Ponte de papel", "area": "Logica", "dif": 3,
     "desc": "Use apenas papel para construir uma ponte que segure um brinquedo. Teste e melhore."},
    {"titulo": "Invente uma historia", "area": "Palavras", "dif": 2,
     "desc": "Crie uma historia com comeco, meio e fim usando 3 palavras sorteadas por voce."},
    {"titulo": "Desafio do corpo", "area": "Corpo", "dif": 1,
     "desc": "Crie uma sequencia de 5 movimentos e ensine para alguem da familia."},
    {"titulo": "Cozinheiro mirim", "area": "Mundo", "dif": 1,
     "desc": "Ajude a preparar um lanche e descreva, passo a passo, o que voce fez."},
    {"titulo": "Robo de sucata", "area": "Arte", "dif": 3,
     "desc": "Monte um robo usando materiais reciclaveis que existem na sua casa."},
]

# Responsive scale: filled in by setup_scale() once the Tk root exists.
S = 1.0
F_TITLE = F_SUB = F_CARD = F_BODY = F_SMALL = F_PILL = F_BTN = F_NAV = F_STAT = F_INPUT = ("Helvetica", 12)


def setup_scale(root):
    global S, F_TITLE, F_SUB, F_CARD, F_BODY, F_SMALL, F_PILL, F_BTN, F_NAV, F_STAT, F_INPUT
    sw = root.winfo_screenwidth()
    S = min(1.4, max(0.7, sw / 1080.0))

    def f(px, *style):
        # Negative size = pixels in Tk (DPI-independent), scaled by screen width.
        return ("Helvetica", -max(11, int(px * S))) + style

    F_TITLE = f(56, "bold")
    F_SUB = f(32)
    F_CARD = f(44, "bold")
    F_BODY = f(34)
    F_SMALL = f(28)
    F_PILL = f(28, "bold")
    F_BTN = f(40, "bold")
    F_NAV = f(36, "bold")
    F_STAT = f(60, "bold")
    F_INPUT = f(38)


def P(v):
    return max(1, int(v * S))


def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            data = {}
    else:
        data = {}
    data.setdefault("aluno", "Aluno(a)")
    if not data.get("missoes"):
        data["missoes"] = []
        for i, m in enumerate(DEFAULT_MISSIONS):
            item = dict(m)
            item["id"] = i + 1
            item["status"] = "A fazer"
            data["missoes"].append(item)
    data.setdefault("portfolio", [])
    save_data(data)
    return data


def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError:
        pass


def wrap(label, margin=8):
    """Make a label re-flow its text to its own width (true responsive wrapping)."""
    def _on_resize(e):
        label.configure(wraplength=max(40, e.width - P(margin)))
    label.bind("<Configure>", _on_resize)
    return label


def pill(parent, text, bg, fg=DARK_INK):
    return tk.Label(parent, text=text, bg=bg, fg=fg, font=F_PILL,
                    padx=P(12), pady=P(4))


class Scrollable(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG)
        self.canvas = tk.Canvas(self, bg=BG, highlightthickness=0)
        self.bar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview, width=P(10))
        self.inner = tk.Frame(self.canvas, bg=BG)
        self.inner.bind("<Configure>",
                        lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.win = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.win, width=e.width))
        self.canvas.configure(yscrollcommand=self.bar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.bar.pack(side="right", fill="y")
        self.bind_touch(self.canvas)
        self.bind_touch(self.inner)

    def bind_touch(self, widget):
        widget.bind("<ButtonPress-1>", lambda e: self.canvas.scan_mark(e.x, e.y))
        widget.bind("<B1-Motion>", lambda e: self.canvas.scan_dragto(e.x, e.y, gain=1))
        widget.bind("<MouseWheel>", self._wheel)
        widget.bind("<Button-4>", lambda e: self.canvas.yview_scroll(-2, "units"))
        widget.bind("<Button-5>", lambda e: self.canvas.yview_scroll(2, "units"))

    def _wheel(self, e):
        self.canvas.yview_scroll(int(-e.delta / 60) or (-1 if e.delta > 0 else 1), "units")

    def clear(self):
        for w in self.inner.winfo_children():
            w.destroy()


def big_button(parent, text, command, bg=PRIMARY, fg="white"):
    b = tk.Button(parent, text=text, command=command, bg=bg, fg=fg,
                  activebackground=PRIMARY_DARK, activeforeground="white",
                  font=F_BTN, relief="flat", bd=0, highlightthickness=0,
                  padx=P(12), pady=P(16), cursor="hand2")
    return b


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        setup_scale(self)
        self.title("Trilha Criativa")
        self.configure(bg=BG)
        self.geometry("420x820")
        self.minsize(300, 520)
        self.data = load_data()

        style = ttk.Style(self)
        try:
            style.theme_use("default")
        except tk.TclError:
            pass
        style.configure("P.Horizontal.TProgressbar", troughcolor=CARD_SOFT,
                        background=GREEN, thickness=P(22), borderwidth=0)
        style.configure("TCombobox", fieldbackground=CARD_SOFT, background=CARD_SOFT,
                        foreground=TEXT, arrowcolor=TEXT, borderwidth=0)

        self.container = tk.Frame(self, bg=BG)
        self.container.pack(side="top", fill="both", expand=True)

        self.nav = tk.Frame(self, bg=CARD)
        self.nav.pack(side="bottom", fill="x")

        self.screens = {
            "hub": HubScreen(self.container, self),
            "portfolio": PortfolioScreen(self.container, self),
            "pais": ParentScreen(self.container, self),
        }
        self.nav_buttons = {}
        items = [("hub", "Missoes"), ("portfolio", "Portfolio"), ("pais", "Pais")]
        for key, label in items:
            b = tk.Button(self.nav, text=label, command=lambda k=key: self.show(k),
                          bg=CARD, fg=MUTED, activebackground=PRIMARY,
                          activeforeground="white", font=F_NAV,
                          relief="flat", bd=0, highlightthickness=0, pady=P(16))
            b.pack(side="left", fill="both", expand=True)
            self.nav_buttons[key] = b

        self.show("hub")

    def show(self, key):
        for k, s in self.screens.items():
            s.pack_forget()
            self.nav_buttons[k].configure(fg=MUTED, bg=CARD)
        self.screens[key].pack(fill="both", expand=True)
        self.nav_buttons[key].configure(fg="white", bg=PRIMARY)
        self.screens[key].refresh()

    def persist(self):
        save_data(self.data)


class Header(tk.Frame):
    def __init__(self, parent, title, subtitle):
        super().__init__(parent, bg=BG)
        tk.Label(self, text=title, bg=BG, fg=TEXT, font=F_TITLE,
                 anchor="w").pack(fill="x", padx=P(18), pady=(P(16), 0))
        wrap(tk.Label(self, text=subtitle, bg=BG, fg=MUTED, font=F_SUB,
                      anchor="w", justify="left")).pack(fill="x", padx=P(18), pady=(P(2), P(12)))


class HubScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        Header(self, "Trilha Criativa", "Escolha um projeto e mao na massa").pack(fill="x")
        big_button(self, "+  Nova missao", self.add_mission).pack(
            fill="x", padx=P(16), pady=(0, P(10)))
        self.list = Scrollable(self)
        self.list.pack(fill="both", expand=True)

    def refresh(self):
        self.list.clear()
        for m in self.app.data["missoes"]:
            self.card(m)

    def card(self, m):
        area = m.get("area", "Mundo")
        ac = AREA_COLORS.get(area, MUTED)
        st = m.get("status", "A fazer")

        f = tk.Frame(self.list.inner, bg=CARD)
        f.pack(fill="x", padx=P(14), pady=P(7))
        self.list.bind_touch(f)

        tk.Frame(f, bg=ac, height=P(7)).pack(fill="x")

        top = tk.Frame(f, bg=CARD)
        top.pack(fill="x", padx=P(14), pady=(P(12), 0))
        self.list.bind_touch(top)
        pill(top, area, ac).pack(side="left")
        pill(top, "Nivel " + str(int(m.get("dif", 1))), CARD_SOFT, ORANGE).pack(
            side="left", padx=(P(6), 0))
        pill(top, st, STATUS_COLORS.get(st, MUTED)).pack(side="right")

        tt = tk.Label(f, text=m.get("titulo", ""), bg=CARD, fg=TEXT, font=F_CARD,
                      justify="left", anchor="w")
        wrap(tt)
        tt.pack(fill="x", padx=P(14), pady=(P(8), 0))
        self.list.bind_touch(tt)

        ds = tk.Label(f, text=m.get("desc", ""), bg=CARD, fg=MUTED, font=F_BODY,
                      justify="left", anchor="w")
        wrap(ds)
        ds.pack(fill="x", padx=P(14), pady=(P(4), P(12)))
        self.list.bind_touch(ds)

        done = st == "Concluida"
        big_button(f, "Avancar etapa", lambda: self.advance(m), bg=PRIMARY).pack(
            fill="x", padx=P(14), pady=(0, P(8)))
        big_button(f, "Reabrir" if done else "Concluir", lambda: self.toggle_done(m),
                   bg=CARD_SOFT if done else GREEN,
                   fg=TEXT if done else DARK_INK).pack(fill="x", padx=P(14), pady=(0, P(14)))

    def advance(self, m):
        i = STATUS_FLOW.index(m.get("status", "A fazer"))
        m["status"] = STATUS_FLOW[(i + 1) % len(STATUS_FLOW)]
        self.app.persist()
        self.refresh()

    def toggle_done(self, m):
        m["status"] = "A fazer" if m.get("status") == "Concluida" else "Concluida"
        self.app.persist()
        self.refresh()

    def add_mission(self):
        MissionDialog(self.app, self.refresh)


class MissionDialog(tk.Toplevel):
    def __init__(self, app, on_save):
        super().__init__(app)
        self.app = app
        self.on_save = on_save
        self.title("Nova missao")
        self.configure(bg=BG)
        self.geometry("400x640")
        tk.Label(self, text="Nova missao", bg=BG, fg=TEXT, font=F_TITLE).pack(
            anchor="w", padx=P(16), pady=P(14))
        self.titulo = self._entry("Titulo do projeto")
        tk.Label(self, text="Area", bg=BG, fg=MUTED, font=F_SUB).pack(anchor="w", padx=P(16))
        self.area = ttk.Combobox(self, values=list(AREA_COLORS.keys()), state="readonly",
                                 font=F_INPUT)
        self.area.current(0)
        self.area.pack(fill="x", padx=P(16), pady=(P(2), P(10)), ipady=P(6))
        tk.Label(self, text="Dificuldade", bg=BG, fg=MUTED, font=F_SUB).pack(anchor="w", padx=P(16))
        self.dif = ttk.Combobox(self, values=["1", "2", "3"], state="readonly", font=F_INPUT)
        self.dif.current(0)
        self.dif.pack(fill="x", padx=P(16), pady=(P(2), P(10)), ipady=P(6))
        tk.Label(self, text="Descricao", bg=BG, fg=MUTED, font=F_SUB).pack(anchor="w", padx=P(16))
        self.desc = tk.Text(self, height=4, bg=CARD_SOFT, fg=TEXT, insertbackground=TEXT,
                            font=F_BODY, relief="flat", wrap="word", padx=P(8), pady=P(8))
        self.desc.pack(fill="x", padx=P(16), pady=(P(2), P(12)))
        big_button(self, "Salvar missao", self.save, bg=GREEN, fg=DARK_INK).pack(
            fill="x", padx=P(16), pady=P(6))
        big_button(self, "Cancelar", self.destroy, bg=CARD_SOFT).pack(fill="x", padx=P(16))

    def _entry(self, label):
        tk.Label(self, text=label, bg=BG, fg=MUTED, font=F_SUB).pack(anchor="w", padx=P(16))
        e = tk.Entry(self, bg=CARD_SOFT, fg=TEXT, insertbackground=TEXT, font=F_INPUT,
                     relief="flat")
        e.pack(fill="x", padx=P(16), pady=(P(2), P(10)), ipady=P(8))
        return e

    def save(self):
        titulo = self.titulo.get().strip()
        if not titulo:
            messagebox.showwarning("Atencao", "De um titulo para a missao.")
            return
        ids = [m["id"] for m in self.app.data["missoes"]] or [0]
        self.app.data["missoes"].append({
            "id": max(ids) + 1,
            "titulo": titulo,
            "area": self.area.get(),
            "dif": int(self.dif.get()),
            "desc": self.desc.get("1.0", "end").strip(),
            "status": "A fazer",
        })
        self.app.persist()
        self.on_save()
        self.destroy()


class PortfolioScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        Header(self, "Meu Portfolio", "Registre o que voce criou e aprendeu").pack(fill="x")
        form = tk.Frame(self, bg=CARD)
        form.pack(fill="x", padx=P(14), pady=(0, P(10)))
        tk.Frame(form, bg=PRIMARY, height=P(7)).pack(fill="x")
        tk.Label(form, text="Sobre qual projeto?", bg=CARD, fg=MUTED, font=F_SMALL).pack(
            anchor="w", padx=P(14), pady=(P(12), P(2)))
        self.combo = ttk.Combobox(form, state="readonly", font=F_INPUT)
        self.combo.pack(fill="x", padx=P(14), ipady=P(6))
        tk.Label(form, text="O que voce fez?", bg=CARD, fg=MUTED, font=F_SMALL).pack(
            anchor="w", padx=P(14), pady=(P(10), P(2)))
        self.text = tk.Text(form, height=4, bg=CARD_SOFT, fg=TEXT, insertbackground=TEXT,
                            font=F_BODY, relief="flat", wrap="word", padx=P(8), pady=P(8))
        self.text.pack(fill="x", padx=P(14), pady=(0, P(10)))
        big_button(form, "Salvar conquista", self.save, bg=GREEN, fg=DARK_INK).pack(
            fill="x", padx=P(14), pady=(0, P(14)))
        self.list = Scrollable(self)
        self.list.pack(fill="both", expand=True)

    def options(self):
        return ["Conquista livre"] + [m["titulo"] for m in self.app.data["missoes"]]

    def refresh(self):
        opts = self.options()
        self.combo.configure(values=opts)
        if not self.combo.get() or self.combo.get() not in opts:
            self.combo.current(0)
        self.list.clear()
        entries = list(reversed(self.app.data["portfolio"]))
        if not entries:
            wrap(tk.Label(self.list.inner,
                          text="Nada registrado ainda. Crie sua primeira conquista!",
                          bg=BG, fg=MUTED, font=F_BODY, justify="center")).pack(
                fill="x", padx=P(20), pady=P(30))
            return
        for e in entries:
            self.card(e)

    def card(self, e):
        f = tk.Frame(self.list.inner, bg=CARD)
        f.pack(fill="x", padx=P(14), pady=P(7))
        self.list.bind_touch(f)
        tk.Frame(f, bg=PINK, height=P(7)).pack(fill="x")
        head = tk.Frame(f, bg=CARD)
        head.pack(fill="x", padx=P(14), pady=(P(12), 0))
        self.list.bind_touch(head)
        tk.Label(head, text=e.get("titulo", "Conquista"), bg=CARD, fg=PINK,
                 font=F_CARD).pack(side="left")
        tk.Label(head, text=e.get("data", ""), bg=CARD, fg=MUTED, font=F_SMALL).pack(side="right")
        body = tk.Label(f, text=e.get("texto", ""), bg=CARD, fg=TEXT, font=F_BODY,
                        justify="left", anchor="w")
        wrap(body)
        body.pack(fill="x", padx=P(14), pady=(P(6), P(10)))
        self.list.bind_touch(body)
        big_button(f, "Apagar", lambda: self.delete(e), bg=CARD_SOFT, fg=PINK).pack(
            fill="x", padx=P(14), pady=(0, P(14)))

    def save(self):
        txt = self.text.get("1.0", "end").strip()
        if not txt:
            messagebox.showwarning("Atencao", "Escreva o que voce fez antes de salvar.")
            return
        self.app.data["portfolio"].append({
            "titulo": self.combo.get(),
            "texto": txt,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        })
        self.app.persist()
        self.text.delete("1.0", "end")
        self.refresh()

    def delete(self, entry):
        if not messagebox.askyesno("Apagar", "Remover este registro?"):
            return
        try:
            self.app.data["portfolio"].remove(entry)
        except ValueError:
            pass
        self.app.persist()
        self.refresh()


class ParentScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        Header(self, "Painel dos Pais", "Acompanhe o progresso do aprendizado").pack(fill="x")
        self.body = Scrollable(self)
        self.body.pack(fill="both", expand=True)

    def block(self, accent):
        b = tk.Frame(self.body.inner, bg=CARD)
        b.pack(fill="x", padx=P(14), pady=P(7))
        self.body.bind_touch(b)
        tk.Frame(b, bg=accent, height=P(7)).pack(fill="x")
        return b

    def refresh(self):
        self.body.clear()
        c = self.body.inner

        name_box = self.block(PRIMARY)
        tk.Label(name_box, text="Nome do aluno(a)", bg=CARD, fg=MUTED, font=F_SMALL).pack(
            anchor="w", padx=P(14), pady=(P(12), P(2)))
        self.name = tk.Entry(name_box, bg=CARD_SOFT, fg=TEXT, insertbackground=TEXT,
                             font=F_INPUT, relief="flat")
        self.name.insert(0, self.app.data.get("aluno", ""))
        self.name.pack(fill="x", padx=P(14), ipady=P(8))
        big_button(name_box, "Salvar nome", self.save_name, bg=PRIMARY).pack(
            fill="x", padx=P(14), pady=P(14))

        missoes = self.app.data["missoes"]
        total = len(missoes)
        done = sum(1 for m in missoes if m.get("status") == "Concluida")
        doing = sum(1 for m in missoes if m.get("status") == "Fazendo")
        pct = int(done / total * 100) if total else 0

        prog = self.block(GREEN)
        tk.Label(prog, text="Progresso geral", bg=CARD, fg=TEXT, font=F_CARD).pack(
            anchor="w", padx=P(14), pady=(P(12), P(8)))
        ttk.Progressbar(prog, style="P.Horizontal.TProgressbar", maximum=100, value=pct).pack(
            fill="x", padx=P(14))
        tk.Label(prog, text=str(pct) + "%   " + str(done) + " de " + str(total) + " concluidos",
                 bg=CARD, fg=GREEN, font=F_BODY).pack(anchor="w", padx=P(14), pady=(P(8), P(14)))

        stats = tk.Frame(c, bg=BG)
        stats.pack(fill="x", padx=P(8), pady=P(2))
        self.body.bind_touch(stats)
        self.stat(stats, doing, "Fazendo", ORANGE)
        self.stat(stats, len(self.app.data["portfolio"]), "Conquistas", PINK)
        self.stat(stats, total - done, "A fazer", MUTED)

        area_box = self.block(ORANGE)
        tk.Label(area_box, text="Concluido por area", bg=CARD, fg=TEXT, font=F_CARD).pack(
            anchor="w", padx=P(14), pady=(P(12), P(8)))
        areas = {}
        for m in missoes:
            a = m.get("area", "Mundo")
            areas.setdefault(a, [0, 0])
            areas[a][1] += 1
            if m.get("status") == "Concluida":
                areas[a][0] += 1
        for a, (d, t) in areas.items():
            row = tk.Frame(area_box, bg=CARD)
            row.pack(fill="x", padx=P(14), pady=P(3))
            self.body.bind_touch(row)
            tk.Label(row, text=a, bg=CARD, fg=AREA_COLORS.get(a, TEXT), font=F_BODY).pack(side="left")
            tk.Label(row, text=str(d) + "/" + str(t), bg=CARD, fg=MUTED, font=F_BODY).pack(side="right")
        tk.Frame(area_box, bg=CARD, height=P(10)).pack()

        recent = self.block(PINK)
        tk.Label(recent, text="Ultimas conquistas", bg=CARD, fg=TEXT, font=F_CARD).pack(
            anchor="w", padx=P(14), pady=(P(12), P(8)))
        entries = list(reversed(self.app.data["portfolio"]))[:5]
        if not entries:
            tk.Label(recent, text="Nenhum registro ainda.", bg=CARD, fg=MUTED, font=F_BODY).pack(
                anchor="w", padx=P(14), pady=(0, P(14)))
        else:
            for e in entries:
                tk.Label(recent, text="- " + e.get("titulo", ""), bg=CARD, fg=TEXT,
                         font=F_BODY).pack(anchor="w", padx=P(14))
                tk.Label(recent, text="   " + e.get("data", ""), bg=CARD, fg=MUTED,
                         font=F_SMALL).pack(anchor="w", padx=P(14), pady=(0, P(6)))
            tk.Frame(recent, bg=CARD, height=P(8)).pack()

    def stat(self, parent, value, label, color):
        f = tk.Frame(parent, bg=CARD)
        f.pack(side="left", fill="both", expand=True, padx=P(6), pady=P(4))
        tk.Label(f, text=str(value), bg=CARD, fg=color, font=F_STAT).pack(pady=(P(14), 0))
        tk.Label(f, text=label, bg=CARD, fg=MUTED, font=F_SMALL).pack(pady=(0, P(14)))

    def save_name(self):
        self.app.data["aluno"] = self.name.get().strip() or "Aluno(a)"
        self.app.persist()
        messagebox.showinfo("Pronto", "Nome salvo com sucesso.")


if __name__ == "__main__":
    App().mainloop()
