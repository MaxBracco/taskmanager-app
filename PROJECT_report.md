# PROJECT REPORT

## Wie hat uns SCRUM geholfen?
SCRUM hat uns in diesem Projekt kaum unterstützt. Die Methodik wirkte eher wie eine zusätzliche organisatorische Belastung. Der Nutzen blieb im Vergleich zum Aufwand gering.

## Wie hat uns SCRUM behindert?
Die Einteilung der Aufgaben nach SCRUM war mit zusätzlichem Zeitaufwand verbunden. Da mehrere Teammitglieder an eigenen Versionen gearbeitet haben, war das parallele Arbeiten an derselben Datei kaum möglich. Schlussendlich wurde im Vier-Augen-Prinzip gearbeitet, um das Beste mit dem möglichen Mitteln zu erreichen.

## Wo stehen wir gerade?
Wir haben eine voll funktionsfähige Taskmanager-Webapplikation entwickelt, die unsere ursprünglichen Anforderungen deutlich übertrifft. Neben den Basisfunktionen enthält sie ein Dashboard, eine Statistikansicht und speichert alle Daten in einer separaten ` .json-Datei`. Die Anwendung ist stabil und einsatzbereit.

## Was kommt als Nächstes?
Als Nächstes werden kleinere Optimierungen vorgenommen, z. B. zur Verbesserung der Performance und Nutzerfreundlichkeit. Im Team wird außerdem besprochen, welche Funktionen noch ergänzt oder überarbeitet werden können. Der Fokus liegt nun auf Feinschliff und Qualitätssicherung.

---
```mermaid
flowchart TD
    A[Taskmanager] --> B1[Aufgabenverwaltung]
    A --> B2[Benutzeroberfläche]
    A --> B3[Synchronisierung]
    A --> B4[Datenhaltung]
    A --> B5[Statistik & Auswertung]

    B1 --> C1[Aufgabe erstellen]
    B1 --> C2[Aufgabe bearbeiten]
    B1 --> C3[Aufgabe löschen]
    B1 --> C4[Aufgaben kategorisieren]
    B1 --> C5[Priorität festlegen]
    B1 --> C6[Zeitraum definieren]
    B1 --> C7[Erinnerung setzen]

    B2 --> D1[Dashboard]
    B2 --> D2[Filter & Suche]
    B2 --> D3[Dark-/Light-Mode]
    B2 --> D4[Responsive Design]

    B3 --> E1[Geräteübergreifende Sync]
    B3 --> E2[Offline-Nutzung]
    B3 --> E3[Konfliktlösung]

    B4 --> F1[Lokale Speicherung]
    B4 --> F2[JSON-Datei]
    B4 --> F3[Backup-Funktion]

    B5 --> G1[Erledigte Aufgaben]
    B5 --> G2[Zeitaufwand]
    B5 --> G3[Aufgabenverteilung]
    B5 --> G4[Fortschrittsanzeige]

```
---

# Zwischenbilanz – Stand 10.06.2025

# Was ist in den vergangenen Sprints gut gelaufen?
Der Code hat inzwischen eine stabile und gut strukturierte Basis, was Erweiterungen erleichtert. Viele Funktionen des Taskmanagers sind bereits umgesetzt, wodurch nur noch wenige neue Anforderungen bestehen. Insgesamt verlief die Entwicklung bisher sehr erfolgreich und zielgerichtet.

# Wo stehen wir gerade & was kommt als Nächstes?
Wir verfügen über eine funktionsfähige Webapplikation mit einem umfangreichen Taskmanager. Der Fokus liegt nun auf der Umsetzung einer Synchronisationsfunktion, um Daten geräteübergreifend aktuell zu halten. Dazu werden in den nächsten Sprints verschiedene Methoden recherchiert.

# Wie hat sich die Komplexität in unserem Projekt entwickelt?
Durch die Einführung der Webapplikation ist die Komplexität gestiegen. Neue Abhängigkeiten, etwa in der `requirements.txt`, wurden eingebunden und die Systemarchitektur erweitert. Trotz dieser Herausforderungen konnten wir die Entwicklung gut kontrollieren.

# Wie gehen wir damit um?
Das Repository wächst zwar, bleibt aber durch klare Strukturierung und Dokumentation übersichtlich. Neue Funktionen werden systematisch integriert und regelmäßig überprüft. So stellen wir sicher, dass das Projekt auch bei wachsender Größe stabil und verständlich bleibt.
