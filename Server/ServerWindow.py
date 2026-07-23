import tkinter
from tkinter import ttk, messagebox

import cotton_candy

from ServerLogic import ServerLogic


class ServerWindow:
    def __init__(self):
        self.logic = ServerLogic()

        self._setup_root()
        self._setup_ui()

        self.running = True

    def _setup_root(self):
        self.root = tkinter.Tk()
        self.root.title = "Server"
        self.root.geometry("300x150")
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)


    def _setup_ui(self):
        self.label = ttk.Label(text="")
        self.label.pack()

        self.active_btn = ActiveButton(self)

    def _on_closing(self):
        if not self.running:
            return
        try:
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                self.root.destroy()
        except Exception as e:
            print(e)
        finally:
            self.logic.stop()
            self.running = False


    def _update_clock(self):
        state = cotton_candy.shared_state.get('clients')
        self.label.config(text=f"Подключено: {len(state['clients']) if state else 0}")
        self.active_btn.body.config(text=self.active_btn.name)
        self.root.after(100, self._update_clock)



    def run(self):
        """Запуск приложения"""
        try:
            self._update_clock()
            self.root.mainloop()
        except Exception as e:
            print("Ошибка при запуске")
            print(e)
        finally:
            self._on_closing()




class ActiveButton:
    def __init__(self, window: ServerWindow):
        self.window = window

        self.body = ttk.Button(text=self.name, command=self.on_click)
        self.body.pack()

    @property
    def active(self):
        return self.window.logic.running

    @property
    def name(self):
        return "Начать" if not self.active else "Завершить"

    def on_click(self):
        if self.active:
            self.window.logic.stop()
        else:
            self.window.logic.start()
