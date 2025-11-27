import turtle
import csv
from datetime import datetime, date
import math
import requests


class HorgaszSzolunarApp:
    def __init__(self):
        self.screen = None
        self.pen = None
        self.fogasok = []
        self.aktivitasi_szint = None
        self.holdfazis_szoveg = None
        self.lat = 46.95
        self.lon = 18.10
        self.api_key = "8c48ff6c86ee3bd83e34f82adf151f35"
        self.api_url = "https://api.openweathermap.org/data/3.0/onecall"
        self.aktualis_viz_nev = "Balaton - Keleti medence"
        self.horgaszvizek = [
            ("Balaton - Keleti medence", 46.95, 18.10),
            ("Balaton - Nyugati medence", 46.75, 17.25),
            ("Duna - Budapest", 47.50, 19.05),
            ("Tisza-tó", 47.60, 20.78),
            ("Velencei-tó", 47.20, 18.63),
            ("Ráckevei Dunaág (RSD)", 47.27, 18.98),
            ("Hévízi-csatorna", 46.78, 17.18),
            ("Kis-Balaton", 46.65, 17.15),
            ("Atkai Holt-Tisza", 46.45, 20.15),
            ("Deseda-tó", 46.38, 17.80),
            ("Gyékényesi bányatavak", 46.25, 16.98),
            ("Tatai Öreg-tó", 47.65, 18.32),
            ("Keve-víztározó", 46.00, 20.80),
            ("Tisza - Szeged", 46.25, 20.15),
            ("Tisza - Tokaj", 48.12, 21.40),
            ("Nyéki tavak (Budapest)", 47.43, 19.10),
            ("Rakaca-víztározó", 48.47, 20.62),
            ("Pátkai-tó", 47.18, 18.40),
            ("Dinnyési-fertő", 47.16, 18.45),
            ("Kis-Duna - Dunaharaszti", 47.34, 19.10),
            ("Vén-Duna - Szigetköz", 47.90, 17.40),
            ("S2-tó (Várpalota)", 47.22, 18.15),
            ("Fenyves-tó (Várpalota)", 47.23, 18.14),
            ("Fehérvárcsurgói-víztározó", 47.27, 18.25),
            ("Sárszentmihályi-tó", 47.15, 18.32),
            ("Palotavárosi tavak (Székesfehérvár)", 47.19, 18.43),
        ]

    def run(self):
        self.load_fogasok_from_csv()
        self.setup_screen()
        self.valassz_horgaszvizet_kezdokor()
        self.update_solunar()
        self.draw_all()
        self.register_events()
        turtle.mainloop()

    def setup_screen(self):
        self.screen = turtle.Screen()
        self.screen.title("Horgász szolunár asszisztens")
        self.screen.setup(width=900, height=600)
        self.screen.bgcolor("darkblue")
        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.pen.speed(0)

    def valassz_horgaszvizet_kezdokor(self):
        if not self.screen:
            return
        lista_szoveg = ""
        for i, (nev, _, _) in enumerate(self.horgaszvizek, start=1):
            lista_szoveg += f"{i}. {nev}\n"
        valasz = self.screen.textinput(
            "Horgászvíz választás",
            lista_szoveg + "Add meg a választott horgászvíz sorszámát:"
        )
        try:
            n = int(valasz)
            if 1 <= n <= len(self.horgaszvizek):
                nev, lat, lon = self.horgaszvizek[n - 1]
                self.lat = lat
                self.lon = lon
                self.aktualis_viz_nev = nev
        except:
            pass

    def update_solunar(self):
        moon_value = None
        try:
            params = {
                "lat": self.lat,
                "lon": self.lon,
                "exclude": "current,minutely,hourly,alerts",
                "appid": self.api_key,
                "units": "metric"
            }
            r = requests.get(self.api_url, params=params, timeout=5)
            data = r.json()
            daily = data.get("daily")
            if daily and len(daily) > 0 and "moon_phase" in daily[0]:
                moon_value = daily[0]["moon_phase"]
        except:
            moon_value = None
        if moon_value is None:
            moon_value = self._approx_moon_phase_from_date()
        phase_text = self._phase_text(moon_value)
        self.holdfazis_szoveg = "Holdfázis: " + phase_text
        self.aktivitasi_szint = self._ertekeld_aktivitas(moon_value)

    def _approx_moon_phase_from_date(self):
        today = date.today()
        known_new_moon = date(2000, 1, 6)
        days = (today - known_new_moon).days
        synodic = 29.530588853
        phase = (days % synodic) / synodic
        return phase

    def _phase_text(self, value):
        if value is None:
            return "ismeretlen"
        try:
            v = float(value)
        except:
            return "ismeretlen"
        if v == 0 or v == 1:
            return "újhold"
        if 0 < v < 0.25:
            return "növő holdsarló"
        if v == 0.25:
            return "első negyed"
        if 0.25 < v < 0.5:
            return "növő hold"
        if v == 0.5:
            return "telihold"
        if 0.5 < v < 0.75:
            return "fogyó hold"
        if v == 0.75:
            return "utolsó negyed"
        if 0.75 < v < 1:
            return "csökkenő holdsarló"
        return "ismeretlen"

    def _ertekeld_aktivitas(self, value):
        try:
            v = float(value)
        except:
            return "közepes"
        if 0.45 <= v <= 0.55:
            return "erős"
        if 0.2 <= v <= 0.8:
            return "közepes"
        return "gyenge"

    def draw_all(self):
        if not self.screen or not self.pen:
            return
        self.screen.tracer(0)
        self.pen.clear()
        self._draw_kozep_blokk()
        self._draw_bal_menu()
        self._draw_fogas_lista()
        self.screen.tracer(1)

    def _draw_kozep_blokk(self):
        self.pen.up()
        self.pen.color("white")
        y = 80
        self.pen.goto(0, y)
        self.pen.write(
            "Horgász szolunár asszisztens",
            align="center",
            font=("Arial", 22, "bold")
        )
        y -= 35
        self.pen.goto(0, y)
        self.pen.write(
            self.aktualis_viz_nev,
            align="center",
            font=("Arial", 18, "bold")
        )
        y -= 30
        self.pen.goto(0, y)
        self.pen.write(
            f"Koordináta: {self.lat:.3f}, {self.lon:.3f}",
            align="center",
            font=("Arial", 14, "normal")
        )
        y -= 30
        self.pen.goto(0, y)
        self.pen.write(
            f"Aktivitás: {self.aktivitasi_szint}",
            align="center",
            font=("Arial", 16, "normal")
        )
        y -= 30
        self.pen.goto(0, y)
        self.pen.write(
            self.holdfazis_szoveg or "Holdfázis: ismeretlen",
            align="center",
            font=("Arial", 16, "normal")
        )

    def _draw_bal_menu(self):
        self.pen.up()
        self.pen.goto(-430, 260)
        self.pen.write(
            "F = új fogás felvétele",
            font=("Arial", 12, "normal")
        )
        self.pen.goto(-430, 240)
        self.pen.write(
            "ESC = kilépés",
            font=("Arial", 12, "normal")
        )

    def _draw_fogas_lista(self):
        self.pen.up()
        self.pen.goto(0, -150)
        self.pen.write(
            "Utolsó fogások:",
            align="center",
            font=("Arial", 14, "bold")
        )
        y = -175
        for fogas in self.fogasok[-8:]:
            self.pen.goto(0, y)
            self.pen.write(
                f"{fogas.get('idopont')} – {fogas.get('hely')} – "
                f"{fogas.get('halfaj')} – {fogas.get('suly_kg')} kg "
                f"({fogas.get('aktivitas')})",
                align="center",
                font=("Arial", 11, "normal")
            )
            y -= 20

    def handle_new_catch(self):
        if not self.screen:
            return
        lista_szoveg = ""
        for i, (nev, _, _) in enumerate(self.horgaszvizek, start=1):
            lista_szoveg += f"{i}. {nev}\n"
        valasz = self.screen.textinput(
            "Horgászvíz választás",
            lista_szoveg + "Add meg a horgászvíz sorszámát:"
        )
        if not valasz:
            self._restore_events_after_dialog()
            return
        try:
            n = int(valasz)
            if 1 <= n <= len(self.horgaszvizek):
                viz_nev = self.horgaszvizek[n - 1][0]
            else:
                viz_nev = "Ismeretlen víz"
        except:
            viz_nev = "Ismeretlen víz"
        halfaj = self.screen.textinput("Új fogás", "Halfaj:")
        if not halfaj:
            self._restore_events_after_dialog()
            return
        suly = self.screen.textinput("Új fogás", "Súly (kg):")
        if not suly:
            self._restore_events_after_dialog()
            return
        try:
            suly_kg = float(suly.replace(",", "."))
        except:
            suly_kg = 0.0
        adat = {
            "idopont": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "hely": viz_nev,
            "halfaj": halfaj.strip(),
            "suly_kg": f"{suly_kg:.2f}",
            "aktivitas": self.aktivitasi_szint or "",
        }
        self.fogasok.append(adat)
        self.save_fogasok_to_csv()
        self.draw_all()
        self._restore_events_after_dialog()

    def _restore_events_after_dialog(self):
        if self.screen:
            self.register_events()

    def register_events(self):
        if not self.screen:
            return
        self.screen.listen()
        self.screen.onkey(self.handle_new_catch, "f")
        self.screen.onkey(self.handle_new_catch, "F")
        self.screen.onkey(self.exit_app, "Escape")

    def exit_app(self):
        self.save_fogasok_to_csv()
        if self.screen:
            self.screen.bye()

    def load_fogasok_from_csv(self, filename="fogasok.csv"):
        try:
            with open(filename, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                self.fogasok = list(reader)
        except:
            self.fogasok = []

    def save_fogasok_to_csv(self, filename="fogasok.csv"):
        fieldnames = ["idopont", "hely", "halfaj", "suly_kg", "aktivitas"]
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.fogasok)
