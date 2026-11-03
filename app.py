import io
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import streamlit as st

st.set_page_config(page_title='Traces of Dance', page_icon='〰️', layout='wide')
st.title('Traces of Dance')
st.caption('An interactive generative poster inspired by traditional Korean dance movements.')
st.markdown('Explore how movement, rhythm and breath can become visible traces.')

with st.sidebar:
    st.header('Poster Controls')
    style = st.selectbox('Visual style', ['Korean Color Dynamics (Stage 4)', 'Pastel Interactive Movements (Stage 3)'])
    curves = st.slider('Number of curves', 2, 8, 4)
    amplitude = st.slider('Amplitude', 0.2, 1.8, 1.0, 0.2)
    frequency = st.slider('Frequency', 0.5, 3.0, 1.0, 0.25)
    opacity = st.slider('Opacity', 0.2, 1.0, 0.8, 0.1)
    particles = st.slider('Background particles', 0, 120, 28, 4)
    seed = st.number_input('Variation seed', min_value=0, max_value=99999, value=42, step=1)


def make_poster(style, curves, amplitude, frequency, opacity, particles, seed):
    rng = np.random.default_rng(int(seed))
    fig, ax = plt.subplots(figsize=(8, 11))
    is_korean = style.startswith('Korean')
    background = '#F8F5EC' if is_korean else '#FAF7F0'
    ink = '#20252C' if is_korean else '#42434A'
    colors = ['#1764B0', '#D93636', '#F2C230'] if is_korean else ['#A8C9DF', '#EBC1C5', '#BFC0C5']
    fig.patch.set_facecolor(background)
    ax.set_facecolor(background)
    ax.set(xlim=(0,10), ylim=(0,14))
    ax.set_aspect('equal')
    ax.axis('off')

    if is_korean:
        t = np.linspace(0, 1, 800)
        for i in range(curves):
            phase = i * 1.8
            offset = (i - (curves - 1) / 2) * 0.22
            color = colors[i % len(colors)]
            x = 5 + (2.5 * amplitude) * np.sin(2 * np.pi * frequency * t + phase) + 0.65 * np.sin(6 * np.pi * frequency * t + phase)
            y = 2 + 9.1 * t + (0.7 * amplitude) * np.sin(4 * np.pi * frequency * t + phase) + offset
            for layer in range(18):
                shift = (layer - 8.5) * 0.055
                ax.plot(x + shift, y, color=color, lw=2.5, alpha=0.035 * opacity, zorder=2)
            ax.plot(x, y, color=color, lw=2.0, alpha=0.85 * opacity, zorder=4)
            ax.plot(x - 0.08, y + 0.06, color='white', lw=1.1, alpha=0.8 * opacity, zorder=5)
            idx = np.linspace(30, 760, 45, dtype=int)
            ax.scatter(x[idx], y[idx], s=rng.uniform(3, 17, len(idx)), color=color, alpha=0.55 * opacity, zorder=6)
        subtitle = 'Korean Color Dynamics'
    else:
        t = np.linspace(0, 1, 500)
        for i in range(curves):
            start_y = 2.2 + i * (8.5 / max(curves - 1, 1))
            x = 0.8 + 8.4 * t
            phase = i * 0.7
            y = start_y + amplitude * np.sin(2 * np.pi * frequency * t + phase) + 0.25 * amplitude * np.sin(4 * np.pi * frequency * t + phase)
            color = colors[i % len(colors)]
            ax.plot(x, y, color=color, lw=1.8, alpha=opacity, solid_capstyle='round')
            for pos in [0.2, 0.5, 0.8]:
                idx = int(pos * (len(t) - 1))
                ax.add_patch(Circle((x[idx], y[idx]), radius=rng.uniform(0.15, 0.4), facecolor=color, edgecolor='none', alpha=opacity * 0.45))
            idx = np.linspace(20, len(t)-20, 25, dtype=int)
            ax.scatter(x[idx], y[idx], s=rng.uniform(5, 20, len(idx)), color=color, alpha=opacity)
        subtitle = 'Interactive Movements'

    for _ in range(particles):
        ax.scatter(rng.uniform(1.2, 8.8), rng.uniform(2, 11.3), s=rng.uniform(4,35), color=rng.choice(colors), alpha=0.18 * opacity, zorder=1)
    ax.text(5, 13.15, 'TRACES OF DANCE', ha='center', va='center', fontsize=25, fontweight='bold', color=ink)
    ax.text(5, 12.6, subtitle, ha='center', va='center', fontsize=11, color='#666666')
    ax.text(5, 0.75, 'MOVEMENT  ·  BREATH  ·  TRACE', ha='center', va='center', fontsize=9, color=ink, alpha=0.7)
    return fig

fig = make_poster(style, curves, amplitude, frequency, opacity, particles, seed)
left, right = st.columns([1, 2])
with left:
    st.subheader('Concept')
    st.write('This project transforms the invisible traces of traditional Korean dance into flowing lines, layered colors and particles. The interactive controls let each viewer create their own interpretation of motion.')
    st.markdown('**Plan → Do → See**')
    st.write('Plan: express Korean dance movement visually. Do: adjust generative parameters in Streamlit. See: observe how variations change the poster.')
with right:
    st.pyplot(fig, use_container_width=True)
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', dpi=250, bbox_inches='tight', facecolor=fig.get_facecolor())
    st.download_button('Download poster as PNG', data=buffer.getvalue(), file_name='traces_of_dance.png', mime='image/png')
plt.close(fig)
