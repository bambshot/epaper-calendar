#!/usr/bin/python
# -*- coding:utf-8 -*-

from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


def get_dirpath_project_root(name):
    return os.path.join(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
        name,
    )


class GoogleCalendar:
    def __init__(self):
        self.scopes = ["https://www.googleapis.com/auth/calendar.readonly"]
        creds = None

        token_path = get_dirpath_project_root("token.json")
        cred_path = get_dirpath_project_root("credentials.json")

        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, self.scopes)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(cred_path, self.scopes)
                creds = flow.run_local_server(port=0)
            with open(token_path, "w") as token:
                token.write(creds.to_json())

        self.service = build("calendar", "v3", credentials=creds)

    def get_events(self):
        now = datetime.datetime.utcnow().isoformat() + "Z"
        print("Getting the upcoming 10 events")
        events_result = (
            self.service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            print(start, event["summary"])
