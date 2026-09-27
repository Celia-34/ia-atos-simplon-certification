from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


OUT = Path("flux_donnees.png")
W, H = 2800, 1780
SCALE = 2
W *= SCALE
H *= SCALE
im = Image.new("RGB", (W, H), "#f7f8fa")
d = ImageDraw.Draw(im)

FONT_DIR = Path("C:/Windows/Fonts")
font_regular = ImageFont.truetype(str(FONT_DIR / "segoeui.ttf"), 19 * SCALE)
font_bold = ImageFont.truetype(str(FONT_DIR / "segoeuib.ttf"), 22 * SCALE)
font_title = ImageFont.truetype(str(FONT_DIR / "segoeuib.ttf"), 36 * SCALE)
font_subtitle = ImageFont.truetype(str(FONT_DIR / "segoeui.ttf"), 18 * SCALE)

COLORS = {
    "data": (232, 241, 251),
    "service": (233, 246, 236),
    "governance": (255, 244, 223),
    "optional": (242, 234, 250),
    "line": (71, 84, 103),
    "muted": (91, 103, 119),
    "border": (210, 216, 225),
}


def p(x, y):
    return int(x * SCALE), int(y * SCALE)


def text_width(text, font):
    box = d.textbbox((0, 0), text, font=font)
    return box[2] - box[0]


def wrap(text, font, max_width):
    words = text.split()
    rows, row = [], ""
    for word in words:
        candidate = f"{row} {word}".strip()
        if row and text_width(candidate, font) > max_width * SCALE:
            rows.append(row)
            row = word
        else:
            row = candidate
    if row:
        rows.append(row)
    return rows


def box(x, y, w, h, title, body, kind, small=False):
    x, y, w, h = [int(v * SCALE) for v in (x, y, w, h)]
    fill = COLORS[kind]
    outline = (71, 118, 168) if kind == "data" else (75, 138, 89)
    if kind == "governance":
        outline = (179, 131, 47)
    elif kind == "optional":
        outline = (128, 86, 166)
    d.rounded_rectangle((x, y, x + w, y + h), radius=14 * SCALE,
                        fill=fill, outline=outline, width=2 * SCALE)
    pad = 13 * SCALE
    f_title = font_regular if small else font_bold
    d.text((x + pad, y + 10 * SCALE), title, fill="#101820", font=f_title)
    lines = []
    for paragraph in body.split("\n"):
        lines.extend(wrap(paragraph, font_regular, (w - 2 * pad) / SCALE))
    d.multiline_text((x + pad, y + 40 * SCALE), "\n".join(lines),
                     fill="#263238", font=font_regular, spacing=4 * SCALE)
    return (x, y, w, h)


def group(x, y, w, h, label, accent):
    x, y, w, h = [int(v * SCALE) for v in (x, y, w, h)]
    d.rounded_rectangle((x, y, x + w, y + h), radius=20 * SCALE,
                        fill="#ffffff", outline=accent, width=3 * SCALE)
    d.rounded_rectangle((x, y, x + w, y + 45 * SCALE), radius=18 * SCALE,
                        fill=accent)
    d.rectangle((x, y + 24 * SCALE, x + w, y + 45 * SCALE), fill=accent)
    d.text((x + 18 * SCALE, y + 6 * SCALE), label, fill="#ffffff", font=font_bold)


def arrow(points, label=None, dashed=False, color=None, label_pos=None):
    color = color or COLORS["line"]
    pts = [p(*point) for point in points]
    if dashed:
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            dx, dy = x2 - x1, y2 - y1
            length = max(abs(dx), abs(dy))
            if length == 0:
                continue
            steps = max(1, length // (10 * SCALE))
            for i in range(0, steps, 2):
                a, b = i / steps, min(i + 1, steps) / steps
                d.line((int(x1 + dx * a), int(y1 + dy * a),
                        int(x1 + dx * b), int(y1 + dy * b)), fill=color,
                       width=2 * SCALE)
    else:
        d.line(pts, fill=color, width=2 * SCALE, joint="curve")
    x1, y1 = pts[-2]
    x2, y2 = pts[-1]
    import math
    angle = math.atan2(y2 - y1, x2 - x1)
    size = 10 * SCALE
    left = (x2 - size * math.cos(angle - 0.48), y2 - size * math.sin(angle - 0.48))
    right = (x2 - size * math.cos(angle + 0.48), y2 - size * math.sin(angle + 0.48))
    d.polygon([(x2, y2), left, right], fill=color)
    if label:
        lx, ly = label_pos or points[len(points) // 2]
        lines = wrap(label, font_subtitle, 310)
        tw = max(text_width(line, font_subtitle) for line in lines)
        th = len(lines) * 24 * SCALE
        cx, cy = p(lx, ly)
        d.rounded_rectangle((cx - 8 * SCALE, cy - 5 * SCALE,
                             cx + tw + 8 * SCALE, cy + th),
                            radius=5 * SCALE, fill="#f7f8fa")
        d.multiline_text((cx, cy), "\n".join(lines), fill=COLORS["muted"],
                         font=font_subtitle, spacing=2 * SCALE)


# Title and visual legend.
d.text(p(70, 34), "Flux de données — Emploi-Retour", fill="#152337", font=font_title)
d.text(p(72, 92), "Préparation et entraînement hors ligne · scoring · annotation · audit et promotion contrôlée",
       fill=COLORS["muted"], font=font_subtitle)

# Offline preparation lane.
group(55, 145, 2690, 300, "HORS LIGNE — PRÉPARATION ET ENTRAÎNEMENT", (74, 112, 159))
box(80, 220, 300, 150, "Jeu historique", "dataset_trajectoire_emploi.csv\nvariables, synthèse, classe réelle", "data")
box(430, 220, 330, 150, "Préparation", "nettoyage, anonymisation du texte,\nfamille thématique, split", "governance")
box(815, 220, 300, 150, "Entraînement", "Notebook §1-§7 / src/train.py\nfit et évaluation", "governance")
box(1170, 220, 300, 150, "Modèle retenu S1", "RandomForest · 8 features\nartefact complet", "optional")
box(1530, 220, 350, 150, "Export du modèle", "export_model_prod.py\njoblib + métadonnées JSON", "governance")
box(1960, 205, 300, 105, "Jeu de référence", "350 lignes, disjoint du trafic annoté", "data", small=True)
box(1960, 325, 300, 90, "MLflow (facultatif)", "tracking des runs hors ligne", "optional", small=True)
box(2350, 220, 330, 150, "Modèle servi", "artefact versionné chargé\nau démarrage du service", "service")
arrow([(380, 295), (430, 295)])
arrow([(760, 295), (815, 295)])
arrow([(1115, 295), (1170, 295)])
arrow([(1470, 295), (1530, 295)])
arrow([(1880, 280), (2350, 280)])
arrow([(760, 260), (785, 260), (785, 255), (1960, 255)], "partition de référence", True, label_pos=(1470, 212))
arrow([(1115, 340), (1150, 340), (1150, 370), (1960, 370)], "URI configurée", True, label_pos=(1510, 345))

# Online scoring lane.
group(55, 485, 2690, 405, "EN LIGNE — SAISIE, SCORING ET SUPERVISION", (75, 138, 89))
box(85, 590, 290, 145, "Conseiller", "saisit les 8 champs\nreçoit le score et request_id", "governance")
box(445, 590, 290, 145, "Frontend nginx", "formulaire :8088\naucun texte libre transmis", "service")
box(805, 590, 300, 145, "Backend BFF", "validation et orchestration\n:8001 · propage request_id", "service")
box(1175, 590, 300, 145, "API du modèle", "POST /predict :8000\nmodèle figé, aucune inférence", "service")
box(1545, 590, 330, 145, "Résultat", "classe, probabilité, version\ndu modèle et request_id", "data")
box(2040, 550, 260, 105, "Prometheus :9090", "métriques HTTP et métier", "service", small=True)
box(2390, 550, 260, 105, "Grafana :3001", "dashboards agrégés", "service", small=True)
box(2040, 710, 330, 125, "Service feedback :8002", "POST /feedback\nclasse réelle + request_id", "service")
box(2405, 710, 250, 125, "SQLite", "feedbacks.db\nannotations", "data")
arrow([(375, 660), (445, 660)])
arrow([(735, 660), (805, 660)])
arrow([(1105, 660), (1175, 660)])
arrow([(1475, 660), (1545, 660)])
arrow([(1545, 710), (1520, 785), (375, 785), (375, 735)], "résultat présenté au conseiller", label_pos=(850, 765))
arrow([(2600, 655), (2600, 710)], "métriques", label_pos=(2610, 665))
arrow([(2300, 603), (2390, 603)])
arrow([(375, 720), (1870, 720), (1870, 770), (2040, 770)], "annotation ultérieure · canal conseiller à raccorder", True, label_pos=(1470, 735))
arrow([(2370, 770), (2405, 770)])
arrow([(2500, 370), (2500, 465), (1325, 465), (1325, 590)], "chargement du joblib", label_pos=(1920, 458))

# Feedback, audit and retraining lane.
group(55, 930, 2690, 560, "HORS LIGNE — JOURNAL, ANNOTATIONS, AUDIT ET BOUCLE DE RETOUR", (179, 131, 47))
box(85, 1040, 390, 165, "Journal prod_scored.csv", "request_id, features, prédiction,\nprobabilité, version, horodatage\nclasse réelle connue en démo seulement", "data")
box(560, 1040, 330, 145, "Jointure feedback_store.py", "contrôle de request_id\net enrichissement des labels", "governance")
box(990, 1010, 330, 130, "Audit d'équité", "audit_equite.py\npar sous-groupes, hors ligne", "governance")
box(990, 1190, 330, 145, "Réentraînement", "retrain.py\nfeatures + labels, candidat", "governance")
box(1450, 1190, 340, 145, "Politique de promotion", "planchers · non-régression\ngain minimum", "governance")
box(1915, 1155, 310, 115, "Décision", "decisions_log.jsonl\npromotion ou rejet tracé", "data")
box(2310, 1155, 350, 135, "Artefact candidat promu", "emploi_retour_s1_1.joblib\ndistinct du modèle servi", "optional")
box(990, 1380, 330, 80, "Jeu de référence", "reste séparé du trafic", "data", small=True)
arrow([(475, 1110), (560, 1110)])
arrow([(890, 1080), (990, 1080)])
arrow([(890, 1140), (940, 1140), (940, 1260), (990, 1260)])
arrow([(1320, 1260), (1450, 1260)])
arrow([(1790, 1260), (1915, 1215)])
arrow([(2225, 1215), (2310, 1215)])
arrow([(1155, 1380), (1155, 1335)], "évaluation comparable", True, label_pos=(1170, 1350))
arrow([(475, 1170), (525, 1170), (525, 1145), (560, 1145)], "features + prediction", label_pos=(445, 1185))
arrow([(2565, 835), (2565, 900), (2700, 900), (2700, 1120), (455, 1120), (455, 1040)], "API renvoie request_id · journal temps réel à raccorder", True, label_pos=(1360, 895))
arrow([(2515, 835), (2515, 910), (875, 910), (875, 1040)], "feedbacks stockés en SQLite", True, label_pos=(1760, 915))

# Demo and governance note.
d.rounded_rectangle((80 * SCALE, 1530 * SCALE, 2720 * SCALE, 1690 * SCALE),
                    radius=14 * SCALE, fill="#fff", outline=COLORS["border"], width=2 * SCALE)
d.text(p(105, 1548), "À retenir", fill="#152337", font=font_bold)
note = (
    "Le CSV de scoring est statique dans la démo ; /predict ne le persiste pas encore. "
    "Le formulaire ne saisit pas encore les annotations.\n"
    "La nationalité hors UE est une feature et un axe d'audit J0 : finalité restreinte, jamais dans les logs ou la supervision. "
    "Aucun réentraînement ni déploiement automatique."
)
d.multiline_text(p(105, 1590), note, fill="#263238", font=font_regular,
                 spacing=6 * SCALE)

im.resize((W // SCALE, H // SCALE), Image.Resampling.LANCZOS).save(OUT)
print(OUT.resolve())
