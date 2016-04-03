from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import random


class Game:

    TIME_TO_SOLVE = 100

    time_left = None

    def __init__(self):
        self.create_gui()
        self.importer = ImportQuestions('questions.data')

        for question in self.importer:
            question_obj = QuestionFrame(self.question_table, question)
            question_obj.pack(anchor=W, pady=10, padx=5)

        self.refresh()
        self.root.mainloop()

    def create_gui(self):
        self.root = Tk()
        self.root.title('Kvízjáték')

        self.root.rowconfigure(0, weight=1)
        # időmértő (time_left)
        self.time_left = IntVar(value=self.TIME_TO_SOLVE)

        # számláló (timer_label)
        self.timer_label = ttk.Label(self.root,
                                     textvariable=self.time_left,
                                     font=('Arial', 12, 'bold'),
                                     background="green",
                                     foreground="white",
                                     anchor=CENTER
                                     )
        self.timer_label.grid(row=0, column=0, sticky="nesw")

        # kérdések vászna (question_table)
        self.question_table = ttk.Frame(self.root, relief=GROOVE)
        self.question_table.grid(row=1, column=0, sticky="nesw")

    def refresh(self):
        if self.time_left.get() == 0:
            # kiértékelés
            total = 0
            for item in self.question_table.winfo_children():
                if item.correct():
                    total += 1
            # értesítés
            messagebox.showinfo('Eredmény', 'Összesen {} pontot értél el'.format(total))
            return

        self.time_left.set(self.time_left.get() - 1)
        self.root.after(1000, self.refresh)


class ImportQuestions:

    questions = []
    active_index = 0

    def __init__(self, filename):
        """
        TODO:
        Olvasd be a filename által jelölt file-t utf-8 karakterkódolással.
        Az utolsó válaszról vágd le a \n karaktert.
        A questions tömbbe tárold el a kérdést a Question osztály példányával.

        """
        with open(filename, 'r', encoding='utf-8') as file:
            for row in file:
                row2 = row.rstrip('\n').split(',')
                self.questions.append(Question(row2[0], row2[1:]))
                print(self.questions)

    def __iter__(self):
        return self

    def __next__(self):
        if self.active_index >= len(self.questions):
            raise StopIteration
        self.active_index += 1
        return self.questions[self.active_index - 1]


class Question:

    def __init__(self, sentence, answers):
        if not isinstance(answers, list):
            raise AttributeError
        self.sentence = sentence
        self.answers = answers

    def correct(self, answer):
        """
        TODO:
        Ha a bejövő válasz azonos az answers 0. elemével, adj vissza True értéket, különben False-t.
        """
        if answer == self.answers[0]:
            return True
        else:
            return False
        print('adott:',answer, '\nhelyes:',self.answers[0],'\n\n')



class QuestionFrame(ttk.Frame):

    selected = None
    question = None

    def __init__(self, master, question):
        """
        TODO:
        A kérdést tedd label-re és fűzd fel.
        A válaszokról készíts egy másolatot és keverd meg.
        A másolatok alapján készítsd el a radiobutton-öket, melynek értékét a selected tárolja el.
        """
        ttk.Frame.__init__(self, master)

        self.question = question

        self.selected = StringVar()

        # kérdés kiírása Label-re
        ttk.Label(self, text=question.sentence).pack()

        # válaszok másolása, keverése
        copy = question.answers[:]
        random.shuffle(copy)

        # radiobutton generálása
        for ans in copy:
            radio = ttk.Radiobutton(self, text=ans, value=ans, variable=self.selected)
            radio.pack(anchor=W)

    def correct(self):
        """
        TODO:
        Hívd meg a javítást metódust és eredményét return-öld
        """
        return self.question.correct(self.selected.get())


if __name__ == '__main__':
    game = Game()