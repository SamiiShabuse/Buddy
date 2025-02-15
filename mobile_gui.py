from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
import webbrowser
import platform

class MyApp(App):
    def build(self):
        self.counter = 0

        # Create a label to display messages
        self.label = Label(
            text="Hello! Click the button.",
            size_hint=(0.3, 0.1),
        )

        # Button to change the label text
        click_button = Button(
            text="Click Me",
            size_hint=(0.3, 0.1),
        )
        click_button.bind(on_press=self.change_text)

        # Button to open the Microsoft Authenticator download page
        auth_button = Button(
            text="Open Authenticator",
            size_hint=(0.3, 0.1),
        )
        auth_button.bind(on_press=self.open_authenticator)

        # Layout to organize widgets vertically
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        layout.add_widget(self.label)
        layout.add_widget(click_button)
        layout.add_widget(auth_button)

        return layout

    def change_text(self, instance):
        """Update the label text with the number of button clicks."""
        self.counter += 1
        self.label.text = f"You clicked the button {self.counter} times!"

    def open_authenticator(self, instance):
        """Open the Microsoft Authenticator download page based on the platform."""
        user_platform = platform.system()
        if user_platform == 'Android':
            # Open Google Play Store page for Microsoft Authenticator
            webbrowser.open("https://play.google.com/store/apps/details?id=com.azure.authenticator")
        elif user_platform == 'iOS':
            # Open App Store page for Microsoft Authenticator
            webbrowser.open("https://apps.apple.com/app/microsoft-authenticator/id983156458")
        else:
            # For other platforms, open the Microsoft Authenticator setup page
            webbrowser.open("https://support.microsoft.com/en-us/account-billing/how-to-use-the-microsoft-authenticator-app-9783c865-0308-42fb-a519-8cf3131762d2")

if __name__ == "__main__":
    MyApp().run()
