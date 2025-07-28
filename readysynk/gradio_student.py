# coding: utf-8

import gradio as gr
from readysynk.ramdb import RAMDB
from PIL import Image
import time


def ready_pressed(name: str, request: gr.Request, progress=gr.Progress()):
    if name == "":
        raise gr.Error("Обозначьте себя сначала")
    req_hash = request.session_hash
    try:
        ramdb = RAMDB()
        ramdb.do_ready(req_hash, name)
        for _ in progress.tqdm(range(1)):
            time.sleep(1.0)
        return name
    except Exception as e:
        raise gr.Error(str(e))


def update_slide(scale: float):
    try:
        factor = scale/100
        ramdb = RAMDB()
        cur_clide_num = ramdb.get_cur_slide_num()
        slide_img = ramdb.get_slide(cur_clide_num)
        original_size = slide_img.size
        new_size = (int(original_size[0] * factor), int(original_size[1] * factor))
        resized_image = slide_img.resize(new_size, Image.LANCZOS)
        return resized_image
    except Exception as e:
        # raise gr.Error(str(e))
        pass


def sync_presentation_button_fn():
    try:
        ramdb = RAMDB()
        presentation = ramdb.get_all_presentation()
        return presentation
    except Exception as e:
        raise gr.Error(str(e))


def gradio_interface_student_entry_point():
    with gr.Tabs():
        with gr.Tab("Интерактив"):
            with gr.Row():
                name = gr.Textbox(label="Введите ФИО и рабочее место (РМ). Например, \"Иванов Иван Иванович (РМ 3)\"): ")
            with gr.Row():
                ready_button = gr.Button("✅ Сообщить об готовности")

            with gr.Row():
                scale = gr.Slider(minimum=10, maximum=300, value=100, step=10, interactive=True, label="Масштаб, %")
            with gr.Row():
                slide_image = gr.Image(value=update_slide, inputs=[scale], every=3)

            ready_button.click(fn=ready_pressed, inputs=[name], outputs=[name])
        with gr.Tab("Вся презентация"):
            with gr.Row():
                sync_presentation_button = gr.Button("🔄")
            with gr.Row():
                presentation_gallery = gr.Gallery(interactive=False, label="Презентация")
            sync_presentation_button.click(fn=sync_presentation_button_fn, inputs=[], outputs=[presentation_gallery])
