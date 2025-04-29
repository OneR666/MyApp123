from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from database import Database
from combination_generator import CombinationGenerator


class RootWidget(BoxLayout):
    m_input = ObjectProperty(None)
    n_input = ObjectProperty(None)
    k_input = ObjectProperty(None)
    j_input = ObjectProperty(None)
    s_input = ObjectProperty(None)
    sample_input = ObjectProperty(None)
    results_table = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.generator = CombinationGenerator()

    def start_generation(self):
        try:
            m = int(self.m_input.text)
            n = int(self.n_input.text)
            k = int(self.k_input.text)
            j = int(self.j_input.text)
            s = int(self.s_input.text)
            samples_text = self.sample_input.text.strip()
            if samples_text:
                samples = [int(x.strip()) for x in samples_text.split(',')]
                if len(samples) != n:
                    raise ValueError(f"Number of samples must be {n}")
            else:
                samples = self.generator.generate_random_samples(m, n)

            combos = self.generator.generate_combinations(samples, k, j, s)
            base_name = f"{m}-{n}-{k}-{j}-{s}-1-{len(combos)}"
            self.db.save_combinations(base_name, combos)
            self.update_ui_with_results(combos)
        except Exception as e:
            print(f"Error: {e}")

    def load_from_db(self):
        print("Load from DB not implemented in Kivy version.")

    def delete_results(self):
        print("Delete results not implemented in Kivy version.")

    def update_ui_with_results(self, combos):
        self.results_table.clear_widgets()
        self.results_table.cols = len(combos[0]) if combos else 1
        for row in combos:
            for val in row:
                from kivy.uix.label import Label
                self.results_table.add_widget(Label(text=str(val)))


class OptimalSampleSelectionApp(App):
    def build(self):
        return Builder.load_file("main.kv")
