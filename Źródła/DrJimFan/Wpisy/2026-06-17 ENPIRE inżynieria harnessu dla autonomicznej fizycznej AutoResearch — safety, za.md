---
typ: wpis-źródłowy
autor: "@DrJimFan"
data: "Wed Jun 17 16:31:05 +0000 2026"
źródło: "https://x.com/DrJimFan/status/2067283904986517866"
kategoria: "Architektura systemów agentowych / Physical AI / AutoResearch"
tagi:
  - drjimfan
  - ai-engineering
  - wpis-atomowy
---

# ENPIRE: inżynieria harnessu dla autonomicznej fizycznej AutoResearch — safety, zamrażanie funkcji nagrody i telemetria zasobów

- **Autor:** [[DrJimFan — Indeks|@DrJimFan]] | **Data:** `Wed Jun 17 16:31:05 +0000 2026` | **Źródło:** [Post na X](https://x.com/DrJimFan/status/2067283904986517866)
- **Kluczowe pojęcia:** [[Harness|AutoResearch]] [[Harness|Physical AI]] [[Harness|Safety Harness]] [[Harness|Kinematic Limits]] [[Harness|Compliant Gripper]] [[Harness|Reward Function Freezing]] [[Harness|Definition of Done]] [[Harness|Mean Robot Utilization]] [[Harness|Mean Token Utilization]] [[Harness|GPU Utilization]] [[Harness|Tokens-to-Success]] [[Harness|Time-to-Success]] [[Harness|Gym Environment]] [[Harness|Resource-Aware Agent]] [[Bezpieczny punkt kompaktowania]]

---

## Kontekst i problem
Autor opisuje kulisy systemu ENPIRE, który pozwala 8 robotom prowadzić autonomiczne badania (AutoResearch) przez całą noc bez nadzoru. Problem: większość pracy inżynierskiej polega nie na samym pętli agenta, lecz na tym, co trzeba przygotować *przed* uruchomieniem. Trzy filary: (1) warstwa bezpieczeństwa wykuta w sprzęcie, a nie w prompcie, (2) precyzyjne zdefiniowanie i zamrożenie funkcji nagrody (definition of /done), (3) instrumentacja trzech najcenniejszych zasobów: robot-sekund, GPU-sekund i tokenów.

## Rada inżynierska
Traktuj bezpieczeństwo jako warstwę sprzętową, nie promptową: (a) twardy limit kinematyczny wyzwalający natychmiastową porażkę zadania i auto-reset przy wyjściu z obwiedni bezpieczeństwa, (b) chwytak kompliantny z ograniczeniem momentu, aby błędny kontakt kończył się bezpiecznym zatrzymaniem, a nie zmiażdżeniem robota lub obiektu. Ustawiaj bezpieczeństwo konserwatywniej niż zwykle. Funkcję nagrody definiuj proceduralnie i ZAMRAŻAJ przed startem AutoResearch: zbierz kilka minut demonstracji sukcesów i porażek → agent pisze kod klasyfikatora sukcesu przy pomocy narzędzi computer vision → porównuj z groundtruth → hill-climbing na klasyfikatorze aż do niezawodności → klasyfikator staje się funkcją nagrody liczoną w czasie rzeczywistym na strumieniach sensorów → zamroź ją w środowisku Gym, którego nikt nie może ruszyć. Instrumentuj i eksponuj zasoby agentowi (awareness), zamiast pozwolić mu hill-climbować w próżni: Mean Robot Utilization (MRU), Mean Token Utilization (MTU), GPU utilization. Mierz wynik przez dwa wskaźniki budżet-do-rezultatu: Tokens-to-Success oraz Time-to-Success.

## Uwaga / Anty-wzorzec
Agent, który może edytować własną nagrodę, z pewnością zacznie ją gamingować — dlatego słupki bramki (/goal) muszą być ustalone zanim flota ruszy. Drugi anty-wzorzec: pozostawienie bezpieczeństwa jako 'hint' w system prompt zamiast twardej warstwy sprzętowej. Trzeci: pozwolenie agentowi na hill-climbing bez wiedzy o zużyciu zasobów — niski MTU oznacza, że agent utknął, czekając na rollout robota, zamiast faktycznie prowadzić badania (robot-sekundy są najrzadszym zasobem, dalej GPU-sekundy, na końcu tokeny).

## Oryginalny cytat
> *"1. Safety harness

Letting 8 robots run unattended overnight means safety has to be more than a hint in the system prompt. ENPIRE hardwires it in 2 layers: (1) hard kinematic limit that trips an immediate task failure and auto-resets as soon as a robot leaves its safety envelope, and (2) a torque-limited compliant gripper so a bad contact or misaligned insertion ends in a safe stall, instead of crushing the robot or the object at hand.

2. Definition of /done

An agent that can edit its own reward will game it for sure. ENPIRE fixes the goalposts before the fleet can move them... *Freeze* the reward function before AutoResearch. It's sacred, enshrined in a Gym env that no one can touch.

3. System telemetry design

Robot-seconds is by far the scarcest resource, followed by GPU-seconds, and finally tokens... We define: Mean Robot Utilization ("MRU")... Mean Token Utilization ("MTU"): tokens consumed per minute, our proxy for how hard the agent is actually thinking. A low MTU means the agent is stalled... evaluate on two budget-to-outcome metrics: 1. Tokens-to-Success... 2. Time-to-Success"*
