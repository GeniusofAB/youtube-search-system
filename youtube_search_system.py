import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
from pytube import Search
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import AgeRestricted, TranscriptsDisabled, NoTranscriptFound
import threading
import time

texts = {
    "ru": {
        "start": "▶ Начать", "stop": "⏸ Остановить", "resume": "⏵ Продолжить", "cancel": "⏹ Завершить",
        "save": "💾 Сохранить результат", "status_done": "✅ Поиск завершён", "status_searching": "🔍 Идёт поиск...",
        "enter_phrase": "🔎 Фраза для поиска:", "enter_count": "📺 Количество видео:", "status_invalid": "❌ Введите корректные данные"
    },
    "en": {
        "start": "▶ Start", "stop": "⏸ Pause", "resume": "⏵ Resume", "cancel": "⏹ Stop",
        "save": "💾 Save Results", "status_done": "✅ Search finished", "status_searching": "🔍 Searching...",
        "enter_phrase": "🔎 Search phrase:", "enter_count": "📺 Number of videos:", "status_invalid": "❌ Enter valid inputs"
    }
}

current_language = "ru"
is_paused = False
is_stopped = False
search_thread = None
results_cache = []

def get_text(key):
    return texts[current_language].get(key, key)

def apply_theme():
    theme = theme_var.get()
    themes = {
        "light":      {"bg": "#f0f0f0", "fg": "#000000", "entry": "#ffffff"},
        "dark":       {"bg": "#2e2e2e", "fg": "#ffffff", "entry": "#3b3b3b"},
        "solarized":  {"bg": "#fdf6e3", "fg": "#657b83", "entry": "#eee8d5"},
        "dracula":    {"bg": "#282a36", "fg": "#f8f8f2", "entry": "#44475a"},
        "monokai":    {"bg": "#272822", "fg": "#f8f8f2", "entry": "#3e3d32"},
        "matrix":     {"bg": "#000000", "fg": "#00ff00", "entry": "#001100"},
        "blue":       {"bg": "#7673D9", "fg": "#534ED9", "entry": "#333086"},
    }

    color = themes.get(theme, themes["light"])
    root.configure(bg=color["bg"])

    for widget in root.winfo_children():
        apply_widget_theme(widget, color)

    result_text.configure(bg=color["entry"], fg=color["fg"], insertbackground=color["fg"])

    style = ttk.Style()
    style.theme_use("default")
    style.configure("TLabel", background=color["bg"], foreground=color["fg"])
    style.configure("TButton", background=color["bg"], foreground=color["fg"])
    style.configure("TCombobox", fieldbackground=color["entry"], background=color["bg"], foreground=color["fg"])

def apply_widget_theme(widget, color):
    try:
        wclass = widget.winfo_class()
        if wclass.startswith("T") or wclass in ("Canvas", "Scrollbar"):
            return
        if wclass in ("Label", "Button"):
            widget.configure(bg=color["bg"], fg=color["fg"])
        elif wclass == "Entry":
            widget.configure(bg=color["entry"], fg=color["fg"], insertbackground=color["fg"])
        elif wclass == "Text":
            widget.configure(bg=color["entry"], fg=color["fg"], insertbackground=color["fg"])
        elif wclass == "Frame":
            widget.configure(bg=color["bg"])
    except:
        pass

    for child in widget.winfo_children():
        apply_widget_theme(child, color)

def get_transcript(video_id):
    try:
        return YouTubeTranscriptApi.get_transcript(video_id)
    except AgeRestricted:
        return "AGE_RESTRICTED"
    except (TranscriptsDisabled, NoTranscriptFound):
        return None
    except Exception as e:
        return f"ERROR: {e}"

def start_search():
    global is_paused, is_stopped, search_thread, results_cache
    results_cache.clear()
    is_paused = False
    is_stopped = False

    phrase = entry_phrase.get().strip()
    try:
        video_count = int(entry_count.get())
    except ValueError:
        show_status(get_text("status_invalid"), "red")
        return

    if not phrase:
        show_status(get_text("status_invalid"), "red")
        return

    result_text.config(state="normal")
    result_text.delete(1.0, tk.END)
    result_text.config(state="disabled")
    progress_label.config(text="0 / 0")
    show_status(get_text("status_searching"), "blue")

    search_thread = threading.Thread(target=search_and_fetch, args=(phrase, video_count), daemon=True)
    search_thread.start()

def pause_search():
    global is_paused
    is_paused = True
    show_status("⏸ Пауза", "orange")

def resume_search():
    global is_paused
    is_paused = False
    show_status(get_text("status_searching"), "blue")

def cancel_search():
    global is_stopped
    is_stopped = True
    show_status("⛔ Поиск прерван", "red")

def search_and_fetch(phrase, count):
    global is_paused, is_stopped
    try:
        search = Search(phrase)
        results = search.results[:count]

        for idx, video in enumerate(results, 1):
            while is_paused and not is_stopped:
                time.sleep(0.3)
            if is_stopped:
                break

            video_id = video.video_id
            title = video.title
            url = f"https://www.youtube.com/watch?v={video_id}"
            transcript = get_transcript(video_id)

            text = f"[{idx}/{count}] "
            if transcript == "AGE_RESTRICTED":
                text += f"⛔ Возрастное ограничение\n{title}\n{url}"
            elif isinstance(transcript, str) and transcript.startswith("ERROR:"):
                text += f"⚠️ Ошибка\n{title}\n{url}"
            elif transcript:
                text += f"✅ Субтитры найдены\n{title}\n{url}"
            else:
                text += f"❌ Субтитров нет\n{title}\n{url}"

            results_cache.append(text)
            append_result(text + "\n" + "-" * 70 + "\n")
            progress_label.config(text=f"{idx} / {count}")

        if not is_stopped:
            show_status(get_text("status_done"), "green")
    except Exception as e:
        show_status(f"❌ Ошибка: {e}", "red")

def append_result(text):
    result_text.config(state="normal")
    result_text.insert(tk.END, text + "\n")
    result_text.see(tk.END)
    result_text.config(state="disabled")

def show_status(message, color):
    status_label.config(text=message, fg=color)

def save_to_txt():
    if not results_cache:
        show_status("⚠️ Нет результатов для сохранения", "orange")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n\n".join(results_cache))
        show_status("💾 Сохранено", "green")

def switch_language(*args):
    global current_language
    current_language = lang_var.get()
    label_phrase.config(text=get_text("enter_phrase"))
    label_count.config(text=get_text("enter_count"))
    button_start.config(text=get_text("start"))
    button_stop.config(text=get_text("stop"))
    button_resume.config(text=get_text("resume"))
    button_cancel.config(text=get_text("cancel"))
    button_save.config(text=get_text("save"))

# === GUI ===
root = tk.Tk()
root.title("🎥 Поиск субтитров YouTube")
root.geometry("800x650")
root.resizable(False, False)

theme_var = tk.StringVar(value="light")
lang_var = tk.StringVar(value="ru")
lang_var.trace("w", switch_language)

frame_top = tk.Frame(root)
frame_top.pack(pady=5)

ttk.Label(frame_top, text="🎨 Тема:").pack(side=tk.LEFT, padx=(10, 2))
theme_options = ["light", "dark", "solarized", "dracula", "monokai", "matrix", "blue"]
ttk.Combobox(frame_top, textvariable=theme_var, values=theme_options, width=10, state="readonly").pack(side=tk.LEFT)
ttk.Label(frame_top, text="🌐 Язык:").pack(side=tk.LEFT, padx=(10, 2))
ttk.Combobox(frame_top, textvariable=lang_var, values=["ru", "en"], width=5, state="readonly").pack(side=tk.LEFT)
ttk.Button(frame_top, text="Применить", command=apply_theme).pack(side=tk.LEFT, padx=10)

label_phrase = tk.Label(root, text=get_text("enter_phrase"))
label_phrase.pack()
entry_phrase = tk.Entry(root, width=50)
entry_phrase.pack()

label_count = tk.Label(root, text=get_text("enter_count"))
label_count.pack()
entry_count = tk.Entry(root, width=10)
entry_count.pack()

frame_btns = tk.Frame(root)
frame_btns.pack(pady=10)
button_start = tk.Button(frame_btns, text=get_text("start"), command=start_search, bg="#4caf50", fg="white", width=12)
button_start.pack(side=tk.LEFT, padx=5)
button_stop = tk.Button(frame_btns, text=get_text("stop"), command=pause_search, bg="#ff9800", fg="white", width=12)
button_stop.pack(side=tk.LEFT, padx=5)
button_resume = tk.Button(frame_btns, text=get_text("resume"), command=resume_search, bg="#2196f3", fg="white", width=12)
button_resume.pack(side=tk.LEFT, padx=5)
button_cancel = tk.Button(frame_btns, text=get_text("cancel"), command=cancel_search, bg="#f44336", fg="white", width=12)
button_cancel.pack(side=tk.LEFT, padx=5)

progress_label = tk.Label(root, text="0 / 0")
progress_label.pack()
result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=95, height=20, font=("Consolas", 10))
result_text.pack(padx=10, pady=10)
result_text.config(state="disabled")

frame_bottom = tk.Frame(root)
frame_bottom.pack(pady=5)
button_save = tk.Button(frame_bottom, text=get_text("save"), command=save_to_txt, width=20)
button_save.pack()

status_label = tk.Label(root, text="", font=("Segoe UI", 10, "bold"))
status_label.pack(pady=(5, 10))

apply_theme()
root.mainloop()
