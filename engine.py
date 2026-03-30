import os
import json
import time
from threading import Thread
from interface import normalize

CACHE_FILE = os.path.expanduser("~/.cache/ufinder_index.json")

class SearchEngine:
    def __init__(self, home_path):
        self.home = home_path
        self.index = self.load_cache()
        Thread(target=self.index_loop, daemon=True).start()

    def load_cache(self):
        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE, 'r') as f:
                    data = json.load(f)
                    return data if isinstance(data, list) else []
            except:
                return []
        return []

    def index_loop(self):
        while True:
            self.build_index()
            time.sleep(2)  # 🔥 Near real-time update

    def build_index(self):
        new_index = []
        ignore = {'.cache', '.git', 'node_modules', '.local', '.mozilla', '.npm', 'snap', 'venv'}

        try:
            for root, dirs, files in os.walk(self.home, topdown=True):
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ignore]

                for name in dirs + files:
                    if name.startswith('.'):
                        continue

                    path = os.path.join(root, name)

                    try:
                        if not os.access(path, os.R_OK):
                            continue

                        st = os.stat(path)

                        new_index.append({
                            "norm": normalize(name),
                            "path": path,
                            "is_dir": os.path.isdir(path),
                            "mtime": st.st_mtime
                        })
                    except:
                        continue

                if len(new_index) > 100000:
                    break
        except:
            pass

        self.index = sorted(new_index, key=lambda x: x.get('mtime', 0), reverse=True)
        self.save_cache()

    def save_cache(self):
        try:
            temp_cache = CACHE_FILE + ".tmp"
            with open(temp_cache, 'w') as f:
                json.dump(self.index, f)
            os.replace(temp_cache, CACHE_FILE)
        except:
            pass

    def search(self, query, max_results):
        clean_query = normalize(query)
        scored = []
        current_index = list(self.index)

        for item in current_index:
            if item['norm'].startswith(clean_query):
                score = 0
            elif clean_query in item['norm']:
                score = 1
            else:
                continue

            scored.append((score, item))

            if len(scored) > 500:
                break

        scored.sort(key=lambda x: (x[0], -x[1].get('mtime', 0)))
        return [r[1] for r in scored[:max_results]]
