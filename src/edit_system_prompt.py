import streamlit as st
import os
from pathlib import Path

def save_preset(preset_name, prompt_text):
    """Save the current prompt as a preset"""
    presets_dir = Path("presets")
    presets_dir.mkdir(exist_ok=True)
    preset_file = presets_dir / f"{preset_name}.txt"
    preset_file.write_text(prompt_text)
    return str(preset_file)

def load_presets():
    """Load all available presets"""
    presets_dir = Path("presets")
    presets_dir.mkdir(exist_ok=True)
    return [f.stem for f in presets_dir.glob("*.txt")]

def load_preset(preset_name):
    """Load a specific preset"""
    preset_file = Path("presets") / f"{preset_name}.txt"
    if preset_file.exists():
        return preset_file.read_text()
    return ""

def show_prompt_editor(initial_prompt):
    """Show the system prompt editor interface"""
    st.subheader("Hier können Sie Einfluss auf Dr. Freuds Persönlichkeit nehmen")
    
    # Load existing presets
    presets = load_presets()
    
    # If no presets exist, create a default one
    if not presets:
        default_preset = "default"
        save_preset(default_preset, initial_prompt)
        presets = [default_preset]
    
    # Create columns for preset controls
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Find if current prompt matches any preset
        current_preset = None
        for preset in presets:
            if load_preset(preset) == initial_prompt:
                current_preset = preset
                break
        
        # Set the default index to the current preset or 0
        default_index = presets.index(current_preset) + 1 if current_preset in presets else 0
        
        selected_preset = st.selectbox(
            "Voreinstellung laden",
            [""] + presets,
            index=default_index,
            key="preset_selector"
        )
    
    with col2:
        st.write("\n")  # For vertical alignment
        if st.button("Voreinstellung laden", key="load_preset_btn"):
            if selected_preset:
                initial_prompt = load_preset(selected_preset)
                st.session_state.prompt_editor = initial_prompt
    
    # Add CSS for the apply button
    st.markdown("""
    <style>
    .apply-button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 12px;
        border: none;
        width: 100%;
    }
    .apply-button:hover {
        background-color: #45a049;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Text area for editing
    prompt_text = st.text_area(
        "Verändere Dr. Freuds Persönlichkeit",
        value=initial_prompt,
        height=400,
        key="prompt_editor"
    )
    
    # Save as new preset
    new_preset_col1, new_preset_col2 = st.columns([3, 1])
    with new_preset_col1:
        new_preset_name = st.text_input("Als neue Voreinstellung speichern", key="new_preset_name")
    with new_preset_col2:
        st.write("\n")  # For vertical alignment
        if st.button("Voreinstellung speichern") and new_preset_name:
            save_preset(new_preset_name, prompt_text)
            st.success(f"Gespeichert als '{new_preset_name}'")
    
    # Apply button
    if st.button("👨‍⚕️ Auf Dr. Freuds Gehirn anwenden", 
                use_container_width=True,
                type="primary",
                help="Klicken Sie hier, um die Änderungen auf Dr. Freuds Persönlichkeit anzuwenden"):
        st.balloons()
        st.success("✅ Die neue Persönlichkeit wurde erfolgreich auf Dr. Freud übertragen!")
        return prompt_text
    
    # If not applying, return the current prompt
    return initial_prompt