import streamlit as st
import icalendar
import pandas as pd

def extract_meeting_details(ics_content):
    calendar = icalendar.Calendar.from_ical(ics_content)
    meetings = []

    for component in calendar.walk():
        if component.name == "VEVENT":
            summary = component.get('summary')
            attendees = component.get('attendee')
            if not isinstance(attendees, list):
                attendees = [attendees]
            
            attendees_list = [str(attendee).replace('mailto:', '') for attendee in attendees]
            meetings.append({
                'Meeting Summary': summary,
                'Attendees': ', '.join(attendees_list)
            })
    
    return meetings

st.title("ICS File Meeting Extractor")

uploaded_file = st.file_uploader("Choose an ICS file", type="ics")

if uploaded_file is not None:
    ics_content = uploaded_file.read()
    meetings = extract_meeting_details(ics_content)

    if meetings:
        df = pd.DataFrame(meetings)
        st.table(df)
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='meeting_details.csv',
            mime='text/csv',
        )
    else:
        st.write("No meetings found in the ICS file.")
