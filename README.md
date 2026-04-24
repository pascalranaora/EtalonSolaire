---
# L'Étalon Solaire : Coût Thermodynamique du Satoshi

Ce dépôt héberge un outil de modélisation en Python permettant de calculer la **pression exergétique réelle** du réseau Bitcoin. Contrairement aux analyses financières classiques basées sur le prix (fiat), ce modèle évalue la valeur d'un Satoshi en fonction de l'effort physique total fourni par la biosphère, mesuré en **emjoules solaires (sej)**.

Ce projet s'inscrit dans le cadre des recherches sur l'économie biophysique et le concept de **"The Sun Standard"** (L'Étalon Solaire), popularisé dans l'ouvrage *[Homo Biodiversitas](https://github.com/pascalranaora/HomoBiodiversitas)*.

## 🔬 Contexte Théorique

Le modèle repose sur les travaux d'**Howard T. Odum** et son concept d'**émergie** (énergie incorporée). L'idée est de quantifier la "mémoire énergétique" nécessaire pour produire une unité d'information inaltérable sur la blockchain. 

Le script convertit le travail brut du réseau (Hashrate) en flux d'émergie en utilisant la **transformité** du réseau électrique mondial, révélant ainsi le coût thermodynamique objectif derrière la preuve de travail (Proof of Work).

## 🚀 Fonctionnalités

- **Extraction Automatisée :** Récupération du Hashrate historique via l'API TradingView (`tvDatafeed`).
- **Modélisation des Halvings :** Intégration des sauts de phase thermodynamiques lors des divisions de la subvention de bloc.
- **Analyse Exergétique :** Calcul du coût en emjoules solaires (sej) par Satoshi.
- **Visualisation :** Génération de graphiques en échelle logarithmique pour observer l'évolution de l'étalon solaire.

## 🛠️ Installation

```bash
# Cloner le dépôt
git clone https://github.com/votre-username/etalon-solaire.git
cd etalon-solaire

# Installer les dépendances
pip install tvDatafeed pandas numpy matplotlib

# Lancer le script depuis un terminal
python satoshi_emergy.py
```

## 📊 Méthodologie de Calcul

La valeur thermodynamique ($C_{sej}$) est calculée selon la formule :

$$C_{sej} = \frac{H_t \times E_t \times Tr_e}{\left(\frac{B_t \times 10^8}{600}\right)}$$

Où :
- **$H_t$** : Taux de hachage (Hash/s).
- **$E_t$** : Efficacité énergétique du matériel (J/Hash).
- **$Tr_e$** : Transformité électrique (sej/J).
- **$B_t$** : Subvention de bloc (BTC).

## ⚠️ Simplifications Actuelles & Appel à Contributions

Ce modèle est une version initiale et comporte des simplifications qui ne demandent qu'à être affinées par la communauté :

1. **Efficacité Matérielle ($E_t$) :** Actuellement basée sur une courbe de décroissance exponentielle théorique. Une intégration directe des données du *Cambridge Bitcoin Electricity Consumption Index (CBECI)* permettrait une précision accrue.
2. **Transformité Électrique ($Tr_e$) :** Utilise une moyenne mondiale constante. Le modèle pourrait être complexifié en intégrant l'évolution du mix énergétique mondial (données IEA/EIA).
3. **Frais de Transaction :** Pour l'instant, seule la subvention de bloc est utilisée. L'inclusion des *fees* permettrait de calculer la valeur totale sécurisée par le réseau.

**Vous avez une suggestion ?** Les Pull Requests sont les bienvenues pour paufiner ces variables ou proposer de nouvelles visualisations (ex: ratio EMR dynamique).

## 📜 Licence

Ce projet est sous licence MIT. Libre à vous de l'utiliser, de le modifier et de le partager pour faire avancer la compréhension de la thermodynamique des systèmes décentralisés.

---
<img width="1536" height="2752" alt="Gemini_Generated_Image_8jo9ke8jo9ke8jo9" src="https://github.com/user-attachments/assets/f6526a09-ad5c-40a0-9187-2ec1c4b69e91" />
---

*Développé dans le cadre des travaux de l'Information Physics Institute.*

<img width="1400" height="700" alt="Figure_1" src="https://github.com/user-attachments/assets/c39e1dff-91f1-4f2e-90b0-126a855eefbf" />
