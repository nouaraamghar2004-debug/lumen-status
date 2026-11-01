"""Génère la page de statut public/index.html à partir des données du dépôt.

Usage (depuis la racine du dépôt) :
    python status/build_page.py

Entrées : data/services.json (services et incidents) et config/flags.json
(feature flags). Sortie : public/index.html, page autonome (CSS intégré).
"""
import html
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE))

from status.sla import disponibilite, mttr, statut_service  # noqa: E402

# --- Textes de la page (ticket LUM-33 : à améliorer) -----------------------
TITRE_PAGE = "État des services numériques — Réseau Lumen"
PIED_DE_PAGE = "Un problème ? Signalez-le sur le portail du support (SUP). Page mise à jour automatiquement à chaque déploiement."

FICHIER_SERVICES = RACINE / "data" / "services.json"
FICHIER_FLAGS = RACINE / "config" / "flags.json"
DOSSIER_SORTIE = RACINE / "public"

COULEURS = {"OK": "#1E7A45", "DÉGRADÉ": "#B45309", "KO": "#B42318"}
LIBELLES = {"OK": "Opérationnel", "DÉGRADÉ": "Dégradé", "KO": "Hors objectif"}

CSS = """
*{box-sizing:border-box}
body{margin:0;font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
     background:#F5F7FA;color:#1C2430;line-height:1.5}
header{background:#1C2430;color:#fff;padding:28px 20px}
header .inner,main,footer{max-width:900px;margin:0 auto}
header h1{margin:0 0 6px;font-size:1.7rem}
header p{margin:0;color:#D9DEE5}
main{padding:20px}
.bandeau{background:#FFF4E5;border:1px solid #F6D7A7;border-left:6px solid #B45309;
         color:#7A3E00;padding:12px 16px;border-radius:8px;margin-bottom:18px;font-weight:600}
.resume{display:flex;gap:12px;flex-wrap:wrap;margin:0 0 18px}
.resume div{background:#fff;border:1px solid #D9DEE5;border-radius:8px;padding:10px 14px}
.resume b{font-size:1.3rem;display:block}
.carte{background:#fff;border:1px solid #D9DEE5;border-radius:10px;overflow-x:auto}
table{width:100%;border-collapse:collapse;min-width:560px}
th,td{padding:11px 14px;text-align:left;border-bottom:1px solid #EEF1F5}
th{font-size:.8rem;text-transform:uppercase;letter-spacing:.04em;color:#4A5565;background:#FAFBFC}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
tr:last-child td{border-bottom:0}
.pastille{display:inline-flex;align-items:center;gap:7px;font-weight:600}
.pastille::before{content:"";width:12px;height:12px;border-radius:50%;background:currentColor}
.legende{font-size:.85rem;color:#4A5565;margin-top:12px}
footer{padding:0 20px 28px;font-size:.85rem;color:#7A8494}
"""


def lire_json(chemin):
    with open(chemin, encoding="utf-8") as f:
        return json.load(f)


def nombre_fr(valeur, decimales):
    """99.803 -> '99,803' (format français)."""
    return f"{valeur:.{decimales}f}".replace(".", ",")


def calculer_services(donnees):
    """Calcule disponibilité, statut et MTTR de chaque service."""
    total = donnees["periode"]["minutes_totales"]
    resultats = []
    for s in donnees["services"]:
        indispo = sum(s["incidents"])
        dispo = disponibilite(total, indispo)
        resultats.append({
            "nom": s["nom"],
            "objectif": s["objectif"],
            "nb_incidents": len(s["incidents"]),
            "dispo": dispo,
            "statut": statut_service(dispo, s["objectif"]),
            "mttr": mttr(s["incidents"]),
        })
    return resultats


def generer_html(donnees, flags, maintenant=None):
    maintenant = maintenant or datetime.now(timezone.utc)
    services = calculer_services(donnees)
    avec_mttr = bool(flags.get("afficher_mttr", False))

    bandeau = ""
    if flags.get("bandeau_maintenance", False):
        message = flags.get("message_maintenance") or "Maintenance en cours."
        bandeau = f'<div class="bandeau">Maintenance : {html.escape(message)}</div>'

    compte = {k: sum(1 for s in services if s["statut"] == k) for k in COULEURS}
    resume = "".join(
        f'<div><b style="color:{COULEURS[k]}">{compte[k]}</b>{LIBELLES[k]}</div>'
        for k in COULEURS
    )

    entete = ("<tr><th>Service</th><th>Statut</th><th class=num>Disponibilité</th>"
              "<th class=num>Objectif</th><th class=num>Incidents</th>")
    if avec_mttr:
        entete += "<th class=num>MTTR</th>"
    entete += "</tr>"

    lignes = []
    for s in services:
        ligne = (
            f"<tr><td>{html.escape(s['nom'])}</td>"
            f'<td><span class="pastille" style="color:{COULEURS[s["statut"]]}">'
            f"{LIBELLES[s['statut']]}</span></td>"
            f"<td class=num>{nombre_fr(s['dispo'], 3)} %</td>"
            f"<td class=num>{nombre_fr(s['objectif'], 1)} %</td>"
            f"<td class=num>{s['nb_incidents']}</td>"
        )
        if avec_mttr:
            ligne += f"<td class=num>{nombre_fr(s['mttr'], 1)} min</td>"
        lignes.append(ligne + "</tr>")

    periode = html.escape(donnees["periode"]["libelle"])
    date_txt = maintenant.strftime("%d/%m/%Y à %H:%M UTC")
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(TITRE_PAGE)}</title>
<style>{CSS}</style>
</head>
<body>
<header><div class="inner">
<h1>{html.escape(TITRE_PAGE)}</h1>
<p>{html.escape(donnees["message_accueil"])}</p>
</div></header>
<main>
{bandeau}
<div class="resume">{resume}</div>
<div class="carte">
<table>
<thead>{entete}</thead>
<tbody>
{chr(10).join(lignes)}
</tbody>
</table>
</div>
<p class="legende">Période : {periode}. Disponibilité = temps sans incident / temps total.
Dégradé : moins de 0,5 point sous l'objectif. Hors objectif : au-delà.</p>
</main>
<footer>{html.escape(PIED_DE_PAGE)} Générée le {date_txt}.</footer>
</body>
</html>
"""


def main():
    donnees = lire_json(FICHIER_SERVICES)
    flags = lire_json(FICHIER_FLAGS)
    DOSSIER_SORTIE.mkdir(exist_ok=True)
    sortie = DOSSIER_SORTIE / "index.html"
    sortie.write_text(generer_html(donnees, flags), encoding="utf-8")
    print(f"Page générée : {sortie.relative_to(RACINE)} "
          f"({len(donnees['services'])} services)")


if __name__ == "__main__":
    main()
