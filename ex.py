
from kivy.app import App
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.uix.button import Button
global age,name,pulsi,s,ir,first_15,last_15
age = 0
name = ''
pulsi = 0
first_15 = 0
last_15 = 0
class AnimatedButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        animate = Animation(pos_hint = {'y':1.1},duration = 0.5)
        animate = animate + Animation(pos_hint={'y': 0.1},duration = 0.5)
        back = Animation(pos_hint = {'y':1.1},duration = 0.5)
        self.animate = animate + back
    def start_animation(self):
        self.animate.start(self)
class Screen1(Screen):
    text1_value = NumericProperty(0)  # объявляем свойство
    text2_value = StringProperty('')
    color = '#f7f3e1'
    Window.clearcolor = color
    def clear(self):
        self.ids.text1.text = ''
    def check_age(self):
        try:
            global name,age
            age = int(self.ids.text1.text)
            name = self.ids.text2.text
        except ValueError:
            print('Пожалуйста, введите корректный возраст.')
            return
        if age < 7 or age > 16:
            print('Ваш возраст должен быть не меньше 7 и не больше 16!')
        else:
            print(f'Возраст {age} подходит.')
            self.text1_value = age
            self.manager.current = 'screen2'
class Screen2(Screen):
    color = 'f7f3e1'
    Window.clearcolor = color
    def next(self):
        try:
            global pulsi
            pulsi = int(self.ids.pulse.text)
            self.manager.current = 'screen3'
        except ValueError:
            print('Что-то пошло не так, проверьте введеные вами данные')
            self.manager.current = 'screen2'
class Screen3(Screen):
    color = 'f7f3e1'
    Window.clearcolor = color
    timer = NumericProperty(5)
    seconds_passed = NumericProperty(0)
    squats_done = NumericProperty(0)
    exercise_active = False
    def __init__(self, **kw):
        super().__init__(**kw)
        self.event = None
    def start_exercise(self):
        if not self.exercise_active:
            self.squats_done = 0
            self.seconds_passed = 0
            self.ids.status_label.text = '[color=#594712]' + 'Начинайте приседания!' + '[/color]'
            self.exercise_active = True
            self.event = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self,dt):
        self.seconds_passed += 1
        remaining_time = self.timer - self.seconds_passed
        self.ids.timer_label.text = '[color=#594712]' +  f'Время: {self.seconds_passed} / {self.timer} сек' + '[/color]'
        if remaining_time == 0:
            self.end_exercise()
    def end_exercise(self):
        if hasattr(self, 'event'):
            self.event.cancel()
        self.exercise_active = False
        if self.seconds_passed >= 45:
            self.ids.status_label.text = '[color=#594712]' + 'Задание выполнено! Молодец!'  + '[/color]'
        self.ids.squats_label.text = 'Продолжить'
    def next(self):
        if self.ids.squats_label.text == 'Продолжить':
            self.manager.current = 'screen4'
        else:
            pass
class Screen4(Screen):
    timer = NumericProperty(5)
    seconds_passed = NumericProperty(0)
    exercise_active = False

    def __init__(self, **kw):
        super().__init__(**kw)
        self.event = None

    def start(self):
        if not self.exercise_active:
            self.seconds_passed = 0
            self.ids.status_label2.text = '[color=#594712]' + 'Начинайте мерить пульс!' + '[/color]'
            self.exercise_active = True
            self.event = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        self.seconds_passed += 1
        remaining_time = self.timer - self.seconds_passed
        self.ids.timer_label2.text = '[color=#594712]' + f'Время: {self.seconds_passed} / {self.timer} сек' + '[/color]'
        if remaining_time == 45:
            self.ids.status_label2.text = '[color=#594712]' + 'Стоп, отдыхаем...'+ '[/color]'
        elif remaining_time == 15:
            self.ids.status_label2.text = '[color=#594712]' + 'Начинайте мерить пульс!'+ '[/color]'
        elif remaining_time == 0:
            self.ids.status_label2.text = '[color=#594712]' + 'Всё!'+ '[/color]'
            self.end_exercise()

    def end_exercise(self):
        if hasattr(self, 'event'):
            self.event.cancel()
        self.exercise_active = False
        if self.seconds_passed >= 45:
            self.ids.status_label2.text = '[color=#594712]' + 'Задание выполнено! Молодец!' + '[/color]'
        self.ids.btn_text.text = 'Продолжить'

    def next(self):
        if self.ids.btn_text.text == 'Продолжить':
            try:
                global last_15,first_15
                first_15 = self.ids.first_15_pulse.text
                last_15 = self.ids.last_15_pulse.text
                self.manager.current = 'screen5'
            except ValueError:
                print('Что-то пошло не так, проверьте введеные вами данные')
        else:
            pass
class Screen5(Screen):
    color = '#f7f3e1'
    Window.clearcolor = color
    def on_enter(self):
        global age, pulsi, last_15, first_15
        self.age = age
        self.s = 4 * (pulsi + float(last_15) + float(first_15))
        self.ir = (self.s - 200) / 10
    def check(self):
        if self.age == 7 or self.age ==8:
            if self.ir < 6.5:
                return 5
            elif self.ir >= 6.5:
                return 4
            elif self.ir >=12 and self.ir < 17:
                return 3
            elif self.ir >= 17 and self.ir < 21:
                return 2
            elif self.ir >= 21:
                return 1
        elif age == 9 or age ==10:
            if self.ir < 5:
                return 5
            elif self.ir >= 5 and self.ir < 10.5:
                return 4
            elif self.ir >= 10.5 and self.ir < 15.5:
                return 3
            elif self.ir >= 15.5 and self.ir < 19.5:
                return 2
            elif self.ir >= 19.5:
                return 1
        elif age == 11 or age ==12:
            if self.ir < 3.5:
                return 5
            elif self.ir >= 3.5 and self.ir < 9:
                return 4
            elif self.ir >= 9 and self.ir < 14:
                return 3
            elif self.ir >= 14 and self.ir < 18:
                return 2
            elif self.ir >= 18:
                return 1
        elif age == 13 or age ==14:
            if self.ir < 2:
                return 5
            elif self.ir >= 2 and self.ir < 7.5:
                return 4
            elif self.ir >= 7.5 and self.ir < 12.5:
                return 3
            elif self.ir >= 12.5 and self.ir < 16.5:
                return 2
            elif self.ir >= 16.5:
                return 1
        elif age == 15 or age ==16:
            if self.ir < 0.5:
                return 5
            elif self.ir >= 0.5 and self.ir < 6:
                return 4
            elif self.ir >= 6 and self.ir < 11:
                return 3
            elif self.ir >= 11 and self.ir < 15:
                return 2
            elif self.ir >= 15:
                return 1
    def res(self):
        self.ids.text_index.text = '[color=#594712]' + 'Ваш индекс Руфье:' + str(self.ir) + '[/color]'
        if self.check() == 1:
            self.ids.txt_data.text = '[color=#594712]' + 'Работоспособность сердца:низкая. Срочно обратитесь к врачу!'+ '[/color]'
        elif self.check() == 2:
            self.ids.txt_data.text = '[color=#594712]' + 'Работоспособность сердца:удовлетворительная. Обратитесь к врачу!'+ '[/color]'
        elif self.check() == 3:
            self.ids.txt_data.text = '[color=#594712]' + 'Работоспособность сердца: средняя.Возможно, стоит дополнительно обследоваться у врача.'+ '[/color]'
        elif self.check() == 4:
            self.ids.txt_data.text = '[color=#594712]' + 'Работоспособность сердца:выше среднего'+ '[/color]'
        elif self.check() == 5:
            self.ids.txt_data.text = '[color=#594712]' + 'Работоспособность сердца:высокая'+ '[/color]'
class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Screen1(name='screen1'))
        sm.add_widget(Screen2(name='screen2'))
        sm.add_widget(Screen3(name='screen3'))
        sm.add_widget(Screen4(name='screen4'))
        sm.add_widget(Screen5(name='screen5'))
        return sm
if __name__ == '__main__':
    MyApp().run()