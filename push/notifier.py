from __future__ import annotations
import json
from pywebpush import webpush, WebPushException

VAPID_PRIVATE = "vapid_private.pem"
VAPID_CLAIMS = {"sub": "mailto:admin@school.edu"}

def send_push(subscription: dict, title: str, body: str):
    try:
        webpush(
            subscription_info=subscription,
            data=json.dumps({"title": title, "body": body}),
            vapid_private_key=open(VAPID_PRIVATE).read(),
            vapid_claims=VAPID_CLAIMS,
        )
    except WebPushException as ex:
        print(ex)