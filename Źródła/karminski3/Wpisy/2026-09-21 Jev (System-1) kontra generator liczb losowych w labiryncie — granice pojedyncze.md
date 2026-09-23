---
typ: wpis-źródłowy
autor: "@karminski3"
data: "Mon Sep 21 07:49:04 +0000 2026"
źródło: "https://x.com/karminski3/status/2101941770003361893"
kategoria: "Architektura systemów agentowych / Ocena modeli / Planowanie wieloetapowe"
tagi:
  - karminski3
  - ai-engineering
  - wpis-atomowy
---

# Jev (System-1) kontra generator liczb losowych w labiryncie — granice pojedynczego kroku decyzyjnego

- **Autor:** [[karminski3 — Indeks|@karminski3]] | **Data:** `Mon Sep 21 07:49:04 +0000 2026` | **Źródło:** [Post na X](https://x.com/karminski3/status/2101941770003361893)
- **Kluczowe pojęcia:** [[Harness|System-1 vs System-2]] [[Harness|Optimum lokalne]] [[Harness|Twierdzenie Pólyi o błądzeniu losowym]] [[Harness|Maze pathfinding]] [[Harness|Heurystyka Manhattan]] [[Harness|Backtracking]] [[Harness|Planowanie wieloetapowe]] [[Harness|xoshiro256++]] [[Harness|Benchmark modeli]] [[Harness|Nagła śmierć (sudden death)]]

---

## Kontekst i problem
Autor @karminski3 poddał w wątpliwość sens stosowania szybkiego modelu System-1 (Jev) do zadań wymagających planowania. Zbudował środowisko testowe typu labirynt (maze pathfinding) w Rust (xoshiro256++ + bit reservoir + Tokio/Hyper) i wystawił serwer czystego generatora losowego o API identycznym z Jevem. Teoretyczną podstawą eksperymentu jest twierdzenie Pólyi o błądzeniu losowym (Pólya's Random Walk Theorem): w skończonej, spójnej siatce 2D prosty błądzenie losowe jest nawracające (recurrent), więc 'pijany' agent z prawdopodobieństwem 1 w końcu trafi do celu. Celem było sprawdzenie, czy tak szybki model jak Jev nie zostanie czasem pokonany przez bezmyślny random w zadaniu wymagającym nawigacji.

## Rada inżynierska
Traktuj modele typu System-1 (szybkie, pojedynczokrokowe klasyfikatory/decyzyjne) wyłącznie jako jednostki strukturalnej oceny jednego kroku — NIE jako planery. Gdy zadanie wymaga obejścia przeszkody, cofania się (backtracking) lub wieloetapowego planowania, dołącz model System-2 (planner/reasoner) albo użyj klasycznego algorytmu wyszukiwania. W eksperymencie czysty RNG wygrał z Jevem: random ukończył labirynt w 892 krokach w <300 ms, podczas gdy Jev utknął w optimum lokalnym (2295 z 2306 kroków w 3 komórkach narożnika (7,4)) aż do timeoutu. Wniosek inżynierski: dla problemów, gdzie heurystyka lokalna rozmija się z optimum globalnym, pojedynczy krok decyzyjny jest strukturalnie niewystarczający.

## Uwaga / Anty-wzorzec
Pułapka: dostarczenie modelowi historii (last_move, visited_count sąsiadów) oraz heurystyki (odległość Manhattan) NIE gwarantuje, że model będzie z niej korzystał. Jev zignorował regułę drugorzędną ('gdy bliższa komórka jest zablokowana lub zbyt często odwiedzana, wybierz najmniej odwiedzone otwarcie'), ponieważ w jego jednostkowym rozumieniu sąsiednie komórki w prawo/dół miały mniejszą odległość Manhattan — reguła warunkowa nigdy nie została wywołana. To klasyczne uwięzienie w optimum lokalnym: model optymalizuje sygnał heurystyczny kroku, nie stan globalny. Anty-wzorce: (1) powierzanie Jev/System-1 zadań z nagłą śmiercią (snake, Tetris, jazda autonomiczna — jeden zły krok = koniec); (2) nieodwracalne decyzje o wysokim koszcie (DROP bazy danych, operacje transakcyjne, scenariusze audytowe); (3) problemy grafowe, gdzie lokalna heurystyka i optimum globalne się rozchodzą (labirynty, bin packing, scheduling).

## ⚡ Kwestia sporna / do rozstrzygnięcia
Teza kontrowersyjna wobec powszechnego konsensusu, że lepszy/nowszy model zawsze bije baseline. Autor dowodzi, że w zadaniach nawigacyjnych szybki model System-1 może zostać systematycznie pobity przez czysty RNG (nawet bez równoległości), ponieważ sam RNG korzysta z własności nawracalności błądzenia losowego. Do rozstrzygnięcia: w jakich dokładnie klasach zadań 'głupi, ale szybki' random jest realnym baseline'em, którego nie wolno pomijać w ewaluacji, oraz kiedy dołożenie pamięci/heurystyki do System-1 daje regresję zamiast poprawy (bo reguły warunkowe nigdy nie zostają wywołane).

## Oryginalny cytat
> *"为什么Jev有些时候不如随机数发生器? ... 测了一波后直接说结论：纯随机赢麻了, Jev 被系统性打崩了 ... 所以, Jev 它只是一个极速的单步结构化判断器, 但绝不是规划器. 最好还是带一个System-2模型才能进行复杂任务. ... 最后给大家整理慎用 Jev 的场景：需要绕路, 回溯, 多步规划的：迷宫, 装箱, 调度等局部启发和全局最优不一致的图问题. 突然死亡型控制：贪吃蛇, 俄罗斯方块, 自动驾驶等. 一步踏错当场GG. 不可逆高代价决策：删库, 事务操作, 尤其是需要审计的场景."*
