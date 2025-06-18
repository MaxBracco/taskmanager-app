# PROJECT REPORT
---
# Project Review 01

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
    A[Taskmanager] --> B1[Aufgaben verwalten]
    A --> B2[Dashboard]
    A --> B3[Berichte & Analyse]
    A --> B4[Einstellungen]

    B1 --> C1[erstellen/bearbeiteb/löschen]
    B1 --> C2[Priorität]
    B1 --> C3[Zeitraum]
    B1 --> C4[Status]

    B2 --> D1[Übersicht]
    B2 --> D2[Diagramme]

    B3 --> E1[Verteilung]
    B3 --> E2[Nutzung]
    B3 --> E3[Anteile]

    B4 --> F1[Import]
    B4 --> F2[Export]
    B4 --> F3[Aufgaben löschen]

```
---

# Projekt Review 02

## Was ist in den vergangenen Sprints gut gelaufen?
Der Code hat inzwischen eine stabile und gut strukturierte Basis, was Erweiterungen erleichtert. Viele Funktionen des Taskmanagers sind bereits umgesetzt, wodurch nur noch wenige neue Anforderungen bestehen. Insgesamt verlief die Entwicklung bisher sehr erfolgreich und zielgerichtet.

## Wo stehen wir gerade & was kommt als Nächstes?
Wir verfügen über eine funktionsfähige Webapplikation mit einem umfangreichen Taskmanager. Der Fokus liegt nun auf der Umsetzung einer Synchronisationsfunktion, um Daten geräteübergreifend aktuell zu halten. Dazu werden in den nächsten Sprints verschiedene Methoden recherchiert.

## Wie hat sich die Komplexität in unserem Projekt entwickelt?
Durch die Einführung der Webapplikation ist die Komplexität gestiegen. Neue Abhängigkeiten, etwa in der `requirements.txt`, wurden eingebunden und die Systemarchitektur erweitert. Trotz dieser Herausforderungen konnten wir die Entwicklung gut kontrollieren.

## Wie gehen wir damit um?
Das Repository wächst zwar, bleibt aber durch klare Strukturierung und Dokumentation übersichtlich. Neue Funktionen werden systematisch integriert und regelmäßig überprüft. So stellen wir sicher, dass das Projekt auch bei wachsender Größe stabil und verständlich bleibt.

---
# Produkt Review

## Welche User-Stories haben wir erfolgreich umgesetzt?

- Beschreibungen zu Tasks hinzufügen
- Nach Prioritäten sortieren
- Fälligkeitsdatum hinzufügen
- Tasks bearbeiten
- Tasks löschen
- Tasks anlegen
- Tasks abschließen


## Welche User-Stories mussten wir zurückstellen, oder konnten wir nicht umsetzen?

- An Task erinnert werden
- Synchronisierung
- Listen erstellen **(stattdessen wurden Tags eingeführt)**

## Wie sieht unsere App am Ende der Projektlaufzeit aus?

![image](https://github.com/user-attachments/assets/1e248d2c-6a46-4418-be95-1d60cb9927e7)

In unserer App kann man jetzt bequem zwischen verschiedenen Bereichen wechseln: Dashboard, Aufgabenverwaltung, Bericht & Analyse sowie Einstellungen.

- Dashboard: Bietet eine Übersicht über alle Aufgaben inklusive Anzahl, Status, Statistiken und detaillierten Informationen.
- Aufgabenverwaltung: Hier können neue Aufgaben detailliert hinzugefügt und nach verschiedenen Kriterien gefiltert werden.
- Bericht & Analyse: Stellt eine Auswertung der Aufgaben in übersichtlicher Form dar.
- Einstellungen: Ermöglicht das Löschen aller Aufgaben, den Export der Aufgaben als ´.json´-Datei sowie den Import einer vorhandenen ´.json´-Datei.

## Wie gut passt unser Finales Produkt zu der eingangs formulierten Produkt Vision?

Die ursprüngliche Vision orientierte sich stark an einem klassischen Task-Manager. Im Verlauf des Projekts wurde die App jedoch stetig weiterentwickelt und um zahlreiche Funktionen erweitert. So kamen unter anderem verschiedene Auswertungsmöglichkeiten sowie die Synchronisierung über eine `.json`-Datei hinzu.

Letztlich bietet unser finales Produkt deutlich mehr Funktionalität, als ursprünglich in der Produktvision vorgesehen war.

---

# Die Web-Applikation

https://taskmanager-app.streamlit.app/

# Das Github Repository

https://github.com/MaxBracco/taskmanager-app
](https://github.com/MaxBracco/taskmanager-app)
