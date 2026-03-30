import os
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction

from engine import SearchEngine
from interface import UIBuilder, Translator

class UFinder(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.home = os.path.expanduser("~")
        self.extension_dir = os.path.dirname(os.path.realpath(__file__))
        self.engine = SearchEngine(self.home)
        self.translator = Translator(self.extension_dir)

class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        query = (event.get_argument() or "").strip()
        prefs = extension.preferences
        
        try:
            val_results = prefs.get("max_results")
            max_res = int(val_results) if val_results else 9
        except:
            max_res = 9
            
        action_type = (prefs.get("action_type") or "open").lower()

        if not query:
            return RenderResultListAction([
                UIBuilder.create_item(None, extension, action_type, extension.translator, is_message=True)
            ])

        results = extension.engine.search(query, max_res)

        if not results:
            return RenderResultListAction([
                UIBuilder.create_item(None, extension, action_type, extension.translator, is_message=True, is_no_results=True)
            ])

        items = [UIBuilder.create_item(r, extension, action_type, extension.translator) for r in results]
        return RenderResultListAction(items)

if __name__ == "__main__":
    UFinder().run()
