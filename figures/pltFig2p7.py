import numpy as np
import plotly.graph_objects as go

FONT = "Times New Roman, Times, serif"
FONT_SIZE = 14
FIG_NANE = "fig2p7_refractivity_profiles"
Ns = 313.0 # Refractivity at the surface [N units]
a = 6374.0 # The radius of the Earth at latitudes 22-25 deg. [km]
num_samples = 1000
h = np.linspace(0, 28, num_samples) # [km]

def refractivity_to_index(N):
    return 1.0 + 1e-6 * N

def index_to_refractivity(n_idx):
    return 1e6 * (n_idx - 1.0)

ns_idx = refractivity_to_index(Ns)

# 4/3 earth's radius model (dn/dh = -1/(4a))
n_idx_43 = np.maximum(ns_idx - 0.25 * h / a, 1.0)
N_43 = index_to_refractivity(n_idx_43)
N_43 = np.where(N_43 > 0.0, N_43, np.nan)

# CRPL exponential reference atmosphere (Eq. 2.29)
N_ref = Ns * np.exp(-0.143859 * h)
n_idx_ref = refractivity_to_index(N_ref)

# ------ Plot ------
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=h, y=N_ref, mode="lines", name="CRPL Exponential Reference " +  
    "Atmosphere (decay constant = 0.143859)",
    line=dict(color="black", width=2, dash="solid"),
))
fig.add_trace(go.Scatter(
    x=h, y=N_43, mode="lines", name="4/3 Earth's Radius Model",
    line=dict(color="red", width=2, dash="dashdot"),
))

axis_common = dict(
    showgrid=True, gridcolor="rgba(0,0,0,0.2)",
    showline=True, linecolor="black", mirror=True, ticks="inside",
)

fig.update_layout(
    template="simple_white",
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(family=FONT, size=FONT_SIZE),
    title=dict(text="Variation of Atmospheric Refractivity with Height",
               x=0.5, xanchor="center", font=dict(size=FONT_SIZE + 4)),    
    xaxis=dict(
        title="HEIGHT ABOVE SEA LEVEL h (km)",
        range=[0, 28], tickmode="array", tickvals=list(range(0, 29, 4)),
        **axis_common,
    ),
    yaxis=dict(
        title="REFRACTIVITY (N)",
        type="log",
        range=[0.0, np.log10(600.0)],
        minorloglabels="complete",
        **axis_common,
    ),
    legend=dict(x=0.98, y=0.98, xanchor="right", yanchor="top",
                bordercolor="black", borderwidth=1),
    width=700, height=600,
)

fig.write_html(FIG_NANE + ".html", include_plotlyjs="cdn")
print("saved:"+ FIG_NANE + ".html")