# Horgász Szolunáris Asszisztens 

**Hallgató:** Sőrés József  
**Tárgy:** Szkript nyelvek – Python  
**Projekt típusa:** Egyéni beadandó  
**Technológiák:** Python, Turtle grafika, Requests API, CSV fájlkezelés  

---

# 1. A feladat rövid leírása

A beadandó célja egy Python alapú, grafikus horgász asszisztens elkészítése.  
A program feladata, hogy a kiválasztott horgászvíz alapján lekérje az adott terület **holdfázisát**, meghatározza a **szolunáris aktivitást**, és lehetőséget adjon **fogások rögzítésére**, amelyek CSV fájlban kerülnek mentésre.

Az alkalmazás:

- horgászvizet lehet kiválasztani egy listából,
- megjeleníti a hely koordinátáit,
- API segítségével lekérdezi a holdfázist,
- aktivitási szintet számít (erős / közepes / gyenge),
- CSV fájlban fogásnaplót vezet,
- grafikus felületen megjeleníti:
  - címet,
  - horgászvíz nevét,
  - koordinátákat,
  - aktivitást,
  - holdfázist (szöveg + piktogram),
  - az utolsó 8 fogást,
- eseményvezérelten működik:
  - **F** → új fogás rögzítése  
  - **ESC** → kilépés  

---

# 2. Indításhoz szükséges modulok

A program kizárólag olyan modulokat használ, amelyek minden hallgató számára elérhetők.

| Modul | Típus | Funkció |
|-------|-------|---------|
| `turtle` | beépített | grafikus felület, rajzolás, eseménykezelés |
| `requests` | külső | webes API hívás (holdfázis) |
| `csv` | beépített | fogásnapló mentése/betöltése |
| `datetime` | beépített | időbélyeg létrehozása |
| `math` | beépített | számítások a holdfázishoz |

Telepítés:
```bash
pip install requests
