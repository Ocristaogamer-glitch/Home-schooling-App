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

BG = "#1B1B2F"
CARD = "#252544"
CARD_SOFT = "#2E2E55"
PRIMARY = "#7C5CFC"
PRIMARY_DARK = "#5B3FD6"
GREEN = "#3DDC97"
ORANGE = "#FFB86B"
PINK = "#FF7EB6"
TEXT = "#F5F5F7"
MUTED = "#A6A6C8"

AREA_COLORS = {
    "Arte": PINK,
    "Ciencia": GREEN,
    "Mundo": ORANGE,
    "Logica": PRIMARY,
    "Palavras": "#69C0FF",
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


class Scrollable(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG)
        self.canvas = tk.Canvas(self, bg=BG, highlightthickness=0)
        self.bar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview, width=16)
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
    return tk.Button(parent, text=text, command=command, bg=bg, fg=fg,
                     activebackground=PRIMARY_DARK, activeforeground="white",
                     font=("Helvetica", 14, "bold"), relief="flat", bd=0,
                     padx=14, pady=12, cursor="hand2")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Trilha Criativa")
        self.configure(bg=BG)
        self.geometry("420x780")
        self.minsize(320, 560)
        self.data = load_data()

        style = ttk.Style(self)
        try:
            style.theme_use("default")
        except tk.TclError:
            pass
        style.configure("P.Horizontal.TProgressbar", troughcolor=CARD,
                        background=GREEN, thickness=18, borderwidth=0)
        style.configure("TCombobox", fieldbackground=CARD, background=CARD,
                        foreground=TEXT, arrowcolor=TEXT)

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
                          bg=CARD, fg=MUTED, activebackground=CARD_SOFT,
                          activeforeground="white", font=("Helvetica", 13, "bold"),
                          relief="flat", bd=0, pady=14)
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
        tk.Label(self, text=title, bg=BG, fg=TEXT,
                 font=("Helvetica", 22, "bold")).pack(anchor="w", padx=18, pady=(18, 0))
        tk.Label(self, text=subtitle, bg=BG, fg=MUTED,
                 font=("Helvetica", 12)).pack(anchor="w", padx=18, pady=(2, 12))


class HubScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        Header(self, "Trilha Criativa", "Escolha um projeto e mao na massa").pack(fill="x")
        big_button(self, "+ Nova missao", self.add_mission).pack(fill="x", padx=18, pady=(0, 10))
        self.list = Scrollable(self)
        self.list.pack(fill="both", expand=True)

    def refresh(self):
        self.list.clear()
        for m in self.app.data["missoes"]:
            self.card(m)

    def card(self, m):
        f = tk.Frame(self.list.inner, bg=CARD)
        f.pack(fill="x", padx=14, pady=7)
        self.list.bind_touch(f)
        top = tk.Frame(f, bg=CARD)
        top.pack(fill="x", padx=14, pady=(12, 0))
        self.list.bind_touch(top)
        area = m.get("area", "Mundo")
        tk.Label(top, text=" " + area + " ", bg=CARD, fg=AREA_COLORS.get(area, MUTED),
                 font=("Helvetica", 11, "bold")).pack(side="left")
        tk.Label(top, text="  " + "*" * int(m.get("dif", 1)), bg=CARD, fg=ORANGE,
                 font=("Helvetica", 11, "bold")).pack(side="left")
        st = m.get("status", "A fazer")
        tk.Label(top, text=st, bg=CARD, fg=STATUS_COLORS.get(st, MUTED),
                 font=("Helvetica", 11, "bold")).pack(side="right")
        tt = tk.Label(f, text=m.get("titulo", ""), bg=CARD, fg=TEXT,
                      font=("Helvetica", 16, "bold"), justify="left", anchor="w")
        tt.pack(fill="x", padx=14, pady=(6, 0))
        self.list.bind_touch(tt)
        ds = tk.Label(f, text=m.get("desc", ""), bg=CARD, fg=MUTED, font=("Helvetica", 12),
                      justify="left", anchor="w", wraplength=300)
        ds.pack(fill="x", padx=14, pady=(4, 10))
        self.list.bind_touch(ds)
        label = "Concluir" if st != "Concluida" else "Reabrir"
        color = GREEN if st != "Concluida" else CARD_SOFT
        big_button(f, "Avancar etapa", lambda: self.advance(m), bg=PRIMARY).pack(
            fill="x", padx=14, pady=(0, 4))
        big_button(f, label, lambda: self.toggle_done(m), bg=color,
                   fg="#102016" if st != "Concluida" else TEXT).pack(
            fill="x", padx=14, pady=(0, 12))

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
        self.geometry("360x520")
        tk.Label(self, text="Nova missao", bg=BG, fg=TEXT,
                 font=("Helvetica", 18, "bold")).pack(anchor="w", padx=16, pady=14)
        self.titulo = self._entry("Titulo do projeto")
        tk.Label(self, text="Area", bg=BG, fg=MUTED, font=("Helvetica", 12)).pack(
            anchor="w", padx=16)
        self.area = ttk.Combobox(self, values=list(AREA_COLORS.keys()), state="readonly",
                                 font=("Helvetica", 13))
        self.area.current(0)
        self.area.pack(fill="x", padx=16, pady=(2, 10))
        tk.Label(self, text="Dificuldade", bg=BG, fg=MUTED, font=("Helvetica", 12)).pack(
            anchor="w", padx=16)
        self.dif = ttk.Combobox(self, values=["1", "2", "3"], state="readonly",
                                font=("Helvetica", 13))
        self.dif.current(0)
        self.dif.pack(fill="x", padx=16, pady=(2, 10))
        tk.Label(self, text="Descricao", bg=BG, fg=MUTED, font=("Helvetica", 12)).pack(
            anchor="w", padx=16)
        self.desc = tk.Text(self, height=4, bg=CARD, fg=TEXT, insertbackground=TEXT,
                            font=("Helvetica", 13), relief="flat", wrap="word")
        self.desc.pack(fill="x", padx=16, pady=(2, 12))
        big_button(self, "Salvar missao", self.save, bg=GREEN, fg="#102016").pack(
            fill="x", padx=16, pady=6)
        big_button(self, "Cancelar", self.destroy, bg=CARD_SOFT).pack(fill="x", padx=16)

    def _entry(self, label):
        tk.Label(self, text=label, bg=BG, fg=MUTED, font=("Helvetica", 12)).pack(
            anchor="w", padx=16)
        e = tk.Entry(self, bg=CARD, fg=TEXT, insertbackground=TEXT,
                     font=("Helvetica", 14), relief="flat")
        e.pack(fill="x", padx=16, pady=(2, 10), ipady=6)
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
        form.pack(fill="x", padx=14, pady=(0, 10))
        tk.Label(form, text="Sobre qual projeto?", bg=CARD, fg=MUTED,
                 font=("Helvetica", 12)).pack(anchor="w", padx=12, pady=(12, 2))
        self.combo = ttk.Combobox(form, state="readonly", font=("Helvetica", 13))
        self.combo.pack(fill="x", padx=12)
        tk.Label(form, text="O que voce fez?", bg=CARD, fg=MUTED,
                 font=("Helvetica", 12)).pack(anchor="w", padx=12, pady=(10, 2))
        self.text = tk.Text(form, height=4, bg=CARD_SOFT, fg=TEXT, insertbackground=TEXT,
                            font=("Helvetica", 13), relief="flat", wrap="word")
        self.text.pack(fill="x", padx=12, pady=(0, 10))
        big_button(form, "Salvar conquista", self.save, bg=GREEN, fg="#102016").pack(
            fill="x", padx=12, pady=(0, 12))
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
            tk.Label(self.list.inner, text="Nada registrado ainda.\nCrie sua primeira conquista!",
                     bg=BG, fg=MUTED, font=("Helvetica", 13), justify="center").pack(pady=30)
            return
        for e in entries:
            self.card(e)

    def card(self, e):
        f = tk.Frame(self.list.inner, bg=CARD)
        f.pack(fill="x", padx=14, pady=7)
        self.list.bind_touch(f)
        head = tk.Frame(f, bg=CARD)
        head.pack(fill="x", padx=14, pady=(12, 0))
        tk.Label(head, text=e.get("titulo", "Conquista"), bg=CARD, fg=PRIMARY,
                 font=("Helvetica", 14, "bold")).pack(side="left")
        tk.Label(head, text=e.get("data", ""), bg=CARD, fg=MUTED,
                 font=("Helvetica", 10)).pack(side="right")
        body = tk.Label(f, text=e.get("texto", ""), bg=CARD, fg=TEXT, font=("Helvetica", 12),
                        justify="left", anchor="w", wraplength=300)
        body.pack(fill="x", padx=14, pady=(4, 8))
        self.list.bind_touch(body)
        big_button(f, "Apagar", lambda: self.delete(e), bg=CARD_SOFT, fg=PINK).pack(
            fill="x", padx=14, pady=(0, 12))

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

    def refresh(self):
        self.body.clear()
        c = self.body.inner

        name_box = tk.Frame(c, bg=CARD)
        name_box.pack(fill="x", padx=14, pady=8)
        tk.Label(name_box, text="Nome do aluno(a)", bg=CARD, fg=MUTED,
                 font=("Helvetica", 12)).pack(anchor="w", padx=12, pady=(12, 2))
        self.name = tk.Entry(name_box, bg=CARD_SOFT, fg=TEXT, insertbackground=TEXT,
                             font=("Helvetica", 14), relief="flat")
        self.name.insert(0, self.app.data.get("aluno", ""))
        self.name.pack(fill="x", padx=12, ipady=6)
        big_button(name_box, "Salvar nome", self.save_name, bg=PRIMARY).pack(
            fill="x", padx=12, pady=12)

        missoes = self.app.data["missoes"]
        total = len(missoes)
        done = sum(1 for m in missoes if m.get("status") == "Concluida")
        doing = sum(1 for m in missoes if m.get("status") == "Fazendo")
        pct = int(done / total * 100) if total else 0

        prog = tk.Frame(c, bg=CARD)
        prog.pack(fill="x", padx=14, pady=8)
        tk.Label(prog, text="Progresso geral", bg=CARD, fg=TEXT,
                 font=("Helvetica", 15, "bold")).pack(anchor="w", padx=12, pady=(12, 6))
        bar = ttk.Progressbar(prog, style="P.Horizontal.TProgressbar", maximum=100, value=pct)
        bar.pack(fill="x", padx=12)
        tk.Label(prog, text=f"{pct}%  ({done} de {total} projetos concluidos)", bg=CARD,
                 fg=GREEN, font=("Helvetica", 12, "bold")).pack(anchor="w", padx=12, pady=(6, 12))

        stats = tk.Frame(c, bg=BG)
        stats.pack(fill="x", padx=8, pady=4)
        self.stat(stats, str(doing), "Em andamento", ORANGE)
        self.stat(stats, str(len(self.app.data["portfolio"])), "Conquistas", PINK)
        self.stat(stats, str(total - done), "A fazer", MUTED)

        area_box = tk.Frame(c, bg=CARD)
        area_box.pack(fill="x", padx=14, pady=8)
        tk.Label(area_box, text="Concluido por area", bg=CARD, fg=TEXT,
                 font=("Helvetica", 15, "bold")).pack(anchor="w", padx=12, pady=(12, 6))
        areas = {}
        for m in missoes:
            a = m.get("area", "Mundo")
            areas.setdefault(a, [0, 0])
            areas[a][1] += 1
            if m.get("status") == "Concluida":
                areas[a][0] += 1
        for a, (d, t) in areas.items():
            row = tk.Frame(area_box, bg=CARD)
            row.pack(fill="x", padx=12, pady=3)
            tk.Label(row, text=a, bg=CARD, fg=AREA_COLORS.get(a, TEXT),
                     font=("Helvetica", 12, "bold")).pack(side="left")
            tk.Label(row, text=f"{d}/{t}", bg=CARD, fg=MUTED,
                     font=("Helvetica", 12)).pack(side="right")
        tk.Frame(area_box, bg=CARD, height=8).pack()

        recent = tk.Frame(c, bg=CARD)
        recent.pack(fill="x", padx=14, pady=8)
        tk.Label(recent, text="Ultimas conquistas", bg=CARD, fg=TEXT,
                 font=("Helvetica", 15, "bold")).pack(anchor="w", padx=12, pady=(12, 6))
        entries = list(reversed(self.app.data["portfolio"]))[:5]
        if not entries:
            tk.Label(recent, text="Nenhum registro ainda.", bg=CARD, fg=MUTED,
                     font=("Helvetica", 12)).pack(anchor="w", padx=12, pady=(0, 12))
        else:
            for e in entries:
                tk.Label(recent, text="- " + e.get("titulo", ""), bg=CARD, fg=TEXT,
                         font=("Helvetica", 12, "bold")).pack(anchor="w", padx=12)
                tk.Label(recent, text="  " + e.get("data", ""), bg=CARD, fg=MUTED,
                         font=("Helvetica", 10)).pack(anchor="w", padx=12, pady=(0, 6))
            tk.Frame(recent, bg=CARD, height=6).pack()

    def stat(self, parent, value, label, color):
        f = tk.Frame(parent, bg=CARD)
        f.pack(side="left", fill="both", expand=True, padx=6, pady=4)
        tk.Label(f, text=value, bg=CARD, fg=color,
                 font=("Helvetica", 22, "bold")).pack(pady=(12, 0))
        tk.Label(f, text=label, bg=CARD, fg=MUTED,
                 font=("Helvetica", 11)).pack(pady=(0, 12))

    def save_name(self):
        self.app.data["aluno"] = self.name.get().strip() or "Aluno(a)"
        self.app.persist()
        messagebox.showinfo("Pronto", "Nome salvo com sucesso.")


if __name__ == "__main__":
    App().mainloop()
