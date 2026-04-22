# 🌱 Slimme Beregening voor Home Assistant

Een complete en flexibele **automatische beregeningsoplossing** voor Home Assistant.

⚡ Ontworpen om volledig schaalbaar te zijn — van 1 tot 20+ zones zonder extra configuratie.

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

* 🔄 **Onbeperkt aantal zones (volledig dynamisch)**
* Voeg simpelweg zones toe in je configuratie — de rest wordt automatisch gegenereerd

Per zone:

* ⏱️ Eigen duur
* 📅 Eigen dagen (weekplanner)
* ▶️ Handmatige start
* 📊 Eigen timerbalk met realtime voortgang

---

### 📊 Dashboard

* Overzichtelijke UI met:

  * Actieve status
  * Totale geplande duur
  * Resterende tijd
  * Eindtijd

Per zone:

* Timerbalk (visueel)
* Realtime voortgang
* Automatisch kleurgebruik:

  * 🔴 Uit → tekst verborgen
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

### 1. Download dit project

Download of clone deze repository naar je **eigen computer** (NIET direct in Home Assistant):

```bash
git clone <repo-url>
```

---

### 2. Maak een configuratiebestand

Maak een bestand in dezelfde map als het script:

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
```

➡️ De generator maakt automatisch:

* alle helpers
* alle sensoren
* alle automations
* dashboard kaarten per zone

---

### 3. Run de generator

Voer het script uit op je computer:

```bash
python3 script.py
```

Dit genereert:

* `beregening_tuin.yaml` → Home Assistant package
* `beregening_tuin_dashboard.yaml` → Dashboard

---

### 4. Upload naar Home Assistant

Kopieer het package bestand naar:

```
/config/packages/
```

---

### 5. Activeer packages

Zorg dat dit in je `configuration.yaml` staat:

```yaml
homeassistant:
  packages: !include_dir_named packages
```

---

### 6. Herstart Home Assistant

---

### 7. Dashboard importeren

* Ga naar je dashboard
* Klik op **Bewerken**
* Ga naar **YAML modus**
* Plak de inhoud van:

```
beregening_tuin_dashboard.yaml
```

---

## ⚙️ Gebruik

### Automatisch

* Zet **Automatische modus** aan
* Stel in:

  * starttype
  * minimale temperatuur
  * maximale regen
* Kies per zone de dagen

---

### Handmatig

* Start zones via dashboard
* Stel handmatige duur in

---

### Timerbalken

* Groene balk = actief
* Balk loopt af tijdens gebruik
* Tekst toont resterende minuten

---

## 🧠 Hoe het werkt

Het systeem berekent:

1. Wanneer de volgende run start
2. Welke zones actief zijn op die dag
3. Totale looptijd
4. Of beregening toegestaan is

Daarna:

* Start het systeem automatisch
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

### Custom kaarten

* `mushroom`
* `bar-card`
* `stack-in-card`
* `card-mod`

---

## 🚀 Toekomstige uitbreidingen

* 🌧️ Integratie met meerdere weerservices
* 📱 Notificaties bij starten/stoppen
* 📊 Waterverbruik tracking
* 🤖 AI-gebaseerde planning

---

## ❤️ Bijdragen

Pull requests en ideeën zijn welkom!

---

## 📜 Licentie

Vrij te gebruiken en aan te passen.
