# Makeup by Lolka – koncept početne strane

Koncept dizajna početne strane za Makeup by Lolka (šminkanje i kursevi šminkanja, Beograd).
Dizajn je rađen kao Claude Design platno: https://claude.ai/artifact/43enF3QZxw77ocFH4VDKX1

Sajt: https://cze45.github.io/makeup-by-lolka/

Ovo nije zvanični sajt. Sve sa oznakom `[PRIMER]` čeka Lolkinu potvrdu.

## Šta je u repou

| Putanja | Sadržaj |
| --- | --- |
| `index.html` | Stranica za GitHub Pages, napravljena iz table za računar (radi i na telefonu) |
| `assets/sajt.js` | Meni, pauza utisaka, klizač 1. i 5. dana, karusel radova polaznica, pojavljivanje sekcija |
| `tools/build_site.py` | Pravi `index.html` iz `project/Racunar.dc.html` |
| `project/Main.dc.html` | Tabla za telefon (390 px) |
| `project/Racunar.dc.html` | Tabla za računar (1280 px, raste do širine prozora) |
| `project/canvas.json` | Raspored tabli na platnu |
| `assets/` | Slike i pozadine |
| `assets/radovi/` | Fotografije radova |
| `assets/blobs.json` | Koja `/_blob/…` adresa iz tabli odgovara kom fajlu u `assets/` |

## Izmene na platnu

`index.html` se ne menja ručno. Kad se tabla promeni na platnu, nova `Racunar.dc.html` ide u `project/`, pa:

```
python tools/build_site.py
```

Ako se na platnu promene podaci o kursevima ili radovima polaznica, iste izmene idu i u `COURSES` / `DECK`
u `tools/build_site.py`, jer ih tabla pravi u svojoj logici.

## Napomene

- `assets/hero.webp` je fotografija iz hero sekcije kojoj se donji deo topi u čistu studijsku pozadinu;
  `assets/hero-original.webp` je izvorna fotografija.
- `assets/mesh-bordo.webp` i `assets/mesh-beli.webp` su meke "zebra" teksture za pozadinu sekcija.
