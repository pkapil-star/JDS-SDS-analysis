import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D

outdir = sys.argv[1]

BLUE = "#2C5F8A"
BLUE_LIGHT = "#DCE8F2"
ORANGE = "#E07B39"
ORANGE_LIGHT = "#FBE6D6"
GRAY = "#5A5A5A"
GRAY_LIGHT = "#EDEDED"

def box(ax, x, y, w, h, text, fc, ec, fontsize=9.5, weight="normal", textcolor="#1A1A1A"):
    r = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.06",
                        linewidth=1.3, edgecolor=ec, facecolor=fc)
    ax.add_patch(r)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fontsize,
            color=textcolor, weight=weight, wrap=True)

def arrow(ax, p1, p2, color=GRAY, style="-|>", lw=1.6, connectionstyle="arc3,rad=0.0"):
    a = FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=14, color=color,
                         linewidth=lw, connectionstyle=connectionstyle)
    ax.add_patch(a)

# =====================================================================
# Diagram 1: Analytics Methodology / Workflow
# =====================================================================
fig, ax = plt.subplots(figsize=(10.2, 6.0))
ax.set_xlim(0, 10.2)
ax.set_ylim(0, 6.0)
ax.axis("off")

steps = [
    ("1. Business\nUnderstanding &\nAnalytics Objective", 0.3, "Define the problem,\nscope & success criteria"),
    ("2. Data Collection\n& Inventory", 0.3, "4 source files;\ndata dictionary review"),
    ("3. Data Exploration\n& Preparation", 0.3, "Cleaning, derivation,\nreduction, quality checks"),
    ("4. Data Analysis\n(Descriptive →\nDiagnostic → Predictive)", 0.3, "EDA, correlation,\nclassification models"),
    ("5. Results\nValidation", 0.3, "Metrics, cross-checks,\nstakeholder review"),
    ("6. Conclusions &\nImplications", 0.3, "Insights, recommendations,\nlimitations"),
]

n = len(steps)
box_w, box_h = 1.42, 1.15
gap = (10.2 - n * box_w) / (n + 1)
y_box = 3.55
xs = []
for i, (label, _, sub) in enumerate(steps):
    x = gap + i * (box_w + gap)
    xs.append(x)
    box(ax, x, y_box, box_w, box_h, label, BLUE_LIGHT, BLUE, fontsize=8.3, weight="bold")
    ax.text(x + box_w / 2, y_box - 0.42, sub, ha="center", va="top", fontsize=7.2, color=GRAY, style="italic")

for i in range(n - 1):
    arrow(ax, (xs[i] + box_w, y_box + box_h / 2), (xs[i + 1], y_box + box_h / 2), color=BLUE, lw=1.8)

# feedback loop arrow
arrow(ax, (xs[-1] + box_w / 2, y_box + box_h + 0.02), (xs[0] + box_w / 2, y_box + box_h + 0.02),
      color=ORANGE, lw=1.4, connectionstyle="arc3,rad=-0.35")
ax.text(5.1, 5.35, "Iterative refinement of objective & scope as findings emerge",
        ha="center", fontsize=7.6, color=ORANGE, style="italic")

# Tooling lane
tool_y = 1.35
ax.text(0.3, tool_y + 0.95, "Tooling", fontsize=9, weight="bold", color="#1A1A1A")
box(ax, 0.3, tool_y, 4.55, 0.75,
    "Python (pandas, scikit-learn, matplotlib)\nUsed for steps 2–5: cleaning, EDA, statistics, modelling",
    ORANGE_LIGHT, ORANGE, fontsize=8)
box(ax, 5.1, tool_y, 4.8, 0.75,
    "SAS Viya for Learners (VFL)\nVisual Analytics → reporting layer | Model Studio → modelling layer",
    GRAY_LIGHT, GRAY, fontsize=8)
arrow(ax, (2.5, tool_y + 0.75), (2.5, y_box - 0.55), color="#999999", lw=1.0, style="-")
arrow(ax, (7.5, tool_y + 0.75), (7.5, y_box - 0.55), color="#999999", lw=1.0, style="-")

ax.set_title("Exhibit A — Analytics Methodology and Workflow", fontsize=12.5, weight="bold", pad=14)
plt.tight_layout()
plt.savefig(f"{outdir}/diagram_methodology.png", dpi=170)
plt.close()

# =====================================================================
# Diagram 2: Conceptual Data Relationship Map
# =====================================================================
fig, ax = plt.subplots(figsize=(10.0, 6.4))
ax.set_xlim(0, 10.0)
ax.set_ylim(0, 6.4)
ax.axis("off")

box(ax, 0.4, 4.6, 3.6, 1.0, "Data Science Jobs\n(1,602 postings · company, title,\nexperience, salary)", BLUE_LIGHT, BLUE, fontsize=8.6)
box(ax, 0.4, 3.2, 3.6, 1.0, "Analytics Jobs\n(15,841 postings · designation,\nskills, location, salary band)", BLUE_LIGHT, BLUE, fontsize=8.6)
box(ax, 6.0, 4.6, 3.6, 1.0, "JDS Skill Traits\n(139 junior data scientists ·\ntechnical skill scores, salary hike)", ORANGE_LIGHT, ORANGE, fontsize=8.6)
box(ax, 6.0, 3.2, 3.6, 1.0, "SDS Personality Traits\n(161 senior data scientists ·\nBig-Five traits, success outcome)", ORANGE_LIGHT, ORANGE, fontsize=8.6)

ax.text(2.2, 5.75, "EXTERNAL MARKET SIGNALS", ha="center", fontsize=8.6, weight="bold", color=BLUE)
ax.text(7.8, 5.75, "INTERNAL TALENT SIGNALS", ha="center", fontsize=8.6, weight="bold", color=ORANGE)

box(ax, 2.6, 1.55, 4.8, 1.0, "Integrated Workforce – Market\nAnalytics Layer\n(cleaned, joined at the skill / role concept level)",
    "#EAF1E8", "#4C7A4A", fontsize=8.8, weight="bold")

arrow(ax, (2.2, 4.6), (4.0, 2.65), color=BLUE, connectionstyle="arc3,rad=0.15")
arrow(ax, (2.2, 3.2), (4.2, 2.35), color=BLUE, connectionstyle="arc3,rad=-0.1")
arrow(ax, (7.8, 4.6), (6.2, 2.65), color=ORANGE, connectionstyle="arc3,rad=-0.15")
arrow(ax, (7.8, 3.2), (6.0, 2.35), color=ORANGE, connectionstyle="arc3,rad=0.1")

box(ax, 0.4, 0.2, 2.8, 0.9, "Descriptive dashboards\n(market pay & demand)", GRAY_LIGHT, GRAY, fontsize=8)
box(ax, 3.6, 0.2, 2.8, 0.9, "Predictive models\n(hike / success drivers)", GRAY_LIGHT, GRAY, fontsize=8)
box(ax, 6.8, 0.2, 2.8, 0.9, "Strategic recommendations\n(talent & L&D actions)", GRAY_LIGHT, GRAY, fontsize=8)

arrow(ax, (1.8, 1.55), (1.8, 1.1), color="#4C7A4A")
arrow(ax, (5.0, 1.55), (5.0, 1.1), color="#4C7A4A")
arrow(ax, (8.2, 1.55), (8.2, 1.1), color="#4C7A4A")

ax.set_title("Exhibit B — Conceptual Relationship Across the Four Datasets", fontsize=12.5, weight="bold", pad=14)
plt.tight_layout()
plt.savefig(f"{outdir}/diagram_data_map.png", dpi=170)
plt.close()

print("done")
