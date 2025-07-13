# coding: utf-8

import gradio as gr

from readysynk.settings_manager import SettingsManager
from readysynk.gradio_student import gradio_interface_student_entry_point
from readysynk.gradio_teacher import gradio_interface_teacher_entry_point


def start_gradio_interface():
    sm = SettingsManager()
    css_str = """
        .small_btn {
            margin: 0.3em 0em 0.25em 0;
            max-width: 2em;
            min-width: 2em !important;
            height: 2em;
        }
"""
    with gr.Blocks(css=css_str) as demo:
        with gr.Tabs():
            with gr.Tab("Слушатель"):
                gradio_interface_student_entry_point()
            with gr.Tab("Преподаватель"):
                gradio_interface_teacher_entry_point()

    (ip, port), share = sm.get_connection(), sm.is_share()
    demo.launch(server_name=ip, server_port=port, share=share)
