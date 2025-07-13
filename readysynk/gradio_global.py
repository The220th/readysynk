# coding: utf-8

import gradio as gr
from readysynk.settings_manager import SettingsManager


def check_password_or_raise(password: str):
    sm = SettingsManager()
    real_password = sm.get_password()
    if password != real_password:
        raise gr.Error("Пароль не подходит. ")