def summary_stats(location, summary_data, color):
    """
    Generate demographic summary statistics and visualizations for a specific location.
    
    This function creates three charts for a given location:
    1. Age distribution (horizontal bar chart)
    2. Gender distribution (pie chart) 
    3. Years lived in community (horizontal bar chart)
    
    Args:
        location (str): Name of the location to analyze (e.g., 'Pittsboro', 'Fayetteville')
        summary_data (pd.DataFrame): Complete dataset containing participant demographics
        color (list): Color scheme for the charts (single color in list format)
    
    Returns:
        None: Displays charts directly in Streamlit interface
    """
    
    # Define categorical orderings for consistent chart display
    # Year categories represent duration lived in community (removed 36-40+ for data availability)
    year_cat_order = ["1-5", "6-10", "11-15", "16-20", "21-25", "26-30", "31-35"]
    # Age groups used in the study
    age_order = ["6-17", "18-50", "51-70", ">70"]
    
    # Filter data to specific location
    location = location
    df_location = summary_data[summary_data['Location'] == location] 
    
    # Focus on 2023 data for current snapshot (can be modified for dynamic year filtering)
    df_location_2023 = df_location[df_location['Year'] == 2023]
    # === AGE DISTRIBUTION ANALYSIS ===
    # Count unique participants by age category (observed=True prevents pandas FutureWarning)
    df_age_counts = df_location_2023.groupby('age_cat', observed=True)['unique_id'].nunique().reset_index()
    sample_size = int(df_age_counts['unique_id'].sum())
    # Calculate percentage distribution for each age group
    df_age_counts['Percentage'] = (df_age_counts['unique_id'] / sample_size) * 100  

    # Create age distribution horizontal bar chart
    # Handle empty data case (e.g., Wilmington with no 2023 data) to prevent errors
    if df_age_counts.empty:
        fig_age = px.bar(
            title="Age Distribution"
        )
    else:
        # Round percentages for cleaner display in hover text
        df_age_counts['Percentage_Display'] = df_age_counts['Percentage'].round(0).astype(int)
        fig_age = px.bar(
            df_age_counts,
            y='age_cat',                               # Age categories on y-axis
            x='Percentage',                            # Percentage values on x-axis
            title="Age Distribution",
            labels={'y': 'Age Group', 'x': 'Percentage'},
            category_orders={'age_cat': age_order},    # Ensure consistent ordering
            orientation='h',                           # Horizontal bars
            color_discrete_sequence=color,             # Location-specific color
            custom_data=['Percentage_Display']         # Data for custom hover
        )
        # Update hover template to show rounded percentages only
        fig_age.update_traces(
            hovertemplate='%{customdata[0]}%<extra></extra>'
        )

    # === GENDER DISTRIBUTION ANALYSIS ===
    # Count unique participants by gender (observed=True prevents pandas FutureWarning)
    gender_count = df_location_2023.groupby('gender', observed=True)['unique_id'].nunique().reset_index()
    
    # Handle empty data case to prevent chart errors
    if gender_count.empty:
        fig_gender = px.pie(
            gender_count,
            names='gender',
            values='unique_id',
            title="Gender Distribution",
            #category_orders={'gender': ['Female', 'Male']}  # Commented out for empty case
        )
    else:
        # Calculate rounded percentages for cleaner display
        gender_count['Percentage'] = (gender_count['unique_id'] / gender_count['unique_id'].sum() * 100).round(0).astype(int)
        fig_gender = px.pie(
            gender_count,
            names='gender',                                    # Gender labels
            values='unique_id',                                # Count values for pie sizing
            title="Gender Distribution",
            category_orders={'gender': ['Female', 'Male']},    # Consistent ordering
            hover_data=['Percentage']                          # Include percentage in hover
        )
        # Customize hover template and text display for better UX
        fig_gender.update_traces(
            hovertemplate='%{label}: %{customdata[0]}%<extra></extra>',  # Custom hover format
            customdata=gender_count[['Percentage']],                      # Percentage data
            textinfo='text',                                              # Show custom text only
            text=[f"{row['Percentage']}%" for _, row in gender_count.iterrows()],  # Display percentages
            textfont=dict(size=16, color="white"),                        # White text for visibility
            textposition="inside"                                         # Center text in pie slices
        )
    
    # === YEARS LIVED IN COMMUNITY ANALYSIS ===
    # Count participants by duration lived in community (observed=True prevents pandas FutureWarning)
    df_year_counts = df_location_2023.groupby('years_lived_cat', observed=True)['unique_id'].nunique().reset_index()
    
    # Ensure all year categories appear in chart for consistent y-axis across locations
    # This prevents missing categories when some locations have no participants in certain ranges
    all_year_categories_df = pd.DataFrame({'years_lived_cat': year_cat_order})
    df_year_counts = all_year_categories_df.merge(df_year_counts, on='years_lived_cat', how='left')
    df_year_counts['unique_id'] = df_year_counts['unique_id'].fillna(0)  # Fill missing with 0
    
    # Calculate percentages for display
    sample_size = int(df_year_counts['unique_id'].sum())
    if sample_size > 0:
        df_year_counts['Percentage'] = (df_year_counts['unique_id'] / sample_size) * 100
    else:
        df_year_counts['Percentage'] = 0  # Handle division by zero case
        
    # Round percentages for cleaner hover display
    df_year_counts['Percentage_Display'] = df_year_counts['Percentage'].round(0).astype(int)
    
    # Create horizontal bar chart with all categories (even if some are zero)
    fig_year = px.bar(df_year_counts, 
        y='years_lived_cat',                    # Year categories on y-axis
        x='Percentage',                         # Percentage values on x-axis
        title="Years Lived in Community", 
        labels={'y': 'Years', 'x': 'Percentage'},
        orientation='h',                        # Horizontal orientation
        color_discrete_sequence=color,          # Location-specific color
        custom_data=['Percentage_Display'])     # Data for custom hover
    
    # Force all categories to appear on y-axis in correct order for consistency
    fig_year.update_layout(
        yaxis=dict(
            categoryorder='array',              # Use custom ordering
            categoryarray=year_cat_order,       # Predefined order
            autorange='reversed'                # Fix axis direction (top to bottom)
        )
    )
    
    # Update hover template to show rounded percentages only
    fig_year.update_traces(
        hovertemplate='%{customdata[0]}%<extra></extra>'
    )

    # === CHART LAYOUT CUSTOMIZATION ===
    # Configure age distribution chart styling for consistent appearance
    fig_age.update_layout(
        xaxis=dict(
            title=dict(
                text="Percentage",
                font=dict(size=16, weight="bold")  # Bold axis title, theme-adaptive color
            ),
            tickfont=dict(size=14)  # Larger tick labels for readability
        ),
        yaxis=dict(
            title=dict(
                text="Age Group",
                font=dict(size=16, weight="bold")  # Bold axis title, theme-adaptive color
            ),
            tickfont=dict(size=14)  # Larger tick labels for readability
        ),
        title_x=0.25,                           # Center title positioning
        height=300,                             # Fixed chart height
        width=300,                              # Fixed chart width  
        font=dict(size=18),                     # Overall font size, theme-adaptive color
        title=dict(font=dict(size=18)),         # Title font size, theme-adaptive color
        paper_bgcolor='rgba(0,0,0,0)',          # Transparent background for theme compatibility
        plot_bgcolor='rgba(0,0,0,0)',           # Transparent plot area for theme compatibility
    )
    
    # Configure years lived chart styling (similar to age chart)
    fig_year.update_layout(
        xaxis=dict(
            title=dict(
                text="Percentage",
                font=dict(size=16, weight="bold")  # Bold axis title, theme-adaptive color
            ),
            tickfont=dict(size=14)  # Larger tick labels for readability
        ),
        yaxis=dict(
            title=dict(
                text="Year Group",
                font=dict(size=16, weight="bold")  # Bold axis title, theme-adaptive color
            ),
            tickfont=dict(size=14)  # Larger tick labels for readability
        ), 
        title_x=0.25,                           # Center title positioning  
        height=300,                             # Fixed chart height (was 400, reduced for consistency)
        width=300,                              # Fixed chart width
        font=dict(size=18),                     # Overall font size, theme-adaptive color
        title=dict(font=dict(size=18)),         # Title font size, theme-adaptive color
        paper_bgcolor='rgba(0,0,0,0)',          # Transparent background for theme compatibility
        plot_bgcolor='rgba(0,0,0,0)',           # Transparent plot area for theme compatibility
    )

    # Configure gender pie chart styling
    fig_gender.update_layout(
        title_x=0.25,                           # Center title positioning
        title_y=0.95,                           # Position title near top
        legend=dict(
            x=-0.3,                             # Position legend to the left
            y=1.0,                              # Align legend with top
            xanchor="left",                     # Anchor legend to left
            yanchor="middle",                   # Center legend vertically
            font=dict(size=14, weight="bold")   # Bold legend text, theme-adaptive color
        ),
        height=300,                             # Fixed chart height
        width=300,                              # Fixed chart width
        font=dict(size=18),                     # Overall font size, theme-adaptive color
        title=dict(font=dict(size=18)),         # Title font size, theme-adaptive color
        paper_bgcolor='rgba(0,0,0,0)',          # Transparent background for theme compatibility
        plot_bgcolor='rgba(0,0,0,0)',           # Transparent plot area for theme compatibility
    )

    # Configuration to remove toolbar/interactive elements for cleaner presentation
    config_dict = {
        'displayModeBar': False,  # Remove the plotly toolbar completely
        'staticPlot': False       # Keep charts interactive but without toolbar
    }

    # === CHART DISPLAY IN STREAMLIT INTERFACE ===
    # Display charts in vertical layout with containers for proper spacing
    
    # Age distribution chart (first chart)
    with st.container():
        st.plotly_chart(fig_age, use_container_width=True, key = f"{location}_age", config=config_dict)
        fig_age.update_layout(title={'x': 0.25})  # Ensure title centering
        fig_age.update_layout(height=300)         # Maintain consistent height

    # Gender distribution chart (second chart) 
    with st.container():
        st.plotly_chart(fig_gender, use_container_width=True, key = f"{location}_gender", config=config_dict)
        fig_gender.update_layout(title={'x': 0.25})  # Ensure title centering
        fig_gender.update_layout(height=300)         # Maintain consistent height

    # Location info box with sample size (displayed before years lived chart)
    st.markdown(f"""
        <div style="background-color: rgba(128, 128, 128, 0.1); padding: 10px; border-radius: 5px; border: 1px solid rgba(128, 128, 128, 0.3); pointer-events: none;">
            <h4 style="text-align:center; cursor: default; margin: 10px 0;">{location}</h4>
            <p style="text-align:center; cursor: default; margin: 5px 0;">Sample Size: {sample_size} participants</p>
        </div>
    """, unsafe_allow_html=True)

    # Years lived in community chart (third chart, larger for better readability)
    with st.container():
        st.plotly_chart(fig_year, use_container_width=True, key = f"{location}_year", config=config_dict)
        fig_year.update_layout(title={'x': 0.25})   # Ensure title centering
        fig_year.update_layout(height=500)          # Larger height for better category visibility

    # Debug output (commented out in production)
    #print(summary_data[summary_data['Location'] == 'Wilmington'])


st.title("GenX Exposure Study Dashboard")
# Create two-column layout: main content on left, study map on right
col1, col2 = st.columns([2, 1])
with col2:
    # Study map image (stored locally, update path if relocated)
    st.image('study map.png')
with col1:
    # === STUDY OVERVIEW SECTION ===
    st.markdown("""
The GenX Exposure Study collects blood samples and other health information from people in North Carolina that have been exposed to a man-made group of chemicals called PFAS (per- and polyfluoroalkyl substances). 

The people in the study come from three communities: Pittsboro, the lower Cape Fear River (LCFR), and the private well community outside of Fayetteville (Fayetteville). 

Each person’s sample is tested to see how much PFAS is in their blood. By collecting multiple samples over time from the same person, we can track how the levels of PFAS in their blood have changed. 
Then, by comparing samples from many people in the same community over several years, we can understand how the PFAS levels in blood across a large population are changing, too.
                
To learn more about PFAS and how the GenX Exposure Study began, check out these pages on our website:  
- [Study Overview](https://genxstudy.ncsu.edu/study-overview/)  
- [Timeline](https://genxstudy.ncsu.edu/study-timeline/)
""")

    # === HOW TO USE THIS TOOL SECTION ===
    st.subheader("How do I use this tool to learn about PFAS in North Carolina?")
    
    # CSS styling for enhanced visual presentation and theme compatibility
    st.markdown("""
    <style>
    .big-font {
        font-size:20px !important;
    }
    
    /* Dark mode compatibility improvements */
    .stApp {
        color: inherit;
    }
    
    /* Make sure text adapts to theme */
    .markdown-text-container {
        color: inherit !important;
    }
    
    /* Ensure plotly charts adapt to theme */
    .js-plotly-plot .plotly .main-svg {
        background: transparent !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # === MAIN RESEARCH QUESTIONS ===
    # Highlight the two primary questions this dashboard addresses
    st.markdown("""
    <p class="big-font">
    <b>This tool answers two main questions:</b>
    </p>
    <ul>
    <li><b>How are PFAS levels changing over time?</b></li>
    <li><b>How are PFAS levels different across these three communities?</b></li>
    </ul>
    """, unsafe_allow_html=True)

    # === FREQUENTLY ASKED QUESTIONS SECTION ===
    # Expandable FAQ sections for common user questions

    # === FREQUENTLY ASKED QUESTIONS SECTION ===
    # Expandable FAQ sections for common user questions
    #with st.expander("FAQ 1"):
        #st.write("Insert '<insert answer>")
    
    #with st.expander("FAQ 2"):
        #st.write("Insert '<insert answer>")
    
    #with st.expander("FAQ 3"):
        #st.write("Insert '<insert answer>")
    
    #with st.expander("FAQ 4"):
        #st.write("Insert '<insert answer>")
    # === DETAILED TOOL USAGE INFORMATION ===
    # Comprehensive description of dashboard capabilities and data sources
    st.markdown("""
    You can use this tool to view the PFAS concentration levels in blood for many demographics, such as age group, sex, and community. You can look at the PFAS levels for specific individual PFAS, such as PFOS, or by important groups like the NASEM 7, (the only PFAS to have official clinical guidance at this time). You can learn more about the NASEM 7 under the “Learn More” tab above.

    You can also look at PFAS concentration levels in blood by year. However, it is important to note that not all communities were sampled at the same time or every year. More information about when each community joined the study and when they have been sampled can be found on our [timeline](https://genxstudy.ncsu.edu/study-timeline/) page.

    """)

# === DATA PREPARATION FOR SUMMARY STATISTICS ===
# Create a copy of the complete dataset for demographic analysis
summary_data = complete.copy()

# === SUMMARY STATISTICS DISPLAY SECTION ===
st.title("Summary Statistics (2023)")

# Create three-column layout for side-by-side demographic comparisons
col1, col2, col3 = st.columns(3)

# === LOCATION-SPECIFIC DEMOGRAPHIC SUMMARIES ===
# Generate demographic charts for each of the three study locations
# Each location gets its own column with consistent color coding

# Pittsboro community demographics (green color scheme)
with col1:
    summary_stats(location = 'Pittsboro', summary_data=summary_data, color = ['#33bfa7'])

# Fayetteville community demographics (orange color scheme) 
with col2:
    summary_stats(location = 'Fayetteville', summary_data = summary_data, color = ['#f07f2f'])

# Lower Cape Fear Region demographics (blue color scheme)
with col3:
    summary_stats(location = 'Lower Cape Fear Region', summary_data=summary_data, color = ['#6e7ee0'])
    
