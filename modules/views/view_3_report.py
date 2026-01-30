import streamlit as st

from modules.data.report_data import ParticipantReportData, ReportData
from modules.utils import format_number_to_currency


def participant_view(participant_report: ParticipantReportData) -> None:
    """Element to show report of a participant.

    Args:
        participant_report (ParticipantReportData): the participant
            report data
    """
from modules.data import session_data


def participant_view(participant_report: ParticipantReportData) -> None:
    """Element to show report of a participant.

    Args:
        participant_report (ParticipantReportData): the participant
            report data
    """
    # Use premium-card class for better UI
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    
    name_col, total_str_col, total_col = st.columns([7, 1, 2])
    with name_col:
        st.markdown(f"##### {participant_report.name}")
    with total_str_col:
        st.markdown("##### Total:")
    with total_col:
        total_str = format_number_to_currency(
            int(participant_report.purchased_total)
        )
        st.markdown(f"##### {total_str}")
    st.table(participant_report.to_dataframe_display(), border="horizontal")
    subtotal_str = format_number_to_currency(participant_report.purchased_subtotal)
    st.markdown(f"###### Subtotal: {subtotal_str}")
    total_str = format_number_to_currency(participant_report.purchased_others)
    st.markdown(f"###### Others\*: {total_str}")
    
    st.markdown('</div>', unsafe_allow_html=True)


def controller(report: ReportData | None) -> bool:
    """Main controller of page 3, report view.

    Returns:
        bool: always False, to prevent action to go to
        next page in main controller
    """
    if report is None:
        st.error("Please submit assignment first!")
        return False
        
    st.markdown("### Split Bill Report")
    
    for participant_report in report.participants_reports:
        participant_view(participant_report)
    
    st.markdown("*\*tax, services, discount, etc.*")
    
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(" Start New Bill", use_container_width=True):
            session_data.reset_app_state()
            st.rerun()
            
    return False