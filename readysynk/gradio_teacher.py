# coding: utf-8

import gradio as gr

from readysynk.ramdb import RAMDB
from readysynk.gradio_global import check_password_or_raise


def sync_table_button_fn(password: str):
    check_password_or_raise(password)
    try:
        ramdb = RAMDB()
        table, hashes = ramdb.get_ready_users_table()
        return table, gr.update(choices=hashes, value=hashes[0])
    except Exception as e:
        raise gr.Error(str(e))

def reset_ready_button_fn(password: str):
    check_password_or_raise(password)
    try:
        ramdb = RAMDB()
        ramdb.set_all_unready()
        table, hashes = ramdb.get_ready_users_table()
        return table, gr.update(choices=hashes, value=hashes[0])
    except Exception as e:
        raise gr.Error(str(e))


def user_set_unready_fn(password: str, user_hash: str):
    check_password_or_raise(password)
    try:
        ramdb = RAMDB()
        ramdb.set_unready(user_hash)
        table, hashes = ramdb.get_ready_users_table()
        return table, gr.update(choices=hashes, value=hashes[0])
    except Exception as e:
        raise gr.Error(str(e))


def user_delete_fn(password: str, user_hash: str):
    check_password_or_raise(password)
    try:
        ramdb = RAMDB()
        ramdb.remove_user(user_hash)
        table, hashes = ramdb.get_ready_users_table()
        if len(hashes) == 0 or table is None or hashes is None:
            return table, gr.update(choices=[], value=None)
        else:
            return table, gr.update(choices=hashes, value=hashes[0])
    except Exception as e:
        raise gr.Error(str(e))


def presentation_slide_change(password: str, slider: int):
    if slider == -1:
        return
    check_password_or_raise(password)
    try:
        ramdb = RAMDB()
        image = ramdb.get_slide(slider)
        ramdb.set_cur_slide(slider)
        return image
    except Exception as e:
        raise gr.Error(str(e))


def presentation_load(password: str, file: str):
    check_password_or_raise(password)
    try:
        ramdb = RAMDB()
        ramdb.init_presentation(file)
        image = ramdb.get_slide(1)
        ramdb.set_cur_slide(1)
        return gr.update(minimum=1, maximum=ramdb.get_slides_num(), value=1, step=1, interactive=True), image
    except Exception as e:
        raise gr.Error(str(e))


def presentation_next(password: str, slider: int):
    check_password_or_raise(password)
    try:
        needed_slide_num = slider + 1
        ramdb = RAMDB()
        if needed_slide_num > ramdb.get_slides_num():
            needed_slide_num = slider
        ramdb.set_cur_slide(needed_slide_num)
        return gr.update(value=needed_slide_num)
    except Exception as e:
        raise gr.Error(str(e))


def presentation_prev(password: str, slider: int):
    check_password_or_raise(password)
    try:
        needed_slide_num = slider - 1
        ramdb = RAMDB()
        if needed_slide_num < 1:
            needed_slide_num = slider
        ramdb.set_cur_slide(needed_slide_num)
        return gr.update(value=needed_slide_num)
    except Exception as e:
        raise gr.Error(str(e))


def gradio_interface_teacher_entry_point():
    password = gr.Textbox(label="🔐 Пароль", interactive=True)
    with gr.Tabs():
        with gr.Tab("Готовность"):
            with gr.Row():
                sync_table_button = gr.Button("🔄")
                reset_ready_button = gr.Button("Сброс")
            with gr.Row():
                table = gr.Dataframe(headers=["Хэш", "Имя", "Готовность"],
                                        label="Таблица готовности", wrap=True, column_widths=["15%", "75%", "10%"], interactive=False)
            with gr.Group():
                users_dropbox = gr.Dropdown()
                user_set_unready = gr.Button("Не готов")
                user_delete = gr.Button("Удалить")
        with gr.Tab("Презентация"):
            with gr.Row():
                presentation_file = gr.File(label="Файл презентации (PDF ТОЛЬКО)")
                load_presentation_button = gr.Button("Загрузить презентацию")
                gr.Markdown("# Слушателям нужно нажать кнопку \"Обновить презентацию\" после загрузки")
            with gr.Row():
                presentation_slider = gr.Slider(minimum=-100, maximum=100, value=-1, step=1, interactive=False, label="Номер слайда")
                presentation_prev_button = gr.Button("⬅️️")
                presentation_next_button = gr.Button("➡️")
            with gr.Row():
                presentation_image = gr.Image()

    sync_table_button.click(fn=sync_table_button_fn, inputs=[password], outputs=[table, users_dropbox])
    reset_ready_button.click(fn=reset_ready_button_fn, inputs=[password], outputs=[table, users_dropbox])
    user_set_unready.click(fn=user_set_unready_fn, inputs=[password, users_dropbox], outputs=[table, users_dropbox])
    user_delete.click(fn=user_delete_fn, inputs=[password, users_dropbox], outputs=[table, users_dropbox])

    load_presentation_button.click(fn=presentation_load, inputs=[password, presentation_file], outputs=[presentation_slider, presentation_image])
    presentation_slider.change(fn=presentation_slide_change, inputs=[password, presentation_slider], outputs=[presentation_image])
    presentation_prev_button.click(fn=presentation_prev, inputs=[password, presentation_slider], outputs=[presentation_slider])
    presentation_next_button.click(fn=presentation_next, inputs=[password, presentation_slider], outputs=[presentation_slider])
