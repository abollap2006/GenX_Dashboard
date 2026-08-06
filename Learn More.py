"""
Learn More Tab - Educational Content and Background Information

This module provides comprehensive educational content about PFAS, the GenX Exposure Study,
and frequently asked questions. It serves as the primary information resource for
dashboard users seeking to understand the scientific background and methodology.

The content includes:
- PFAS background and health implications
- Study methodology and privacy protections
- Data limitations and inclusion criteria
- Contact information and additional resources

Author: [Your Name]
Last Updated: [Date]
"""

# === MAIN PAGE TITLE ===
st.title("Learn More")

st.markdown("""
### Why are only some of the PFAS the study tests for included?
We included data on a PFAS if it was detected in at least <span style="color:red;"><b>50% of the population</b></span>. This helps protect our participants’ privacy. If we shared data for a PFAS that was detected in less than 50% of the study participants, it could be easier to identify individuals. Our top priority is keeping our participants safe and their data protected.

""", unsafe_allow_html=True)

st.markdown("""
### Want to learn more about PFAS and what the study is up to?
Check out these pages on our website. We host educational webinars, virtual office hours, and in-person meetings several times a year to share our latest findings, so check out our [events calendar](https://genxstudy.ncsu.edu/events/) and follow us on [social media](https://linktr.ee/ncsugenx_study) to stay up to date.
""")

st.markdown("""
### FAQs
""")

# === EXPANDABLE FAQ SECTIONS ===
# Each expandable section addresses common user questions with detailed explanations

# PFAS Background Information
with st.expander("What are PFAS?"):
    st.markdown(
        "<b>PFAS are a broad class of chemicals</b> that are used for their stain and water-resistant properties. They are found in the Cape Fear River as a result of chemical manufacturing, use in firefighting, textile and furniture manufacturing as well as disposal of everyday products such as pizza boxes, furniture, etc. to landfills. For more information about PFAS, click <a href='https://superfund.ncsu.edu/what-is-pfas/' style='color:red;' target='_blank'>here</a>.",
        unsafe_allow_html=True
    )

# Future Data Expansion Plans    
with st.expander("Will you add more data to the dashboard?"):
    st.write("Yes, we plan on expanding the dashboard to include more individual PFAS, locations, more years as data is available.")

# Project Funding Information        
with st.expander("Who is funding the dashboard?"):
    st.write("The North Carolina Collaboratory funded this project.")

# Joining the GenX Study   
with st.expander("How do I join the GenX Exposure Study?"):
    st.write("The GenX Exposure Study is no longer enrolling new participants. However, if you are interested in paying to have your blood tested for PFAS, check out this resource from [PFAS REACH](https://docs.google.com/spreadsheets/d/1kUdZIkpA-cIaKbEwv_7vm8_l1q6kOu-r3zErxwYwr08/edit?gid=346039373#gid=346039373)")

# What is NHANES
with st.expander("What is NHANES?"):
    st.write("NHANES stands for the National Health and Nutrition Examination Survey and it is run by the CDC. This survey collects information from intrviews, physical health exams, and lab tests to check the health and diet of people in the United States.")

# === CONTACT INFORMATION SECTION ===
# Provide clear contact details for user questions and support

st.subheader("Contact Us")
st.markdown("If you have any questions, please reach out to us at (855) 854–2641 or genx-exposure-study@ncsu.edu.")
