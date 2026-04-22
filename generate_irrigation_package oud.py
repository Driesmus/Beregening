from pathlib import Path
import yaml

DAYS = [
    ("maandag", "Maandag"),
    ("dinsdag", "Dinsdag"),
    ("woensdag", "Woensdag"),
    ("donderdag", "Donderdag"),
    ("vrijdag", "Vrijdag"),
    ("zaterdag", "Zaterdag"),
    ("zondag", "Zondag"),
]

DAY_INDEX = {
    "maandag": 0,
    "dinsdag": 1,
    "woensdag": 2,
    "donderdag": 3,
    "vrijdag": 4,
    "zaterdag": 5,
    "zondag": 6,
}


def build_day_expr_for_offset(slug, i, offset_expr):
    parts = []
    for day_key, _day_label in DAYS:
        idx = DAY_INDEX[day_key]
        parts.append(
            f"((((basisdag + ({offset_expr})) % 7) == {idx}) and is_state('{zone_day_entity(slug, day_key, i)}', 'on'))"
        )
    return " or\n                ".join(parts)


def q(text: str) -> str:
    return '"' + str(text).replace('"', '\\"') + '"'


def add(lines, text="", indent=0):
    lines.append(" " * indent + text)


# -----------------
# Object IDs (zonder domain)
# -----------------
def zone_switch_object_id(slug, i):
    return f"{slug}_zone_{i}_klep"


def rain_24h_object_id(slug):
    return f"{slug}_regen_komende_24_uur"


def max_temp_24h_object_id(slug):
    return f"{slug}_max_temperatuur_komende_24_uur"


def rain_now_object_id(slug):
    return f"{slug}_regen_nu"


def active_now_object_id(slug):
    return f"{slug}_actief_nu"


def total_duration_object_id(slug):
    return f"{slug}_totale_duur_minuten"


def total_duration_pretty_object_id(slug):
    return f"{slug}_totale_geplande_duur"


def block_reason_object_id(slug):
    return f"{slug}_blokkade_reden"


def remaining_object_id(slug):
    return f"{slug}_resterend_tot_klaar"


def end_time_object_id(slug):
    return f"{slug}_eindtijd"


def last_run_object_id(slug):
    return f"{slug}_laatste_run"


def zone_start_helper_object_id(slug, i):
    return f"{slug}_zone_{i}_starttijd_helper"


def zone_running_duration_object_id(slug, i):
    return f"{slug}_zone_{i}_lopende_duur"


def zone_remaining_object_id(slug, i):
    return f"{slug}_zone_{i}_resterend"


# -----------------
# Entity IDs
# -----------------
def zone_bool_entity(slug, i):
    return f"input_boolean.{slug}_zone_{i}_actief"


def zone_day_entity(slug, day_key, i):
    return f"input_boolean.{slug}_{day_key}_zone_{i}"


def zone_duration_entity(slug, i):
    return f"input_number.{slug}_zone_{i}_duur"


def zone_manual_duration_entity(slug, i):
    return f"input_number.{slug}_zone_{i}_handmatig_duur"


def zone_running_duration_entity(slug, i):
    return f"input_number.{zone_running_duration_object_id(slug, i)}"


def zone_start_helper_entity(slug, i):
    return f"input_datetime.{zone_start_helper_object_id(slug, i)}"


def zone_remaining_sensor_entity(slug, i):
    return f"sensor.{zone_remaining_object_id(slug, i)}"


def zone_switch_entity(slug, i):
    return f"switch.{zone_switch_object_id(slug, i)}"


def rain_24h_sensor_entity(slug):
    return f"sensor.{rain_24h_object_id(slug)}"


def max_temp_24h_sensor_entity(slug):
    return f"sensor.{max_temp_24h_object_id(slug)}"


def rain_now_binary_entity(slug):
    return f"binary_sensor.{rain_now_object_id(slug)}"


def active_now_binary_entity(slug):
    return f"binary_sensor.{active_now_object_id(slug)}"


def total_duration_sensor_entity(slug):
    return f"sensor.{total_duration_object_id(slug)}"


def total_duration_pretty_sensor_entity(slug):
    return f"sensor.{total_duration_pretty_object_id(slug)}"


def block_reason_sensor_entity(slug):
    return f"sensor.{block_reason_object_id(slug)}"


def remaining_sensor_entity(slug):
    return f"sensor.{remaining_object_id(slug)}"


def end_time_sensor_entity(slug):
    return f"sensor.{end_time_object_id(slug)}"


def last_run_sensor_entity(slug):
    return f"sensor.{last_run_object_id(slug)}"


def build_today_expr(slug, i):
    parts = []
    for day_key, _day_label in DAYS:
        idx = DAY_INDEX[day_key]
        parts.append(
            f"(dag == {idx} and is_state('{zone_day_entity(slug, day_key, i)}', 'on'))"
        )
    return " or\n                ".join(parts)


def generate_package(cfg: dict) -> str:
    slug = cfg["slug"]
    title = cfg["title"]
    weather_entity = cfg["weather_entity"]
    zones = cfg["zones"]

    if not zones:
        raise ValueError("Er moet minimaal 1 zone zijn")

    lines = []

    # -----------------
    # input_boolean
    # -----------------
    add(lines, "input_boolean:")
    add(lines, f"{slug}_ingeschakeld:", 2)
    add(lines, f"name: {title} ingeschakeld", 4)
    add(lines, "icon: mdi:sprinkler-variant", 4)
    add(lines)

    add(lines, f"{slug}_parallel:", 2)
    add(lines, "name: Alle zones tegelijk", 4)
    add(lines, "icon: mdi:call-split", 4)
    add(lines)

    for i, zone in enumerate(zones, start=1):
        add(lines, f"{slug}_zone_{i}_actief:", 2)
        add(lines, f"name: {zone['name']} actief", 4)
        add(lines, "icon: mdi:valve", 4)
    add(lines)

    for day_key, day_label in DAYS:
        for i, zone in enumerate(zones, start=1):
            add(lines, f"{slug}_{day_key}_zone_{i}:", 2)
            add(lines, f"name: {day_label} {zone['name']}", 4)
    add(lines)

    # -----------------
    # input_datetime
    # -----------------
    add(lines, "input_datetime:")
    add(lines, f"{slug}_vaste_tijd:", 2)
    add(lines, "name: Vaste starttijd", 4)
    add(lines, "has_date: false", 4)
    add(lines, "has_time: true", 4)
    add(lines)

    add(lines, f"{slug}_laatste_run_helper:", 2)
    add(lines, "name: Beregening laatste run helper", 4)
    add(lines, "has_date: true", 4)
    add(lines, "has_time: true", 4)
    add(lines)

    for i, zone in enumerate(zones, start=1):
        add(lines, zone_start_helper_object_id(slug, i) + ":", 2)
        add(lines, f"name: {zone['name']} starttijd helper", 4)
        add(lines, "has_date: true", 4)
        add(lines, "has_time: true", 4)
        add(lines)

    # -----------------
    # input_number
    # -----------------
    add(lines, "input_number:")
    add(lines, f"{slug}_offset_minuten:", 2)
    add(lines, "name: Offset starttijd", 4)
    add(lines, "min: -180", 4)
    add(lines, "max: 180", 4)
    add(lines, "step: 5", 4)
    add(lines, "unit_of_measurement: min", 4)
    add(lines, "icon: mdi:timeline-clock", 4)
    add(lines)

    add(lines, f"{slug}_min_temp:", 2)
    add(lines, "name: Minimale temperatuur", 4)
    add(lines, "min: 0", 4)
    add(lines, "max: 40", 4)
    add(lines, "step: 1", 4)
    add(lines, 'unit_of_measurement: "°C"', 4)
    add(lines, "icon: mdi:thermometer", 4)
    add(lines)

    add(lines, f"{slug}_max_regen_24u:", 2)
    add(lines, "name: Max regen komende 24 uur", 4)
    add(lines, "min: 0", 4)
    add(lines, "max: 20", 4)
    add(lines, "step: 0.5", 4)
    add(lines, "unit_of_measurement: mm", 4)
    add(lines, "icon: mdi:weather-rainy", 4)
    add(lines)

    for i, zone in enumerate(zones, start=1):
        add(lines, f"{slug}_zone_{i}_duur:", 2)
        add(lines, f"name: {zone['name']} duur", 4)
        add(lines, "min: 1", 4)
        add(lines, "max: 120", 4)
        add(lines, "step: 1", 4)
        add(lines, "unit_of_measurement: min", 4)
        add(lines, "icon: mdi:timer", 4)
    add(lines)

    for i, zone in enumerate(zones, start=1):
        add(lines, f"{slug}_zone_{i}_handmatig_duur:", 2)
        add(lines, f"name: {zone['name']} handmatige duur", 4)
        add(lines, "min: 1", 4)
        add(lines, "max: 120", 4)
        add(lines, "step: 1", 4)
        add(lines, "unit_of_measurement: min", 4)
        add(lines, "icon: mdi:timer-play-outline", 4)
    add(lines)

    for i, zone in enumerate(zones, start=1):
        add(lines, zone_running_duration_object_id(slug, i) + ":", 2)
        add(lines, f"name: {zone['name']} lopende duur", 4)
        add(lines, "min: 0", 4)
        add(lines, "max: 120", 4)
        add(lines, "step: 1", 4)
        add(lines, "unit_of_measurement: min", 4)
        add(lines, "icon: mdi:progress-clock", 4)
    add(lines)

    # -----------------
    # input_select
    # -----------------
    add(lines, "input_select:")
    add(lines, f"{slug}_start_type:", 2)
    add(lines, "name: Startmoment", 4)
    add(lines, "options:", 4)
    add(lines, "- Zonsopkomst", 6)
    add(lines, "- Zonsondergang", 6)
    add(lines, "- Vaste tijd", 6)
    add(lines, "icon: mdi:clock-start", 4)
    add(lines)

    # -----------------
    # template
    # -----------------
    add(lines, "template:")

    # -----------------
    # template switches
    # -----------------
    add(lines, "- switch:", 2)

    for i, zone in enumerate(zones, start=1):
        relay = zone["relay"]
        zone_name = zone["name"]

        add(lines, f'- name: {q(f"{title} {zone_name} klep")}', 6)
        add(lines, f"default_entity_id: {zone_switch_entity(slug, i)}", 8)
        add(lines, f"unique_id: {zone_switch_object_id(slug, i)}", 8)

        state_template = f"{{{{ is_state('{relay}', 'on') }}}}"
        add(lines, f"state: {q(state_template)}", 8)

        add(lines, "turn_on:", 8)
        add(lines, "- action: switch.turn_on", 10)
        add(lines, "target:", 12)
        add(lines, f"entity_id: {relay}", 14)

        add(lines, "turn_off:", 8)
        add(lines, "- action: switch.turn_off", 10)
        add(lines, "target:", 12)
        add(lines, f"entity_id: {relay}", 14)
        add(lines)

    # -----------------
    # template forecast sensors
    # -----------------
    add(lines, "- triggers:", 2)
    add(lines, "- trigger: homeassistant", 4)
    add(lines, "event: start", 6)
    add(lines, "- trigger: time_pattern", 4)
    add(lines, 'minutes: "/30"', 6)
    add(lines)
    add(lines, "actions:", 4)
    add(lines, "- action: weather.get_forecasts", 6)
    add(lines, "target:", 8)
    add(lines, f"entity_id: {weather_entity}", 10)
    add(lines, "data:", 8)
    add(lines, "type: hourly", 10)
    add(lines, "response_variable: wx", 8)
    add(lines)
    add(lines, "sensor:", 4)

    add(lines, f"- name: {q(title + ' regen komende 24 uur')}", 6)
    add(lines, f"default_entity_id: {rain_24h_sensor_entity(slug)}", 8)
    add(lines, f"unique_id: {rain_24h_object_id(slug)}", 8)
    add(lines, 'unit_of_measurement: "mm"', 8)
    add(lines, "state: >", 8)
    add(lines, f"{{% set f = wx.get('{weather_entity}', {{}}).get('forecast', []) %}}", 10)
    add(lines, "{{ f[:24] | map(attribute='precipitation') | map('float', 0) | sum | round(1) }}", 10)
    add(lines)

    add(lines, f"- name: {q(title + ' max temperatuur komende 24 uur')}", 6)
    add(lines, f"default_entity_id: {max_temp_24h_sensor_entity(slug)}", 8)
    add(lines, f"unique_id: {max_temp_24h_object_id(slug)}", 8)
    add(lines, 'unit_of_measurement: "°C"', 8)
    add(lines, "state: >", 8)
    add(lines, f"{{% set f = wx.get('{weather_entity}', {{}}).get('forecast', []) %}}", 10)
    add(lines, "{% if f | count > 0 %}", 10)
    add(lines, "{{ f[:24] | map(attribute='temperature') | map('float', 0) | max | round(1) }}", 12)
    add(lines, "{% else %}", 10)
    add(lines, "unknown", 12)
    add(lines, "{% endif %}", 10)
    add(lines)

    # -----------------
    # binary sensors
    # -----------------
    add(lines, "- binary_sensor:", 2)

    add(lines, f"- name: {q(title + ' regen nu')}", 6)
    add(lines, f"default_entity_id: {rain_now_binary_entity(slug)}", 8)
    add(lines, f"unique_id: {rain_now_object_id(slug)}", 8)
    add(lines, "state: >", 8)
    add(lines, f"{{{{ states('{weather_entity}') in ['rainy', 'pouring', 'lightning-rainy'] }}}}", 10)
    add(lines)

    active_states = " or\n            ".join(
        [f"is_state('{zone_switch_entity(slug, i)}', 'on')" for i in range(1, len(zones) + 1)]
    )

    add(lines, f"- name: {q(title + ' actief nu')}", 6)
    add(lines, f"default_entity_id: {active_now_binary_entity(slug)}", 8)
    add(lines, f"unique_id: {active_now_object_id(slug)}", 8)
    add(lines, "state: >", 8)
    add(lines, "{{", 10)
    add(lines, active_states, 12)
    add(lines, "}}", 10)
    add(lines, "icon: >", 8)
    add(lines, f"{{% if is_state('{active_now_binary_entity(slug)}', 'on') %}}", 10)
    add(lines, "mdi:sprinkler-variant", 12)
    add(lines, "{% else %}", 10)
    add(lines, "mdi:sprinkler-variant-off", 12)
    add(lines, "{% endif %}", 10)
    add(lines)

    # -----------------
    # overige sensors
    # -----------------
    add(lines, "- sensor:", 2)

    add(lines, f"- name: {q(title + ' totale duur minuten')}", 6)
    add(lines, f"default_entity_id: {total_duration_sensor_entity(slug)}", 8)
    add(lines, f"unique_id: {total_duration_object_id(slug)}", 8)
    add(lines, 'unit_of_measurement: "min"', 8)
    add(lines, "state: >", 8)
    add(lines, "{% set basisdag = now().weekday() %}", 10)
    add(lines, f"{{% set start_type = states('input_select.{slug}_start_type') %}}", 10)
    add(lines, f"{{% set offset = states('input_number.{slug}_offset_minuten') | int(0) %}}", 10)
    add(lines, "{% set nu = now() %}", 10)
    add(lines, "{% set dag_offset = 0 %}", 10)
    add(lines)

    add(lines, "{% if start_type == 'Vaste tijd' %}", 10)
    add(lines, f"{{% set t = states('input_datetime.{slug}_vaste_tijd') %}}", 12)
    add(lines, "{% set start_vandaag = today_at(t[0:5]) %}", 12)
    add(lines, "{% if nu >= start_vandaag %}", 12)
    add(lines, "{% set dag_offset = 1 %}", 14)
    add(lines, "{% endif %}", 12)

    add(lines, "{% elif start_type == 'Zonsopkomst' %}", 10)
    add(lines, "{% set nr = as_datetime(state_attr('sun.sun', 'next_rising')) %}", 12)
    add(lines, "{% if nr and nr.date() != nu.date() %}", 12)
    add(lines, "{% set dag_offset = 1 %}", 14)
    add(lines, "{% endif %}", 12)

    add(lines, "{% elif start_type == 'Zonsondergang' %}", 10)
    add(lines, "{% set ns = as_datetime(state_attr('sun.sun', 'next_setting')) %}", 12)
    add(lines, "{% if ns and ns.date() != nu.date() %}", 12)
    add(lines, "{% set dag_offset = 1 %}", 14)
    add(lines, "{% endif %}", 12)

    add(lines, "{% endif %}", 10)
    add(lines)

    for i in range(1, len(zones) + 1):
        add(lines, f"{{% set z{i}_planner =", 10)
        add(lines, build_day_expr_for_offset(slug, i, "dag_offset"), 12)
        add(lines, "%}", 10)

    add(lines)
    for i in range(1, len(zones) + 1):
        add(lines,
            f"{{% set z{i} = states('{zone_duration_entity(slug, i)}') | int(0) "
            f"if is_state('{zone_bool_entity(slug, i)}','on') and z{i}_planner else 0 %}}",
            10
        )

    nums = ", ".join([f"z{i}" for i in range(1, len(zones) + 1)])
    add(lines)
    add(lines, f"{{% if is_state('input_boolean.{slug}_parallel','on') %}}", 10)
    add(lines, f"{{{{ [{nums}] | max }}}}", 12)
    add(lines, "{% else %}", 10)
    add(lines, f"{{{{ {' + '.join([f'z{i}' for i in range(1, len(zones) + 1)])} }}}}", 12)
    add(lines, "{% endif %}", 10)
    add(lines)

    add(lines, f"- name: {q(title + ' totale geplande duur')}", 6)
    add(lines, f"default_entity_id: {total_duration_pretty_sensor_entity(slug)}", 8)
    add(lines, f"unique_id: {total_duration_pretty_object_id(slug)}", 8)
    add(lines, "state: >", 8)
    add(lines, f"{{% set totaal = states('{total_duration_sensor_entity(slug)}') | int(0) %}}", 10)
    add(lines, "{% set uren = totaal // 60 %}", 10)
    add(lines, "{% set minuten = totaal % 60 %}", 10)
    add(lines, "{% if uren > 0 %}", 10)
    add(lines, "{{ uren }}u {{ minuten }}m", 12)
    add(lines, "{% else %}", 10)
    add(lines, "{{ minuten }}m", 12)
    add(lines, "{% endif %}", 10)
    add(lines)

    add(lines, f"- name: {q(title + ' blokkade reden')}", 6)
    add(lines, f"default_entity_id: {block_reason_sensor_entity(slug)}", 8)
    add(lines, f"unique_id: {block_reason_object_id(slug)}", 8)
    add(lines, "state: >", 8)
    add(lines, "{% set basisdag = now().weekday() %}", 10)
    add(lines, f"{{% set start_type = states('input_select.{slug}_start_type') %}}", 10)
    add(lines, "{% set nu = now() %}", 10)
    add(lines, "{% set dag_offset = 0 %}", 10)
    add(lines)

    add(lines, "{% if start_type == 'Vaste tijd' %}", 10)
    add(lines, f"{{% set t = states('input_datetime.{slug}_vaste_tijd') %}}", 12)
    add(lines, "{% set start_vandaag = today_at(t[0:5]) %}", 12)
    add(lines, "{% if nu >= start_vandaag %}", 12)
    add(lines, "{% set dag_offset = 1 %}", 14)
    add(lines, "{% endif %}", 12)

    add(lines, "{% elif start_type == 'Zonsopkomst' %}", 10)
    add(lines, "{% set nr = as_datetime(state_attr('sun.sun', 'next_rising')) %}", 12)
    add(lines, "{% if nr and nr.date() != nu.date() %}", 12)
    add(lines, "{% set dag_offset = 1 %}", 14)
    add(lines, "{% endif %}", 12)

    add(lines, "{% elif start_type == 'Zonsondergang' %}", 10)
    add(lines, "{% set ns = as_datetime(state_attr('sun.sun', 'next_setting')) %}", 12)
    add(lines, "{% if ns and ns.date() != nu.date() %}", 12)
    add(lines, "{% set dag_offset = 1 %}", 14)
    add(lines, "{% endif %}", 12)

    add(lines, "{% endif %}", 10)
    add(lines, "{% set doel_dag = (basisdag + dag_offset) % 7 %}", 10)
    add(lines, "{% set dagnaam = ['maandag','dinsdag','woensdag','donderdag','vrijdag','zaterdag','zondag'][doel_dag] %}", 10)
    add(lines, "{% set redenen = namespace(items=[]) %}", 10)
    add(lines)

    for i in range(1, len(zones) + 1):
        add(lines, f"{{% set planner_zone_{i} =", 10)
        add(lines, build_day_expr_for_offset(slug, i, "dag_offset"), 12)
        add(lines, "%}", 10)

    planned_target = " or ".join([
        f"(planner_zone_{i} and is_state('{zone_bool_entity(slug, i)}', 'on'))"
        for i in range(1, len(zones) + 1)
    ])
    inactive_all = " and ".join(
        [f"is_state('{zone_bool_entity(slug, i)}', 'off')" for i in range(1, len(zones) + 1)]
    )

    add(lines)
    add(lines, f"{{% set doel_gepland = {planned_target} %}}", 10)
    add(lines)

    add(lines, f"{{% if is_state('input_boolean.{slug}_ingeschakeld', 'off') %}}", 10)
    add(lines, "{% set redenen.items = redenen.items + ['Systeem uitgeschakeld'] %}", 12)
    add(lines, "{% endif %}", 10)

    add(lines, f"{{% if is_state('{rain_now_binary_entity(slug)}', 'on') %}}", 10)
    add(lines, "{% set redenen.items = redenen.items + ['Geblokkeerd door regen nu'] %}", 12)
    add(lines, "{% endif %}", 10)

    add(lines, f"{{% if states('{rain_24h_sensor_entity(slug)}')|float(0) > states('input_number.{slug}_max_regen_24u')|float(0) %}}", 10)
    add(lines, "{% set redenen.items = redenen.items + ['Te veel regen verwacht'] %}", 12)
    add(lines, "{% endif %}", 10)

    add(lines, f"{{% if states('{max_temp_24h_sensor_entity(slug)}')|float(0) < states('input_number.{slug}_min_temp')|float(0) %}}", 10)
    add(lines, "{% set redenen.items = redenen.items + ['Temperatuur te laag'] %}", 12)
    add(lines, "{% endif %}", 10)

    add(lines, "{% if not doel_gepland %}", 10)
    add(lines, "{% set redenen.items = redenen.items + ['Geen zones gepland op ' ~ dagnaam] %}", 12)
    add(lines, "{% endif %}", 10)

    add(lines, "{% if " + inactive_all + " %}", 10)
    add(lines, "{% set redenen.items = redenen.items + ['Geen actieve zones'] %}", 12)
    add(lines, "{% endif %}", 10)

    add(lines, "{% if redenen.items | count == 0 %}", 10)
    add(lines, "Geen blokkade", 12)
    add(lines, "{% else %}", 10)
    add(lines, "{{ redenen.items | join(' | ') }}", 12)
    add(lines, "{% endif %}", 10)
    add(lines)

    add(lines, f"- name: {q(title + ' resterend tot klaar')}", 6)
    add(lines, f"default_entity_id: {remaining_sensor_entity(slug)}", 8)
    add(lines, f"unique_id: {remaining_object_id(slug)}", 8)
    add(lines, 'unit_of_measurement: "min"', 8)
    add(lines, "state: >", 8)
    add(lines, "{% set resterend = [", 10)
    for i in range(1, len(zones) + 1):
        comma = "," if i < len(zones) else ""
        add(lines, f"states('{zone_remaining_sensor_entity(slug, i)}') | int(0){comma}", 12)
    add(lines, "] | max %}", 10)
    add(lines, "{{ resterend }}", 10)
    add(lines)

    add(lines, f"- name: {q(title + ' eindtijd')}", 6)
    add(lines, f"default_entity_id: {end_time_sensor_entity(slug)}", 8)
    add(lines, f"unique_id: {end_time_object_id(slug)}", 8)
    add(lines, "icon: mdi:clock-end", 8)
    add(lines, "state: >", 8)
    add(lines, f"{{% set resterend = states('{remaining_sensor_entity(slug)}') | int(0) %}}", 10)
    add(lines, "{% if resterend > 0 %}", 10)
    add(lines, "{{ (now() + timedelta(minutes=resterend)).strftime('%H:%M') }}", 12)
    add(lines, "{% else %}", 10)
    add(lines, "-", 12)
    add(lines, "{% endif %}", 10)
    add(lines)
    
    add(lines, f"- name: {q(title + ' geplande eindtijd')}", 6)
    add(lines, f"default_entity_id: sensor.{slug}_geplande_eindtijd", 8)
    add(lines, f"unique_id: {slug}_geplande_eindtijd", 8)
    add(lines, "icon: mdi:clock-end", 8)
    add(lines, "state: >", 8)
    add(lines, f"{{% set duur = states('{total_duration_sensor_entity(slug)}') | int(0) %}}", 10)
    add(lines, f"{{% set start_type = states('input_select.{slug}_start_type') %}}", 10)
    add(lines, f"{{% set offset = states('input_number.{slug}_offset_minuten') | int(0) %}}", 10)
    add(lines, "{% set nu = now() %}", 10)
    add(lines)
    add(lines, "{% if duur <= 0 %}", 10)
    add(lines, "-", 12)
    add(lines, "{% else %}", 10)
    add(lines, "{% if start_type == 'Vaste tijd' %}", 12)
    add(lines, f"{{% set t = states('input_datetime.{slug}_vaste_tijd') %}}", 14)
    add(lines, "{% set start_vandaag = today_at(t[0:5]) %}", 14)
    add(lines, "{% if nu < start_vandaag %}", 14)
    add(lines, "{% set starttijd = start_vandaag %}", 16)
    add(lines, "{% else %}", 14)
    add(lines, "{% set starttijd = start_vandaag + timedelta(days=1) %}", 16)
    add(lines, "{% endif %}", 14)
    add(lines, "{% elif start_type == 'Zonsopkomst' %}", 12)
    add(lines, "{% set nr = as_datetime(state_attr('sun.sun', 'next_rising')) %}", 14)
    add(lines, "{% if nr %}", 14)
    add(lines, "{% set starttijd = nr + timedelta(minutes=offset) %}", 16)
    add(lines, "{% else %}", 14)
    add(lines, "{% set starttijd = none %}", 16)
    add(lines, "{% endif %}", 14)
    add(lines, "{% elif start_type == 'Zonsondergang' %}", 12)
    add(lines, "{% set ns = as_datetime(state_attr('sun.sun', 'next_setting')) %}", 14)
    add(lines, "{% if ns %}", 14)
    add(lines, "{% set starttijd = ns + timedelta(minutes=offset) %}", 16)
    add(lines, "{% else %}", 14)
    add(lines, "{% set starttijd = none %}", 16)
    add(lines, "{% endif %}", 14)
    add(lines, "{% else %}", 12)
    add(lines, "{% set starttijd = none %}", 14)
    add(lines, "{% endif %}", 12)
    add(lines)
    add(lines, "{% if starttijd %}", 12)
    add(lines, "{{ (starttijd + timedelta(minutes=duur)).strftime('%H:%M') }}", 14)
    add(lines, "{% else %}", 12)
    add(lines, "-", 14)
    add(lines, "{% endif %}", 12)
    add(lines, "{% endif %}", 10)
    add(lines)

    add(lines, f"- name: {q(title + ' laatste run')}", 6)
    add(lines, f"default_entity_id: {last_run_sensor_entity(slug)}", 8)
    add(lines, f"unique_id: {last_run_object_id(slug)}", 8)
    add(lines, "device_class: timestamp", 8)
    add(lines, "state: >", 8)
    add(lines, f"{{{{ state_attr('script.{slug}_start_zones', 'last_triggered') }}}}", 10)
    add(lines, "icon: mdi:clock-check-outline", 8)
    add(lines)

    # per-zone resterend sensors
    for i, zone in enumerate(zones, start=1):
        add(lines, f"- name: {q(title + ' ' + zone['name'] + ' resterend')}", 6)
        add(lines, f"default_entity_id: {zone_remaining_sensor_entity(slug, i)}", 8)
        add(lines, f"unique_id: {zone_remaining_object_id(slug, i)}", 8)
        add(lines, 'unit_of_measurement: "min"', 8)
        add(lines, "icon: mdi:timer-sand", 8)
        add(lines, "state: >", 8)
        add(lines, f"{{% set gestart = states('{zone_start_helper_entity(slug, i)}') %}}", 10)
        add(lines, f"{{% set duur = states('{zone_running_duration_entity(slug, i)}') | int(0) %}}", 10)
        add(lines, f"{{% if is_state('{zone_switch_entity(slug, i)}', 'on') and gestart not in ['unknown', 'unavailable', '', 'none'] and duur > 0 %}}", 10)
        add(lines, "{% set eind = as_datetime(gestart) + timedelta(minutes=duur) %}", 12)
        add(lines, "{% set resterend = ((as_timestamp(eind) - as_timestamp(now())) / 60) | round(0) %}", 12)
        add(lines, "{{ [resterend, 0] | max }}", 12)
        add(lines, "{% else %}", 10)
        add(lines, "0", 12)
        add(lines, "{% endif %}", 10)
        add(lines)

    for i, zone in enumerate(zones, start=1):
        add(
            lines,
            f"- name: \"{{{{ 'Resterende tijd ' ~ (states('{zone_remaining_sensor_entity(slug, i)}') | int(0)) ~ ' min' }}}}\"",
            6,
        )
        add(lines, f"default_entity_id: sensor.{slug}_zone_{i}_balk_procent", 8)
        add(lines, f"unique_id: {slug}_zone_{i}_balk_procent", 8)
        add(lines, 'unit_of_measurement: "%"', 8)
        add(lines, "state: >", 8)
        add(lines, "{% set _ = now() %}", 10)
        add(lines, f"{{% set resterend = states('{zone_remaining_sensor_entity(slug, i)}') | float(0) %}}", 10)
        add(lines, f"{{% set totaal = states('{zone_running_duration_entity(slug, i)}') | float(0) %}}", 10)
        add(lines, "{% if totaal > 0 %}", 10)
        add(lines, "{{ ((resterend / totaal) * 100) | round(0) }}", 12)
        add(lines, "{% else %}", 10)
        add(lines, "0", 12)
        add(lines, "{% endif %}", 10)
        add(lines)
    # -----------------
    # automations
    # -----------------
    add(lines, "automation:")
    add(lines, f"- id: {slug}_auto_start", 2)
    add(lines, f"alias: {title} automatisch starten", 4)
    add(lines, 'description: ""', 4)
    add(lines, "triggers:", 4)
    add(lines, "- trigger: time_pattern", 6)
    add(lines, "minutes: /1", 8)
    add(lines, "conditions:", 4)

    add(lines, "- condition: state", 6)
    add(lines, f"entity_id: input_boolean.{slug}_ingeschakeld", 8)
    add(lines, 'state: "on"', 8)

    add(lines, "- condition: state", 6)
    add(lines, f"entity_id: {rain_now_binary_entity(slug)}", 8)
    add(lines, 'state: "off"', 8)

    add(lines, "- condition: template", 6)
    add(lines, "value_template: |", 8)
    add(lines, "{{", 10)
    add(lines, f"states('{rain_24h_sensor_entity(slug)}') | float(0)", 12)
    add(lines, f"< states('input_number.{slug}_max_regen_24u') | float(0)", 12)
    add(lines, "}}", 10)

    add(lines, "- condition: template", 6)
    add(lines, "value_template: |", 8)
    add(lines, "{{", 10)
    add(lines, f"state_attr('{weather_entity}', 'temperature') | float(0)", 12)
    add(lines, f">= states('input_number.{slug}_min_temp') | float(0)", 12)
    add(lines, "or", 12)
    add(lines, f"states('{max_temp_24h_sensor_entity(slug)}') | float(0)", 12)
    add(lines, f">= states('input_number.{slug}_min_temp') | float(0)", 12)
    add(lines, "}}", 10)

    add(lines, "- condition: template", 6)
    add(lines, "value_template: >", 8)
    add(lines, f"{{% set start_type = states('input_select.{slug}_start_type') %}}", 10)
    add(lines, f"{{% set offset = states('input_number.{slug}_offset_minuten') | int(0) %}}", 10)
    add(lines, "{% set n = now() %}", 10)
    add(lines)
    add(lines, "{% if start_type == 'Vaste tijd' %}", 10)
    add(lines, f"{{% set t = states('input_datetime.{slug}_vaste_tijd') %}}", 12)
    add(lines, "{{ n.strftime('%H:%M') == t[0:5] }}", 12)
    add(lines, "{% elif start_type == 'Zonsopkomst' %}", 10)
    add(lines, "{% set target = as_datetime(state_attr('sun.sun','next_rising')) + timedelta(minutes=offset) %}", 12)
    add(lines, "{{ n.hour == target.hour and n.minute == target.minute }}", 12)
    add(lines, "{% elif start_type == 'Zonsondergang' %}", 10)
    add(lines, "{% set target = as_datetime(state_attr('sun.sun','next_setting')) + timedelta(minutes=offset) %}", 12)
    add(lines, "{{ n.hour == target.hour and n.minute == target.minute }}", 12)
    add(lines, "{% else %}", 10)
    add(lines, "false", 12)
    add(lines, "{% endif %}", 10)

    add(lines, "- condition: template", 6)
    add(lines, "value_template: |", 8)
    add(lines, "{% set dag = now().weekday() %}", 10)
    for day_key, _label in DAYS:
        idx = DAY_INDEX[day_key]
        expr = " or\n            ".join([
            f"(is_state('{zone_day_entity(slug, day_key, i)}', 'on') and is_state('{zone_bool_entity(slug, i)}', 'on'))"
            for i in range(1, len(zones) + 1)
        ])
        if idx == 0:
            add(lines, f"{{% if dag == {idx} %}}", 10)
        else:
            add(lines, f"{{% elif dag == {idx} %}}", 10)
        add(lines, "{{", 12)
        add(lines, expr, 14)
        add(lines, "}}", 12)
    add(lines, "{% else %}", 10)
    add(lines, "false", 12)
    add(lines, "{% endif %}", 10)

    add(lines, "actions:", 4)
    add(lines, f"- action: script.{slug}_start_zones", 6)
    add(lines, "mode: single", 4)
    add(lines)

    # -----------------
    # veiligheidsstop
    # -----------------
    add(lines, f"- id: {slug}_veiligheidsstop", 2)
    add(lines, f"alias: {title} veiligheidsstop 10 uur", 4)
    add(lines, "description: Zet zone uit als die langer dan 10 uur aanstaat", 4)
    add(lines, "triggers:", 4)
    add(lines, "- trigger: state", 6)
    add(lines, "entity_id:", 8)
    for i in range(1, len(zones) + 1):
        add(lines, f"- {zone_switch_entity(slug, i)}", 10)
    add(lines, 'to: "on"', 8)
    add(lines, "for:", 8)
    add(lines, "hours: 10", 10)
    add(lines, "actions:", 4)
    add(lines, "- action: switch.turn_off", 6)
    add(lines, "target:", 8)
    add(lines, 'entity_id: "{{ trigger.entity_id }}"', 10)
    add(lines, "- action: input_number.set_value", 6)
    add(lines, "target:", 8)
    add(lines, "entity_id: >", 10)
    add(lines, f"{{{{ 'input_number.{slug}_zone_' ~ (trigger.entity_id.split('_zone_')[1].split('_klep')[0]) ~ '_lopende_duur' }}}}", 12)
    add(lines, "data:", 8)
    add(lines, "value: 0", 10)
    add(lines, "mode: parallel", 4)
    add(lines)

    # -----------------
    # failsafe stop bij HA start of systeem uit
    # -----------------
    add(lines, f"- id: {slug}_failsafe_stop", 2)
    add(lines, f"alias: {title} failsafe stop", 4)
    add(lines, "description: Zet alle beregening uit bij HA herstart of als systeem wordt uitgeschakeld", 4)
    add(lines, "triggers:", 4)

    add(lines, "- trigger: homeassistant", 6)
    add(lines, "event: start", 8)
    add(lines, "id: ha_start", 8)

    add(lines, "- trigger: state", 6)
    add(lines, f"entity_id: input_boolean.{slug}_ingeschakeld", 8)
    add(lines, 'to: "off"', 8)
    add(lines, "id: systeem_uit", 8)

    add(lines, "actions:", 4)
    add(lines, "- choose:", 6)
    add(lines, "- conditions:", 8)
    add(lines, "- condition: trigger", 10)
    add(lines, "id: ha_start", 12)
    add(lines, "sequence:", 10)
    add(lines, '- delay: "00:02:00"', 12)

    add(lines, "- action: script.turn_on", 6)
    add(lines, "target:", 8)
    add(lines, f"entity_id: script.{slug}_stop_alles", 10)
    add(lines, "data: {}", 8)

    add(lines, "- action: switch.turn_off", 6)
    add(lines, "target:", 8)
    add(lines, "entity_id:", 10)
    for i in range(1, len(zones) + 1):
        add(lines, f"- {zone_switch_entity(slug, i)}", 12)

    for i in range(1, len(zones) + 1):
        add(lines, "- action: input_number.set_value", 6)
        add(lines, "target:", 8)
        add(lines, f"entity_id: {zone_running_duration_entity(slug, i)}", 10)
        add(lines, "data:", 8)
        add(lines, "value: 0", 10)

    add(lines, "mode: single", 4)
    add(lines)

    # -----------------
    # scripts
    # -----------------
    add(lines, "script:")
    add(lines, f"{slug}_start_zones:", 2)
    add(lines, f"alias: {title} - start zones", 4)
    add(lines, "mode: single", 4)
    add(lines, "sequence:", 4)

    add(lines, "- variables:", 6)
    add(lines, 'dag: "{{ now().weekday() }}"', 10)
    add(lines)

    for i in range(1, len(zones) + 1):
        add(lines, f"zone_{i}_vandaag: >", 10)
        add(lines, "{{", 12)
        add(lines, f"is_state('{zone_bool_entity(slug, i)}', 'on') and (", 14)
        add(lines, build_today_expr(slug, i), 16)
        add(lines, ")", 14)
        add(lines, "}}", 12)
    add(lines)

    add(lines, "- choose:", 6)
    add(lines, "- conditions:", 8)
    add(lines, "- condition: state", 10)
    add(lines, f"entity_id: input_boolean.{slug}_parallel", 12)
    add(lines, 'state: "on"', 12)
    add(lines, "sequence:", 10)
    add(lines, "- parallel:", 12)

    for i in range(1, len(zones) + 1):
        add(lines, "- sequence:", 14)
        add(lines, "- if:", 16)
        add(lines, "- condition: template", 18)
        add(lines, f'value_template: "{{{{ zone_{i}_vandaag }}}}"', 20)
        add(lines, "then:", 18)

        add(lines, "- action: input_datetime.set_datetime", 20)
        add(lines, "target:", 22)
        add(lines, f"entity_id: {zone_start_helper_entity(slug, i)}", 24)
        add(lines, "data:", 22)
        add(lines, 'datetime: "{{ now().strftime(\'%Y-%m-%d %H:%M:%S\') }}"', 24)

        add(lines, "- action: input_number.set_value", 20)
        add(lines, "target:", 22)
        add(lines, f"entity_id: {zone_running_duration_entity(slug, i)}", 24)
        add(lines, "data:", 22)
        add(lines, f"value: \"{{{{ states('{zone_duration_entity(slug, i)}') | int(0) }}}}\"", 24)

        add(lines, "- action: switch.turn_on", 20)
        add(lines, "target:", 22)
        add(lines, f"entity_id: {zone_switch_entity(slug, i)}", 24)

        delay_tpl = (
            f"{{{{ '%02d:%02d:00' | format("
            f"(states('{zone_duration_entity(slug, i)}') | int(0)) // 60, "
            f"(states('{zone_duration_entity(slug, i)}') | int(0)) % 60) }}}}"
        )
        add(lines, f"- delay: {q(delay_tpl)}", 20)

        add(lines, "- action: switch.turn_off", 20)
        add(lines, "target:", 22)
        add(lines, f"entity_id: {zone_switch_entity(slug, i)}", 24)

        add(lines, "- action: input_number.set_value", 20)
        add(lines, "target:", 22)
        add(lines, f"entity_id: {zone_running_duration_entity(slug, i)}", 24)
        add(lines, "data:", 22)
        add(lines, "value: 0", 24)

    add(lines, "default:", 8)

    for i in range(1, len(zones) + 1):
        add(lines, "- if:", 10)
        add(lines, "- condition: template", 12)
        add(lines, f'value_template: "{{{{ zone_{i}_vandaag }}}}"', 14)
        add(lines, "then:", 12)
        if i > 1:
            add(lines, '- delay: "00:00:05"', 14)

        add(lines, "- action: input_datetime.set_datetime", 14)
        add(lines, "target:", 16)
        add(lines, f"entity_id: {zone_start_helper_entity(slug, i)}", 18)
        add(lines, "data:", 16)
        add(lines, 'datetime: "{{ now().strftime(\'%Y-%m-%d %H:%M:%S\') }}"', 18)

        add(lines, "- action: input_number.set_value", 14)
        add(lines, "target:", 16)
        add(lines, f"entity_id: {zone_running_duration_entity(slug, i)}", 18)
        add(lines, "data:", 16)
        add(lines, f"value: \"{{{{ states('{zone_duration_entity(slug, i)}') | int(0) }}}}\"", 18)

        add(lines, "- action: switch.turn_on", 14)
        add(lines, "target:", 16)
        add(lines, f"entity_id: {zone_switch_entity(slug, i)}", 18)

        delay_tpl = (
            f"{{{{ '%02d:%02d:00' | format("
            f"(states('{zone_duration_entity(slug, i)}') | int(0)) // 60, "
            f"(states('{zone_duration_entity(slug, i)}') | int(0)) % 60) }}}}"
        )
        add(lines, f"- delay: {q(delay_tpl)}", 14)

        add(lines, "- action: switch.turn_off", 14)
        add(lines, "target:", 16)
        add(lines, f"entity_id: {zone_switch_entity(slug, i)}", 18)

        add(lines, "- action: input_number.set_value", 14)
        add(lines, "target:", 16)
        add(lines, f"entity_id: {zone_running_duration_entity(slug, i)}", 18)
        add(lines, "data:", 16)
        add(lines, "value: 0", 18)

    for i, zone in enumerate(zones, start=1):
        add(lines, f"{slug}_zone_{i}_handmatig_start:", 2)
        add(lines, f"alias: {title} - {zone['name']} handmatig start", 4)
        add(lines, "mode: restart", 4)
        add(lines, "sequence:", 4)

        add(lines, "- action: input_datetime.set_datetime", 6)
        add(lines, "target:", 8)
        add(lines, f"entity_id: {zone_start_helper_entity(slug, i)}", 10)
        add(lines, "data:", 8)
        add(lines, 'datetime: "{{ now().strftime(\'%Y-%m-%d %H:%M:%S\') }}"', 10)

        add(lines, "- action: input_number.set_value", 6)
        add(lines, "target:", 8)
        add(lines, f"entity_id: {zone_running_duration_entity(slug, i)}", 10)
        add(lines, "data:", 8)
        add(lines, f"value: \"{{{{ states('{zone_manual_duration_entity(slug, i)}') | int(0) }}}}\"", 10)

        add(lines, "- action: switch.turn_on", 6)
        add(lines, "target:", 8)
        add(lines, f"entity_id: {zone_switch_entity(slug, i)}", 10)

        delay_tpl = (
            f"{{{{ '%02d:%02d:00' | format("
            f"(states('{zone_manual_duration_entity(slug, i)}') | int(0)) // 60, "
            f"(states('{zone_manual_duration_entity(slug, i)}') | int(0)) % 60) }}}}"
        )
        add(lines, f"- delay: {q(delay_tpl)}", 6)

        add(lines, "- action: switch.turn_off", 6)
        add(lines, "target:", 8)
        add(lines, f"entity_id: {zone_switch_entity(slug, i)}", 10)

        add(lines, "- action: input_number.set_value", 6)
        add(lines, "target:", 8)
        add(lines, f"entity_id: {zone_running_duration_entity(slug, i)}", 10)
        add(lines, "data:", 8)
        add(lines, "value: 0", 10)
        add(lines)

    add(lines)
    add(lines, f"{slug}_stop_alles:", 2)
    add(lines, f"alias: {title} - stop alles", 4)
    add(lines, "mode: parallel", 4)
    add(lines, "sequence:", 4)
    add(lines, "- action: script.turn_off", 6)
    add(lines, "target:", 8)
    add(lines, f"entity_id: script.{slug}_start_zones", 10)
    add(lines)
    for i in range(1, len(zones) + 1):
        add(lines, "- action: script.turn_off", 6)
        add(lines, "target:", 8)
        add(lines, f"entity_id: script.{slug}_zone_{i}_handmatig_start", 10)
    add(lines)
    add(lines, "- action: switch.turn_off", 6)
    add(lines, "target:", 8)
    add(lines, "entity_id:", 10)
    for i in range(1, len(zones) + 1):
        add(lines, f"- {zone_switch_entity(slug, i)}", 12)
    add(lines)

    for i in range(1, len(zones) + 1):
        add(lines, "- action: input_number.set_value", 6)
        add(lines, "target:", 8)
        add(lines, f"entity_id: {zone_running_duration_entity(slug, i)}", 10)
        add(lines, "data:", 8)
        add(lines, "value: 0", 10)

    return "\n".join(lines) + "\n"


def generate_dashboard(cfg: dict) -> str:
    slug = cfg["slug"]
    title = cfg["title"]
    zones = cfg["zones"]

    zone_icons = [
        "mdi:grass",
        "mdi:flower",
        "mdi:tree",
        "mdi:sprout",
        "mdi:pine-tree",
        "mdi:leaf",
        "mdi:shrub",
        "mdi:forest",
        "mdi:sprinkler-variant",
        "mdi:flower-pollen",
        "mdi:tree-outline",
        "mdi:grass",
        "mdi:leaf-maple",
        "mdi:flower-tulip",
        "mdi:forest-outline",
        "mdi:water",
    ]

    def zone_icon(i):
        return zone_icons[(i - 1) % len(zone_icons)]

    lines = []

    add(lines, "type: sections")
    add(lines, "max_columns: 4")
    add(lines, f"title: {slug}")
    add(lines, f"path: {slug}")
    add(lines, "sections:")

    # SECTION 1
    add(lines, "- type: grid", 2)
    add(lines, "cards:", 4)
    add(lines, "- type: vertical-stack", 6)
    add(lines, "cards:", 8)

    add(lines, "- type: custom:mushroom-title-card", 10)
    add(lines, f"title: 🌱 {title}", 12)
    add(lines, "subtitle: Slimme irrigatie", 12)

    add(lines, "- type: custom:mushroom-chips-card", 10)
    add(lines, "chips:", 12)

    chip_entities = [
        (rain_24h_sensor_entity(slug), "Regen", "mdi:weather-rainy"),
        (max_temp_24h_sensor_entity(slug), "Temperatuur", "mdi:sun-thermometer"),
        (remaining_sensor_entity(slug), "Nog te gaan", "mdi:timer-sand"),
        (end_time_sensor_entity(slug), "Klaar om", "mdi:clock-end"),
    ]
    
    for entity, name, icon in chip_entities:
        add(lines, "- type: entity", 14)
        add(lines, f"entity: {entity}", 16)
        add(lines, "content_info: state", 16)
        add(lines, f"name: {name}", 16)
        add(lines, f"icon: {icon}", 16)

    add(lines, "- type: horizontal-stack", 10)
    add(lines, "cards:", 12)

    add(lines, "- type: custom:mushroom-template-card", 14)
    add(lines, f"entity: input_boolean.{slug}_ingeschakeld", 16)
    add(lines, "primary: Automatische modus", 16)
    add(lines, "secondary: >", 16)
    add(lines, f"{{{{ 'Ingeschakeld' if is_state('input_boolean.{slug}_ingeschakeld', 'on') else 'Uitgeschakeld' }}}}", 18)
    add(lines, "icon: mdi:sprinkler-variant", 16)
    add(lines, "icon_color: >", 16)
    add(lines, f"{{{{ 'green' if is_state('input_boolean.{slug}_ingeschakeld', 'on') else 'grey' }}}}", 18)

    add(lines, "- type: custom:mushroom-template-card", 14)
    add(lines, f"entity: {active_now_binary_entity(slug)}", 16)
    add(lines, "primary: Beregening nu", 16)
    add(lines, "secondary: |", 16)
    add(lines, f"{{% if is_state('{active_now_binary_entity(slug)}', 'on') %}}", 18)
    add(lines, "Actief", 20)
    add(lines, "{% else %}", 18)
    add(lines, "Niet actief", 20)
    add(lines, "{% endif %}", 18)
    add(lines, "icon: mdi:sprinkler", 16)
    add(lines, "icon_color: >", 16)
    add(lines, f"{{{{ 'blue' if is_state('{active_now_binary_entity(slug)}', 'on') else 'grey' }}}}", 18)

    add(lines, "- type: horizontal-stack", 10)
    add(lines, "cards:", 12)

    add(lines, "- type: custom:mushroom-template-card", 14)
    add(lines, "primary: Nu starten", 16)
    add(lines, "secondary: Start alle actieve zones", 16)
    add(lines, "icon: mdi:play-circle-outline", 16)
    add(lines, "icon_color: green", 16)

    add(lines, "- type: custom:mushroom-template-card", 14)
    add(lines, "primary: Alles stoppen", 16)
    add(lines, "secondary: Direct uitschakelen", 16)
    add(lines, "icon: mdi:stop-circle-outline", 16)
    add(lines, "icon_color: red", 16)

    add(lines, "- type: custom:mushroom-title-card", 10)
    add(lines, "title: ℹ️ Diagnose", 12)

    add(lines, "- type: entities", 10)
    add(lines, "show_header_toggle: false", 12)
    add(lines, "entities:", 12)
    diag_entities = [
        (last_run_sensor_entity(slug), "Laatste run"),
        (total_duration_pretty_sensor_entity(slug), "Totale geplande duur"),
        (remaining_sensor_entity(slug), "Nog te gaan"),
        (end_time_sensor_entity(slug), "Klaar om nu"),
        (f"sensor.{slug}_geplande_eindtijd", "Gepland klaar om"),
        (block_reason_sensor_entity(slug), "Blokkade reden"),
    ]
    for entity, name in diag_entities:
        add(lines, f"- entity: {entity}", 14)
        add(lines, f"name: {name}", 16)

    add(lines, "- type: custom:mushroom-title-card", 10)
    add(lines, "title: ⚙️ Instellingen", 12)

    add(lines, "- type: entities", 10)
    add(lines, "show_header_toggle: false", 12)
    add(lines, "entities:", 12)
    settings_entities = [
        (f"input_select.{slug}_start_type", "Starttype"),
        (f"input_number.{slug}_min_temp", "Minimale temperatuur"),
        (f"input_number.{slug}_max_regen_24u", "Maximale regen 24u"),
        (f"input_boolean.{slug}_parallel", "Parallel sproeien"),
    ]
    for entity, name in settings_entities:
        add(lines, f"- entity: {entity}", 14)
        add(lines, f"name: {name}", 16)

    add(lines, "- type: conditional", 10)
    add(lines, "conditions:", 12)
    add(lines, f"- entity: input_select.{slug}_start_type", 14)
    add(lines, "state: Vaste tijd", 16)
    add(lines, "card:", 12)
    add(lines, "type: entities", 14)
    add(lines, "show_header_toggle: false", 14)
    add(lines, "entities:", 14)
    add(lines, f"- entity: input_datetime.{slug}_vaste_tijd", 16)
    add(lines, "name: Starttijd", 18)

    add(lines, "- type: conditional", 10)
    add(lines, "conditions:", 12)
    add(lines, "- condition: or", 14)
    add(lines, "conditions:", 16)
    add(lines, f"- entity: input_select.{slug}_start_type", 18)
    add(lines, "state: Zonsopkomst", 20)
    add(lines, f"- entity: input_select.{slug}_start_type", 18)
    add(lines, "state: Zonsondergang", 20)
    add(lines, "card:", 12)
    add(lines, "type: entities", 14)
    add(lines, "show_header_toggle: false", 14)
    add(lines, "entities:", 14)
    add(lines, f"- entity: input_number.{slug}_offset_minuten", 16)
    add(lines, "name: Offset minuten", 18)

    add(lines, "- type: custom:mushroom-title-card", 10)
    add(lines, "title: 💧 Zones", 12)

    add(lines, "- type: vertical-stack", 10)
    add(lines, "cards:", 12)
    for i, zone in enumerate(zones, start=1):
        add(lines, "- type: custom:stack-in-card", 14)
        add(lines, "cards:", 16)

        add(lines, "- type: custom:mushroom-number-card", 18)
        add(lines, f"entity: input_number.{slug}_zone_{i}_duur", 20)
        add(lines, f"name: {zone['name']}", 20)
        add(lines, f"icon: {zone_icon(i)}", 20)

        add(lines, "- type: custom:bar-card", 18)
        add(lines, "min: 0", 20)
        add(lines, "max: 100", 20)
        add(lines, "height: 26px", 20)
        add(lines, "decimal: 0", 20)
        add(lines, "positions:", 20)
        add(lines, 'icon: "off"', 22)
        add(lines, 'indicator: "off"', 22)
        add(lines, 'name: "inside"', 22)
        add(lines, 'value: "inside"', 22)
        add(lines, "severity:", 20)
        add(lines, "- from: 0", 22)
        add(lines, '  to: 30', 22)
        add(lines, '  color: "#3b82f6"', 22)
        add(lines, "- from: 31", 22)
        add(lines, '  to: 70', 22)
        add(lines, '  color: "#2563eb"', 22)
        add(lines, "- from: 71", 22)
        add(lines, '  to: 100', 22)
        add(lines, '  color: "#1d4ed8"', 22)
        add(lines, "card_mod:", 20)
        add(lines, "style: |", 22)
        add(lines, "  bar-card-name {", 24)
        add(lines, "    font-weight: 600;", 26)
        add(lines, "    font-size: 13px;", 26)
        add(lines, "  }", 24)
        add(lines, "  bar-card-value {", 24)
        add(lines, "    font-weight: 600;", 26)
        add(lines, "    font-size: 13px;", 26)
        add(lines, "  }", 24)
        add(lines, "entities:", 20)
        add(lines, f"- entity: sensor.{slug}_zone_{i}_balk_procent", 22)
        add(lines, f"  name: {zone['name']} voortgang", 22)

    add(lines, "column_span: 1", 4)
    # SECTION 2 Weekplanner
    add(lines, "- type: grid", 2)
    add(lines, "cards:", 4)
    add(lines, "- type: vertical-stack", 6)
    add(lines, "cards:", 8)

    add(lines, "- type: custom:mushroom-title-card", 10)
    add(lines, "title: 🗓️ Weekplanner", 12)

    day_pairs = [
        ("maandag", "Ma"),
        ("dinsdag", "Di"),
        ("woensdag", "Wo"),
        ("donderdag", "Do"),
        ("vrijdag", "Vr"),
        ("zaterdag", "Za"),
        ("zondag", "Zo"),
    ]

    for i, zone in enumerate(zones, start=1):
        add(lines, "- type: custom:stack-in-card", 10)
        add(lines, "cards:", 12)

        add(lines, "- type: custom:mushroom-template-card", 14)
        add(lines, f"entity: input_boolean.{slug}_zone_{i}_actief", 16)
        add(lines, f"primary: {zone['name']}", 16)
        add(lines, "secondary: >", 16)

        dag_states = ", ".join(
            [f"is_state('input_boolean.{slug}_{day}_zone_{i}','on')" for day, _ in day_pairs]
        )
        add(lines, f"{{% set dagen = [{dag_states}] %}} {{{{ dagen | select('eq', true) | list | count }}}} dagen actief", 18)

        add(lines, f"icon: {zone_icon(i)}", 16)
        add(lines, "icon_color: >", 16)
        add(lines, f"{{{{ 'green' if is_state('input_boolean.{slug}_zone_{i}_actief', 'on') else 'red' }}}}", 18)
        add(lines, "tap_action:", 16)
        add(lines, "action: toggle", 18)

        add(lines, "- type: grid", 14)
        add(lines, "columns: 7", 16)
        add(lines, "square: false", 16)
        add(lines, "cards:", 16)

        for day, short in day_pairs:
            add(lines, "- type: custom:mushroom-template-card", 18)
            add(lines, f"primary: {short}", 20)
            add(lines, "icon: >", 20)
            add(lines, f"{{% if is_state('input_boolean.{slug}_{day}_zone_{i}', 'on') %}}", 22)
            add(lines, "mdi:check", 24)
            add(lines, "{% else %}", 22)
            add(lines, "mdi:close", 24)
            add(lines, "{% endif %}", 22)
            add(lines, "icon_color: >", 20)
            add(lines, f"{{% if is_state('input_boolean.{slug}_{day}_zone_{i}', 'on') %}}", 22)
            add(lines, "green", 24)
            add(lines, "{% else %}", 22)
            add(lines, "grey", 24)
            add(lines, "{% endif %}", 22)
            add(lines, f"entity: input_boolean.{slug}_{day}_zone_{i}", 20)
            add(lines, "layout: vertical", 20)
            add(lines, "fill_container: true", 20)
            add(lines, "tap_action:", 20)
            add(lines, "action: toggle", 22)

    # handmatig
    add(lines, "- type: vertical-stack", 6)
    add(lines, "cards:", 8)
    add(lines, "- type: custom:mushroom-title-card", 10)
    add(lines, "title: 🎛️ Handmatige bediening", 12)
    add(lines, "subtitle: Tik om zone aan of uit te zetten", 12)

    add(lines, "- type: custom:stack-in-card", 10)
    add(lines, "cards:", 12)
    add(lines, "- type: grid", 14)
    add(lines, "columns: 2", 16)
    add(lines, "square: false", 16)
    add(lines, "cards:", 16)

    for i, zone in enumerate(zones, start=1):
        add(lines, "- type: custom:stack-in-card", 18)
        add(lines, "cards:", 20)

        add(lines, "- type: custom:mushroom-number-card", 22)
        add(lines, f"entity: input_number.{slug}_zone_{i}_handmatig_duur", 24)
        add(lines, f"name: {zone['name']} duur", 24)
        add(lines, "icon: mdi:timer-play-outline", 24)


        add(lines, "- type: horizontal-stack", 22)
        add(lines, "cards:", 24)

        add(lines, "- type: custom:mushroom-template-card", 26)
        add(lines, f"entity: {zone_switch_entity(slug, i)}", 28)
        add(lines, f"primary: {zone['name']}", 28)
        add(lines, "secondary: >", 28)
        add(lines, f"{{{{ 'AAN' if is_state('{zone_switch_entity(slug, i)}', 'on') else 'UIT' }}}}", 30)
        add(lines, f"icon: {zone_icon(i)}", 28)
        add(lines, "icon_color: >", 28)
        add(lines, f"{{{{ 'blue' if is_state('{zone_switch_entity(slug, i)}', 'on') else 'grey' }}}}", 30)
        add(lines, "fill_container: true", 28)
        add(lines, "tap_action:", 28)
        add(lines, "action: toggle", 30)
        add(lines, "hold_action:", 28)
        add(lines, "action: more-info", 30)

        add(lines, "- type: custom:mushroom-template-card", 26)
        add(lines, f"primary: Start {zone['name']}", 28)
        add(lines, "secondary: Handmatige looptijd", 28)
        add(lines, "icon: mdi:play", 28)
        add(lines, "fill_container: true", 28)
        add(lines, "tap_action:", 28)
        add(lines, "action: call-service", 30)
        add(lines, f"service: script.{slug}_zone_{i}_handmatig_start", 30)

    add(lines, "- type: custom:mushroom-template-card", 10)
    add(lines, "primary: Alles stoppen", 12)
    add(lines, "secondary: Zet alle zones direct uit", 12)
    add(lines, "icon: mdi:stop-circle-outline", 12)
    add(lines, "icon_color: red", 12)
    add(lines, "tap_action:", 12)
    add(lines, "action: call-service", 14)
    add(lines, "service: script.turn_on", 14)
    add(lines, "target:", 14)
    add(lines, f"entity_id: script.{slug}_stop_alles", 16)

    return "\n".join(lines) + "\n"


def main():
    config_path = Path("beregening_tuin_config.yaml")

    cfg = yaml.safe_load(config_path.read_text(encoding="utf-8"))

    slug = cfg["slug"]

    package_output_path = Path(f"{slug}.yaml")
    dashboard_output_path = Path(f"{slug}_dashboard.yaml")

    package_output = generate_package(cfg)
    dashboard_output = generate_dashboard(cfg)

    package_output_path.write_text(package_output, encoding="utf-8")
    dashboard_output_path.write_text(dashboard_output, encoding="utf-8")

    print(f"Package gemaakt: {package_output_path}")
    print(f"Dashboard gemaakt: {dashboard_output_path}")


if __name__ == "__main__":
    main()