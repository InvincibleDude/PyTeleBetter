from typing import TypedDict


class ChannelDictItem(TypedDict):
    channel: int
    linked_chat: int


class ReplyTemplate(TypedDict):
    mode: str
    text: str


class Account(TypedDict):
    number: int | None
    session_string: str | None
    assigned_to: list[int | str]
    reply_template: ReplyTemplate
    channel_layer: bool | "ChannelLayer"


class ChannelLayer(TypedDict):
    name: str
    description: str
    caption: str


class AccountsConfig(TypedDict):
    accounts: list[Account]
