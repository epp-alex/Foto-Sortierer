# 📷 Foto Sortierer

A cross-platform desktop tool that automatically sorts photos and videos into date-based folders.  
Built with Python and Tkinter — no internet connection required, works entirely offline.

---

## 📥 Download & Run (No Python needed)

| Platform | File | Instructions |
|----------|------|--------------|
| 🪟 Windows | `Foto_Sortierer.exe` | Download and double-click to run |
| 🍎 macOS | `Foto_Sortierer.app` | Open the `.app` bundle — right-click → Open if blocked by Gatekeeper |
| 🐧 Linux | `Foto_Sortierer` (binary) | `chmod +x Foto_Sortierer && ./Foto_Sortierer` |

> **Linux note:** If the app doesn't start, make it executable first:
> ```bash
> chmod +x Foto_Sortierer
> ./Foto_Sortierer
> ```

---

## 🎯 What it does

Select a folder full of unsorted photos and videos — the app reads the **EXIF date** from each file (or falls back to the file creation date) and moves or copies them into automatically created subfolders by date.

**Before:**
```
📁 Photos/
   IMG_0001.jpg
   IMG_0002.jpg
   VID_2024.mp4
   DSC_9981.NEF
```

**After (YYYY/Month name):**
```
📁 Photos/
   📁 2024/
      📁 June/
         IMG_0001.jpg
         IMG_0002.jpg
         VID_2024.mp4
      📁 March/
         DSC_9981.NEF
```

---

## ✨ Features

- **EXIF date reading** — uses the original capture date from photo metadata, not the file modification date
- **4 folder structures** — choose how subfolders are named and organized
- **Move or Copy** — keep originals untouched by choosing Copy mode
- **Duplicate detection** — skips files with identical content (MD5 hash) so nothing is imported twice
- **Undo** — one click to reverse the last sort operation completely
- **Preview** — see exactly where each file will go before sorting starts
- **Cancel** — stop a running sort at any time
- **File type filter** — sort only images, only videos, both, or all files
- **Persistent settings** — last folder, mode, structure and filter are remembered on next launch
- **12 languages** — switchable from the menu at any time

---

## 📁 Folder Structures

| Option | Example result |
|--------|----------------|
| `DD.MM.YYYY` | `15.06.2024/` |
| `YYYY/MM` | `2024/06/` |
| `YYYY/MM/DD` | `2024/06/15/` |
| `YYYY/Month name` | `2024/June/` (language-aware) |

---

## 🖼️ Supported File Formats

**Images:** JPG, JPEG, PNG, GIF, BMP, TIFF, WEBP, HEIC, HEIF, RAW, CR2, CR3, NEF, ARW, DNG, ORF, RW2, PEF, SRW

**Videos:** MP4, MOV, AVI, MKV, WMV, FLV, M4V, 3GP, MTS, M2TS, TS, WEBM, MPG, MPEG

---

## 🌍 Languages

Switch language at any time from the **Sprache / Language** menu — saved automatically.

| | | | |
|---|---|---|---|
| 🇩🇪 Deutsch | 🇬🇧 English | 🇫🇷 Français | 🇪🇸 Español |
| 🇮🇹 Italiano | 🇳🇱 Nederlands | 🇵🇱 Polski | 🇹🇷 Türkçe |
| 🇬🇷 Ελληνικά | 🇷🇺 Русский | 🇺🇦 Українська | 🇭🇺 Magyar |

Month names in folder names are always in the selected language (e.g. `2024/Juni` in German, `2024/June` in English).

### Adding a new language

Open `Foto_Sortiren.py` and add a new entry to the `LANG` dictionary — the menu entry appears automatically:

```python
"Svenska": {
    "title":         "Fotosorterare",
    "source_label":  "Källmapp:",
    "no_folder":     "Ingen mapp vald",
    "btn_choose":    "Välj mapp",
    "btn_start":     "Starta sortering",
    "btn_preview":   "Förhandsgranskning",
    "btn_open":      "Öppna mapp",
    "btn_undo":      "Ångra",
    "btn_cancel":    "Avbryt",
    "btn_quit":      "Avsluta",
    "lbl_mode":      "Åtgärd:",
    "mode_move":     "Flytta",
    "mode_copy":     "Kopiera",
    "lbl_structure": "Mappstruktur:",
    "struct_day":    "DD.MM.ÅÅÅÅ",
    "struct_ym":     "ÅÅÅÅ/MM",
    "struct_ymd":    "ÅÅÅÅ/MM/DD",
    "struct_ymon":   "ÅÅÅÅ/Månadsnamn",
    "lbl_filter":    "Filtyper:",
    "filter_images": "Endast bilder",
    "filter_videos": "Endast video",
    "filter_both":   "Bilder + Video",
    "filter_all":    "Alla filer",
    "lbl_dupes":     "Hoppa över dubbletter",
    "status_ready":  "Redo",
    "status_start":  "Startar sortering...",
    "status_cancel": "Avbrott begärt",
    "status_done":   "Klar",
    "log_folder":    "Mapp vald",
    "log_start":     "Sortering startad.",
    "log_cancel":    "Avbrott begärt...",
    "log_done":      "Klart: {moved} av {total} filer {action}.",
    "log_skipped":   "Inget datum för {f} — hoppades över",
    "log_dupe":      "Dubblett hoppades över: {f}",
    "log_moved":     "{action}: {f} → {d}",
    "log_error":     "Fel med {f}: {e}",
    "log_undo_done": "Ångra: {n} filer återställda.",
    "log_undo_none": "Inget att ångra.",
    "log_undo_error":"Fel vid ångra: {e}",
    "action_moved":  "flyttade",
    "action_copied": "kopierade",
    "prev_title":    "Förhandsgranskning",
    "prev_no_files": "Inga filer i mappen.",
    "prev_no_date":  "inget datum",
    "err_open":      "Kunde inte öppna mappen: {e}",
    "err_sort":      "Fel under sortering: ",
    "months": ["Januari","Februari","Mars","April","Maj","Juni",
               "Juli","Augusti","September","Oktober","November","December"],
},
```

---

## ⚙️ Settings storage

Settings (last folder, language, mode, structure, filter, duplicate option) are saved automatically:

| Platform | Path |
|----------|------|
| Windows | `%APPDATA%\FotoSortierer\settings.json` |
| macOS | `~/Library/Application Support/FotoSortierer/settings.json` |
| Linux | `~/.config/FotoSortierer/settings.json` |

---

## 🐍 Run from Source

**Requirements:** Python 3.8+ and Pillow

```bash
pip install Pillow
python Foto_Sortiren.py
```

---

## 📄 License

MIT License — free to use, modify and distribute.
