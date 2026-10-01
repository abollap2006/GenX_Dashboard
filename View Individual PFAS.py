"""
View Individual PFAS Tab - Single Compound Analysis

This module provides detailed analysis of individual PFAS compounds with
location-based comparisons and temporal trends. It creates interactive
visualizations focused on one PFAS at a time for detailed examination.

Key Features:
- Individual PFA# === MAIN USER INTERFACE SECTION ===
# This section creates the interactive interface for individual PFAS analysis

# === EDUCATIONAL CONTENT SECTION ===
# Provide educational resources to help users understand boxplot visualizations
st.subheader("Before You Begin: Understanding Boxplots")
st.markdown("""
"We recommend that you view this video to understand how to read a box plot. We use boxplots to share our data because they show a more ""complete picture"" than bar charts or pie graphs. With a box plot, we can share range, upper and lower values, and the median. To learn more about how to read a boxplot, watch the video below or read the document." 

""")

# === CENTERED LAYOUT FOR EDUCATIONAL CONTENT ===
# Center the image and content for better visual presentation
col1, col2, col3 = st.columns([1, 3, 1])d analysis
- Multi-location comparison for single compounds
- Time series visualization with flexible year selection
- Interactive boxplots with NHANES reference lines
- Enhanced visual styling with consistent borders

Functions:
- pfas_by_row(): Main visualization function for individual PFAS analysis
- format_year_label(): Helper function for year label formatting

Author: [Your Name]
Last Updated: [Date]
"""

def pfas_by_row(pfas_list, y_max, df_plot_adjusted, plot_years_numeric, plot_years_formatted, loc_order, selected_years, num_cols=3, plot_height=350):
    """
    Create detailed visualizations for individual PFAS compounds across locations.
    
    This function generates interactive Altair boxplots for each PFAS compound,
    showing concentration distributions across different locations and time periods
    with NHANES reference data for context.
    
    Args:
        pfas_list (list): List of PFAS compounds to visualize
        y_max (float): Maximum y-axis value for consistent scaling
        df_plot_adjusted (pd.DataFrame): Processed dataset with PFAS concentrations
        plot_years_numeric (list): Numeric year values for filtering
        plot_years_formatted (list): Formatted year labels for display
        loc_order (list): Ordered list of locations for consistent presentation
        selected_years (list): Specific years to include in analysis
        num_cols (int): Number of columns in the grid layout (default: 3)
    
    Returns:
        None: Displays charts directly in Streamlit interface
    """
    import altair as alt
    import pandas as pd
    
    # === YEAR LABEL FORMATTING FUNCTION ===
    def format_year_label(year):
        """
        Convert year to abbreviated format for cleaner display.
        
        Format: 2017, '18, '19, '20, '21, '22, 2023
        First and last years shown in full, middle years abbreviated
        
        Args:
            year (int): Full year value
            
        Returns:
            str: Formatted year label
        """
        if year == 2017 or year == 2023:
            return str(year)                    # Show full year for endpoints
        elif 2018 <= year <= 2022:
            return f"'{str(year)[2:]}"          # Abbreviated format for middle years
        else:
            return str(year)                    # Default to full year
    
    # === LAYOUT CONFIGURATION ===
    # Create grid layout for displaying multiple PFAS visualizations
    cols = st.columns(num_cols)
    i = 0

    # === INDIVIDUAL PFAS ANALYSIS LOOP ===
    # Process each PFAS compound individually for detailed analysis
    for lab in pfas_list:
        # Filter data for current PFAS compound
        df_plot = df_plot_adjusted[df_plot_adjusted['PFAS'] == lab].copy()
        
        # === DATA AVAILABILITY CHECK ===
        # Skip PFAS compounds with no data or all missing values
        if len(df_plot) == 0 or df_plot['conc_adjusted'].notna().sum() == 0:
            continue  # Skip entirely - don't show any plot for compounds with no data
        
        # === YEAR RANGE OPTIMIZATION ===
        # Get actual years with data for this specific PFAS compound
        available_years = sorted(df_plot['Year'].dropna().unique())
        
        # Optimize year range display based on data availability and user selection
        if len(available_years) > 0:
            # === SINGLE vs MULTIPLE YEAR HANDLING ===
            if len(selected_years) == 1:
                # Single year selection - use focused single-year display for better centering
                single_year = available_years[0]
                focused_years_numeric = [single_year]
                focused_years_formatted = [format_year_label(single_year)]
            else:
                # Multiple year selection - show continuous range for temporal context
                # Create continuous range from min to max selected year
                min_selected = min(selected_years)
                max_selected = max(selected_years)
                continuous_years = list(range(min_selected, max_selected + 1))
                focused_years_numeric = continuous_years
                focused_years_formatted = [format_year_label(year) for year in continuous_years]
        else:
            # === FALLBACK YEAR HANDLING ===
            # No data available - use selected years or default years as fallback
            if len(selected_years) > 1:
                min_selected = min(selected_years)
                max_selected = max(selected_years)
                focused_years_numeric = list(range(min_selected, max_selected + 1))
                focused_years_formatted = [format_year_label(year) for year in focused_years_numeric]
            else:
                focused_years_numeric = selected_years if selected_years else plot_years_numeric
                focused_years_formatted = [format_year_label(year) for year in focused_years_numeric]
        
        # Create mapping from numeric to formatted years and add formatted column
        year_mapping = {year: format_year_label(year) for year in focused_years_numeric}
        df_plot['Year_formatted'] = df_plot['Year'].map(year_mapping)
        
        # Calculate boxplot statistics manually for complete control
        alt.data_transformers.disable_max_rows()
        
        # Calculate quantiles grouped by Location and Year_formatted
        quantiles = df_plot.groupby(['Location', 'Year_formatted'], observed=True)['conc_adjusted'].quantile([0.05, 0.25, 0.5, 0.75, 0.95])
        quantiles_unstacked = quantiles.unstack()
        quantiles_unstacked.columns = ['5th percentile', 'lower', 'middle', 'upper', '95th percentile']
        quantiles_unstacked = quantiles_unstacked.reset_index()
        
        # Create base chart
        base = alt.Chart(quantiles_unstacked)
        
        # Create color mapping for locations
        location_colors = {
            'Pittsboro': "#44a482",
            'Fayetteville': '#d47200', 
            'Lower Cape Fear Region': "#5e76a7"
        }
        
        color_domain = []
        color_range = []
        for loc in ["Pittsboro", "Fayetteville", "Lower Cape Fear Region"]:
            if loc in quantiles_unstacked['Location'].unique():
                color_domain.append(loc)
                color_range.append(location_colors.get(loc, '#808080'))
        
        # Create box (25th to 75th percentile)
        box = base.mark_bar(
            size=25,
            opacity=1,
            stroke='black',
            strokeWidth=1
        ).encode(
            x=alt.X('Year_formatted:O', 
                   title='Year',
                   sort=focused_years_formatted,
                   scale=alt.Scale(domain=focused_years_formatted),
                   axis=alt.Axis(labelFontSize=14, titleFontSize=15, titleFontWeight='bold')),
            y=alt.Y('lower:Q', title='Concentration (ng/mL)', 
                   scale=alt.Scale(domain=[0, y_max]),
                   axis=alt.Axis(values=[0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5]) if y_max <= 1.6 else alt.Axis()),
            y2=alt.Y2('upper:Q'),
            color=alt.Color('Location:N', 
                          scale=alt.Scale(domain=color_domain, range=color_range),
                          legend=None),
            xOffset=alt.XOffset('Location:N', sort=["Pittsboro", "Fayetteville", "Lower Cape Fear Region"]),
            tooltip=[
                alt.Tooltip('Location:N', title='Location'),
                alt.Tooltip('Year_formatted:O', title='Year'),
                alt.Tooltip('5th percentile:Q', title='5th Percentile (ng/mL)', format='.1f'),
                alt.Tooltip('middle:Q', title='Median (ng/mL)', format='.1f'),
                alt.Tooltip('95th percentile:Q', title='95th Percentile (ng/mL)', format='.1f')
            ]
        )
        
        # Create median line
        median_line = base.mark_tick(
            size=25,
            thickness=2,
            color='black',
            stroke='black',
            strokeWidth=0.75,
            opacity=1  # Make visible with border
        ).encode(
            x=alt.X('Year_formatted:O', sort=focused_years_formatted),
            y=alt.Y('middle:Q', 
                   scale=alt.Scale(domain=[0, y_max]),
                   axis=alt.Axis(values=[0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5]) if y_max <= 1.6 else alt.Axis()),
            xOffset=alt.XOffset('Location:N', sort=["Pittsboro", "Fayetteville", "Lower Cape Fear Region"]),
            tooltip=[
                alt.Tooltip('Location:N', title='Location'),
                alt.Tooltip('Year_formatted:O', title='Year'),
                alt.Tooltip('5th percentile:Q', title='5th Percentile (ng/mL)', format='.1f'),
                alt.Tooltip('middle:Q', title='Median (ng/mL)', format='.1f'),
                alt.Tooltip('95th percentile:Q', title='95th Percentile (ng/mL)', format='.1f')
            ]
        )
        
        # Create whiskers - split into lower and upper whiskers to avoid going through box
        # Lower whisker: from 5th percentile to lower quartile (Q1)
        lower_whiskers = base.mark_rule(
            strokeWidth=2.5,
            opacity=1,
            stroke='black'
        ).encode(
            x=alt.X('Year_formatted:O', sort=focused_years_formatted),
            y=alt.Y('5th percentile:Q', 
                   scale=alt.Scale(domain=[0, y_max]),
                   axis=alt.Axis(values=[0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5]) if y_max <= 1.6 else alt.Axis()),
            y2=alt.Y2('lower:Q'),
            color=alt.Color('Location:N', 
                          scale=alt.Scale(domain=color_domain, range=color_range),
                          legend=None),
            xOffset=alt.XOffset('Location:N', sort=["Pittsboro", "Fayetteville", "Lower Cape Fear Region"]),
            tooltip=[
                alt.Tooltip('Location:N', title='Location'),
                alt.Tooltip('Year_formatted:O', title='Year'),
                alt.Tooltip('5th percentile:Q', title='5th Percentile (ng/mL)', format='.1f'),
                alt.Tooltip('middle:Q', title='Median (ng/mL)', format='.1f'),
                alt.Tooltip('95th percentile:Q', title='95th Percentile (ng/mL)', format='.1f')
            ]
        )
        
        # Upper whisker: from upper quartile (Q3) to 95th percentile
        upper_whiskers = base.mark_rule(
            strokeWidth=2.5,
            opacity=1,
            stroke='black'
        ).encode(
            x=alt.X('Year_formatted:O', sort=focused_years_formatted),
            y=alt.Y('upper:Q', 
                   scale=alt.Scale(domain=[0, y_max]),
                   axis=alt.Axis(values=[0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5]) if y_max <= 1.6 else alt.Axis()),
            y2=alt.Y2('95th percentile:Q'),
            color=alt.Color('Location:N', 
                          scale=alt.Scale(domain=color_domain, range=color_range),
                          legend=None),
            xOffset=alt.XOffset('Location:N', sort=["Pittsboro", "Fayetteville", "Lower Cape Fear Region"]),
            tooltip=[
                alt.Tooltip('Location:N', title='Location'),
                alt.Tooltip('Year_formatted:O', title='Year'),
                alt.Tooltip('5th percentile:Q', title='5th Percentile (ng/mL)', format='.1f'),
                alt.Tooltip('middle:Q', title='Median (ng/mL)', format='.1f'),
                alt.Tooltip('95th percentile:Q', title='95th Percentile (ng/mL)', format='.1f')
            ]
        )
        
        # Create min indicator (5th percentile tick)
        min_tick = base.mark_tick(
            size=18,
            thickness=1,
            stroke='black',  # Black border like the box
            strokeWidth=0.5
        ).encode(
            x=alt.X('Year_formatted:O', sort=focused_years_formatted),
            y=alt.Y('5th percentile:Q', 
                   scale=alt.Scale(domain=[0, y_max]),
                   axis=alt.Axis(values=[0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5]) if y_max <= 1.6 else alt.Axis()),
            color=alt.Color('Location:N', 
                          scale=alt.Scale(domain=color_domain, range=color_range),
                          legend=None),
            xOffset=alt.XOffset('Location:N', sort=["Pittsboro", "Fayetteville", "Lower Cape Fear Region"]),
            tooltip=[
                alt.Tooltip('Location:N', title='Location'),
                alt.Tooltip('Year_formatted:O', title='Year'),
                alt.Tooltip('5th percentile:Q', title='5th Percentile (ng/mL)', format='.1f'),
                alt.Tooltip('middle:Q', title='Median (ng/mL)', format='.1f'),
                alt.Tooltip('95th percentile:Q', title='95th Percentile (ng/mL)', format='.1f')
            ]
        )
        
        # Create max indicator (95th percentile tick)
        max_tick = base.mark_tick(
            size=18,
            thickness=1,
            stroke='black',  # Black border like the box
            strokeWidth=0.5
        ).encode(
            x=alt.X('Year_formatted:O', sort=focused_years_formatted),
            y=alt.Y('95th percentile:Q', 
                   scale=alt.Scale(domain=[0, y_max]),
                   axis=alt.Axis(values=[0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5]) if y_max <= 1.6 else alt.Axis()),
            color=alt.Color('Location:N', 
                          scale=alt.Scale(domain=color_domain, range=color_range),
                          legend=None),
            xOffset=alt.XOffset('Location:N', sort=["Pittsboro", "Fayetteville", "Lower Cape Fear Region"]),
            tooltip=[
                alt.Tooltip('Location:N', title='Location'),
                alt.Tooltip('Year_formatted:O', title='Year'),
                alt.Tooltip('5th percentile:Q', title='5th Percentile (ng/mL)', format='.1f'),
                alt.Tooltip('middle:Q', title='Median (ng/mL)', format='.1f'),
                alt.Tooltip('95th percentile:Q', title='95th Percentile (ng/mL)', format='.1f')
            ]
        )
        
        # Add NHANES reference line if available
        nhanes_layer = alt.Chart(pd.DataFrame({'y': [0]})).mark_rule(color='darkred', size=2).encode(y=alt.Y('y:Q'))
        try:
            if lab in nhanes['pfas'].values:
                selected_chemical = nhanes.loc[nhanes['pfas'] == lab, 'median'].iloc[0]
                nhanes_layer = alt.Chart(pd.DataFrame({'y': [selected_chemical]})).mark_rule(
                    color='darkred', 
                    size=2,
                    strokeDash=[5, 5]
                ).encode(y=alt.Y('y:Q'))
            else:
                nhanes_layer = alt.Chart(pd.DataFrame({'y': [0]})).mark_rule(color='darkred', size=0).encode(y=alt.Y('y:Q'))
        except:
            nhanes_layer = alt.Chart(pd.DataFrame({'y': [0]})).mark_rule(color='darkred', size=0).encode(y=alt.Y('y:Q'))
        
        ##### COMMENT OUT TO REPLACE
        # Combine all parts
        #chart = (box + median_line + lower_whiskers + upper_whiskers + min_tick + max_tick + nhanes_layer).resolve_scale(
            #color='independent'
        #).properties(
            #width=300,
            #height=320,
            #title=alt.TitleParams(
                #text=lab,
                #fontSize=16,
                #fontWeight='bold',
                #color='#333',
                #anchor='middle',
                #offset=20
            #)
        #).configure_axis(
            #grid=True,
            #gridOpacity=0.3
        #).configure_view(
            #strokeWidth=0
        #)

# Combine all parts
        chart = (box + median_line + lower_whiskers + upper_whiskers + min_tick + max_tick + nhanes_layer).resolve_scale(
            color='independent'
        ).properties(
            height=plot_height, # <-- Uses the passed plot_height parameter now!
            title=alt.TitleParams(
                text=lab,
                fontSize=16,
                fontWeight='bold',
                color='#333',
                anchor='middle',
                offset=20
            )
        ).configure_axis(
            grid=True,
            gridOpacity=0.3
        ).configure_view(
            strokeWidth=0
        )

##### ===== COMMENT OUT FOLLOWING CODE TO REPLACE WITH DYNAMIC CENTERING === #####
        #col_idx = i % num_cols
        #with cols[col_idx]:
            #st.altair_chart(chart, use_container_width=True)

        #i += 1

# === DYNAMIC CENTERING FOR PLOTS ===
        num_plots = len(pfas_list)
        if num_plots == 0:
            return

        # If 1 plot is selected, center it using a 3-column split [1, 2, 1]
        if num_plots == 1:
            c1, c2, c3 = st.columns([1, 2, 1])
            with c2:
                st.altair_chart(chart, use_container_width=True)
        # If 2 plots are selected, center them in a 4-column split [0.5, 2, 2, 0.5]
        elif num_plots == 2:
            c1, c2, c3, c4 = st.columns([0.5, 2, 2, 0.5])
            with c2 if i == 0 else c3:
                st.altair_chart(chart, use_container_width=True)
        # If 3 or more plots, use standard grid columns
        else:
            cols = st.columns(num_cols)
            col_idx = i % num_cols
            with cols[col_idx]:
                st.altair_chart(chart, use_container_width=True)

        i += 1


# Placeholder for boxplot infographic
# I would recommend updating this infographic to be a image of an actual boxplot from this dashboard
st.subheader("Before You Begin: Understanding Boxplots")
st.markdown("""
We recommend that you view this video to understand how to read a box plot. We use boxplots to share our data because they show a more “complete picture” than bar charts or pie graphs. With a box plot, we can share range, upper and lower values, and the median. To learn more about how to read a boxplot, watch the video below or read the document. 

""")
# Center the image and content
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    # Center the image using Streamlit's native centering
    st.image('Median.png', caption="Boxplot Infographic", use_container_width=True)
    
    # Center the video link
    st.markdown(
        '<div style="text-align: center;">'
        '<a href="https://www.youtube.com/watch?v=b2C9I8HuCe4&t=3s" target="_blank" style="font-size: 22px; font-weight: bold;">'
        'Watch the Boxplot Video</a></div>',
        unsafe_allow_html=True
    )
    
    # Center the disclaimer on one line with nowrap
    st.markdown("""
    <div style="text-align: center; font-size: 16px; color: #666; margin-top: 10px; white-space: nowrap;">
    <strong>Disclaimer:</strong> This video is produced and owned by Khan Academy and is not affiliated with the GenX Exposure Study.
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)  # <-- Add this line for spacing
st.markdown("""
<div style="font-size: 16px;">
Note: The boxplot infographic is a general overview of how to read a boxplot. The boxplots in this dashboard may look different because they are based on real data and may have different ranges, medians, and outliers.
Additionally, the red lines represent the median NHANES 95th percentile for each PFAS, which is a reference point for comparison.
</div>

""", unsafe_allow_html=True)



unique_pfas = ['PFOS', 'PFOA', 'PFHxS', 'PFNA', 'PFDA', 'PFUnDA', 'MeFOSAA', 'PFO5DoA', 'Nafion byproduct 2']

# Step-by-step guided selection with borders and limited width
st.markdown("### 📋 Data Selection Guide")
st.markdown("Please follow these steps to select your data:")

# Add custom CSS to constrain dropdowns and remove centering for selection guide
st.markdown("""
<style>
.main .block-container {
    max-width: 100%;
}
.stMultiSelect {
    max-width: 40%;
    margin: 0;
    display: block;
}
.stMultiSelect > div {
    margin: 0;
}
</style>
""", unsafe_allow_html=True)

# Step 1: PFAS Selection
st.markdown("#### Step 1: Choose PFAS Compounds")

lab_results = st.multiselect(
    "Select PFAS (Up to 9):", 
    options=unique_pfas, 
    max_selections=9,
    default=['PFOA'],  # Set default to only PFOA
    help="Choose the PFAS compounds you want to analyze. We recommend starting with PFOA."
)

large_range = ["PFOS", "PFOA", "PFO5DoA"]
medium_range = ["PFHxS", "PFNA", "Nafion byproduct 2"]
small_range = ["PFDA", "PFUnDA", "MeFOSAA"]
predefined_large_order = ["PFOS", "PFOA", "PFO5DoA"]
predefined_medium_order = ["PFHxS", "PFNA", "Nafion byproduct 2"]
predefined_small_order = ["PFDA", "PFUnDA",  "MeFOSAA"]
fixed_location = ['Pittsboro', 'Fayetteville', 'Lower Cape Fear Region']

selected_medium = sorted(
    [lab for lab in lab_results if lab in ["PFHxS", "PFNA", "Nafion byproduct 2"]],
    key=lambda x: predefined_medium_order.index(x) if x in predefined_medium_order else len(predefined_medium_order)
)

selected_small = sorted(
    [lab for lab in lab_results if lab in ["PFDA", "PFUnDA", "MeFOSAA"]],
    key=lambda x: predefined_small_order.index(x) if x in predefined_small_order else len(predefined_small_order)
)

selected_large = sorted(
    [lab for lab in lab_results if lab in ["PFOS", "PFOA", "PFO5DoA"]],
    key=lambda x: predefined_large_order.index(x) if x in predefined_large_order else len(predefined_large_order)
)

# Step 2: Location Selection (only show if PFAS selected)
if lab_results:
    st.markdown("#### Step 2: Choose Locations")
    
    location_options = complete["Location"].unique().tolist()

    location = st.multiselect("Select Location(s):", 
                                    options = location_options,
                                    default=location_options,
                                    help="Choose which locations to include in your analysis.")
    
else:
    st.markdown("#### Step 2: Choose Locations")
    st.info("👆 Please select PFAS compounds first to continue.")
    location = []

# Step 3: Year Selection (only show if both PFAS and location selected)
if location:
    st.markdown("#### Step 3: Choose Years")
    
    # Function to convert years to abbreviated format
    def format_year_label(year):
        """Convert year to abbreviated format: 2017, '18, '19, '20, '21, '22, 2023"""
        if year == 2017 or year == 2023:
            return str(year)
        elif 2018 <= year <= 2022:
            return f"'{str(year)[2:]}"
        else:
            return str(year)
    
    # All years for plotting (including placeholders)
    plot_years_numeric = sorted(set(list(complete['Year'].unique()) + [2018, 2022]))
    plot_years = [format_year_label(year) for year in plot_years_numeric]

    # Only real years for selection (exclude 2018 and 2022)
    selectable_years = sorted([y for y in complete['Year'].unique() if y not in [2018, 2022]])

    year = st.multiselect(
        "Select Year(s):",
        options=selectable_years,
        default=selectable_years,
        help="Choose which years to include in your analysis."
    )
    
else:
    st.markdown("#### Step 3: Choose Years")
    st.info("👆 Please select locations first to continue.")
    year = []
    plot_years_numeric = []
    plot_years = []

# Build a continuous range of years between min and max selected
if year:
    min_year = min(year)
    max_year = max(year)
    plot_years_numeric = list(range(min_year, max_year + 1))
    
    # Function to convert years to abbreviated format
    def format_year_label(year):
        """Convert year to abbreviated format: 2017, '18, '19, '20, '21, '22, 2023"""
        if year == 2017 or year == 2023:
            return str(year)
        elif 2018 <= year <= 2022:
            return f"'{str(year)[2:]}"
        else:
            return str(year)
    
    plot_years = [format_year_label(year) for year in plot_years_numeric]
else:
    plot_years_numeric = []
    plot_years = []

if not lab_results or not year or not location:
    st.warning("Please complete all three steps above to view the data.")

    with st.expander("Interested in viewing individual PFAS and compare results by location?"):
        st.write("Select **View Individual PFAS**. Then select the specific PFAS you are interested in viewing.")
    
    with st.expander("Interested in viewing clinical guidance for a combination of PFAS?"):
        st.write("Select **View summed PFAS**.")
    
    with st.expander("What does the NHANES 95th percentile line mean?"):
        st.write("The National Health and Nutrition Examination Survey (NHANES) is a national program of studies designed to assess the health and nutritional status of adults and children in the United States. This line represents the NHANES 95th percentile value for comparison. The 95th percentile line shows which communities have PFAS levels above the 95th percentile of the NHANES data.")
        st.stop()

# Add note about different scales
st.info("📊 **Note:** Each row of charts uses a different scale on the y-axis to better show the data patterns for PFAS with different concentration ranges. Please check the y-axis scale when comparing between different PFAS compounds.")

cols = st.columns([1, 1, 1])
# Dynamic legend that updates based on ONLY the selected locations
with cols[1]:
    if location:  # Only create legend if locations are selected
        # Simple HTML-based dynamic legend that will always work
        #st.markdown("**Location**")
        
        # Define colors for each location (matching the exact colors from the plots)
        location_colors = {
            'Pittsboro': "#44a482",      # Darker green (matches the chart legend exactly)
            'Fayetteville': '#d47200',   # Darker orange (matches the chart legend exactly)
            'Lower Cape Fear Region': "#5e76a7"            # Darker blue (matches the chart legend exactly)
        }
        
        # Create legend HTML for only selected locations in alphabetical order
        legend_items = []
        # Sort locations to match proper order: Pittsboro, Fayetteville, Lower Cape Fear Region
        sorted_locations = []
        order = ["Pittsboro", "Fayetteville", "Lower Cape Fear Region"]
        for loc in order:
            if loc in location:
                sorted_locations.append(loc)
        for loc in sorted_locations:
            color = location_colors.get(loc, '#808080')
            # Display Lower Cape Fear Region 
            display_name = "Lower Cape Fear Region" if loc == "Lower Cape Fear Region" else loc
            legend_items.append(f'<div style="display: inline-block; margin: 5px 15px; white-space: nowrap;"><span style="display: inline-block; width: 20px; height: 15px; background-color: {color}; border: 1px solid #333; margin-right: 8px; vertical-align: middle;"></span><span style="font-weight: bold; font-size: 16px;">{display_name}</span></div>')
        
        # Join all legend items on the same line with no wrapping
        legend_html = f'''
        <div style="text-align: center; padding: 15px; min-height: 50px; display: flex; flex-wrap: nowrap; justify-content: center; align-items: center; gap: 10px;">
            {"".join(legend_items)}
        </div>
        '''
        
        st.markdown(legend_html, unsafe_allow_html=True)
    else:
        st.write("Please select at least one location to view the legend")

filtered_data = complete.copy()
filtered_data = filtered_data[filtered_data["Location"].isin(location)]
filtered_data = filtered_data[filtered_data["PFAS"].isin(lab_results)]
filtered_data = filtered_data[filtered_data["Year"].isin(year)]

# First, let's add some debugging information about data availability
if len(filtered_data) == 0:
    st.error("No data available for the selected combination of locations, PFAS, and years.")
    st.stop()
    
# Add debugging info for location-specific issues
data_by_location = filtered_data.groupby(['Location', 'PFAS'], observed=True).size().reset_index()
data_by_location.columns = ['Location', 'PFAS', 'Count']
if len(location) == 1 and data_by_location['Count'].sum() == 0:
    st.error(f"No data found for {location[0]} with selected PFAS compounds and years. This location may not have data for the selected criteria.")
    st.stop()

# Filter for locations with a detection rate greater than 50% for each PFAS and Location
# For multi-year selections, check detection rates per year to avoid filtering out good years
detection_rates = filtered_data.groupby(["PFAS", "Location", "Year"], observed=True)["detect"].mean().reset_index()
detection_rates.rename(columns={"detect": "detection_rate"}, inplace=True)
locations_above_50_percent = detection_rates[detection_rates["detection_rate"] > 0.50]

# Add debugging information for location changes
if len(locations_above_50_percent) == 0:
    st.warning("⚠️ No PFAS-location-year combinations meet the 50% detection threshold. Using all available data.")
    filtered_data_detected = filtered_data.copy()
else:
    # Merge the detection rates back into the filtered data to keep only combinations with > 50% detection
    filtered_data_detected = filtered_data.merge(locations_above_50_percent[['PFAS', 'Location', 'Year']], on=['PFAS', 'Location', 'Year'], how='inner')
    
    # If no data remains after detection filtering, fall back to original data with warning
    if len(filtered_data_detected) == 0:
        st.warning("⚠️ Detection rate filtering removed all data. Using all available data for selected criteria.")
        filtered_data_detected = filtered_data.copy()

# Check for group sizes, but be more lenient about filtering
group_sizes = filtered_data_detected.groupby(['Year', 'Location', 'PFAS', 'age_cat', 'gender'], observed=True).size()

# Instead of requiring 5+ samples per group, let's be more flexible
# We'll use groups with 2+ samples for plotting to ensure data shows when location changes
valid_groups = group_sizes[group_sizes >= 2].index
filtered_data_valid = filtered_data_detected.set_index(['Year', 'Location', 'PFAS', 'age_cat', 'gender'])

try:
    filtered_data_valid = filtered_data_valid.loc[valid_groups].reset_index()
    # If we have very little data after filtering, add a warning but continue
    if len(filtered_data_valid) < 10:
        st.warning("⚠️ Limited data available for selected criteria. Some plots may show small sample sizes.")
except KeyError:
    # If no groups meet the criteria, use all detected data but add a warning
    st.warning("⚠️ Some plots may show limited data due to small sample sizes.")
    filtered_data_valid = filtered_data_detected.copy()

# Calculate quantiles for valid groups
if len(filtered_data_valid) > 0:
    try:
        quantiles = filtered_data_valid.groupby(['Year', 'Location', 'PFAS', 'age_cat', 'gender'], observed=True)['conc'].quantile([0.05, 0.25, 0.5, 0.75, 0.95])
        quantiles_unstacked = quantiles.unstack()
        quantiles_unstacked.columns = ['5th percentile', 'lower', 'middle', 'upper', '95th percentile']
        
        # Merge the quantiles back into the filtered data
        df_plot_adjusted = filtered_data_valid.merge(quantiles_unstacked, on=['Year', 'Location', 'PFAS', 'age_cat', 'gender'], how='left')
    except Exception as e:
        st.warning(f"Issue calculating quantiles: {str(e)}. Using raw data.")
        df_plot_adjusted = filtered_data_valid.copy()
        # Create dummy quantile columns
        df_plot_adjusted['5th percentile'] = df_plot_adjusted['conc']
        df_plot_adjusted['95th percentile'] = df_plot_adjusted['conc']
else:
    st.error("No valid data groups found for the selected criteria.")
    st.stop()

age_order = ["6-17", "18-50", "51-70", ">70"]
df_plot_adjusted['age_cat'] = pd.Categorical(df_plot_adjusted['age_cat'], categories=age_order, ordered=True)
df_plot_adjusted['Year'] = pd.Categorical(df_plot_adjusted['Year'])
df_plot_adjusted = df_plot_adjusted.copy()  

# Adjust the conc values to ensure that values below the 5th percentile are set to the 5th percentile
# and values above the 95th percentile are set to the 95th percentile
df_plot_adjusted['conc_adjusted'] = df_plot_adjusted['conc']
df_plot_adjusted['conc_adjusted'] = df_plot_adjusted['conc_adjusted'].clip(lower=df_plot_adjusted['5th percentile'], upper=df_plot_adjusted['95th percentile'])

num_large = len(selected_large)
num_medium= len(selected_medium)
num_small = len(selected_small)

num_cols = 3
num_rows = (num_large + num_medium + num_small + num_cols - 1) // num_cols 

plot_height = 350  

# Comment out the following code to center the plot
#cols = st.columns(num_cols)
#i = 0

pfas_by_row(selected_large, y_max=30, num_cols=3, df_plot_adjusted=df_plot_adjusted, plot_years_numeric=plot_years_numeric, plot_years_formatted=plot_years, loc_order=location_options, selected_years=year, plot_height=plot_height)
pfas_by_row(selected_medium, y_max=10, num_cols=3, df_plot_adjusted=df_plot_adjusted, plot_years_numeric=plot_years_numeric, plot_years_formatted=plot_years, loc_order=location_options, selected_years=year, plot_height=plot_height)
pfas_by_row(selected_small, y_max=1.6, num_cols=3, df_plot_adjusted=df_plot_adjusted, plot_years_numeric=plot_years_numeric, plot_years_formatted=plot_years, loc_order=location_options, selected_years=year, plot_height=plot_height)

# Add information about data availability
#st.markdown("---")
#st.markdown("### 📊 Data Availability Notes")

# Check which PFAS-location combinations have no data
available_combinations = df_plot_adjusted.groupby(['PFAS', 'Location'], observed=True).size().reset_index()
available_combinations = available_combinations[available_combinations[0] > 0]

missing_info = []
for pfas in lab_results:
    available_locations = available_combinations[available_combinations['PFAS'] == pfas]['Location'].tolist()
    missing_locations = [loc for loc in location if loc not in available_locations]
    
    if missing_locations:
        if pfas in ['PFO5DoA', 'Nafion byproduct 2'] and 'Pittsboro' in missing_locations:
            missing_info.append(f"• **{pfas}**: No testing conducted in {', '.join(missing_locations)}")
        elif pfas == 'MeFOSAA' and 'Pittsboro' in missing_locations:
            missing_info.append(f"• **{pfas}**: No testing conducted in {', '.join(missing_locations)}")
        elif len(missing_locations) > 0:
            missing_info.append(f"• **{pfas}**: Limited or no data available for {', '.join(missing_locations)} in selected years")

if missing_info:
    # Display each missing info item on separate lines
    info_text = "\n\n".join(missing_info)
    st.info(info_text)

# Check for year-specific limitations
year_limitations = []
for pfas in ['PFDA', 'PFUnDA', 'MeFOSAA']:
    if pfas in lab_results:
        pfas_data = df_plot_adjusted[df_plot_adjusted['PFAS'] == pfas]
        if len(pfas_data) > 0:
            available_years = sorted(pfas_data['Year'].dropna().unique())
            if len(available_years) > 0 and min(available_years) > min(year):
                year_limitations.append(f"• **{pfas}**: Testing began in {min(available_years)}")

if year_limitations:
    # Display year limitations with proper formatting
    timeline_text = "**Sampling Timeline Notes:**\n\n" + "\n\n".join(year_limitations)
    st.info(timeline_text)

title = f"General {lab_results} Overview"
columns_per_row = 3

all_combos = pd.MultiIndex.from_product(
    [plot_years, location, lab_results, age_order, gender_order],
    names=['Year', 'Location', 'PFAS', 'age_cat', 'gender']
).to_frame(index=False)
