---
autor: "@DrJimFan"
źródło: "https://x.com/DrJimFan"
wygenerowano: "2026-09-23 02:26"
typ: synteza-wiedzy
tagi:
  - drjimfan
  - ai-engineering
  - prompt-engineering
  - twitter-extract
---

# @DrJimFan — Baza Wskazówek i Komentarzy

> Destylacja praktycznych porad, heurystyk inżynierskich i komentarzy technicznych z profilu @DrJimFan na platformie X. Wyciągnięto 2 wartościowych wpisów.

## Spis kategorii

- [Architektura harnessu agentowego / Inżynieria systemów autonomicznych](#architektura-harnessu-agentowego--inżynieria-systemów-autonomicznych) (1)
- [Inżynieria kontekstu / Test-Time Training / Systemy agentowe (robotyka)](#inżynieria-kontekstu--test-time-training--systemy-agentowe-(robotyka)) (1)

---

## Architektura harnessu agentowego / Inżynieria systemów autonomicznych

### ENPIRE: harness autonomicznych badań robotycznych — warstwy bezpieczeństwa, zamrażanie funkcji nagrody i telemetria zasobów

- **Data:** `Wed Jun 17 16:31:05 +0000 2026` | **Źródło:** [Post na X](https://x.com/DrJimFan/status/2067283904986517866)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|Harness agentowy]] [[Harness|Physical AutoResearch]] [[Harness|ENPIRE]] [[Harness|Funkcja nagrody]] [[Harness|Reward hacking]] [[Harness|Safety envelope]] [[Harness|Zamrażanie nagrody]] [[Harness|Mean Robot Utilization]] [[Harness|Mean Token Utilization]] [[Harness|Tokens-to-Success]] [[Harness|Time-to-Success]] [[Harness|Telemetria zasobów]] [[Harness|Gym environment]] [[Harness|Hill-climbing na klasyfikatorze]] [[Harness|Kompliantny chwytak]]

**Kontekst / Problem:**
Autor opisuje kulisy systemu ENPIRE (Physical AutoResearch), w którym 8 robotów pracuje bez nadzoru przez całą noc, samodzielnie prowadząc eksperymenty badawcze. Problem: jak zbudować harness, który pozwoli agentowi na iteracyjne ulepszanie polityk robotycznych, nie zabijając sprzętu, nie oszukując metryk sukcesu i nie marnując najdroższego zasobu — czasu pracy robota. Wpis dotyczy tego, co trzeba przygotować *przed* uruchomieniem pętli autonomicznej, a nie samego promptu.

**Rada inżynierska:**
1) Bezpieczeństwo musi być zakodowane w warstwie sprzętowej, nie w promptcie: (a) twardy limit kinematyczny → natychmiastowa porażka zadania i auto-reset po wyjściu z koperty bezpieczeństwa; (b) chwytak z ograniczonym momentem obrotowym → zły kontakt kończy się bezpiecznym zablokowaniem, nie zmiażdżeniem robota/obiektu. 2) Zdefiniuj '/done' zanim uruchomisz pętlę: zbierz kilka minut demonstracji sukcesów i porażek → agent pisze klasyfikator CV i porównuje z groundtruth → hill-climb na klasyfikatorze aż do niezawodności → klasyfikator staje się funkcją nagrody liczącą w czasie rzeczywistym na strumieniach sensorów → ZAMROŹ funkcję nagrody w środowisku Gym, którego nikt nie może modyfikować. Agent, który może edytować własną nagrodę, zawsze ją zgaminguje. 3) Instrumentuj hierarchię zasobów: robot-sekundy (najrzadsze) > GPU-sekundy > tokeny. Mierz MRU (Mean Robot Utilization — frakcja czasu, gdy robot aktywnie wykonuje eksperyment), MTU (Mean Token Utilization — tokeny/min jako proxy intensywności rozumowania agenta) oraz GPU utilization. Ewaluuj przez Tokens-to-Success i Time-to-Success. Niska MTU = agent zablokowany na rolloucie zamiast prowadzić badania.

**Uwaga / Anty-wzorzec:**
Pozostawienie bezpieczeństwa jako 'wskazówki w system promptcie' przy pracy bez nadzoru. Powierzenie agentowi kontroli nad definicją sukcesu (edytowalna funkcja nagrody = gwarantowany reward hacking). Hill-climbing agenta 'w próżni' bez telemetrii zasobów — agent nie widzi, że hardware stoi bezczynnie i czeka na commit kodu.

> **Cytat:** *"I made Physical AutoResearch sound simple (conceptually), but it took a village to pull off and lots of design thinking into the robot /loopcraft. The hardest part is everything we need to setup *before* pressing Enter. Here's a behind-the-scene tour:

1. Safety harness

Letting 8 robots run unattended overnight means safety has to be more than a hint in the system prompt. ENPIRE hardwires it in 2 layers: (1) hard kinematic limit that trips an immediate task failure and auto-resets as soon as a robot leaves its safety envelope, and (2) a torque-limited compliant gripper so a bad contact or misaligned insertion ends in a safe stall, instead of crushing the robot or the object at hand. 

We make safety more conservative than usual so humans can sleep tight. In reality, we still need a few human operators to watch over the "robots of loving grace". 

2. Definition of /done

An agent that can edit its own reward will game it for sure. ENPIRE fixes the goalposts before the fleet can move them. Here's the recipe:

Collect a few minutes of success & failure demos
-> Ask agent to write code using computer vision tools to classify success and measure against groundtruth
-> Agent hill-climbs on classifier until reliably good
-> This classifier becomes the real-time reward function that directly computes on sensor streams 
-> *Freeze* the reward function before AutoResearch. It's sacred, enshrined in a Gym env that no one can touch.

3. System telemetry design

Robot-seconds is by far the scarcest resource, followed by GPU-seconds, and finally tokens. We instrument all three and surface them to ENPIRE for live resource awareness rather than letting it hill-climb in a vacuum. 

We define:
- Mean Robot Utilization ("MRU"): the fraction of wall-clock time when the robot is actively executing an experiment. Otherwise the hardware is sitting idle and waiting for the next code commit.
- Mean Token Utilization ("MTU"): tokens consumed per minute, our proxy for how hard the agent is actually thinking. A low MTU means the agent is stalled, waiting on a robot rollout to finish instead of doing research.
- GPU utilization: fraction of wall-clock time when GPU is active. 

... and evaluate on two budget-to-outcome metrics:

1. Tokens-to-Success: token budget the fleet burns to complete /goal.
2. Time-to-Success: wall-clock time to /goal"*

---

## Inżynieria kontekstu / Test-Time Training / Systemy agentowe (robotyka)

### RoboTTT: skalowanie natywnego kontekstu polityk robotycznych do 8K kroków czasowych (5 min) przez Test-Time Training przy stałym koszcie inferencji

- **Data:** `Wed Jul 15 15:25:02 +0000 2026` | **Źródło:** [Post na X](https://x.com/DrJimFan/status/2077414142340988962)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|Test-Time Training]] [[Harness|Context Scaling Curve]] [[Harness|In-Context Learning]] [[Harness|One-shot Learning]] [[Harness|Robot Policy]] [[Harness|Hidden State]] [[Harness|Constant Inference Cost]] [[Harness|Context Engineering]] [[Harness|Continual Learning]]

**Kontekst / Problem:**
Klasyczne polityki robotyczne działały w reżimie kilku klatek naraz (<0,1 s), natychmiast zapominając niedawną historię i nie ucząc się po wdrożeniu. RoboTTT rozwiązuje problem pamięci długoterminowej i ciągłego uczenia przez natywne skalowanie kontekstu do 8 000 kroków czasowych (≈5 minut „pamięci mięśniowej”) przy stałym koszcie inferencji — o trzy rzędy wielkości ponad poprzedni SOTA. Architektura opiera się na Test-Time Training (TTT): wewnątrz modelu żyje miniaturowy model-rdzeń, a każdy odczyt z sensora wyzwala pojedynczy krok gradientu aktualizujący jego wagi. Historia jest więc bezustannie kompresowana do wag o stałym rozmiarze stanu ukrytego (faktycznie mała sieć neuronowa), co pozwala robotowi „ogarnąć” dowolnie długie doświadczenie przy minimalnym narzucie obliczeniowym i kontynuować uczenie po wdrożeniu. Umożliwia to też one-shot in-context learning z wideo demonstracji człowieka (np. montaż płytki PCB w nieznanej konfiguracji) oraz self-improvement w locie — korekty własnych błędów wchodzą do kontekstu i informują kolejne ruchy.

**Rada inżynierska:**
Stosuj Test-Time Training jako mechanizm pamięci o stałym koszcie: trzymaj mały rdzeń wewnątrz modelu i wykonuj jeden krok gradientu na każdy napływający token/odczyt sensora, kompresując historię do wag zamiast rozrastającego się bufora KV. To daje stały rozmiar stanu ukrytego, stały koszt inferencji i nieograniczone uczenie po wdrożeniu. Traktuj długość kontekstu jako wymiar skalowania — buduj krzywe skalowania kontekstu (Context Scaling Curve) i weryfikuj, czy wydajność pętli zamkniętej rośnie monotonicznie bez saturacji: w RoboTTT pretrening na 8K kontekstu bije 1K o 62%. Wnioski przenoś między domenami: „Co lubi LLM, powinna lubić też robotyka” — skoro modele językowe czerpią korzyść z długiego kontekstu, polityki robotyczne również.

**Uwaga / Anty-wzorzec:**
Anty-wzorzec: projektowanie polityk działających „kilka klatek naraz” (<0,1 s) z natychmiastowym zapominaniem historii — to eliminuje możliwość uczenia się z błędów, naśladowania demonstracji i płynnego recovery. Drugą pułapką jest zakładanie, że dłuższy kontekst zawsze daje saturację lub nieproporcjonalny koszt — RoboTTT pokazuje hill-climbing bez saturacji, więc rezygnacja ze skalowania kontekstu z góry jest błędem. Uwaga też na wiarę, że zdolność do korekty błędów musi być zaprogramowana ręcznie — TTT destyluje ogólną mapę „porażka→korekta” z danych treningowych.

> **Cytat:** *"We scaled a robot model natively to 8,000 timesteps of context, 5 minutes worth of muscle memory, with constant inference cost. Robot policies used to live their lives a few frames at a time (< 0.1 sec), instantly forgetting what just happened. We pushed to 3 orders of magnitude beyond SOTA. ... Test-Time Training ("TTT") carries a tiny model *inside* the model. Every incoming sensor reading triggers one gradient step on that tiny core, so the history keeps getting compressed into its weights. The hidden state has a fixed size (literally a small neural net), so the robot can "grok" arbitrarily long experience with little overhead. ... What excites me the most is a new Context Scaling Curve: from 128 to 8K timesteps, closed-loop performance hill-climbs steadily with no sign of saturation. 8K-context pretraining beats 1K by 62%. What LLM enjoys, robotics should too. Soon, even 1M context is not a fantasy."*

---
