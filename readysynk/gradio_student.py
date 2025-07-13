# coding: utf-8

import gradio as gr
from readysynk.ramdb import RAMDB


def ready_pressed(name: str, request: gr.Request):
    if name == "":
        raise gr.Error("Обозначьте себя сначала")
    req_hash = request.session_hash
    try:
        ramdb = RAMDB()
        ramdb.do_ready(req_hash, name)
    except Exception as e:
        raise gr.Error(str(e))

def update_slide():
    try:
        ramdb = RAMDB()
        cur_clide_num = ramdb.get_cur_slide_num()
        slide_img = ramdb.get_slide(cur_clide_num)
        return slide_img
    except Exception as e:
        # raise gr.Error(str(e))
        pass

def gradio_interface_student_entry_point():
    with gr.Row():
        name = gr.Textbox(label="Обозначьте себя: ")
    with gr.Row():
        ready_button = gr.Button("✅ Сообщить об готовности")

    with gr.Row():
        slide_image = gr.Image(value=update_slide, every=3)

    ready_button.click(fn=ready_pressed, inputs=[name])