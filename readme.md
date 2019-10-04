Fragen
--
- Karten nachladen 
    - Wie finden wir Überschneidungen mit den anderen Kacheln?
    - Wie berücksichtigen wir diese Überschneidungen in unserem Datenmodell?
 - Sollen wir neben base32 auch andere Geocode-Systeme im GeohashWrapper unterstützen?
 - Wie können wir unsere Performance testen?
 - Wie bauen wir unsere Konfiguration auf?
    - API Key
 - Wie können wir den Cache entlasten:
    - Welche Informationen sind nicht essentiell?
    
 - OSM-Ids können sich mit der Zeit ändern. Wir das für uns zu einem Problem?

TODO
--
-  Bugfix und Refactor von loadTile():
    - Performance
    - Einbahnstraßen
    - Abbiegeverbote    
- Refactor GeohashWrapper
- Links um folgenden Informationen ergänzen:
    - vom wem darf ein Link verwendet werden (Radfahrer, Autos, Fußgänger, ...)?
    - in welcher Richtung darf ein Link verwendet werden?
        - auch wieder in Abhängigkeit von der Rolle (Radfahrer, ...)


Ideen
--
- Die Logik aus der REST-API in eine extra API schreiben, sodass die REST-API lesbarer wird.
- Datenmodell um zusätzliche Informationen ergänzen, sodass Ergebnisse im FrontEnd leichter zu verstehen sind:
    - Angeben in welchem Land ein Tile bzw. eine Bounding Box liegt
- FrontEnd ergänzen um:
    - nur die Grenzen eines Tiles anzeigen
 - von einem Tile, die benachbarten Tiles erhalten
 - eine Methode mit der beliebige Polygone geladen werden können
 - mehrere Threads um parallel mehrere Tiles zu laden
 - schauen, ob man auch Wanderwege ausfindig machen kann

