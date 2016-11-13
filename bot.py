from flask import Flask, request
from fbmq import Page
from fbmq import Attachment, Template, QuickReply, Page
PAGE_ACCESS_TOKEN = EAARxI0qHhPgBAJpPGWqgiFN9PAczBuHkIWUBTzZB3uy6wI2V063NndvCA0N6Iir97hofO1a5mCscx1hiMlIZAzvKwutio2OZCoFjQZBUpTcdiXvny5E9ZBhbugxuFvZBXtr3dP4XvwpUUqRktiCMv1gh1gPuhpVLWqyBLZBwAPAMQZDZD
page = fbmq.Page(PAGE_ACCESS_TOKEN)

@app.route('/webhook', methods=['POST'])
def webhook():
    page.handle_webhook(request.get_data(as_text=True))
    return "ok"

@page.handle_message
def message_handler(event):
    """:type event: fbmq.Event"""
    sender_id = event.sender_id
    message = event.message_text

    page.send(sender_id, "thank you! your message is '%s'" % message)

@page.after_send
def after_send(payload, response):
""":type payload: fbmq.Payload"""
    print("complete")
