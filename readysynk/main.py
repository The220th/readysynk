# coding: utf-8


from readysynk.argsparsing import get_args
from readysynk.settings_manager import SettingsManager
from readysynk.ramdb import RAMDB
from readysynk.gradio_main import start_gradio_interface


def main():
    args = get_args()
    sm = SettingsManager(args.settings_path)
    RAMDB()

    start_gradio_interface()


if __name__ == "__main__":
    main()
