import json
import os
import streamlit as st
import base64

@st.cache_data
def get_manifest():
    manifest_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "picture", "Seleções", "manifest.json")
    if not os.path.exists(manifest_path):
        return []
    with open(manifest_path, "r", encoding="utf-8") as f:
        return json.load(f)

@st.cache_data
def get_svg_base64(filename):
    svg_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "picture", "Seleções", filename)
    if not os.path.exists(svg_path):
        return ""
    with open(svg_path, "r", encoding="utf-8") as f:
        svg_content = f.read()
    return base64.b64encode(svg_content.encode("utf-8")).decode("utf-8")

def get_team_flag_svg(team_name):
    if not team_name:
        return ""
    
    manifest = get_manifest()
    
    # We look for the name_pt inside the team_name (ignoring emojis)
    for entry in manifest:
        if entry["name_pt"] in team_name:
            return get_svg_base64(entry["filename"])
            
    return ""

def render_team_html(team_name, extra_classes=""):
    """
    Returns an HTML string to display the team with its SVG flag.
    If no SVG is found, falls back to the original text (which contains the emoji).
    """
    if not team_name:
        return f"<div class='team-flag-container {extra_classes}'><div class='team-name'>TBD</div></div>"
        
    svg_b64 = get_team_flag_svg(team_name)
    
    if svg_b64:
        # We strip the emoji (first 2-3 characters usually, or just replace it)
        # However, the safest visual way is to just display the SVG and the name_pt
        # Let's extract the actual name.
        name_only = team_name
        manifest = get_manifest()
        for entry in manifest:
            if entry["name_pt"] in team_name:
                name_only = entry["name_pt"]
                break
                
        html = f"""
        <div class="team-flag-container {extra_classes}">
            <img class="team-svg-flag" src="data:image/svg+xml;base64,{svg_b64}" alt="{name_only}" />
            <span class="team-name">{name_only}</span>
        </div>
        """
        return html
    else:
        return f"<div class='team-flag-container {extra_classes}'><span class='team-name'>{team_name}</span></div>"
