import os, kivy, requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage

K = os.environ.get("OPENROUTER_API_KEY", "")

class AgoraApp(App):
    def build(self):
        root = BoxLayout(orientation="vertical", padding=10, spacing=10)
        root.add_widget(AsyncImage(source="https://upload.wikimedia.org/wikipedia/commons/b/bc/Socrates_Louvre.jpg", size_hint_y=None, height=200))
        self.out = Label(text="Welcome to Agora. Ask your philosophical question below:", size_hint_y=None, height=80)
        root.add_widget(self.out)
        self.inp = TextInput(text="", size_hint_y=None, height=50)
        root.add_widget(self.inp)
        btn = Button(text="Ask Socratic AI", size_hint_y=None, height=50)
        btn.bind(on_press=self.send)
        root.add_widget(btn)
        return root

    def send(self, inst):
        txt = self.inp.text
        if not txt: return
        h = {"Authorization": f"Bearer {K}", "Content-Type": "application/json"}
        b = {"model": "google/gemini-2.5-flash", "messages": [{"role": "user", "content": txt}]}
        try:
            r = requests.post("https://openrouter.ai/api/v1/chat/completions", json=b, headers=h, timeout=15)
            self.out.text = r.json()["choices"][0]["message"]["content"] if r.status_code == 200 else f"Err: {r.status_code}"
        except Exception as e:
            self.out.text = f"Err: {e}"

if __name__ == "__main__":
    AgoraApp().run()
