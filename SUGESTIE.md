# Pomysły na ulepszenia (`sprzatanie.html`)

Przegląd kodu — same propozycje, **nic w plikach nie zostało zmienione**.

## 🐞 Błędy / rzeczy do poprawienia w pierwszej kolejności

1. **Usuwanie wpisu nie usuwa go z chmury** (`delEntry`).
   Funkcja kasuje wpis tylko z `localStorage`. Jeśli użytkownik jest zalogowany,
   przy następnym `syncFromCloud()` skasowany wpis "wróci" z Firestore, bo merge
   robi `cloud overwrite local`. Trzeba dodać `db.collection(...).doc(date).delete()`.

2. **Brak edycji zapisanego wpisu.**
   Jedyna opcja to usunięcie i wpisanie od nowa albo nadpisanie wpisu z tą samą
   datą (z potwierdzeniem `confirm`). Przycisk „✏️ Edytuj” w historii, który
   wczytuje dany dzień z powrotem do formularza, byłby dużym ułatwieniem.

3. **Sync „cloud wins” może nadpisać świeższe dane lokalne.**
   `mergeEntries()` zawsze bierze wersję z chmury dla tej samej daty. Jeśli
   ktoś edytuje wpis offline na telefonie, a potem zaloguje się na komputerze
   ze starszą wersją w chmurze — dane z telefonu zostaną nadpisane przy kolejnym
   `syncFromCloud`. Warto dodać pole `updatedAt` (timestamp) i porównywać, która
   wersja jest nowsza.

4. **Brak migracji danych przy zmianie `STORAGE_KEY`.**
   Klucz to `sprzatanie_v3` — sugeruje, że wcześniej były `v1`/`v2`. Jeśli ktoś
   aktualizuje aplikację i miał dane pod starym kluczem, stracą je bez ostrzeżenia.
   Warto dodać prostą migrację/odczyt starych kluczy przy starcie.

5. **Możliwy XSS przez `innerHTML`.**
   Adresy obiektów, notatki i powód dopłaty trafiają bezpośrednio do `innerHTML`
   (`renderItems`, `renderHistory`, `renderMonth`, `updEarn`) bez escapowania.
   Przy danej trafiającej do współdzielonej bazy Firestore (np. w przyszłości
   współdzielone konto zespołu) ktoś mógłby wstrzyknąć `<script>`/`<img onerror>`.
   Warto dodać prostą funkcję `escapeHtml()` i użyć jej dla pól tekstowych
   wpisywanych przez użytkownika.

## 🔒 Bezpieczeństwo / Firebase

6. **Reguły bezpieczeństwa Firestore.**
   Instrukcja każe wybrać „Start in test mode” — takie reguły wygasają po
   30 dniach i są w pełni otwarte (każdy może czytać/pisać do całej bazy).
   Warto dopisać do instrukcji konkretne reguły, np.:
   ```
   match /users/{uid}/entries/{entry} {
     allow read, write: if request.auth != null && request.auth.uid == uid;
   }
   ```

7. **Konfiguracja Firebase trzymana w `localStorage` jako zwykły JSON** — to
   nie jest sekret (klucze webowe Firebase są publiczne), ale warto o tym
   wprost wspomnieć w UI, żeby użytkownik się nie martwił o „wyciek hasła do bazy”.

## ✨ Funkcjonalność, która mogłaby się przydać

8. **Edycja/usuwanie pojedynczego obiektu na liście** zamiast tylko dodawania
   i kasowania (np. zmiana adresu po literówce bez usuwania całego wpisu).

9. **„Skopiuj wczorajszy dzień”** — przycisk, który wypełnia formularz danymi
   z poprzedniego wpisu (te same obiekty/godziny), żeby przyspieszyć wpisywanie
   powtarzalnych tras.

10. **Wyszukiwanie w historii** po adresie/notatce, nie tylko filtr miesiąca —
    przydatne np. żeby sprawdzić, kiedy ostatnio sprzątano dany adres.

11. **Edytowalne stawki (`RATES`)** w zakładce Konto/Ustawienia — obecnie są
    zaszyte w kodzie. Zmiana cennika wymaga edycji pliku. Można dodać ekran
    ustawień zapisujący stawki do `localStorage`, z zachowaniem stawek
    historycznych (każdy zapisany wpis już ma `rate` per obiekt, więc stare
    wpisy się nie zepsują).

12. **Kalkulator zwrotu za paliwo / stawka za milę** — skoro mile są już
    zbierane, łatwo dodać pole „£/mila” i pokazywać kwotę zwrotu obok zarobków.

13. **Roczne podsumowanie / eksport rocznego raportu** (np. do rozliczenia
    podatkowego self-employed w UK) — agregacja po miesiącach z sumą roczną.

14. **Wykresy trendów w czasie** (np. zarobki/miesiąc na przestrzeni roku) —
    obecnie statystyki pokazują tylko sumę i podział na typy obiektów,
    bez perspektywy czasowej.

## 📱 PWA / offline

15. **Manifest + Service Worker.** Meta-tagi sugerują instalację na ekranie
    głównym telefonu, ale brak `manifest.json` i ikon (`apple-touch-icon`),
    więc nie pojawi się porządna ikona/splash po dodaniu do ekranu głównego.

16. **Skrypty z CDN wymagają internetu.** `xlsx.full.min.js` i Firebase SDK
    są ładowane z CDN — jeśli aplikacja ma działać offline (a dane trzyma
    lokalnie), warto rozważyć cache'owanie tych plików przez Service Worker
    albo dołączenie ich lokalnie, żeby eksport do Excela działał bez sieci.

## 🎨 Drobiazgi UI/UX

17. Brak trybu ciemnego (dark mode) — łatwo dodać przez media query
    `prefers-color-scheme`, skoro kolory są już w zmiennych CSS (`:root`).

18. W historii brak możliwości „cofnięcia” usunięcia wpisu (tylko `confirm`
    przed kasowaniem) — np. krótki toast z przyciskiem „Cofnij”.

19. Format walutowy (£) jest zaszyty w wielu miejscach jako tekst — jeśli
    kiedyś aplikacja miałaby obsługiwać inną walutę, wymagałoby to zmian
    w wielu miejscach zamiast jednej stałej/funkcji formatującej.

---

To są wyłącznie propozycje — żaden plik projektu nie został zmodyfikowany.
