# Dziennik Sprzątania – aplikacja webowa

Pojedynczy plik HTML (`sprzatanie.html`) – progresywna aplikacja webowa (PWA-like, działa offline)
do rejestrowania dni pracy przy sprzątaniu, liczenia zarobków i eksportu danych do Excela.

## Stack technologiczny

- **Brak builda** – czysty HTML + CSS + vanilla JS w jednym pliku.
- **xlsx.full.min.js** (CDN, SheetJS) – eksport do Excela.
- **Firebase 9.22.2 (compat)** – Authentication (email/hasło) + Firestore – opcjonalna
  synchronizacja danych między urządzeniami.
- **localStorage** – główne, zawsze dostępne źródło danych (`sprzatanie_v3`),
  działa nawet bez konfiguracji Firebase.

## Struktura aplikacji (zakładki)

1. **➕ Wpis** – formularz nowego dnia pracy:
   - data, godzina startu/końca → automatyczne wyliczenie godzin pracy,
   - przejechane mile,
   - lista obiektów (apartamenty/hotele/klatki) ze stawkami i opcjonalnym adresem,
   - licznik pościeli z garażu (£5/szt.),
   - dopłata dodatkowa z opisem powodu,
   - notatki tekstowe,
   - podgląd zarobków na żywo, zapis do localStorage + push do Firestore.

2. **📋 Historia** – lista zapisanych dni z filtrem po miesiącu, usuwanie wpisów,
   eksport do Excela (2 arkusze: podsumowanie + obiekty z adresami).

3. **📅 Miesiąc** – podsumowanie wybranego miesiąca: liczba dni, godzin, zarobków,
   liczba obiektów wg typu, lista adresów, rozpiska dzień po dniu.

4. **📊 Statystyki** – statystyki łączne (cały zapisany okres) + wykresy słupkowe
   udziału poszczególnych typów obiektów.

5. **👤 Konto** – logowanie/rejestracja Firebase, synchronizacja chmurowa,
   konfiguracja Firebase (wklejenie `firebaseConfig`), lokalny backup JSON
   (eksport/import).

## Stawki (`RATES`)

| Typ              | Stawka |
|------------------|--------|
| Apt. 1B          | £20    |
| Apt. 2B          | £40    |
| Apt. 3B          | £60    |
| Apt. 4B          | £70    |
| Hotel 1B         | £18    |
| Hotel 2B         | £36    |
| Hotel 3B         | £54    |
| Klatka schodowa  | £17    |
| Pościel z garażu | £5/szt.|

## Model danych wpisu (localStorage `sprzatanie_v3`)

```json
{
  "date": "2026-06-11",
  "start": "08:00",
  "end": "16:00",
  "hoursWorked": 8,
  "miles": 12.5,
  "items": [{ "type": "a2b", "address": "108 Nicholson Street", "rate": 40 }],
  "a1b": 0, "a2b": 1, "...": "...",
  "totalApts": 1,
  "beddingCount": 2,
  "beddingEarned": 10,
  "earnedBase": 40,
  "extra": 5,
  "extraReason": "bardzo brudno",
  "earned": 55,
  "notes": "..."
}
```

## Plik `Praca sprzatanie razem.xlsx`

Arkusz Excel, prawdopodobnie wcześniejsza/manualna wersja dziennika pracy,
która posłużyła jako wzór do zaprojektowania aplikacji (struktura kolumn,
stawki, sposób liczenia godzin i zarobków).
