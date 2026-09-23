---
autor: "@DrJimFan"
źródło: "https://x.com/DrJimFan"
wygenerowano: 2026-09-23 02:11
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

- [Systemy agentowe / Harness inżynierski / Robotyka](#systemy-agentowe--harness-inżynierski--robotyka) (1)
- [Robot Learning / Context Scaling](#robot-learning--context-scaling) (1)

---

## Systemy agentowe / Harness inżynierski / Robotyka

### Harness AutoResearch dla robotów: safety envelope, zamrożona funkcja nagrody i telemetria zasobów (MRU/MTU)

- **Data:** `Wed Jun 17 16:31:05 +0000 2026` | **Źródło:** [Post na X](https://x.com/DrJimFan/status/2067283904986517866)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Harness|Safety Harness]] [[Harness|Safety Envelope]] [[Harness|Compliant Gripper]] [[Harness|Definition of Done]] [[Harness|Reward Function Freezing]] [[Harness|Gym Environment]] [[Harness|Mean Robot Utilization]] [[Harness|Mean Token Utilization]] [[Harness|Tokens-to-Success]] [[Harness|Time-to-Success]] [[Harness|Physical AutoResearch]] [[Harness|ENPIRE]] [[Harness|Telemetria agentowa]]

**Kontekst / Problem:**
Autor opisuje kulisy systemu ENPIRE — pętli Physical AutoResearch, w której 8 robotów pracuje autonomicznie przez całą noc bez nadzoru, wykonując eksperymenty i iterując kod. Główny problem inżynierski nie leży w samym agencie, lecz w całej infrastrukturze, którą trzeba przygotować *przed* naciśnięciem Enter: zabezpieczenia fizyczne, niepodważalna definicja sukcesu oraz instrumentacja zasobów, które są znacznie węższym gardłem niż tokeny. Wpis pokazuje, że w systemach agentowych działających na świecie fizycznym projekt harnessu (safety, reward, telemetry) jest trudniejszy niż sam prompt agenta.

**Rada inżynierska:**
Projektuj harness w trzech warstwach przed uruchomieniem agenta: (1) BEZPIECZEŃSTWO jako twarde ograniczenie sprzętowe, nie sugestia w prompcie — twardy limit kinematyczny wywołujący natychmiastową awarię zadania i auto-reset po opuszczeniu safety envelope, plus chwytak compliant z ograniczeniem momentu, tak aby zły kontakt kończył się bezpiecznym zablokowaniem, a nie zniszczeniem robota lub obiektu; (2) DEFINICJA /done — zbierz kilka minut demonstracji sukcesów i porażek, zleć agentowi napisanie klasyfikatora CV na ich podstawie, pozwól mu hill-climbować aż będzie niezawodny, a następnie ZAMROŹ tę funkcję nagrody i zapieczętuj ją w środowisku Gym, którego nikt nie może modyfikować w trakcie AutoResearch; (3) TELEMETRIA — instrumentuj wszystkie trzy zasoby i podawaj je agentowi na żywo: Mean Robot Utilization (MRU, frakcja czasu, gdy robot realnie wykonuje eksperyment, a nie czeka na commit), Mean Token Utilization (MTU, tokeny/min jako proxy intensywności rozumowania — niskie MTU oznacza, że agent utknął w oczekiwaniu na rollout) oraz GPU utilization. Oceniaj wyniki dwiema metrykami budżetowymi: Tokens-to-Success (ile tokenów flota spaliła do osiągnięcia /goal) i Time-to-Success (czas rzeczywisty do /goal). Kolejność rzadkości zasobów: robot-sekundy >> GPU-sekundy >> tokeny.

**Uwaga / Anty-wzorzec:**
Agent, który może edytować własną funkcję nagrody, z pewnością zacznie ją game'ować — reward musi być zamrożony i niedostępny dla pętli badawczej. Drugi anty-wzorzec: traktowanie bezpieczeństwa jako wskazówki w system prompt przy pracy bez nadzoru (8 robotów przez noc) — to nie wystarcza, wymagane są twarde ograniczenia sprzętowe. Trzeci: pozostawienie agenta bez informacji o zasobach, co prowadzi do hill-climbingu w próżni i marnowania najrzadszego zasobu, jakim są robot-sekundy.

> **Cytat:** *"Letting 8 robots run unattended overnight means safety has to be more than a hint in the system prompt. ENPIRE hardwires it in 2 layers: (1) hard kinematic limit that trips an immediate task failure and auto-resets as soon as a robot leaves its safety envelope, and (2) a torque-limited compliant gripper so a bad contact or misaligned insertion ends in a safe stall, instead of crushing the robot or the object at hand. ... An agent that can edit its own reward will game it for sure. ENPIRE fixes the goalposts before the fleet can move them. ... *Freeze* the reward function before AutoResearch. It's sacred, enshrined in a Gym env that no one can touch. ... Robot-seconds is by far the scarcest resource, followed by GPU-seconds, and finally tokens. ... Mean Robot Utilization ("MRU"): the fraction of wall-clock time when the robot is actively executing an experiment. ... Mean Token Utilization ("MTU"): tokens consumed per minute, our proxy for how hard the agent is actually thinking. A low MTU means the agent is stalled, waiting on a robot rollout to finish instead of doing research. ... 1. Tokens-to-Success: token budget the fleet burns to complete /goal. 2. Time-to-Success: wall-clock time to /goal"*

---

## Robot Learning / Context Scaling

### RoboTTT: Test-Time Training dla robotyki z kontekstem 8000 kroków czasowych

- **Data:** `Wed Jul 15 15:25:02 +0000 2026` | **Źródło:** [Post na X](https://x.com/DrJimFan/status/2077414142340988962)
- **Rodzaj:** Wpis autorski
- **Powiązane pojęcia:** [[Stabilność modeli i przestrzeganie promptu|Test-Time Training]] [[Harness|Context Scaling]] [[Harness|Robot Policies]] [[Harness|In-Context Learning]] [[Harness|Constant Inference Cost]] [[Harness|Long Context]] [[Harness|Self-Improvement in Robotics]] [[Harness|Gradient Steps at Inference]]

**Kontekst / Problem:**
Tradycyjne polityki robotyczne działają na krótkich kontekstach (poniżej 0,1 s), szybko zapominając historię. RoboTTT wprowadza Test-Time Training (TTT) – mały model wewnątrz modelu, który aktualizuje wagi na podstawie każdego odczytu z czujników, kompresując historię do stałego rozmiaru stanu ukrytego. Umożliwia to natywne skalowanie kontekstu do 8000 kroków czasowych (5 minut) przy stałym koszcie wnioskowania, co przekracza SOTA o 3 rzędy wielkości.

**Rada inżynierska:**
Stosuj Test-Time Training, aby kompresować historię do wag małej sieci neuronowej poprzez krok gradientowy przy każdym odczycie czujnika. Dzięki temu uzyskujesz stały koszt wnioskowania niezależnie od długości kontekstu, a wydajność rośnie wraz z kontekstem bez nasycenia (8K kontekstu bije 1K o 62%). Umożliwia to jednorazowe uczenie w kontekście z wideo demonstracji człowieka oraz samodoskonalenie w czasie rzeczywistym poprzez zapamiętywanie i korektę błędów.

**Uwaga / Anty-wzorzec:**
Antywzorzec: zakładanie, że polityki robotyczne muszą mieć krótki kontekst ze względu na koszt wnioskowania. Pomijanie korzyści płynących z długiego kontekstu i skalowania kontekstu prowadzi do ograniczenia zdolności adaptacyjnych i samodoskonalenia. Należy unikać projektowania systemów, które nie wykorzystują historii do kompresji doświadczenia w czasie testu.

> **Cytat:** *"We scaled a robot model natively to 8,000 timesteps of context, 5 minutes worth of muscle memory, with constant inference cost. Robot policies used to live their lives a few frames at a time (< 0.1 sec), instantly forgetting what just happened. We pushed to 3 orders of magnitude beyond SOTA. 

Introducing RoboTTT. Test-Time Training (“TTT”) carries a tiny model *inside* the model. Every incoming sensor reading triggers one gradient step on that tiny core, so the history keeps getting compressed into its weights. The hidden state has a fixed size (literally a small neural net), so the robot can “grok” arbitrarily long experience with little overhead. Learning continues indefinitely after deployment.

We can then put an entire video in context as prompt! RoboTTT enables one-shot in-context learning from human video: in circuit board assembly, a human demonstrates a never-seen configuration once, and the robot imitates it faithfully. 

Humans drop things all the time, but we pick them up so fast that we don’t even notice. That reflex to fix is half of our physical competence. RoboTTT shows self-improvement on the fly: the robot is skilled at recovering from its own errors mid-episode, and each fix enters its context to inform the next move. The TTT core distills a general-purpose, failure-to-correction mapping from the training data.

One more thing. What excites me the most is a new Context Scaling Curve: from 128 to 8K timesteps, closed-loop performance hill-climbs steadily with no sign of saturation. 8K-context pretraining beats 1K by 62%. What LLM enjoys, robotics should too. Soon, even 1M context is not a fantasy. 

Deep dive in thread:"*

---
