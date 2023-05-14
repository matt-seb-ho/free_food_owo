mock_extracted_fields = [
    {
        "is_free_food_event": {
            "value": False,
            "source": "free food",
            "confidence": 0.9
        },
        "name": {
            "value": "Culture Showcase",
            "source": "Culture Showcase",
            "confidence": 0.8
        },
        "start": {
            "value": "2022-05-12T13:00:00.000Z",
            "source": "Friday, May 12th from 1-4pm",
            "confidence": 0.7
        },
        "end": {
            "value": "2022-05-12T16:00:00.000Z",
            "source": "Friday, May 12th from 1-4pm",
            "confidence": 0.7
        },
            "location": {
            "value": "Storke Plaza",
            "source": "Storke Plaza",
            "confidence": 0.8
        },
        "food_type": {
            "value": None,
            "source": None,
            "confidence": 0.0
        }
    },
    {
        "is_free_food_event": {
            "value": True,
            "source": "free food",
            "confidence": 0.9
        },
        "name": {
            "value": "Culture Showcase",
            "source": "Culture Showcase",
            "confidence": 0.8
        },
        "start": {
            "value": "2022-05-12T13:00:00.000Z",
            "source": "Friday, May 12th from 1-4pm",
            "confidence": 0.7
        },
        "end": {
            "value": "2022-05-12T16:00:00.000Z",
            "source": "Friday, May 12th from 1-4pm",
            "confidence": 0.7
        },
            "location": {
            "value": "Storke Plaza",
            "source": "Storke Plaza",
            "confidence": 0.8
        },
        "food_type": {
            "value": None,
            "source": None,
            "confidence": 0.0
        }
    },
    {
        "is_free_food_event": {
            "value": True,
            "source": "snacks will be provided",
            "confidence": 0.9
        },
        "name": {
            "value": "Engineering Social",
            "source": "Engineering Social",
            "confidence": 0.8
        },
        "start": {
            "value": "2022-09-16T13:00:00.000Z",
            "source": "1-4pm on September 16th",
            "confidence": 0.7
        },
        "end": {
            "value": "2022-09-16T16:00:00.000Z",
            "source": "1-4pm on September 16th",
            "confidence": 0.7
        },
            "location": {
            "value": "Harold Frank Hall",
            "source": "Harold Frank Hall",
            "confidence": 0.8
        },
        "food_type": {
            "value": "Google",
            "source": "Google",
            "confidence": 0.8
        }
    }
]

mock_event_data = [
    {
        "summary": "Free Food at Culture Showcase",
        "location": "",
        "description": "There will be free food at Storke Plaza.",
        "start": {
            "dateTime": "2023-05-12T13:00:00",
            "timeZone": "America/Los_Angeles"
        },
        "end": {
            "dateTime": "2023-05-12T16:00:00",
            "timeZone": "America/Los_Angeles"
        }
    },
    {
        "summary": "Summary2",
        "location": "",
        "description": "There will be free food at Henley Hall.",
        "start": {
            "dateTime": "2023-05-12T13:00:00",
            "timeZone": "America/Los_Angeles"
        },
        "end": {
            "dateTime": "2023-05-12T16:00:00",
            "timeZone": "America/Los_Angeles"
        }
    },
    {
        "summary": "Summary2",
        "location": "",
        "description": "There will be free food at Henley Hall.",
        "start": {
            "dateTime": "2023-05-12T13:00:00",
            "timeZone": "America/Los_Angeles"
        },
        "end": {
            "dateTime": "2023-05-12T16:00:00",
            "timeZone": "America/Los_Angeles"
        }
    }
]
