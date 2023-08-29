# Protokoll Repository GI HSG

[![Vorstandssitzung pipeline status](https://git.cs.uni-paderborn.de/gi-hsg/protokolle/badges/main/pipeline.svg?key_text=Vorstandssitzungen&key_width=120&job=build-vorstandssitzung)](https://git.cs.uni-paderborn.de/gi-hsg/protokolle/-/jobs/artifacts/main/browse?job=build-vorstandssitzung)

[![Mitgliederversammlung pipeline status](https://git.cs.uni-paderborn.de/gi-hsg/protokolle/badges/main/pipeline.svg?key_text=Mitgliederversammlungen&key_width=150&job=build-mitgliederversammlung)](https://git.cs.uni-paderborn.de/gi-hsg/protokolle/-/jobs/artifacts/main/browse?job=build-mitgliederversammlung)

Dieses Repository enthält die Protokolle der Vorstandssitzungen und Mitgliederversammlungen der GI Hochschulgruppe.

## Struktur

Die Protokolle sind in Markdown geschrieben und befinden sich in den Ordnern `Vorstandssitzungen` und `Mitgliederversammlungen`. Die Dateinamen sind nach dem Schema `YYYY-MM-DD.md` benannt.

## Vorlage

Die Vorlage für die Protokolle ist in den Dateien `Vortstandssitzungen/protokollvorlage.md` und `Mitgliederversammlungen/protokollvorlage.md` zu finden. Die Vorlage enthält bereits die notwendigen Strukturen und Formatierungen. Die Vorlage ist in Markdown geschrieben und kann mit jedem Texteditor bearbeitet werden.

## Protokollierende Person

Der protokollierende Person ist für die Erstellung des Protokolls verantwortlich.

Dafür muss er/sie folgende Schritte durchführen:

* Protokollvorlage kopieren und umbenennen
* YAML Frontmatter ausfüllen (der Teil zwischen den `---`)
* Protokoll schreiben

Das Feld `published` sollte auf `false` gesetzt werden, bis das Protokoll fertig ist. Nachdem es reviewed wurde kann es auf `true` gesetzt werden. Dann wird es automatisch auf der Website veröffentlicht.

Es gibt einige Formatierungsregeln, die eingehalten werden müssen:

* Überschriften müssen von Leerzeilen umgeben sein
* Die Datei muss mit **einer** Leerzeile enden
* Das Frontmatter muss mit sinnvollen Werten ausgefüllt werden

Das wird durch die CI überprüft. Wenn die CI fehlschlägt kann das Protokoll nicht veröffentlicht werden.
Um lokal die Formatierung zu überprüfen kann der Linter mit `python3 linter.py` ausgeführt werden. Vor dem ersten Ausführen müssen die Abhängigkeiten mit `pip3 install -r requirements.txt` installiert werden (es ist empfohlen ein virtuelles Python Environment zu verwenden)

## Commit

Das Protokoll wird als Markdown-Datei in das Repository eingecheckt. Der Commit-Message sollte nach dem Schema `Protokoll <Typ> <Datum in ISO 8601>` benannt werden. Der Typ ist entweder `Vorstandssitzung` oder `Mitgliederversammlung`. Das Datum ist das Datum der Sitzung.
