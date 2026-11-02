# Makeup by Lolka – koncept početne strane

Koncept dizajna početne strane za Makeup by Lolka (šminkanje i kursevi šminkanja, Beograd).
Dizajn je rađen kao Claude Design platno: https://claude.ai/artifact/43enF3QZxw77ocFH4VDKX1

Ovo nije zvanični sajt. Sve sa oznakom `[PRIMER]` čeka Lolkinu potvrdu.

## Šta je u repou

| Putanja | Sadržaj |
| --- | --- |
| `project/Main.dc.html` | Tabla za telefon (390 px) |
| `project/Racunar.dc.html` | Tabla za računar (1280 px, raste do širine prozora) |
| `project/canvas.json` | Raspored tabli na platnu |
| `assets/` | Slike i pozadine koje table koriste |
| `assets/radovi/` | Fotografije radova |
| `assets/blobs.json` | Koja `/_blob/…` adresa iz tabli odgovara kom fajlu u `assets/` |
| `preview/` | Statičan pregled obe table sa lokalnim slikama |

## Napomene

- Table su u `.dc.html` formatu Claude Design platna. Slike se u njima učitavaju preko `/_blob/…`
  adresa platna; `assets/blobs.json` ih mapira na fajlove u ovom repou.
- `preview/` se otvara direktno u pregledaču. To je samo statičan pregled: delovi koji se popunjavaju
  logikom table (kartice kurseva, karusel polaznica, dugme za pauzu utisaka) tamo prikazuju `{{…}}`
  umesto sadržaja. Pravi izgled je na platnu.
- `assets/hero.webp` je fotografija iz hero sekcije kojoj se donji deo topi u čistu studijsku pozadinu;
  `assets/hero-original.webp` je izvorna fotografija.
- `assets/mesh-bordo.webp` i `assets/mesh-beli.webp` su meke "zebra" teksture za pozadinu sekcija.
