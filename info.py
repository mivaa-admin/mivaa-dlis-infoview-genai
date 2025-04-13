import streamlit as st
import pandas as pd
from langchain_helper import get_structured_logical_file_summary_cached, summarize_metadata_for_prompt
from dlis_quality import generate_dlis_quality_report

def info(dlis_file):
    st.markdown("<h1 style='color:#2c3e50;'>📘 DLIS InfoView – File Overview</h1>", unsafe_allow_html=True)
    st.markdown("Explore metadata, frames, and log channels inside your DLIS file.", unsafe_allow_html=True)
    st.markdown("---")

    logical_files = list(dlis_file)

    if logical_files:
        logical_files_dict = {f"Logical File {i+1}": lf for i, lf in enumerate(logical_files)}

        logical_file_selection = st.selectbox("📁 Select a Logical File", list(logical_files_dict.keys()))
        selected_logical_file = logical_files_dict[logical_file_selection]

        total_channels = len(getattr(selected_logical_file, 'channels', []))
        total_frames = len(getattr(selected_logical_file, 'frames', []))
        total_origins = len(getattr(selected_logical_file, 'origins', []))

        st.markdown("### 🔍 Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric(label="📈 Channels", value=total_channels)
        col2.metric(label="🧩 Frames", value=total_frames)
        col3.metric(label="🧭 Origins", value=total_origins)

        st.markdown("---")

        # # 🛢️ Well Header Summary
        # with st.expander("📋 Well Header Summary", expanded=True):
        #
        #     origins = getattr(selected_logical_file, 'origins', [])
        #
        #     origin_summary = {}
        #     if origins:
        #         try:
        #             origin_data = origins[0].describe().__dict__
        #
        #             origin_summary = {
        #                 "Field": origin_data.get("field", "N/A"),
        #                 "Well Name": origin_data.get("well_name", "N/A"),
        #                 "Company": origin_data.get("company", "N/A"),
        #                 "Produced For": origin_data.get("produced_for", "N/A"),
        #                 "Logging Date": origin_data.get("creation_date", "N/A"),
        #                 "File Set Name": origin_data.get("file_set_name", "N/A")
        #             }
        #         except Exception as e:
        #             st.warning(f"Unable to extract well header info: {e}")
        #
        #     col1, col2 = st.columns(2)
        #
        #     with col1:
        #         st.markdown(f"**Field:** {origin_summary.get('Field')}")
        #         st.markdown(f"**Well Name:** {origin_summary.get('Well Name')}")
        #         st.markdown(f"**Company:** {origin_summary.get('Company')}")
        #
        #     with col2:
        #         st.markdown(f"**Produced For:** {origin_summary.get('Produced For')}")
        #         st.markdown(f"**Logging Date:** {origin_summary.get('Logging Date')}")
        #         st.markdown(f"**File Set Name:** {origin_summary.get('File Set Name')}")

        persona = st.selectbox("👤 Who should this summary be tailored for?", ["Petrophysicist", "Data Engineer"])

        # Button for AI Summary Generation
        if st.button("Generate AI Summary"):
            try:
                # Generate the metadata summary input
                summary_input = summarize_metadata_for_prompt(selected_logical_file)
                # Call the function to generate the AI summary based on the selected logical file and persona
                response = get_structured_logical_file_summary_cached(summary_input, persona)

                # ✅ FIX: ensure that response is a string and handle it correctly
                summary_text = response if isinstance(response, str) else getattr(response, 'content', str(response))

                # ✅ Display the AI Summary
                if summary_text:
                    st.markdown(f"**🧠 GenAI Summary:**\n\n{summary_text}", unsafe_allow_html=True)
                else:
                    st.info("No summary text returned.")
            except Exception as e:
                st.warning(f"AI Summary generation failed: {e}")

        # Smart DLIS Health / Quality Report
        with st.expander("🩺 Smart DLIS Health / Quality Report", expanded=False):
            report = generate_dlis_quality_report(selected_logical_file)
            st.markdown(report)

            st.download_button("⬇️ Download Report", data=report, file_name="dlis_quality_report.md")

        with st.expander("📄 Logical File Description", expanded=False):
            st.write(selected_logical_file.describe())

        # # DLIS Object Explorer
        # with st.expander("🗂️ DLIS Object Explorer", expanded=False):
        #     DLIS_OBJECTS = {
        #         "Frames": getattr(selected_logical_file, 'frames', []),
        #         "Channels": getattr(selected_logical_file, 'channels', []),
        #         "Parameters": getattr(selected_logical_file, 'parameters', []),
        #         "Tools": getattr(selected_logical_file, 'tools', []),
        #         "Origins": getattr(selected_logical_file, 'origins', []),
        #         "Comments": getattr(selected_logical_file, 'comments', []),
        #         "Unknown Objects": getattr(selected_logical_file, 'unknown', [])
        #     }
        #     st.markdown("### 🔍 DLIS Objects Summary")
        #
        #     for obj_type, obj_list in DLIS_OBJECTS.items():
        #         st.markdown(f"#### {obj_type} ({len(obj_list)})")
        #         if not obj_list:
        #             st.info("No records found.")
        #             continue
        #         if obj_type == "Parameters":
        #             param_data = []
        #             for p in obj_list:
        #                 for k, v in p.items.items():
        #                     param_data.append({"Name": k, "Value": v, "Units": p.units})
        #             st.dataframe(pd.DataFrame(param_data), use_container_width=True)
        #         elif obj_type == "Tools":
        #             for tool in obj_list:
        #                 st.markdown("---")
        #                 st.text(tool.describe())
        #         elif obj_type == "Origins":
        #             for origin in obj_list:
        #                 st.markdown("---")
        #                 st.text(origin.describe())
        #         elif obj_type == "Comments":
        #             for comment in obj_list:
        #                 st.markdown(f"- {comment}")
        #         elif obj_type == "Unknown Objects":
        #             for unknown in obj_list:
        #                 st.markdown(f"- {unknown.object_name}")
        #         else:
        #             st.markdown(f"Total: {len(obj_list)} objects")

        origins = getattr(selected_logical_file, 'origins', []) or []
        with st.expander(f'🧭 Origins ({len(origins)})', expanded=False):
            if origins:
                for origin in origins:
                    st.write(origin.describe())
            else:
                st.info("No origins found.")

        frames = getattr(selected_logical_file, 'frames', []) or []
        with st.expander(f'🧩 Frames ({len(frames)})', expanded=False):
            if frames:
                for i, frame in enumerate(frames, 1):
                    st.subheader(f"Frame {i}")
                    st.write(frame.describe())
                    if hasattr(frame, 'channels'):
                        channel_names = [ch.name for ch in frame.channels]
                        if channel_names:
                            st.markdown("**📈 Channels in this frame:**")
                            st.markdown(f"<div style='color:#34495e;'>{', '.join(channel_names)}</div>", unsafe_allow_html=True)
                        else:
                            st.write("No channels in this frame.")
            else:
                st.info("No frames found.")

        channels = getattr(selected_logical_file, 'channels', []) or []
        with st.expander(f'📈 Channels ({len(channels)})', expanded=False):
            if channels:
                st.subheader('📋 Channel Listing')
                search = st.text_input("🔎 Filter channels by name or unit").lower()
                channel_data = [
                    {
                        'Name': ch.name,
                        'Units': ch.units,
                        'Description': ch.long_name
                    }
                    for ch in channels
                ]
                channel_data = sorted(channel_data, key=lambda x: x['Name'])
                if search:
                    channel_data = [
                        ch for ch in channel_data
                        if search in ch['Name'].lower() or search in ch['Units'].lower()
                    ]
                st.dataframe(pd.DataFrame(channel_data), use_container_width=True)
                st.download_button(
                    label="⬇️ Download Channels as CSV",
                    data=pd.DataFrame(channel_data).to_csv(index=False),
                    file_name="channels.csv",
                    mime="text/csv"
                )
            else:
                st.info("No channels found.")
    else:
        st.warning("No logical files found in this DLIS file.")
