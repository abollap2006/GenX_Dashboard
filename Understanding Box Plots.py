"""
Understanding Box Plots Tab 

This tab is aimed to help the general public understand how to read the plots we have included on this dashboard.

The content includes:
- Description about why box plots are used
- Video link that explains how to read a box plot

Author: [Your Name]
Last Updated: [Date]
"""

# === MAIN PAGE TITLE ===
#st.title("Understanding Box Plots") # This title is unnecessary maybe

st.markdown("""
### Why are box plots used?
We use box plots to share our data because they show a more complete picture than bar charts or pie graphs. With a box plot, we can share range, upper and lower values, and the median for each PFAS. 
""", unsafe_allow_html=True)

st.markdown("""
### How do you read a boxplot?
We recommend that you view this video or view the following infographic to understand how to read a boxplot         


""")

# Center the image and content
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    # Center the image using Streamlit's native centering
    st.image('How to read boxplots.png', caption="Boxplot Infographic", use_container_width=True)
    
    # Center the video link
    st.markdown(
        '<div style="text-align: center;">'
        '<a href="https://drive.google.com/file/d/1y6LbcXVy7-Mnz4FJfG9vGktuz-Vt0fpv/view?usp=sharing" target="_blank" style="font-size: 22px; font-weight: bold;">'
        'Watch the Boxplot Video</a></div>',
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)  # <-- Add this line for spacing
st.markdown("""
<div style="font-size: 16px;">
Note: The boxplots in this dashboard may look different because they are based on real data and may have different ranges, medians, and outliers.
Additionally, the red lines represent the median NHANES 95th percentile for each PFAS, which is a reference point for comparison.
</div>
""", unsafe_allow_html=True)


