from screens.screen import Screen

class WelcomeScreen(Screen):

    welcome_screen_title = ("id", "trastpay.uz:id/textViewWellCome")
    language_drop_down = ("id", "trastpay.uz:id/textViewLang")
    number_input_field = ("id", "trastpay.uz:id/textViewLang")
    language_menu_title = ("id", "trastpay.uz:id/textViewChooseLang")

    def is_welcome_screen_open(self):
        if self.is_element_exist(self.welcome_screen_title):
            return True
        return False

    def