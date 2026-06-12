#!/usr/bin/env python3
# foto_sortir_gui.py
# -*- coding: utf-8 -*-

import os
import sys
import json
import shutil
import hashlib
import threading
import traceback
import subprocess
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image
from PIL.ExifTags import TAGS

# -----------------------
# Sprachpakete
# -----------------------
LANG = {
    "Deutsch": {
        "title":            "Foto Sortierer",
        "source_label":     "Quellordner:",
        "no_folder":        "Kein Ordner gewählt",
        "btn_choose":       "Ordner wählen",
        "btn_start":        "Sortieren starten",
        "btn_preview":      "Vorschau",
        "btn_open":         "Ordner öffnen",
        "btn_undo":         "Rückgängig",
        "btn_cancel":       "Abbrechen",
        "btn_quit":         "Beenden",
        "lbl_mode":         "Aktion:",
        "mode_move":        "Verschieben",
        "mode_copy":        "Kopieren",
        "lbl_structure":    "Ordnerstruktur:",
        "struct_day":       "DD.MM.YYYY",
        "struct_ym":        "YYYY/MM",
        "struct_ymd":       "YYYY/MM/DD",
        "struct_ymon":      "YYYY/Monatsname",
        "lbl_filter":       "Dateitypen:",
        "filter_images":    "Nur Bilder",
        "filter_videos":    "Nur Videos",
        "filter_both":      "Bilder + Videos",
        "filter_all":       "Alle Dateien",
        "lbl_dupes":        "Duplikate überspringen",
        "status_ready":     "Bereit",
        "status_start":     "Starte Sortierung...",
        "status_cancel":    "Abbruch angefordert",
        "status_done":      "Fertig",
        "log_folder":       "Ordner gewählt",
        "log_start":        "Sortierung gestartet.",
        "log_cancel":       "Abbruch angefordert...",
        "log_done":         "Fertig: {moved} von {total} Dateien {action}.",
        "log_skipped":      "Kein Datum für {f} — übersprungen",
        "log_dupe":         "Duplikat übersprungen: {f}",
        "log_moved":        "{action}: {f} → {d}",
        "log_error":        "Fehler bei {f}: {e}",
        "log_undo_done":    "Rückgängig: {n} Dateien zurückverschoben.",
        "log_undo_none":    "Nichts zum Rückgängigmachen.",
        "log_undo_error":   "Fehler beim Rückgängig: {e}",
        "action_moved":     "verschoben",
        "action_copied":    "kopiert",
        "prev_title":       "Vorschau",
        "prev_no_files":    "Keine Dateien im Ordner.",
        "prev_no_date":     "kein Datum",
        "err_open":         "Ordner konnte nicht geöffnet werden: {e}",
        "err_sort":         "Fehler während der Sortierung: ",
        "months": ["Januar","Februar","März","April","Mai","Juni",
                   "Juli","August","September","Oktober","November","Dezember"],
    },
    "English": {
        "title":            "Photo Sorter",
        "source_label":     "Source folder:",
        "no_folder":        "No folder selected",
        "btn_choose":       "Choose folder",
        "btn_start":        "Start sorting",
        "btn_preview":      "Preview",
        "btn_open":         "Open folder",
        "btn_undo":         "Undo",
        "btn_cancel":       "Cancel",
        "btn_quit":         "Quit",
        "lbl_mode":         "Action:",
        "mode_move":        "Move",
        "mode_copy":        "Copy",
        "lbl_structure":    "Folder structure:",
        "struct_day":       "DD.MM.YYYY",
        "struct_ym":        "YYYY/MM",
        "struct_ymd":       "YYYY/MM/DD",
        "struct_ymon":      "YYYY/Month name",
        "lbl_filter":       "File types:",
        "filter_images":    "Images only",
        "filter_videos":    "Videos only",
        "filter_both":      "Images + Videos",
        "filter_all":       "All files",
        "lbl_dupes":        "Skip duplicates",
        "status_ready":     "Ready",
        "status_start":     "Starting sort...",
        "status_cancel":    "Cancel requested",
        "status_done":      "Done",
        "log_folder":       "Folder selected",
        "log_start":        "Sorting started.",
        "log_cancel":       "Cancel requested...",
        "log_done":         "Done: {moved} of {total} files {action}.",
        "log_skipped":      "No date for {f} — skipped",
        "log_dupe":         "Duplicate skipped: {f}",
        "log_moved":        "{action}: {f} → {d}",
        "log_error":        "Error with {f}: {e}",
        "log_undo_done":    "Undo: {n} files moved back.",
        "log_undo_none":    "Nothing to undo.",
        "log_undo_error":   "Undo error: {e}",
        "action_moved":     "moved",
        "action_copied":    "copied",
        "prev_title":       "Preview",
        "prev_no_files":    "No files in folder.",
        "prev_no_date":     "no date",
        "err_open":         "Could not open folder: {e}",
        "err_sort":         "Error during sorting: ",
        "months": ["January","February","March","April","May","June",
                   "July","August","September","October","November","December"],
    },
    "Français": {
        "title":            "Trieur de Photos",
        "source_label":     "Dossier source:",
        "no_folder":        "Aucun dossier sélectionné",
        "btn_choose":       "Choisir un dossier",
        "btn_start":        "Démarrer le tri",
        "btn_preview":      "Aperçu",
        "btn_open":         "Ouvrir le dossier",
        "btn_undo":         "Annuler l'action",
        "btn_cancel":       "Annuler",
        "btn_quit":         "Quitter",
        "lbl_mode":         "Action:",
        "mode_move":        "Déplacer",
        "mode_copy":        "Copier",
        "lbl_structure":    "Structure des dossiers:",
        "struct_day":       "JJ.MM.AAAA",
        "struct_ym":        "AAAA/MM",
        "struct_ymd":       "AAAA/MM/JJ",
        "struct_ymon":      "AAAA/Nom du mois",
        "lbl_filter":       "Types de fichiers:",
        "filter_images":    "Images uniquement",
        "filter_videos":    "Vidéos uniquement",
        "filter_both":      "Images + Vidéos",
        "filter_all":       "Tous les fichiers",
        "lbl_dupes":        "Ignorer les doublons",
        "status_ready":     "Prêt",
        "status_start":     "Tri en cours...",
        "status_cancel":    "Annulation demandée",
        "status_done":      "Terminé",
        "log_folder":       "Dossier sélectionné",
        "log_start":        "Tri démarré.",
        "log_cancel":       "Annulation demandée...",
        "log_done":         "Terminé: {moved} sur {total} fichiers {action}.",
        "log_skipped":      "Pas de date pour {f} — ignoré",
        "log_dupe":         "Doublon ignoré: {f}",
        "log_moved":        "{action}: {f} → {d}",
        "log_error":        "Erreur avec {f}: {e}",
        "log_undo_done":    "Annulation: {n} fichiers déplacés à nouveau.",
        "log_undo_none":    "Rien à annuler.",
        "log_undo_error":   "Erreur d'annulation: {e}",
        "action_moved":     "déplacés",
        "action_copied":    "copiés",
        "prev_title":       "Aperçu",
        "prev_no_files":    "Aucun fichier dans le dossier.",
        "prev_no_date":     "aucune date",
        "err_open":         "Impossible d'ouvrir le dossier: {e}",
        "err_sort":         "Erreur durant le tri: ",
        "months": ["Janvier","Février","Mars","Avril","Mai","Juin",
                   "Juillet","Août","Septembre","Octobre","Novembre","Décembre"],
    },
    "Español": {
        "title":            "Organizador de Fotos",
        "source_label":     "Carpeta de origen:",
        "no_folder":        "Ninguna carpeta seleccionada",
        "btn_choose":       "Seleccionar carpeta",
        "btn_start":        "Iniciar organización",
        "btn_preview":      "Vista previa",
        "btn_open":         "Abrir carpeta",
        "btn_undo":         "Deshacer",
        "btn_cancel":       "Cancelar",
        "btn_quit":         "Salir",
        "lbl_mode":         "Acción:",
        "mode_move":        "Mover",
        "mode_copy":        "Copiar",
        "lbl_structure":    "Estructura de carpetas:",
        "struct_day":       "DD.MM.AAAA",
        "struct_ym":        "AAAA/MM",
        "struct_ymd":       "AAAA/MM/DD",
        "struct_ymon":      "AAAA/Nombre del mes",
        "lbl_filter":       "Tipos de archivos:",
        "filter_images":    "Solo imágenes",
        "filter_videos":    "Solo videos",
        "filter_both":      "Imágenes + Videos",
        "filter_all":       "Todos los archivos",
        "lbl_dupes":        "Omitir duplicados",
        "status_ready":     "Listo",
        "status_start":     "Iniciando organización...",
        "status_cancel":    "Cancelación solicitada",
        "status_done":      "Completado",
        "log_folder":       "Carpeta seleccionada",
        "log_start":        "Organización iniciada.",
        "log_cancel":       "Cancelación solicitada...",
        "log_done":         "Listo: {moved} de {total} archivos {action}.",
        "log_skipped":      "Sin fecha para {f} — omitido",
        "log_dupe":         "Duplicado omitido: {f}",
        "log_moved":        "{action}: {f} → {d}",
        "log_error":        "Error con {f}: {e}",
        "log_undo_done":    "Deshacer: {n} archivos devueltos.",
        "log_undo_none":    "Nada que deshacer.",
        "log_undo_error":   "Error al deshacer: {e}",
        "action_moved":     "movidos",
        "action_copied":    "copiados",
        "prev_title":       "Vista previa",
        "prev_no_files":    "No hay archivos en la carpeta.",
        "prev_no_date":     "sin fecha",
        "err_open":         "No se pudo abrir la carpeta: {e}",
        "err_sort":         "Error durante la organización: ",
        "months": ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
                   "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"],
    },
    "Italiano": {
        "title":            "Riordinatore Foto",
        "source_label":     "Cartella sorgente:",
        "no_folder":        "Nessuna cartella selezionata",
        "btn_choose":       "Seleziona cartella",
        "btn_start":        "Avvia riordino",
        "btn_preview":      "Anteprima",
        "btn_open":         "Apri cartella",
        "btn_undo":         "Annulla",
        "btn_cancel":       "Annulla operazione",
        "btn_quit":         "Esci",
        "lbl_mode":         "Azione:",
        "mode_move":        "Sposta",
        "mode_copy":        "Copia",
        "lbl_structure":    "Struttura cartelle:",
        "struct_day":       "GG.MM.AAAA",
        "struct_ym":        "AAAA/MM",
        "struct_ymd":       "AAAA/MM/GG",
        "struct_ymon":      "AAAA/Nome mese",
        "lbl_filter":       "Tipi di file:",
        "filter_images":    "Solo immagini",
        "filter_videos":    "Solo video",
        "filter_both":      "Immagini + Video",
        "filter_all":       "Tutti i file",
        "lbl_dupes":        "Salta duplicati",
        "status_ready":     "Pronto",
        "status_start":     "Avvio riordino...",
        "status_cancel":    "Annullamento richiesto",
        "status_done":      "Completato",
        "log_folder":       "Cartella selezionata",
        "log_start":        "Riordino avviato.",
        "log_cancel":       "Annullamento richiesto...",
        "log_done":         "Fatto: {moved} di {total} file {action}.",
        "log_skipped":      "Nessuna data per {f} — saltato",
        "log_dupe":         "Duplicato saltato: {f}",
        "log_moved":        "{action}: {f} → {d}",
        "log_error":        "Errore con {f}: {e}",
        "log_undo_done":    "Annulla: {n} file spostati indietro.",
        "log_undo_none":    "Nulla da annullare.",
        "log_undo_error":   "Errore nell'annullamento: {e}",
        "action_moved":     "spostati",
        "action_copied":    "copiati",
        "prev_title":       "Anteprima",
        "prev_no_files":    "Nessun file nella cartella.",
        "prev_no_date":     "nessuna data",
        "err_open":         "Impossibile aprire la cartella: {e}",
        "err_sort":         "Errore durante il riordino: ",
        "months": ["Gennaio","Febbraio","Marzo","Aprile","Maggio","Giugno",
                   "Luglio","Agosto","Settembre","Ottobre","Novembre","Dicembre"],
    },
    "Nederlands": {
        "title":            "Foto Sorteerder",
        "source_label":     "Bronmap:",
        "no_folder":        "Geen map geselecteerd",
        "btn_choose":       "Map kiezen",
        "btn_start":        "Sorteren starten",
        "btn_preview":      "Voorbeeld",
        "btn_open":         "Map openen",
        "btn_undo":         "Ongedaan maken",
        "btn_cancel":       "Annuleren",
        "btn_quit":         "Afsluiten",
        "lbl_mode":         "Actie:",
        "mode_move":        "Verplaatsen",
        "mode_copy":        "Kopiëren",
        "lbl_structure":    "Mapstructuur:",
        "struct_day":       "DD.MM.YYYY",
        "struct_ym":        "YYYY/MM",
        "struct_ymd":       "YYYY/MM/DD",
        "struct_ymon":      "YYYY/Maandnaam",
        "lbl_filter":       "Bestandstypen:",
        "filter_images":    "Alleen afbeeldingen",
        "filter_videos":    "Alleen video's",
        "filter_both":      "Afbeeldingen + Video's",
        "filter_all":       "Alle bestanden",
        "lbl_dupes":        "Duplicaten overslaan",
        "status_ready":     "Gereed",
        "status_start":     "Sorteren starten...",
        "status_cancel":    "Annulering aangevraagd",
        "status_done":      "Klaar",
        "log_folder":       "Map geselecteerd",
        "log_start":        "Sorteren gestart.",
        "log_cancel":       "Annulering aangevraagd...",
        "log_done":         "Gereed: {moved} van {total} bestanden {action}.",
        "log_skipped":      "Geen datum voor {f} — overgeslagen",
        "log_dupe":         "Duplicaat overgeslagen: {f}",
        "log_moved":        "{action}: {f} → {d}",
        "log_error":        "Fout bij {f}: {e}",
        "log_undo_done":    "Ongedaan maken: {n} bestanden teruggezet.",
        "log_undo_none":    "Niets om ongedaan te maken.",
        "log_undo_error":   "Fout bij ongedaan maken: {e}",
        "action_moved":     "verplaatst",
        "action_copied":    "gekopieerd",
        "prev_title":       "Voorbeeld",
        "prev_no_files":    "Geen bestanden in de map.",
        "prev_no_date":     "geen datum",
        "err_open":         "Kon map nicht openen: {e}",
        "err_sort":         "Fout tijdens het sorteren: ",
        "months": ["Januari","Februari","Maart","April","Mei","Juni",
                   "Juli","Augustus","September","Oktober","November","December"],
    },
    "Polski": {
        "title":            "Sorter Zdjęć",
        "source_label":     "Folder źródłowy:",
        "no_folder":        "Nie wybrano folderu",
        "btn_choose":       "Wybierz folder",
        "btn_start":        "Rozpocznij sortowanie",
        "btn_preview":      "Podgląd",
        "btn_open":         "Otwórz folder",
        "btn_undo":         "Cofnij",
        "btn_cancel":       "Anuluj",
        "btn_quit":         "Zamknij",
        "lbl_mode":         "Akcja:",
        "mode_move":        "Przenieś",
        "mode_copy":        "Kopiuj",
        "lbl_structure":    "Struktura folderów:",
        "struct_day":       "DD.MM.YYYY",
        "struct_ym":        "YYYY/MM",
        "struct_ymd":       "YYYY/MM/DD",
        "struct_ymon":      "YYYY/Nazwa miesiąca",
        "lbl_filter":       "Typy plików:",
        "filter_images":    "Tylko zdjęcia",
        "filter_videos":    "Tylko filmy",
        "filter_both":      "Zdjęcia + Filmy",
        "filter_all":       "Wszystkie pliki",
        "lbl_dupes":        "Pomiń duplikaty",
        "status_ready":     "Gotowy",
        "status_start":     "Uruchamianie sortowania...",
        "status_cancel":    "Zażądano anulowania",
        "status_done":      "Zrobione",
        "log_folder":       "Wybrano folder",
        "log_start":        "Sortowanie rozpoczęte.",
        "log_cancel":       "Zażądano anulowania...",
        "log_done":         "Gotowe: {moved} z {total} plików zostało {action}.",
        "log_skipped":      "Brak daty dla {f} — pominięto",
        "log_dupe":         "Pominięto duplikat: {f}",
        "log_moved":        "{action}: {f} → {d}",
        "log_error":        "Błąd przy {f}: {e}",
        "log_undo_done":    "Cofnij: {n} plików przeniesionych z powrotem.",
        "log_undo_none":    "Nie ma nic do cofnięcia.",
        "log_undo_error":   "Błąd podczas cofania: {e}",
        "action_moved":     "przeniesionych",
        "action_copied":    "skopiowanych",
        "prev_title":       "Podgląd",
        "prev_no_files":    "Brak plików w folderze.",
        "prev_no_date":     "brak daty",
        "err_open":         "Nie można otworzyć folderu: {e}",
        "err_sort":         "Błąd podczas sortowania: ",
        "months": ["Styczeń","Luty","Marzec","Kwiecień","Maj","Czerwiec",
                   "Lipiec","Sierpień","Wrzesień","Październik","Listopad","Grudzień"],
    },
    "Türkçe": {
        "title":            "Fotoğraf Düzenleyici",
        "source_label":     "Kaynak Klasör:",
        "no_folder":        "Klasör seçilmedi",
        "btn_choose":       "Klasör Seç",
        "btn_start":        "Sıralamayı Başlat",
        "btn_preview":      "Önizleme",
        "btn_open":         "Klasörü Aç",
        "btn_undo":         "Geri Al",
        "btn_cancel":       "İptal Et",
        "btn_quit":         "Çıkış",
        "lbl_mode":         "İşlem:",
        "mode_move":        "Taşı",
        "mode_copy":        "Kopyala",
        "lbl_structure":    "Klasör Yapısı:",
        "struct_day":       "GG.AA.YYYY",
        "struct_ym":        "YYYY/AA",
        "struct_ymd":       "YYYY/AA/GG",
        "struct_ymon":      "YYYY/Ay Adı",
        "lbl_filter":       "Dosya Türleri:",
        "filter_images":    "Sadece Resimler",
        "filter_videos":    "Sadece Videolar",
        "filter_both":      "Resimler + Videolar",
        "filter_all":       "Tüm Dosyalar",
        "lbl_dupes":        "Kopyaları Atla",
        "status_ready":     "Hazır",
        "status_start":     "Sıralama başlıyor...",
        "status_cancel":    "İptal talep edildi",
        "status_done":      "Tamamlandı",
        "log_folder":       "Klasör seçildi",
        "log_start":        "Sıralama başladı.",
        "log_cancel":       "İptal talep ediliyor...",
        "log_done":         "Tamamlandı: {total} dosyadan {moved} tanesi {action}.",
        "log_skipped":      "{f} için tarih bulunamadı — atlandı",
        "log_dupe":         "Kopya dosya atlandı: {f}",
        "log_moved":        "{action}: {f} → {d}",
        "log_error":        "{f} işleminde hata: {e}",
        "log_undo_done":    "Geri Al: {n} dosya eski yerine taşındı.",
        "log_undo_none":    "Geri alınacak bir işlem yok.",
        "log_undo_error":   "Geri alma hatası: {e}",
        "action_moved":     "taşındı",
        "action_copied":    "kopyalandı",
        "prev_title":       "Önizleme",
        "prev_no_files":    "Klasörde dosya yok.",
        "prev_no_date":     "tarih yok",
        "err_open":         "Klasör açılamadı: {e}",
        "err_sort":         "Sıralama sırasında hata: ",
        "months": ["Ocak","Şubat","Mart","Nisan","Mayıs","Haziran",
                   "Temmuz","Ağustos","Eylül","Ekim","Kasım","Aralık"],
    },
    "Ελληνικά": {
        "title":            "Ταξινόμηση Φωτογραφιών",
        "source_label":     "Φάκελος προέλευσης:",
        "no_folder":        "Δεν επιλέχθηκε φάκελος",
        "btn_choose":       "Επιλογή φακέλου",
        "btn_start":        "Έναρξη ταξινόμησης",
        "btn_preview":      "Προεπισκόπηση",
        "btn_open":         "Άνοιγμα φακέλου",
        "btn_undo":         "Αναίρεση",
        "btn_cancel":       "Ακύρωση",
        "btn_quit":         "Έξοδος",
        "lbl_mode":         "Ενέργεια:",
        "mode_move":        "Μετακίνηση",
        "mode_copy":        "Αντιγραφή",
        "lbl_structure":    "Δομή φακέλων:",
        "struct_day":       "ΗΗ.ΜΜ.ΕΕΕΕ",
        "struct_ym":        "ΕΕΕΕ/ΜΜ",
        "struct_ymd":       "ΕΕΕΕ/ΜΜ/ΗΗ",
        "struct_ymon":      "ΕΕΕΕ/Όνομα μήνα",
        "lbl_filter":       "Τύποι αρχείων:",
        "filter_images":    "Μόνο εικόνες",
        "filter_videos":    "Μόνο βίντεο",
        "filter_both":      "Εικόνες + Βίντεο",
        "filter_all":       "Όλα τα αρχεία",
        "lbl_dupes":        "Παράκαμψη διπλότυπων",
        "status_ready":     "Έτοιμο",
        "status_start":     "Έναρξη ταξινόμησης...",
        "status_cancel":    "Ζητήθηκε ακύρωση",
        "status_done":      "Ολοκληρώθηκε",
        "log_folder":       "Επιλέχθηκε φάκελος",
        "log_start":        "Η ταξινόμηση ξεκίνησε.",
        "log_cancel":       "Ζητήθηκε ακύρωση...",
        "log_done":         "Έτοιμο: {moved} από {total} αρχεία {action}.",
        "log_skipped":      "Δεν βρέθηκε ημερομηνία για το αρχείο {f} — παραλείφθηκε",
        "log_dupe":         "Παραλείφθηκε το διπλότυπο: {f}",
        "log_moved":        "{action}: {f} → {d}",
        "log_error":        "Σφάλμα στο αρχείο {f}: {e}",
        "log_undo_done":    "Αναίρεση: {n} αρχεία μετακινήθηκαν πίσω.",
        "log_undo_none":    "Δεν υπάρχει ενέργεια για αναίρεση.",
        "log_undo_error":   "Σφάλμα αναίρεσης: {e}",
        "action_moved":     "μετακινήθηκαν",
        "action_copied":    "αντιγράφηκαν",
        "prev_title":       "Προεπισκόπηση",
        "prev_no_files":    "Δεν υπάρχουν αρχεία στον φάκελο.",
        "prev_no_date":     "χωρίς ημερομηνία",
        "err_open":         "Αδυναμία ανοίγματος φακέλου: {e}",
        "err_sort":         "Σφάλμα κατά την ταξινόμηση: ",
        "months": ["Ιανουάριος","Φεβρουάριος","Μάρτιος","Απρίλιος","Μάιος","Ιούνιος",
                   "Ιούλιος","Αύγουστος","Σεπτέμβριος","Οκτώβριος","Νοέμβριος","Δεκέμβριος"],
    },
      "Русский": {
        "title":            "Сортировщик Фото",
        "source_label":     "Исходная папка:",
        "no_folder":        "Папка не выбрана",
        "btn_choose":       "Выбрать папку",
        "btn_start":        "Начать сортировку",
        "btn_preview":      "Предпросмотр",
        "btn_open":         "Открыть папку",
        "btn_undo":         "Отменить",
        "btn_cancel":       "Отмена",
        "btn_quit":         "Выход",
        "lbl_mode":         "Действие:",
        "mode_move":        "Переместить",
        "mode_copy":        "Копировать",
        "lbl_structure":    "Структура папок:",
        "struct_day":       "ДД.ММ.ГГГГ",
        "struct_ym":        "ГГГГ/ММ",
        "struct_ymd":       "ГГГГ/ММ/ДД",
        "struct_ymon":      "ГГГГ/Название месяца",
        "lbl_filter":       "Типы файлов:",
        "filter_images":    "Только изображения",
        "filter_videos":    "Только видео",
        "filter_both":      "Изображения + Видео",
        "filter_all":       "Все файлы",
        "lbl_dupes":        "Пропускать дубликаты",
        "status_ready":     "Готово",
        "status_start":     "Сортировка начинается...",
        "status_cancel":    "Запрошена отмена",
        "status_done":      "Завершено",
        "log_folder":       "Папка выбрана",
        "log_start":        "Сортировка запущена.",
        "log_cancel":       "Запрос отмены...",
        "log_done":         "Готово: {moved} из {total} файлов {action}.",
        "log_skipped":      "Нет даты для {f} — пропущено",
        "log_dupe":         "Дубликат пропущен: {f}",
        "log_moved":        "{action}: {f} → {d}",
        "log_error":        "Ошибка с {f}: {e}",
        "log_undo_done":    "Отмена: {n} файлов перемещены обратно.",
        "log_undo_none":    "Нечего отменять.",
        "log_undo_error":   "Ошибка отмены: {e}",
        "action_moved":     "перемещено",
        "action_copied":    "скопировано",
        "prev_title":       "Предпросмотр",
        "prev_no_files":    "В папке нет файлов.",
        "prev_no_date":     "нет даты",
        "err_open":         "Не удалось открыть папку: {e}",
        "err_sort":         "Ошибка во время сортировки: ",
        "months": ["Январь","Февраль","Март","Апрель","Май","Июнь",
                   "Июль","Август","Сентябрь","Октябрь","Ноябрь","Декабрь"],
    },
    "Українська": {
        "title":            "Сортувальник Фото",
        "source_label":     "Вихідна папка:",
        "no_folder":        "Папку не вибрано",
        "btn_choose":       "Вибрати папку",
        "btn_start":        "Почати сортування",
        "btn_preview":      "Перегляд",
        "btn_open":         "Відкрити папку",
        "btn_undo":         "Скасувати",
        "btn_cancel":       "Скасувати",
        "btn_quit":         "Вихід",
        "lbl_mode":         "Дія:",
        "mode_move":        "Перемістити",
        "mode_copy":        "Копіювати",
        "lbl_structure":    "Структура папок:",
        "struct_day":       "ДД.ММ.РРРР",
        "struct_ym":        "РРРР/ММ",
        "struct_ymd":       "РРРР/ММ/ДД",
        "struct_ymon":      "РРРР/Назва місяця",
        "lbl_filter":       "Типи файлів:",
        "filter_images":    "Тільки зображення",
        "filter_videos":    "Тільки відео",
        "filter_both":      "Зображення + Відео",
        "filter_all":       "Всі файли",
        "lbl_dupes":        "Пропускати дублікати",
        "status_ready":     "Готово",
        "status_start":     "Сортування починається...",
        "status_cancel":    "Запит на скасування",
        "status_done":      "Завершено",
        "log_folder":       "Папку вибрано",
        "log_start":        "Сортування запущено.",
        "log_cancel":       "Запит на скасування...",
        "log_done":         "Готово: {moved} з {total} файлів {action}.",
        "log_skipped":      "Немає дати для {f} — пропущено",
        "log_dupe":         "Дублікат пропущено: {f}",
        "log_moved":        "{action}: {f} → {d}",
        "log_error":        "Помилка з {f}: {e}",
        "log_undo_done":    "Скасування: {n} файлів переміщено назад.",
        "log_undo_none":    "Нічого скасовувати.",
        "log_undo_error":   "Помилка скасування: {e}",
        "action_moved":     "переміщено",
        "action_copied":    "скопійовано",
        "prev_title":       "Перегляд",
        "prev_no_files":    "У папці немає файлів.",
        "prev_no_date":     "немає дати",
        "err_open":         "Не вдалося відкрити папку: {e}",
        "err_sort":         "Помилка під час сортування: ",
        "months": ["Січень","Лютий","Березень","Квітень","Травень","Червень",
                   "Липень","Серпень","Вересень","Жовтень","Листопад","Грудень"],
    },
    "Magyar": {
        "title":            "Fotó Rendezó",
        "source_label":     "Forrásmappa:",
        "no_folder":        "Nincs mappa kiválasztva",
        "btn_choose":       "Mappa választása",
        "btn_start":        "Rendezés indítása",
        "btn_preview":      "Előnézet",
        "btn_open":         "Mappa megnyitása",
        "btn_undo":         "Visszavonás",
        "btn_cancel":       "Mégse",
        "btn_quit":         "Bezárás",
        "lbl_mode":         "Művelet:",
        "mode_move":        "Áthelyezés",
        "mode_copy":        "Másolás",
        "lbl_structure":    "Mappaszerkezet:",
        "struct_day":       "ÉÉÉÉ.MM.DD",
        "struct_ym":        "ÉÉÉÉ/MM",
        "struct_ymd":       "ÉÉÉÉ/MM/DD",
        "struct_ymon":      "ÉÉÉÉ/Hónap neve",
        "lbl_filter":       "Fájltípusok:",
        "filter_images":    "Csak képek",
        "filter_videos":    "Csak videók",
        "filter_both":      "Képek + Videók",
        "filter_all":       "Minden fájl",
        "lbl_dupes":        "Duplikációk kihagyása",
        "status_ready":     "Kész",
        "status_start":     "Rendezés indítása...",
        "status_cancel":    "Megszakítás kérve",
        "status_done":      "Befejezve",
        "log_folder":       "Mappa kiválasztva",
        "log_start":        "Rendezés elindult.",
        "log_cancel":       "Megszakítás folyamatban...",
        "log_done":         "Kész: {moved} / {total} fájl {action}.",
        "log_skipped":      "Nincs dátum ehhez: {f} — kihagyva",
        "log_dupe":         "Duplikáció kihagyva: {f}",
        "log_moved":        "{action}: {f} → {d}",
        "log_error":        "Hiba ennél: {f}: {e}",
        "log_undo_done":    "Visszavonás: {n} fájl visszahelyezve.",
        "log_undo_none":    "Nincs mit visszavonni.",
        "log_undo_error":   "Hiba a visszavonáskor: {e}",
        "action_moved":     "áthelyezve",
        "action_copied":    "másolva",
        "prev_title":       "Előnézet",
        "prev_no_files":    "Nincsenek fájlok a mappában.",
        "prev_no_date":     "nincs dátum",
        "err_open":         "Mappa nem nyitható meg: {e}",
        "err_sort":         "Hiba a rendezés során: ",
        "months": ["Január","Február","Március","Április","Május","Június",
                   "Július","Augusztus","Szeptember","Október","November","December"],
    },
  
}

# Unterstützte Dateitypen
IMAGE_EXTS = {".jpg",".jpeg",".png",".gif",".bmp",".tiff",".tif",".webp",
              ".heic",".heif",".raw",".cr2",".cr3",".nef",".arw",".dng",
              ".orf",".rw2",".pef",".srw"}
VIDEO_EXTS = {".mp4",".mov",".avi",".mkv",".wmv",".flv",".m4v",".3gp",
              ".mts",".m2ts",".ts",".webm",".mpg",".mpeg"}

# -----------------------
# Einstellungen
# -----------------------
def _settings_path():
    if sys.platform == "win32":
        base = os.environ.get("APPDATA", os.path.expanduser("~"))
    elif sys.platform == "darwin":
        base = os.path.join(os.path.expanduser("~"), "Library", "Application Support")
    else:
        base = os.environ.get("XDG_CONFIG_HOME",
               os.path.join(os.path.expanduser("~"), ".config"))
    folder = os.path.join(base, "FotoSortierer")
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, "settings.json")

def load_settings():
    defaults = {
        "lang":       "Deutsch",
        "last_folder": "",
        "mode":       "move",
        "structure":  "day",
        "filter":     "images",
        "skip_dupes": True,
    }
    try:
        p = _settings_path()
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
            for k in defaults:
                if k in data:
                    defaults[k] = data[k]
    except Exception:
        pass
    return defaults

def save_settings(s):
    try:
        with open(_settings_path(), "w", encoding="utf-8") as f:
            json.dump(s, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

# -----------------------
# Hilfsfunktionen
# -----------------------
def get_exif_datetimeoriginal(file_path):
    try:
        img = Image.open(file_path)
        exif = img._getexif()
        if not exif:
            return None
        for tag, val in exif.items():
            if TAGS.get(tag, tag) == "DateTimeOriginal":
                return val
    except Exception:
        return None

def get_file_date(file_path):
    """Gibt datetime zurück oder None."""
    exif_dt = get_exif_datetimeoriginal(file_path)
    if exif_dt:
        try:
            return datetime.strptime(exif_dt, "%Y:%m:%d %H:%M:%S")
        except Exception:
            pass
    try:
        return datetime.fromtimestamp(os.path.getctime(file_path))
    except Exception:
        return None

def date_to_folder(dt, structure, months):
    """Gibt relativen Ordnerpfad zurück."""
    if structure == "day":
        return dt.strftime("%d.%m.%Y")
    elif structure == "ym":
        return os.path.join(str(dt.year), f"{dt.month:02d}")
    elif structure == "ymd":
        return os.path.join(str(dt.year), f"{dt.month:02d}", f"{dt.day:02d}")
    elif structure == "ymon":
        return os.path.join(str(dt.year), months[dt.month - 1])
    return dt.strftime("%d.%m.%Y")

def file_hash(path):
    """SHA256-Hash der kompletten Datei — zuverlässige Duplikat-Erkennung."""
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            while True:
                chunk = f.read(131072)  # 128KB Blöcke
                if not chunk:
                    break
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None

def unique_target_path(target_dir, filename):
    base, ext = os.path.splitext(filename)
    candidate = os.path.join(target_dir, filename)
    i = 1
    while os.path.exists(candidate):
        candidate = os.path.join(target_dir, f"{base} ({i}){ext}")
        i += 1
    return candidate

def remove_empty_dirs(root_folder):
    for dirpath, _, _ in os.walk(root_folder, topdown=False):
        if dirpath == root_folder:
            continue
        try:
            if not os.listdir(dirpath):
                os.rmdir(dirpath)
        except Exception:
            pass

def get_allowed_exts(filter_key):
    if filter_key == "images": return IMAGE_EXTS
    if filter_key == "videos": return VIDEO_EXTS
    if filter_key == "both":   return IMAGE_EXTS | VIDEO_EXTS
    return None  # None = alle

# -----------------------
# Sortierlogik
# -----------------------
def sort_photos(source_folder, mode="move", structure="day", filter_key="images",
                skip_dupes=True, months=None, progress_callback=None, stop_event=None):
    if months is None:
        months = LANG["Deutsch"]["months"]

    allowed = get_allowed_exts(filter_key)
    try:
        entries = [f for f in os.listdir(source_folder)
                   if os.path.isfile(os.path.join(source_folder, f))
                   and (allowed is None or
                        os.path.splitext(f)[1].lower() in allowed)]
    except Exception as e:
        raise RuntimeError(f"Fehler beim Lesen des Ordners: {e}")

    total   = len(entries)
    moved   = 0
    undo_log = []          # [(ziel, quelle), ...] für Rückgängig
    seen_hashes = set()    # Duplikat-Erkennung

    for idx, filename in enumerate(entries, start=1):
        if stop_event and stop_event.is_set():
            break

        file_path = os.path.join(source_folder, filename)

        # Duplikat-Check
        if skip_dupes:
            h = file_hash(file_path)
            if h and h in seen_hashes:
                if progress_callback:
                    progress_callback(idx, total, ("dupe", filename))
                continue
            if h:
                seen_hashes.add(h)

        try:
            dt = get_file_date(file_path)
            if not dt:
                if progress_callback:
                    progress_callback(idx, total, ("skip", filename))
                continue

            rel_folder   = date_to_folder(dt, structure, months)
            target_dir   = os.path.join(source_folder, rel_folder)
            target_path  = unique_target_path(target_dir, filename)
            os.makedirs(target_dir, exist_ok=True)

            if mode == "move":
                shutil.move(file_path, target_path)
            else:
                shutil.copy2(file_path, target_path)

            undo_log.append((target_path, file_path))
            moved += 1
            if progress_callback:
                progress_callback(idx, total, ("ok", filename, rel_folder))

        except Exception as e:
            if progress_callback:
                progress_callback(idx, total, ("error", filename, str(e)))

    try:
        remove_empty_dirs(source_folder)
    except Exception:
        pass

    return moved, total, undo_log

def undo_sort(undo_log):
    """Verschiebt alle Dateien aus dem undo_log zurück."""
    n = 0
    for target_path, orig_path in reversed(undo_log):
        try:
            if os.path.exists(target_path):
                os.makedirs(os.path.dirname(orig_path), exist_ok=True)
                shutil.move(target_path, orig_path)
                n += 1
        except Exception:
            pass
    return n

# -----------------------
# GUI
# -----------------------
class PhotoSorterGUI:
    def __init__(self, root):
        self.root = root
        self.cfg  = load_settings()
        self.L    = LANG[self.cfg["lang"]]

        self.source_folder = self.cfg.get("last_folder", "")
        self.worker_thread = None
        self.stop_event    = None
        self.last_undo_log = []

        self._build_ui()
        self._apply_lang()

        if self.source_folder and os.path.isdir(self.source_folder):
            self.folder_label.config(text=self.source_folder, foreground="black")
            self._set_buttons_ready(True)

    # ------ UI aufbauen ------
    def _build_ui(self):
        self.root.resizable(True, True)
        self.root.minsize(700, 480)

        # Menüleiste für Sprache
        menubar = tk.Menu(self.root)
        self.lang_menu = tk.Menu(menubar, tearoff=0)
        for lk in LANG:
            self.lang_menu.add_command(label=lk,
                command=lambda k=lk: self._switch_lang(k))
        menubar.add_cascade(label="Language", menu=self.lang_menu)
        self.root.config(menu=menubar)

        frm = ttk.Frame(self.root, padding=12)
        frm.pack(fill="both", expand=True)

        # Ordnerwahl
        row0 = ttk.Frame(frm)
        row0.pack(fill="x", pady=4)
        self.lbl_source = ttk.Label(row0, text="")
        self.lbl_source.pack(side="left")
        self.folder_label = ttk.Label(row0, text="", foreground="gray")
        self.folder_label.pack(side="left", padx=8)
        self.btn_choose = ttk.Button(row0, command=self.choose_folder)
        self.btn_choose.pack(side="right")

        # Optionen-Zeile 1: Aktion + Struktur
        row1 = ttk.Frame(frm)
        row1.pack(fill="x", pady=4)
        self.lbl_mode = ttk.Label(row1, text="")
        self.lbl_mode.pack(side="left")
        self.mode_var = tk.StringVar(value=self.cfg["mode"])
        self.rb_move = ttk.Radiobutton(row1, variable=self.mode_var, value="move")
        self.rb_move.pack(side="left", padx=4)
        self.rb_copy = ttk.Radiobutton(row1, variable=self.mode_var, value="copy")
        self.rb_copy.pack(side="left", padx=4)

        ttk.Separator(row1, orient="vertical").pack(side="left", fill="y", padx=10)

        self.lbl_struct = ttk.Label(row1, text="")
        self.lbl_struct.pack(side="left")
        self.struct_var = tk.StringVar(value=self.cfg["structure"])
        self.struct_cb  = ttk.Combobox(row1, textvariable=self.struct_var,
                                        state="readonly")
        self.struct_cb.pack(side="left", padx=4)

        # Optionen-Zeile 2: Filter + Duplikate
        row2 = ttk.Frame(frm)
        row2.pack(fill="x", pady=4)
        self.lbl_filter = ttk.Label(row2, text="")
        self.lbl_filter.pack(side="left")
        self.filter_var = tk.StringVar(value=self.cfg["filter"])
        self.filter_cb  = ttk.Combobox(row2, textvariable=self.filter_var,
                                        state="readonly")
        self.filter_cb.pack(side="left", padx=4)

        ttk.Separator(row2, orient="vertical").pack(side="left", fill="y", padx=10)
        self.dupe_var = tk.BooleanVar(value=self.cfg["skip_dupes"])
        self.chk_dupes = ttk.Checkbutton(row2, variable=self.dupe_var)
        self.chk_dupes.pack(side="left")
        self.lbl_dupes = ttk.Label(row2, text="")
        self.lbl_dupes.pack(side="left", padx=4)

        # Buttons
        btn_row = ttk.Frame(frm)
        btn_row.pack(fill="x", pady=6)
        self.btn_start   = ttk.Button(btn_row, command=self.start_sorting,   state="disabled")
        self.btn_preview = ttk.Button(btn_row, command=self.preview_list,    state="disabled")
        self.btn_open    = ttk.Button(btn_row, command=self.open_folder,     state="disabled")
        self.btn_undo    = ttk.Button(btn_row, command=self.undo_last,       state="disabled")
        self.btn_cancel  = ttk.Button(btn_row, command=self.cancel_sorting,  state="disabled")
        self.btn_quit    = ttk.Button(btn_row, command=self._quit)
        for b in (self.btn_start, self.btn_preview, self.btn_open,
                  self.btn_undo, self.btn_cancel):
            b.pack(side="left", padx=3)
        self.btn_quit.pack(side="right", padx=3)

        # Fortschritt
        self.progress = ttk.Progressbar(frm, orient="horizontal", mode="determinate")
        self.progress.pack(fill="x", pady=6)
        self.status_label = ttk.Label(frm, text="")
        self.status_label.pack(anchor="w")

        # Statistik
        self.stat_label = ttk.Label(frm, text="", foreground="#555")
        self.stat_label.pack(anchor="w")

        # Log
        log_frm = ttk.Frame(frm)
        log_frm.pack(fill="both", expand=True, pady=(6, 0))
        self.log = tk.Text(log_frm, height=10, wrap="word", state="disabled")
        sb = ttk.Scrollbar(log_frm, command=self.log.yview)
        self.log.configure(yscrollcommand=sb.set)
        self.log.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

    def _apply_lang(self):
        L = self.L
        self.root.title(L["title"])
        self.lbl_source.config(text=L["source_label"])
        if not self.source_folder:
            self.folder_label.config(text=L["no_folder"])
        self.btn_choose.config(text=L["btn_choose"])
        self.lbl_mode.config(text=L["lbl_mode"])
        self.rb_move.config(text=L["mode_move"])
        self.rb_copy.config(text=L["mode_copy"])
        self.lbl_struct.config(text=L["lbl_structure"])
        structs = [L["struct_day"], L["struct_ym"], L["struct_ymd"], L["struct_ymon"]]
        struct_w = max(len(s) for s in structs) + 2
        self.struct_cb.config(values=structs, width=struct_w)
        keys = ["day", "ym", "ymd", "ymon"]
        cur = self.cfg.get("structure", "day")
        self.struct_cb.current(keys.index(cur) if cur in keys else 0)

        self.lbl_filter.config(text=L["lbl_filter"])
        filters = [L["filter_images"], L["filter_videos"],
                   L["filter_both"], L["filter_all"]]
        filter_w = max(len(s) for s in filters) + 2
        self.filter_cb.config(values=filters, width=filter_w)
        fkeys = ["images", "videos", "both", "all"]
        cur_f = self.cfg.get("filter", "images")
        self.filter_cb.current(fkeys.index(cur_f) if cur_f in fkeys else 0)

        self.lbl_dupes.config(text=L["lbl_dupes"])
        self.btn_start.config(text=L["btn_start"])
        self.btn_preview.config(text=L["btn_preview"])
        self.btn_open.config(text=L["btn_open"])
        self.btn_undo.config(text=L["btn_undo"])
        self.btn_cancel.config(text=L["btn_cancel"])
        self.btn_quit.config(text=L["btn_quit"])
        self.status_label.config(text=L["status_ready"])

    def _switch_lang(self, lang_key):
        self.cfg["lang"] = lang_key
        self.L = LANG[lang_key]
        self._apply_lang()
        save_settings(self.cfg)

    def _get_current_settings(self):
        """Liest aktuelle Werte aus den Widgets."""
        struct_map = {
            self.L["struct_day"]:  "day",
            self.L["struct_ym"]:   "ym",
            self.L["struct_ymd"]:  "ymd",
            self.L["struct_ymon"]: "ymon",
        }
        filter_map = {
            self.L["filter_images"]: "images",
            self.L["filter_videos"]: "videos",
            self.L["filter_both"]:   "both",
            self.L["filter_all"]:    "all",
        }
        return {
            "mode":       self.mode_var.get(),
            "structure":  struct_map.get(self.struct_var.get(), "day"),
            "filter":     filter_map.get(self.filter_var.get(), "images"),
            "skip_dupes": self.dupe_var.get(),
        }

    # ------ Hilfsmethoden ------
    def log_message(self, msg):
        self.log.configure(state="normal")
        self.log.insert("end", msg + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def _set_buttons_ready(self, ready):
        s = "normal" if ready else "disabled"
        self.btn_start.config(state=s)
        self.btn_preview.config(state=s)
        self.btn_open.config(state=s)

    def _quit(self):
        self._save_current_settings()
        self.root.quit()

    def _save_current_settings(self):
        s = self._get_current_settings()
        self.cfg.update(s)
        self.cfg["last_folder"] = self.source_folder
        save_settings(self.cfg)

    # ------ Aktionen ------
    def choose_folder(self):
        folder = filedialog.askdirectory(title=self.L["btn_choose"])
        if folder:
            self.source_folder = folder
            self.folder_label.config(text=folder, foreground="black")
            self._set_buttons_ready(True)
            self.log_message(f"{self.L['log_folder']}: {folder}")
            self.status_label.config(text=self.L["status_ready"])
            self._save_current_settings()

    def open_folder(self):
        if not self.source_folder:
            return
        try:
            if sys.platform == "win32":
                os.startfile(self.source_folder)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", self.source_folder])
            else:
                subprocess.Popen(["xdg-open", self.source_folder])
        except Exception as e:
            messagebox.showerror("Fehler", self.L["err_open"].format(e=e))

    def preview_list(self):
        if not self.source_folder:
            return
        s = self._get_current_settings()
        allowed = get_allowed_exts(s["filter"])
        files = [f for f in os.listdir(self.source_folder)
                 if os.path.isfile(os.path.join(self.source_folder, f))
                 and (allowed is None or
                      os.path.splitext(f)[1].lower() in allowed)]
        if not files:
            messagebox.showinfo(self.L["prev_title"], self.L["prev_no_files"])
            return
        win = tk.Toplevel(self.root)
        win.title(self.L["prev_title"])
        win.geometry("750x450")
        txt = tk.Text(win, wrap="none")
        sb_v = ttk.Scrollbar(win, orient="vertical",   command=txt.yview)
        sb_h = ttk.Scrollbar(win, orient="horizontal", command=txt.xview)
        txt.configure(yscrollcommand=sb_v.set, xscrollcommand=sb_h.set)
        sb_v.pack(side="right",  fill="y")
        sb_h.pack(side="bottom", fill="x")
        txt.pack(fill="both", expand=True)

        lines = []
        for f in sorted(files):
            path = os.path.join(self.source_folder, f)
            dt   = get_file_date(path)
            if dt:
                folder = date_to_folder(dt, s["structure"], self.L["months"])
            else:
                folder = self.L["prev_no_date"]
            lines.append(f"{f:<50}  →  {folder}")

        txt.insert("1.0", "\n".join(lines))
        txt.configure(state="disabled")

        # Statistik im Vorschaufenster
        dated   = sum(1 for l in lines if "→" in l and
                      self.L["prev_no_date"] not in l)
        undated = len(lines) - dated
        ttk.Label(win, text=f"  {dated} mit Datum, {undated} ohne  ",
                  foreground="#555").pack(side="bottom", anchor="w")

    def start_sorting(self):
        if not self.source_folder:
            return
        if self.worker_thread and self.worker_thread.is_alive():
            return
        self._save_current_settings()
        s = self._get_current_settings()

        self.stop_event = threading.Event()
        self.last_undo_log = []
        self.progress["value"] = 0
        self.stat_label.config(text="")
        self.status_label.config(text=self.L["status_start"])
        self.log_message(self.L["log_start"])
        self.btn_start.config(state="disabled")
        self.btn_preview.config(state="disabled")
        self.btn_undo.config(state="disabled")
        self.btn_cancel.config(state="normal")

        L = self.L

        def progress_cb(current, total, info):
            try:
                pct = int((current / total) * 100) if total else 0
                self.progress["value"] = pct
                kind = info[0]
                if kind == "ok":
                    _, fname, folder = info
                    action = L["action_moved"] if s["mode"] == "move" else L["action_copied"]
                    msg = L["log_moved"].format(action=action, f=fname, d=folder)
                elif kind == "skip":
                    msg = L["log_skipped"].format(f=info[1])
                elif kind == "dupe":
                    msg = L["log_dupe"].format(f=info[1])
                else:
                    msg = L["log_error"].format(f=info[1], e=info[2])
                self.status_label.config(text=f"{current}/{total}: {msg}")
                self.log_message(msg)
            except Exception:
                pass

        def worker():
            try:
                moved, total, undo_log = sort_photos(
                    self.source_folder,
                    mode=s["mode"],
                    structure=s["structure"],
                    filter_key=s["filter"],
                    skip_dupes=s["skip_dupes"],
                    months=L["months"],
                    progress_callback=progress_cb,
                    stop_event=self.stop_event,
                )
                self.last_undo_log = undo_log
                action = L["action_moved"] if s["mode"] == "move" else L["action_copied"]
                done_msg = L["log_done"].format(moved=moved, total=total, action=action)
                self.log_message(done_msg)
                self.status_label.config(text=L["status_done"])
                self.stat_label.config(
                    text=f"✔ {moved}/{total}  |  "
                         f"{len(set(date_to_folder(get_file_date(os.path.join(self.source_folder,f)) or datetime.now(), s['structure'], L['months']) for _,f in [(0,os.path.basename(t)) for t,_ in undo_log]))} Ordner erstellt"
                )
                if undo_log:
                    self.btn_undo.config(state="normal")
            except Exception as e:
                self.log_message(L["err_sort"] + str(e))
                traceback.print_exc()
            finally:
                self.btn_start.config(state="normal")
                self.btn_preview.config(state="normal")
                self.btn_cancel.config(state="disabled")
                self.progress["value"] = 100

        self.worker_thread = threading.Thread(target=worker, daemon=True)
        self.worker_thread.start()

    def cancel_sorting(self):
        if self.stop_event:
            self.stop_event.set()
            self.log_message(self.L["log_cancel"])
            self.status_label.config(text=self.L["status_cancel"])

    def undo_last(self):
        if not self.last_undo_log:
            self.log_message(self.L["log_undo_none"])
            return
        try:
            n = undo_sort(self.last_undo_log)
            remove_empty_dirs(self.source_folder)
            self.last_undo_log = []
            self.btn_undo.config(state="disabled")
            msg = self.L["log_undo_done"].format(n=n)
            self.log_message(msg)
            self.status_label.config(text=msg)
            self.stat_label.config(text="")
        except Exception as e:
            self.log_message(self.L["log_undo_error"].format(e=e))

# -----------------------
# Start
# -----------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoSorterGUI(root)
    root.mainloop()
