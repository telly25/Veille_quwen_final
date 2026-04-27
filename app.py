import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 🎨 Configuration de la page
st.set_page_config(page_title="Veille Conformité POC", page_icon="🔍", layout="wide")

# 📊 Données de démonstration (remplaçables par Airtable/Make plus tard)
DEMO_DATA = [
    {
        "id": 1, "date": "27/04/2026", "titre": "Nouvelle obligation DORA – Testing ICT",
        "referentiel": "DORA", "impact": "Élevé", "type": "Obligation",
        "resume": "Le règlement exige des tests réguliers des systèmes ICT, incluant un audit annuel et des tests de pénétration avancés.",
        "recommandation": "Auditer votre registre des actifs ICT critiques et planifier un test TLPT avant Q3 2026.",
        "lu": False
    },
    {
        "id": 2, "date": "26/04/2026", "titre": "Guide ENISA – Résilience NIS2",
        "referentiel": "NIS2", "impact": "Moyen", "type": "Recommandation",
        "resume": "Nouvelles bonnes pratiques pour les entités essentielles : délai de 24h pour l'alerte initiale, format standardisé de rapport.",
        "recommandation": "Mettre à jour votre procédure de gestion d'incidents et former le SOC aux formats ENISA.",
        "lu": False
    },
    {
        "id": 3, "date": "25/04/2026", "titre": "Mise à jour recommandations mobiles – CNIL",
        "referentiel": "RGPD", "impact": "Faible", "type": "Information",
        "resume": "La CNIL actualise son cadre pour les applications mobiles, notamment sur la collecte de données de géolocalisation.",
        "recommandation": "Vérifier la conformité de vos apps mobiles et mettre à jour les mentions légales.",
        "lu": True
    },
    {
        "id": 4, "date": "24/04/2026", "titre": "Révision ISO/IEC 27001:2022 – Contrôle A.5.7",
        "referentiel": "ISO 27001", "impact": "Moyen", "type": "Obligation",
        "resume": "Clarification des exigences pour la gestion des menaces liées aux parties intéressées et la revue des risques.",
        "recommandation": "Intégrer le nouveau contrôle A.5.7 dans votre analyse de risques annuelle.",
        "lu": False
    }
]

df = pd.DataFrame(DEMO_DATA)

# 🎨 CSS personnalisé pour les cartes et badges
st.markdown("""
<style>
    .card {
        border-left: 5px solid #ccc; padding: 15px; border-radius: 8px; background: #fff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 12px;
    }
    .card-élevé { border-left-color: #EF4444; }
    .card-moyen { border-left-color: #F59E0B; }
    .card-faible { border-left-color: #10B981; }
    .badge { display: inline-block; padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; margin-right: 6px; }
    .badge-élevé { background: #FEE2E2; color: #991B1B; }
    .badge-moyen { background: #FEF3C7; color: #92400E; }
    .badge-faible { background: #D1FAE5; color: #065F46; }
    .badge-obligation { background: #DBEAFE; color: #1E40AF; }
    .badge-recommandation { background: #E0E7FF; color: #3730A3; }
    .badge-information { background: #F3F4F6; color: #374151; }
    .stat-card { background: #fff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.08); text-align: center; }
    .stat-number { font-size: 32px; font-weight: 700; color: #1E3A8A; }
    .stat-label { font-size: 14px; color: #6B7280; margin-top: 4px; }
</style>
""", unsafe_allow_html=True)

#  Layout principal
st.sidebar.title(" Navigation")
menu = st.sidebar.radio("Aller à", ["📊 Dashboard", "⚙️ Paramètres"])

if menu == "📊 Dashboard":
    st.title("Tableau de bord Veille Réglementaire")
    
    # 📈 Stats bar
    col1, col2, col3, col4 = st.columns(4)
    stats = df.groupby("referentiel").size()
    col1.markdown(f'<div class="stat-card"><div class="stat-number">{stats.get("RGPD", 0)}</div><div class="stat-label">RGPD</div></div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="stat-card"><div class="stat-number">{stats.get("NIS2", 0)}</div><div class="stat-label">NIS2</div></div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="stat-card"><div class="stat-number">{stats.get("DORA", 0)}</div><div class="stat-label">DORA</div></div>', unsafe_allow_html=True)
    col4.markdown(f'<div class="stat-card"><div class="stat-number">{stats.get("ISO 27001", 0)}</div><div class="stat-label">ISO 27001</div></div>', unsafe_allow_html=True)
    
    # 🔍 Filtres
    st.subheader("🔎 Filtrer les alertes")
    f_col1, f_col2, f_col3 = st.columns([2, 1, 1])
    with f_col1:
        search = st.text_input("Rechercher un titre ou un mot-clé", placeholder="ex: testing, incident, mobile...")
    with f_col2:
        ref_filter = st.multiselect("Référentiel", df["referentiel"].unique(), default=list(df["referentiel"].unique()))
    with f_col3:
        impact_filter = st.multiselect("Impact", df["impact"].unique(), default=list(df["impact"].unique()))
    
    #  Application des filtres
    filtered = df.copy()
    if search:
        filtered = filtered[filtered["titre"].str.contains(search, case=False) | filtered["resume"].str.contains(search, case=False)]
    filtered = filtered[filtered["referentiel"].isin(ref_filter) & filtered["impact"].isin(impact_filter)]
    
    # 🗂️ Affichage des cartes
    st.subheader(f"📑 {len(filtered)} alerte(s) trouvée(s)")
    for _, row in filtered.iterrows():
        impact_class = f"card-{row['impact'].lower()}"
        badge_class = f"badge-{row['impact'].lower()}"
        type_class = f"badge-{row['type'].lower()}"
        
        st.markdown(f"""
        <div class="card {impact_class}">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap;">
                <div style="flex:1; min-width:300px;">
                    <strong style="font-size:16px;">{row['titre']}</strong>
                    <div style="color:#6B7280; font-size:13px; margin:4px 0;">{row['date']} • {row['referentiel']}</div>
                    <div style="margin-top:8px;">{row['resume'][:120]}...</div>
                </div>
                <div style="display:flex; gap:8px; align-items:center; margin-top:8px;">
                    <span class="badge {badge_class}">Impact: {row['impact']}</span>
                    <span class="badge {type_class}">Type: {row['type']}</span>
                    <button style="background:#1E3A8A; color:#fff; border:none; padding:6px 12px; border-radius:6px; cursor:pointer;">Voir détail</button>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

elif menu == "️ Paramètres":
    st.title("Configuration du POC")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📡 Sources surveillées")
        st.toggle("CNIL RSS (RGPD)", value=True)
        st.toggle("EUR-Lex RSS (NIS2)", value=True)
        st.toggle("EUR-Lex RSS (DORA)", value=True)
        st.toggle("ISO.org News", value=False)
        
        st.subheader("⏱️ Fréquence de collecte")
        st.selectbox("Intervalle", ["Toutes les 15 min", "Toutes les heures", "Toutes les 4 heures"], index=1)
        
    with col2:
        st.subheader("🤖 Modèle IA")
        st.selectbox("Provider", ["Groq (Llama 3.1 - Gratuit)", "Hugging Face (Zephyr - Gratuit)", "OpenRouter (Multi-modèles)"], index=0)
        
        st.subheader("🔔 Alertes & Notifications")
        st.text_input("Email de notification", placeholder="dpo@entreprise.fr")
        st.text_input("Webhook Discord", placeholder="https://discord.com/api/webhooks/...")
        st.button("📤 Tester une notification", type="primary")
        
        st.info("💡 Les paramètres sont sauvegardés localement pour le POC. En production, ils seront stockés dans Airtable/PostgreSQL.")

#  Footer
st.sidebar.divider()
st.sidebar.caption("POC Veille Conformité v1.0 • Déployé sur Streamlit Cloud • Données simulées")