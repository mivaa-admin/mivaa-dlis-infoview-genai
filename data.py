import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from io import BytesIO
import base64
from collections import defaultdict
from langchain_helper import get_curve_explanation_from_ai  # already written by you


def data(dlis_file):
    st.markdown("## 📊 Data Visualization & Curve Explorer")
    st.markdown("Browse frames, pick depth channels, select curves, and preview interactive log plots.")
    st.markdown("---")

    if 'selected_curves' not in st.session_state:
        st.session_state.selected_curves = []

    if 'logical_file_dfs' not in st.session_state:
        st.session_state.logical_file_dfs = {}

    DEPTH_MNEMONICS = ['TDEP', 'DEPT', 'DEPTH', 'MD', 'TVD']

    # Curve families and short descriptions
    CURVE_FAMILIES = {
        "Gamma Ray": ["GR", "SGR", "CGR"],
        "Resistivity": ["ILD", "LLD", "MSFL", "RT", "RLA", "RLL"],
        "Porosity": ["NPHI", "DPHI", "PHIT", "PHIE"],
        "Density": ["RHOB", "DEN", "ZDEN"],
        "Sonic": ["DT", "DTS", "DTP", "DTCO"],
        "Caliper": ["CALI"],
        "Others": []
    }

    CURVE_DESCRIPTIONS = {
        "GR": "Gamma Ray log - natural radioactivity",
        "ILD": "Deep Induction Log - resistivity",
        "NPHI": "Neutron Porosity",
        "DT": "Sonic travel time",
        "RHOB": "Bulk Density",
        "CALI": "Caliper log - borehole diameter",
        "MSFL": "Micro Spherically Focused Log - shallow resistivity"
    }

    logical_files = list(dlis_file)

    if logical_files:
        if logical_files:
            # Well Header Summary Panel
            with st.expander("📋 Well Header Summary", expanded=True):
                total_logical_files = len(logical_files)
                total_frames = sum(len(getattr(lf, 'frames', [])) for lf in logical_files)
                total_channels = sum(len(getattr(lf, 'channels', [])) for lf in logical_files)
                total_origins = sum(len(getattr(lf, 'origins', [])) for lf in logical_files)

                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Logical Files", total_logical_files)
                col2.metric("Frames", total_frames)
                col3.metric("Channels", total_channels)
                col4.metric("Origins", total_origins)

        # Step 1
        st.markdown("### 1️⃣ Select a Logical File")
        logical_files_dict = {f"Logical File {i + 1}": lf for i, lf in enumerate(logical_files)}
        logical_file_selection = st.selectbox("📁 Logical Files", list(logical_files_dict.keys()))
        selected_logical_file = logical_files_dict[logical_file_selection]

        # Step 2
        st.markdown("### 2️⃣ Select a Frame")
        frames = getattr(selected_logical_file, 'frames', [])
        frame_names = [f"Frame {i + 1}" for i in range(len(frames))]

        if not frames:
            st.warning("⚠️ No frames found in this logical file.")
            return

        frame_search = st.text_input("🔍 Search Frames", "")
        filtered_frame_names = [f for f in frame_names if frame_search.lower() in f.lower()]
        frame_selection = st.selectbox("🧩 Available Frames", filtered_frame_names)

        selected_frame_index = int(frame_selection.split(' ')[1]) - 1
        selected_frame = frames[selected_frame_index]

        # Step 3: Extract Data
        st.markdown("### 3️⃣ Load Frame Data")
        data_dict = {}

        for channel in selected_frame.channels:
            try:
                values = channel.curves()
                if values is not None and np.ndim(values) == 1:
                    values = np.where(values == -999.25, np.nan, values)
                    data_dict[channel.name] = values
            except Exception as e:
                st.warning(f"❌ Could not load channel {channel.name}: {e}")

        df = pd.DataFrame(data_dict)
        logical_file_key = f"{logical_file_selection} - {frame_selection}"
        st.session_state.logical_file_dfs[logical_file_key] = df
        st.session_state.df = df

        if df.empty:
            st.warning("⚠️ No valid channels found in this frame.")
            return

        # Step 4: Choose Depth
        st.markdown("### 4️⃣ Select Depth Channel")
        auto_depth = None
        for col in df.columns:
            if col in DEPTH_MNEMONICS and df[col].is_monotonic_increasing:
                auto_depth = col
                break

        depth_options = ['Auto (index)'] + list(df.columns)
        selected_depth = st.selectbox("📏 Depth Channel (Y-axis)", depth_options,
                                      index=depth_options.index(auto_depth) if auto_depth else 0)

        if selected_depth == 'Auto (index)':
            df['INDEX'] = range(len(df))
            depth_column = 'INDEX'
            depth_unit = 'index'
            st.info("ℹ️ Using sample index as depth.")
        else:
            depth_column = selected_depth
            depth_channel = next((ch for ch in selected_frame.channels if ch.name == depth_column), None)
            depth_unit = depth_channel.units if depth_channel and hasattr(depth_channel, 'units') else 'unknown'
            st.markdown(f"📐 **Depth unit:** `{depth_unit}`")

        st.session_state.depth_column = depth_column

        # Step 5: Curve Selection & Visualization
        st.markdown("### 5️⃣ Select Curves and Plot")
        curve_names = [col for col in df.columns if col != depth_column]

        # Group and describe
        grouped = defaultdict(list)
        unmatched = set(curve_names)
        for family, tags in CURVE_FAMILIES.items():
            for name in curve_names:
                if any(name.startswith(tag) for tag in tags):
                    grouped[family].append(name)
                    unmatched.discard(name)
        grouped['Others'] += list(unmatched)

        family = st.selectbox("📂 Log Curve Family", list(grouped.keys()))

        # Add search inside selected group
        group_curves = grouped[family]
        curve_filter = st.text_input("🔍 Filter Curves", "")
        filtered_curves = [c for c in group_curves if curve_filter.lower() in c.lower()]

        selected_curves_multi = st.multiselect("📈 Select Curves to Display",
                                               filtered_curves,
                                               format_func=lambda x: f"{x} ({CURVE_DESCRIPTIONS.get(x, 'No description')})")

        for curve_name in selected_curves_multi:
            already_selected = any(
                c['curve'] == curve_name and
                c['logical_file'] == logical_file_selection and
                c['frame'] == frame_selection
                for c in st.session_state.selected_curves
            )
            if not already_selected:
                channel = next((ch for ch in selected_frame.channels if ch.name == curve_name), None)
                unit = channel.units if channel else ''
                description = channel.long_name if channel and channel.long_name else curve_name

                st.session_state.selected_curves.append({
                    'curve': curve_name,
                    'logical_file': logical_file_selection,
                    'frame': frame_selection,
                    'depth_column': depth_column,
                    'depth_unit': depth_unit,
                    'logical_file_key': logical_file_key,
                    'unit': unit,
                    'description': description
                })

        if selected_curves_multi:
            st.success(f"✅ {len(selected_curves_multi)} curve(s) selected")

            layout_type = st.radio("🖼️ Choose Plot Layout", ["Single Track", "Track 1 vs. Track 2"], horizontal=True)
            fig = go.Figure()

            if layout_type == "Single Track":
                for curve in selected_curves_multi:
                    fig.add_trace(go.Scatter(
                        x=df[curve],
                        y=df[depth_column],
                        mode='lines',
                        name=curve,
                        line=dict(width=1)
                    ))
                fig.update_layout(
                    title="📊 Well Log Plot – Single Track",
                    yaxis_title=f"Depth ({depth_unit})" if depth_unit != 'index' else "Sample Index",
                    yaxis_autorange='reversed',
                    height=600
                )
            else:
                left_curve = selected_curves_multi[0]
                fig.add_trace(go.Scatter(
                    x=df[left_curve],
                    y=df[depth_column],
                    mode='lines',
                    name=left_curve,
                    xaxis='x1'
                ))
                if len(selected_curves_multi) > 1:
                    for curve in selected_curves_multi[1:]:
                        fig.add_trace(go.Scatter(
                            x=df[curve],
                            y=df[depth_column],
                            mode='lines',
                            name=curve,
                            xaxis='x2'
                        ))
                fig.update_layout(
                    title="📊 Well Log Plot – Track 1 vs. Track 2",
                    yaxis=dict(title=f"Depth ({depth_unit})", autorange='reversed'),
                    xaxis=dict(domain=[0.0, 0.45], title=left_curve),
                    xaxis2=dict(domain=[0.55, 1.0], title="Track 2"),
                    height=600
                )

            st.plotly_chart(fig, use_container_width=True)

            buffer = BytesIO()
            fig.write_image(buffer, format="png")
            b64 = base64.b64encode(buffer.getvalue()).decode()
            st.markdown(
                f'<a href="data:image/png;base64,{b64}" download="log_plot.png">📥 Download Plot as PNG</a>',
                unsafe_allow_html=True
            )

            if len(selected_curves_multi) == 1:
                st.markdown("### 📊 Curve Statistics")
                stats = df[selected_curves_multi[0]].describe()
                st.table(stats)

            st.markdown("---")
            st.markdown("### ✨ GenAI Powered Curve Explanation")
            st.caption("This explanation is generated using OpenAI GPT-4 to help you understand this log curve better.")

            if st.button(f"Explain {selected_curves_multi[0]} using AI"):
                with st.spinner("Thinking like a Logging Engineer..."):
                    try:
                        explanation = get_curve_explanation_from_ai(selected_curves_multi[0])
                        st.success(explanation)
                    except Exception as e:
                        st.error(f"AI explanation failed: {e}")

        else:
            st.info("💡 Select one or more curves to visualize.")
    else:
        st.warning("⚠️ No logical files available in DLIS file.")
