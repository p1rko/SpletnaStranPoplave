import time

from sqlalchemy import insert

from database import HydroStation, HydroMeasurement, session

import xml.etree.ElementTree as ET
from datetime import datetime, timezone

import requests


HYDRO_API = "https://www.arso.gov.si/xml/vode/hidro_podatki_zadnji.xml"


def get_tag_value(element: ET.Element, selector: str) -> float | None:
    tag = element.find(selector)

    if tag is not None:
        return float(tag.text)


def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).one_or_none()
    if instance:
        return instance, False
    else:
        kwargs |= defaults or {}
        instance = model(**kwargs)
        try:
            session.add(instance)
            session.commit()
        except Exception:
            session.rollback()
            instance = session.query(model).filter_by(**kwargs).one()
            return instance, False
        else:
            return instance, True


def hydro_data_download():
    data = requests.get(HYDRO_API).text
    root = ET.fromstring(data)

    measurements = []

    for station in root.findall("postaja"):
        try:
            station_key = station.get("sifra")
            station_name = station.find("merilno_mesto").text
            station_river = station.find("reka").text

            if station_river == "Jadransko morje":
                continue

            latitude = float(station.get("ge_sirina"))
            longitude = float(station.get("ge_dolzina"))
            altitude = float(station.get("kota_0"))

            timestamp = datetime.fromisoformat(station.find("datum_cet").text + "+01:00")
            level = get_tag_value(station, "vodostaj")
            flow = get_tag_value(station, "pretok")
            temperature = get_tag_value(station, "temp_vode")

            print(f"Station key: {station_key}")
            print(f"Station name: {station_name}")
            print(f"Station river: {station_river}")
            print(f"Latitude: {latitude}")
            print(f"Longitude: {longitude}")
            print(f"Altitude: {altitude}")
            print(f"Timestamp: {timestamp}")
            print(f"Level: {level}")
            print(f"Flow: {flow}")
            print(f"Temperature: {temperature}")
            print()

        except Exception as error:
            print("Error while loading", station.find("ime_kratko").text)
            print(error)
            print()
            continue

        get_or_create(
            session,
            model=HydroStation,
            key=station_key,
            defaults={
                "name": station_name,
                "river": station_river,
                "latitude": latitude,
                "longitude": longitude,
                "altitude": altitude,
            },
        )

        if (
            session.query(HydroMeasurement)
            .filter(HydroMeasurement.station_id == station_key, HydroMeasurement.datetime == timestamp)
            .count()
        ):
            # Skip existing measurements
            continue

        measurements.append(
            {
                "station_id": station_key,
                "datetime": timestamp,
                "level": level,
                "flow": flow,
                "temperature": temperature,
            }
        )

    if measurements:
        print("Adding measurements")
        print()

        session.execute(insert(HydroMeasurement), measurements)
        session.commit()


while True:
    try:
        hydro_data_download()
    except Exception as error:
        print(error)
        print()

    time.sleep(15 * 60)
