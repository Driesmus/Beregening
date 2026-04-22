# 🌱 Slimme Beregening voor Home Assistant

Een complete en flexibele **automatische beregeningsoplossing** voor Home Assistant, inclusief:

* 💧 Automatische planning per zone
* 🌦️ Weerafhankelijke logica (regen & temperatuur)
* 🧠 Slimme beslissingen wanneer wel/niet sproeien
* 📊 Dashboard met realtime voortgang
* ⏱️ Visuele timerbalken per zone
* 🎛️ Handmatige bediening per zone

---

## ✨ Features

### 🌦️ Slimme automatisering

* Start op basis van:

  * 🌅 Zonsopkomst
  * 🌇 Zonsondergang
  * ⏰ Vaste tijd
* Houdt rekening met:

  * Regen nu
  * Regen komende 24 uur
  * Minimale temperatuur

---

### 💧 Zonebeheer
- 🔄 **Onbeperkt aantal zones (volledig dynamisch)**
- Voeg simpelweg zones toe in je configuratie — de rest wordt automatisch gegenereerd
- Per zone:
  - ⏱️ Eigen duur
  - 📅 Eigen dagen (weekplanner)
  - ▶️ Handmatige start
  - 📊 Eigen timerbalk met realtime voortgang

---

### 📊 Dashboard

* Overzichtelijke UI met:

  * Actieve status
  * Totale geplande duur
  * Resterende tijd
  * Eindtijd
* Per zone:

  * Timerbalk (visueel)
  * Realtime voortgang
  * Automatisch kleurgebruik:

    * 🔴 Uit → verborgen tekst
    * 🟢 Actief → fel groen

---

### 🔐 Veiligheid

* Automatische stop bij:

  * Regen
  * Te lage temperatuur
* Fail-safe:

  * Alles uit bij Home Assistant restart
* Max looptijd beveiliging (10 uur)

---

## 📦 Installatie

### 1. Clone of download dit project

Plaats de bestanden in je Home Assistant config map:

```bash
/config/
```

---

### 2. Maak een configuratiebestand

Maak een bestand:

```
beregening_tuin_config.yaml
```

Voorbeeld:

```yaml
slug: beregening_tuin
title: Beregening Tuin
weather_entity: weather.home

zones:
  - name: Zone 1
    relay: switch.zone_1
  - name: Zone 2
    relay: switch.zone_2
  - name: Zone 3
    relay: switch.zone_3
```

---
### ➕ Zones toevoegen

Je kunt **zoveel zones toevoegen als je wilt**.

Voorbeeld:

```yaml
zones:
  - name: Voortuin
    relay: switch.voortuin

  - name: Achtertuin
    relay: switch.achtertuin

  - name: Kas
    relay: switch.kas

  - name: Bloemenborder
    relay: switch.border


### 3. Run de generator

```bash
python3 jouw_script.py
```

Dit maakt:

* `beregening_tuin.yaml` → Home Assistant package
* `beregening_tuin_dashboard.yaml` → Dashboard

---

### 4. Voeg package toe aan Home Assistant

In `configuration.yaml`:

```yaml
homeassistant:
  packages: !include_dir_named packages
```

Plaats daarna het gegenereerde bestand in:

```
/config/packages/
```

---

### 5. Dashboard importeren

* Ga naar je dashboard
* Kies **Edit Dashboard**
* Import YAML
* Plak de inhoud van:

```
beregening_tuin_dashboard.yaml
```

---

## ⚙️ Gebruik

### Automatisch

* Zet **Automatische modus** aan
* Stel:

  * starttype
  * temperatuur
  * regenlimiet
* Kies per zone de dagen

---

### Handmatig

* Start per zone via dashboard
* Stel handmatige duur in

---

### Timerbalken

* Groene balk = actief
* Balk loopt af naarmate tijd verstrijkt
* Tekst toont resterende minuten

---

## 🧠 Hoe het werkt

Het systeem berekent:

1. Wanneer de volgende run moet starten
2. Welke zones actief zijn op die dag
3. Totale looptijd
4. Of beregening toegestaan is

Daarna:

* Start script automatisch
* Zones lopen sequentieel of parallel
* Sensoren houden alles realtime bij

---

## 📁 Structuur

```
project/
├── script.py
├── beregening_tuin_config.yaml
├── beregening_tuin.yaml
├── beregening_tuin_dashboard.yaml
```

---

## 🔧 Vereisten

* Home Assistant
* HACS (aanbevolen)

### Custom kaarten:

* `mushroom`
* `bar-card`
* `stack-in-card`
* `card-mod`

---

## 🚀 Toekomstige uitbreidingen

* 🌧️ Integratie met meer weerservices
* 📱 Meldingen bij starten/stoppen
* 📊 Waterverbruik tracking
* 🤖 AI-gebaseerde planning

---

## ❤️ Bijdragen

Pull requests en ideeën zijn welkom!

---

## 📜 Licentie

Vrij te gebruiken en aan te passen.
