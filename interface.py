import os
import unicodedata
import json
import locale
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction
from ulauncher.api.shared.action.OpenAction import OpenAction

class Translator:
    def __init__(self, extension_dir):
        self.translations = {}
        try:
            # Detecta o idioma do sistema (ex: pt_BR -> pt)
            sys_lang = locale.getdefaultlocale()[0][:2]
        except:
            sys_lang = "en"
            
        lang_path = os.path.join(extension_dir, "translations", f"{sys_lang}.json")
        default_path = os.path.join(extension_dir, "translations", "en.json")
        
        path_to_load = lang_path if os.path.exists(lang_path) else default_path
        
        try:
            with open(path_to_load, 'r', encoding='utf-8') as f:
                self.translations = json.load(f)
        except:
            self.translations = {}

    def get(self, key, default=""):
        return self.translations.get(key, default)

def normalize(text):
    if not text:
        return ""
    return "".join(
        c for c in unicodedata.normalize("NFKD", text)
        if unicodedata.category(c) != "Mn"
    ).lower()

def is_system_folder(path):
    home = os.path.expanduser("~")
    name = os.path.basename(path)
    norm = normalize(name)
    return norm in [
        "desktop", "area de trabalho", "documents", "documentos", "downloads",
        "music", "musica", "musicas", "pictures", "imagens", "videos",
        "public", "publico", "templates", "modelos"
    ] and os.path.dirname(os.path.normpath(path)) == os.path.normpath(home)

def get_system_description(path, translator):
    name = normalize(os.path.basename(path))
    mapping = {
        "desktop": "desc_desktop", "area de trabalho": "desc_desktop",
        "documents": "desc_documents", "documentos": "desc_documents",
        "downloads": "desc_downloads",
        "pictures": "desc_pictures", "imagens": "desc_pictures",
        "templates": "desc_templates", "modelos": "desc_templates",
        "music": "desc_music", "musica": "desc_music", "musicas": "desc_music",
        "public": "desc_public", "publico": "desc_public",
        "videos": "desc_videos",
    }
    key = mapping.get(name)
    return translator.get(key) if key else ""

def get_file_info(path, is_dir, extension_dir):
    img_dir = os.path.join(extension_dir, "images")
    if is_dir:
        home = os.path.expanduser("~")
        name = normalize(os.path.basename(path))
        system_folders = {
            "desktop": "desktop.png", "area de trabalho": "desktop.png",
            "documents": "folder-documents.png", "documentos": "folder-documents.png",
            "downloads": "folder-download.png", "music": "folder-music.png",
            "musica": "folder-music.png", "musicas": "folder-music.png",
            "pictures": "folder-pictures.png", "imagens": "folder-pictures.png",
            "videos": "folder-video.png", "public": "folder-publicshare.png",
            "publico": "folder-publicshare.png", "templates": "folder-templates.png",
            "modelos": "folder-templates.png",
        }
        icon_file = system_folders.get(name, "folder.png") if os.path.dirname(os.path.normpath(path)) == os.path.normpath(home) else "folder.png"
        return os.path.join(img_dir, icon_file)

    ext = os.path.splitext(path)[1].lower()
    if ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
        return path

    mapping = {
        '.doc': 'document.png', '.docx': 'document.png', '.odt': 'document.png',
        '.txt': 'text.png', '.log': 'text.png', '.pdf': 'pdf.png',
        '.xls': 'spreadsheet.png', '.xlsx': 'spreadsheet.png', '.csv': 'spreadsheet.png',
        '.ppt': 'presentation.png', '.pptx': 'presentation.png',
        '.zip': 'archive.png', '.rar': 'archive.png', '.tar': 'archive.png', '.gz': 'archive.png',
        '.mp4': 'video.png', '.mkv': 'video.png', '.avi': 'video.png', '.mov': 'video.png', '.webm': 'video.png',
        '.mp3': 'music.png', '.wav': 'music.png', '.flac': 'music.png', '.m4a': 'music.png', '.ogg': 'music.png',
    }
    return os.path.join(img_dir, mapping.get(ext, "file.png"))

class UIBuilder:
    @staticmethod
    def create_item(data, extension, action_type, translator, is_message=False, is_no_results=False):
        if is_message:
            name_msg = translator.get("no_results_title") if is_no_results else translator.get("home_title")
            desc_msg = translator.get("no_results_desc") if is_no_results else translator.get("home_desc")
            return ExtensionResultItem(
                icon=os.path.join(extension.extension_dir, "images", "icon.png"),
                name=name_msg,
                description=desc_msg,
                on_enter=DoNothingAction()
            )

        path = data['path']
        is_dir = data['is_dir']
        icon_path = get_file_info(path, is_dir, extension.extension_dir)
        home = os.path.expanduser("~")

        if is_dir:
            description = get_system_description(path, translator) if is_system_folder(path) else os.path.relpath(path, home)
        else:
            description = os.path.dirname(os.path.relpath(path, home))

        final_path = path if action_type == "open" or is_dir else os.path.dirname(path)
        
        if not (os.path.exists(icon_path) or icon_path == path):
            icon_path = os.path.join(extension.extension_dir, "images", "file.png")

        return ExtensionResultItem(
            icon=icon_path,
            name=os.path.basename(path),
            description=description,
            on_enter=OpenAction(final_path)
        )
