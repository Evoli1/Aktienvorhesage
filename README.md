# Aktienvorhesage

## Chartanalyse + ML
Die Chartanalyse beinhaltet technische Indikatoren um Trends und Entwicklungen besser analysieren und auswerten zu können. Es werden folgende technische Indikatoren berücksichtigt:

**Relative Stärke Index (RSI):**
Der Relative Stärke Index ist als Indikator sehr interessant, weil er – vereinfacht ausgedrückt – die Intensität einer Kursbewegung misst. Diese wird in Relation zu den durchschnittlichen Auf- und Abwärtsbewegungen einer Vergleichsperiode gesetzt. Der RSI wird in der technischen Analyse sehr häufig eingesetzt. Hierbei schwanken seine   Ausprägungen auf einer Skala zwischen 0 und 100.
    
**Rate Of Change (ROC) / Momentum:**
Das Momentum bezeichnet in der Chartanalyse ein Konzept zur Messung der Stärke einer Kursbewegung. Dazu wird die Preisänderung innerhalb eines bestimmten Zeitraums auf verschiedene Weisen gemessen. Die Theorie dahinter: genau wie bei bewegter Masse (z.B. einem fahrenden Auto) laufen kraftvolle Kursbewegungen immer noch ein gutes Stück weiter bevor sie eine Wende einleiten.
    
**William’s Prozent Range (%R):**
Der William’s Prozent Range Indikator dient in erster Linie dazu,  überkaufte und überverkaufte Situationen anzuzeigen. Dabei ist zu beachten, dass ein Erreichen des Überkauft- bzw. Überverkauft-Bereichs nicht ein sofortiges Handeln anzeigt, da sich der Kurs noch für längere Zeit auf diesem Kurshoch oder Kurstief bewegen kann.
    
**On-Balance-Volume:**
Der On-Balance-Volume Indikator setzt Preis und Volumen eines Basiswertes zueinander in Beziehung und ermöglicht die Berechnung des kumulativen Gesamtvolumens beim Börsenhandel eines Wirtschaftsgutes oder Indexes.

**Moving Average Convergence/Divergence (MACD):**
Indikator für das Zusammen-/Auseinanderlaufen des gleitenden Durchschnitts. Die Komplexität des Indikators erfordert eine umfassende Einarbeitung und eine ständige Verfolgung der Signale des Indikators. Dann jedoch gehört er zu den verlässlichsten und treffsichersten Indikatoren für Trendentwicklungen und Trendstärken.

## News Headlines Analyse

**Vader Sentiment Analysis:**
VADER (Valence Aware Dictionary and sEntiment Reasoner) ist ein lexikon- und regelbasiertes Stimmungsanalysetool, das speziell auf Stimmungen in sozialen Medien abgestimmt ist.

VADER verwendet eine Kombination aus einem Sentiment-Lexikon. Dies ist eine Liste von lexikalischen Merkmalen (z. B. Wörtern), die im Allgemeinen entsprechend ihrer semantischen Ausrichtung entweder als positiv oder negativ gekennzeichnet werden.

Ergebnis: Die Titel werden nach negativ, positiv, neutral und compound Punkt bewertet.

"Compound" ist die Zusammensetzung von der drei anderen Punkten. Mit anderen Worten, er beschreibt die Gesamtstimmung des gesamten Textes. Falls ein Text einen positiven "compound"-Punkt hat, ist der Text eher positiv und umgekehrt.

Ein Beispiel für eine Sentiment Analysis Ergebnis: 

Top Hedge Funds are Selling These 10 Stocks------------------{'neg' : 0.0, 'neu' : 0.795, 'pos' : 0.205, 'compound' : 0.2023}

## Vorhersage Website

**Streamlit**
Öffnen Local URL: 
% streamlit hello
% streamlit run app.py

