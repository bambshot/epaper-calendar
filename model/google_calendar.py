#!/usr/bin/python
# -*- coding:utf-8 -*-

from __future__ import print_function
from datetime import datetime
import os.path
from googleapiclient.discovery import build


def get_dirpath_project_root(name):
    return os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))),
        name,
    )


class GoogleCalendar:
    def __init__(self, cred):
        self.service = build("calendar", "v3", credentials=cred)

    def get_events(self, calendar_id, max_results):
        now = datetime.utcnow().isoformat() + "Z"
        events_result = (
            # pylint: disable=maybe-no-member
            self.service.events()
            .list(
                calendarId=calendar_id,
                timeMin=now,
                maxResults=max_results,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            return []

        return [self.format_event(event) for event in events]

    def format_event(self, event):
        summary = event.get("summary", "タイトルなし")
        start_str = event["start"].get("dateTime", event["start"].get("date"))
        end_str = event["end"].get("dateTime", event["end"].get("date"))
        start_datetime = datetime.fromisoformat(start_str)
        end_datetime = datetime.fromisoformat(end_str)

        return {
            "start": start_str,
            "end": end_str,
            "period": self.format_event_period(start_datetime, end_datetime),
            "summary": summary,
        }

    def format_event_period(self, start_datetime, end_datetime):
        start = {
            "date_str": start_datetime.strftime("%m.%d"),
            "time_str": start_datetime.strftime("%H%M"),
        }
        end = {
            "date_str": end_datetime.strftime("%m.%d"),
            "time_str": end_datetime.strftime("%H%M"),
        }

        if start["date_str"] == end["date_str"]:
            return f'{start["date_str"]} {start["time_str"]}-{end["time_str"]}'

        if start["time_str"] == "0000" and end["time_str"] == "0000":
            return f'{start["date_str"]}-{end["date_str"]}'

        return f'{start["date_str"]} {start["time_str"]}-{end["date_str"]} {end["time_str"]}'
