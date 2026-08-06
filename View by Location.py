"""
View by Location Tab - Geographic PFAS Comparison Analysis

This module provides location-based comparison visualizations for PFAS exposure data.
It creates interactive boxplot grids showing PFAS concentrations across different
geographic locations and time periods.

Key Features:
- Multi-location PFAS concentration comparisons
- Time series analysis with flexible year selection
- Interactive boxplots with NHANES reference data
- Grouped visualization by PFAS concentration ranges
- Consistent visual styling with enhanced borders

Functions:
- view_by_location(): Main visualization function for location-based analysis
- format_year_label(): Helper function for year label formatting

Author: [Your Name]
Last Updated: [Date]
"""

def view_by_location(pfas_range, predefined_order, selected_locations, y_max, ax, df_plot_adjusted, plot_years_numeric, plot_years_formatted, selected_years=None):
    """
    Create a grid of boxplot visualizations comparing PFAS concentrations across locations.
    
    This function generates interactive Altair boxplots for each selected location,
    showing PFAS concentration distributions over time with NHANES reference data.
    
    Args:
        pfas_range (list): List of PFAS compounds to include in this visualization group
        predefined_order (list): Ordered list of PFAS compounds for consistent legend
        selected_locations (list): Geographic locations to display
        y_max (float): Maximum y-axis value for consistent scaling
        ax: Matplotlib axis object (legacy parameter, not used in Altair implementation)
        df_plot_adjusted (pd.DataFrame): Processed dataset with PFAS concentrations
        plot_years_numeric (list): Numeric year values for filtering
        plot_years_formatted (list): Formatted year labels for display
        selected_years (list, optional): Specific years to include in analysis
    
    Returns:
        None: Displays charts directly in Streamlit interface
    """
    import altair as alt
    
    # === LAYOUT CONFIGURATION ===
    num_cols = 3  # Create 3-column grid layout for location comparisons
    cols = st.columns(num_cols)
    i = 0

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

    # === DATA FILTERING FOR PFAS RANGE ===
    # Filter dataset to include only PFAS compounds in the current concentration range
    df_range = df_plot_adjusted[df_plot_adjusted['PFAS'].isin(pfas_range)]
    
    # === LOCATION-SPECIFIC VISUALIZATION LOOP ===
    # Create individual boxplot for each selected location
    for i, loc in enumerate(selected_locations):
        # Filter data for current location
        df_plot = df_range[df_range['Location'] == loc].copy()
        
        if not df_plot.empty:
            # === YEAR LABEL FORMATTING ===
            # Apply consistent year formatting across all charts
            year_mapping = {year: format_year_label(year) for year in plot_years_numeric}
            df_plot['Year_formatted'] = df_plot['Year'].map(year_mapping)
            
            # === COLOR SCHEME CONFIGURATION ===
            # Create color mapping for PFAS compounds maintaining legend consistency
            color_domain = []
            color_range = []
            for pfas in predefined_order:  # Use predefined order to maintain consistent legend
                if pfas in df_plot['PFAS'].unique():
                    color_domain.append(pfas)
                    color_range.append(group_colors_pfas.get(pfas, '#808080'))  # Default gray if color not found
            
            # === COMPLETE YEAR RANGE HANDLING ===
            # Ensure all years in selected range appear on x-axis, even with no data
            if selected_years and len(selected_years) > 0:  # Validate selected_years is not empty
                min_year = min(selected_years)
                max_year = max(selected_years)
                
                # Create complete year range including gaps (e.g., 2017-2023 shows all years)
                complete_year_range = list(range(min_year, max_year + 1))
                complete_year_formatted = [format_year_label(y) for y in complete_year_range]
                
                # === MISSING YEAR HANDLING ===
                # Create placeholder data for years with no measurements to maintain consistent x-axis
                all_years_df = []
                for year_val in complete_year_range:
                    year_formatted = format_year_label(year_val)
                    # Add dummy rows for years with no data to ensure x-axis shows all years
                    if year_formatted not in df_plot['Year_formatted'].values:
                        # We'll let Altair handle missing data naturally
                        pass
                
            else:
                complete_year_formatted = plot_years_formatted
            
            # Create custom boxplot using individual marks to avoid persistent tooltips
            # Calculate boxplot statistics manually for complete control
            alt.data_transformers.disable_max_rows()
            
            # Create base chart
            base = alt.Chart(df_plot)
            
            # Create box (25th to 75th percentile)
            box = base.mark_bar(
                size=8,
                opacity=0.7,
                stroke='black',
                strokeWidth=1
            ).encode(
                x=alt.X('Year_formatted:O', 
                       title='Year',
                       sort=complete_year_formatted,
                       scale=alt.Scale(domain=complete_year_formatted),
                       axis=alt.Axis(labelFontSize=14, titleFontSize=15, titleFontWeight='bold')),
                y=alt.Y('lower:Q', title='Concentration (ng/mL)', 
                       scale=alt.Scale(domain=[0, y_max]),
                       axis=alt.Axis(values=[0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5]) if y_max <= 1.6 else alt.Axis()),
                y2=alt.Y2('upper:Q'),
                color=alt.Color('PFAS:N', 
                              scale=alt.Scale(domain=color_domain, range=color_range),
                              legend=None,
                              sort=predefined_order),
                xOffset=alt.XOffset('PFAS:N', sort=predefined_order),
                tooltip=[
                    alt.Tooltip('PFAS:N', title='PFAS'),
                    alt.Tooltip('Year_formatted:O', title='Year'),
                    alt.Tooltip('5th percentile:Q', title='5th Percentile (ng/mL)', format='.1f'),
                    alt.Tooltip('middle:Q', title='Median (ng/mL)', format='.1f'),
                    alt.Tooltip('95th percentile:Q', title='95th Percentile (ng/mL)', format='.1f')
                ]
            )
            
            # Create median line
            median_line = base.mark_tick(
                size=8,  # Increased from 12 to 8 for better visibility
                thickness=1,  # Increased to 1 for better visibility
                color='black',  # White color for good contrast against colored boxes
                stroke='black',  # Black border like the box
                strokeWidth=0.75,  # Same border width as box
                opacity=1  # Make visible with border
            ).encode(
                x=alt.X('Year_formatted:O', sort=complete_year_formatted),
                y=alt.Y('middle:Q', 
                       scale=alt.Scale(domain=[0, y_max]),
                       axis=alt.Axis(values=[0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5]) if y_max <= 1.6 else alt.Axis()),
                xOffset=alt.XOffset('PFAS:N', sort=predefined_order),
                tooltip=[
                    alt.Tooltip('PFAS:N', title='PFAS'),
                    alt.Tooltip('Year_formatted:O', title='Year'),
                    alt.Tooltip('5th percentile:Q', title='5th Percentile (ng/mL)', format='.1f'),
                    alt.Tooltip('middle:Q', title='Median (ng/mL)', format='.1f'),
                    alt.Tooltip('95th percentile:Q', title='95th Percentile (ng/mL)', format='.1f')
                ]
            )
            
            # Create whiskers - split into lower and upper whiskers to avoid going through box
            # Lower whisker: from 5th percentile to lower quartile (Q1)
            lower_whiskers = base.mark_rule(
                strokeWidth=1.5,
                opacity=1,
                stroke='black'
            ).encode(
                x=alt.X('Year_formatted:O', sort=complete_year_formatted),
                y=alt.Y('5th percentile:Q', 
                       scale=alt.Scale(domain=[0, y_max]),
                       axis=alt.Axis(values=[0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5]) if y_max <= 1.6 else alt.Axis()),
                y2=alt.Y2('lower:Q'),
                color=alt.Color('PFAS:N', 
                              scale=alt.Scale(domain=color_domain, range=color_range),
                              legend=None,
                              sort=predefined_order),
                xOffset=alt.XOffset('PFAS:N', sort=predefined_order),
                tooltip=[
                    alt.Tooltip('PFAS:N', title='PFAS'),
                    alt.Tooltip('Year_formatted:O', title='Year'),
                    alt.Tooltip('5th percentile:Q', title='5th Percentile (ng/mL)', format='.1f'),
                    alt.Tooltip('middle:Q', title='Median (ng/mL)', format='.1f'),
                    alt.Tooltip('95th percentile:Q', title='95th Percentile (ng/mL)', format='.1f')
                ]
            )
            
            # Upper whisker: from upper quartile (Q3) to 95th percentile
            upper_whiskers = base.mark_rule(
                strokeWidth=1.5,
                opacity=1,
                stroke='black'
            ).encode(
                x=alt.X('Year_formatted:O', sort=complete_year_formatted),
                y=alt.Y('upper:Q', 
                       scale=alt.Scale(domain=[0, y_max]),
                       axis=alt.Axis(values=[0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5]) if y_max <= 1.6 else alt.Axis()),
                y2=alt.Y2('95th percentile:Q'),
                color=alt.Color('PFAS:N', 
                              scale=alt.Scale(domain=color_domain, range=color_range),
                              legend=None,
                              sort=predefined_order),
                xOffset=alt.XOffset('PFAS:N', sort=predefined_order),
                tooltip=[
                    alt.Tooltip('PFAS:N', title='PFAS'),
                    alt.Tooltip('Year_formatted:O', title='Year'),
                    alt.Tooltip('5th percentile:Q', title='5th Percentile (ng/mL)', format='.1f'),
                    alt.Tooltip('middle:Q', title='Median (ng/mL)', format='.1f'),
                    alt.Tooltip('95th percentile:Q', title='95th Percentile (ng/mL)', format='.1f')
                ]
            )
            
            # Create min indicator (5th percentile tick)
            min_tick = base.mark_tick(
                size=6,
                thickness=0.75,
                stroke='black',  # Black border like the box
                strokeWidth=0.5
            ).encode(
                x=alt.X('Year_formatted:O', sort=complete_year_formatted),
                y=alt.Y('5th percentile:Q', 
                       scale=alt.Scale(domain=[0, y_max]),
                       axis=alt.Axis(values=[0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5]) if y_max <= 1.6 else alt.Axis()),
                color=alt.Color('PFAS:N', 
                              scale=alt.Scale(domain=color_domain, range=color_range),
                              legend=None,
                              sort=predefined_order),
                xOffset=alt.XOffset('PFAS:N', sort=predefined_order),
                tooltip=[
                    alt.Tooltip('PFAS:N', title='PFAS'),
                    alt.Tooltip('Year_formatted:O', title='Year'),
                    alt.Tooltip('5th percentile:Q', title='5th Percentile (ng/mL)', format='.1f'),
                    alt.Tooltip('middle:Q', title='Median (ng/mL)', format='.1f'),
                    alt.Tooltip('95th percentile:Q', title='95th Percentile (ng/mL)', format='.1f')
                ]
            )
            
            # Create max indicator (95th percentile tick)
            max_tick = base.mark_tick(
                size=6,
                thickness=0.75,
                stroke='black',  # Black border like the box
                strokeWidth=0.5
            ).encode(
                x=alt.X('Year_formatted:O', sort=complete_year_formatted),
                y=alt.Y('95th percentile:Q', 
                       scale=alt.Scale(domain=[0, y_max]),
                       axis=alt.Axis(values=[0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5]) if y_max <= 1.6 else alt.Axis()),
                color=alt.Color('PFAS:N', 
                              scale=alt.Scale(domain=color_domain, range=color_range),
                              legend=None,
                              sort=predefined_order),
                xOffset=alt.XOffset('PFAS:N', sort=predefined_order),
                tooltip=[
                    alt.Tooltip('PFAS:N', title='PFAS'),
                    alt.Tooltip('Year_formatted:O', title='Year'),
                    alt.Tooltip('5th percentile:Q', title='5th Percentile (ng/mL)', format='.1f'),
                    alt.Tooltip('middle:Q', title='Median (ng/mL)', format='.1f'),
                    alt.Tooltip('95th percentile:Q', title='95th Percentile (ng/mL)', format='.1f')
                ]
            )
            
            # Combine all parts
            chart = (box + median_line + lower_whiskers + upper_whiskers + min_tick + max_tick).resolve_scale(
                color='independent'
            ).properties(
                width=300,
                height=320,  # Increased from 280 to 320 to prevent title cutoff
                title=alt.TitleParams(
                    text=loc,
                    fontSize=16,
                    fontWeight='bold',
                    color='#333',
                    anchor='middle',  # Changed from 'start' to 'middle' to center the title
                    offset=20  # Add offset to prevent cutoff
                )
            ).configure_axis(
                grid=True,
                gridOpacity=0.3
            ).configure_view(
                strokeWidth=0
            )
            

            if len(selected_locations) == 1:
                col_index = 1  # middle column in a 3-column layout
            else:
                col_index = i % num_cols

            with cols[col_index]:
                st.altair_chart(chart, use_container_width=True)

            i += 1 

large_range = ["PFOS", "PFOA", "PFO5DoA"]
medium_range = ["PFHxS", "PFNA", "Nafion byproduct 2"]
small_range = ["PFDA", "PFUnDA", "MeFOSAA"]

predefined_large_order = ["PFOS", "PFOA", "PFO5DoA"]
predefined_medium_order = ["PFHxS", "PFNA", "Nafion byproduct 2"]
predefined_small_order = ["PFDA", "PFUnDA",  "MeFOSAA"]
fixed_location = ['Pittsboro', 'Fayetteville', 'Lower Cape Fear Region']

# === MAIN USER INTERFACE SECTION ===
# This section creates the interactive controls and displays for the View by Location tab

with st.container():
    # === PAGE HEADER ===
    st.title("View by Location")
    st.markdown("Compare PFAS blood serum levels across different locations with boxplots.")
    
    # === IMPORTANT USER NOTICE ===
    # Inform users about data collection timeline differences
    st.info("💡 Please note that not all communities were sampled at the same time or every year. More information about when each community joined the study and when they have been sampled can be found on our [timeline](https://genxstudy.ncsu.edu/study-timeline/) page.", icon="ℹ️")

    # === LOCATION SELECTION FILTER ===
    # Multi-select widget for choosing geographic locations to compare
    fixed_location = ['Pittsboro', 'Fayetteville', 'Lower Cape Fear Region']
    selected_locations = st.multiselect(
        "Select Location(s):",
        options=fixed_location,               # Predefined location options
        default=fixed_location,               # Default to all locations selected
        key="multiselect_location_by_location"  # Unique key for this widget
    )

    # === PFAS COMPOUND SELECTION FILTER ===
    # Multi-select widget for choosing which PFAS compounds to display
    lab_result_options = complete["PFAS"].unique().tolist()
    selected_labs = st.multiselect(
        "Select Lab Results:",
        options=lab_result_options,           # All available PFAS compounds
        default=['PFOA'],                     # Default to PFOA only
        key="multiselect_lab_by_location"     # Unique key for this widget
    )

    # === YEAR SELECTION SETUP ===
    # Prepare year options for temporal filtering
    year_options = complete["Year"].unique().tolist()

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
    
    # Select the years to display
    year = st.multiselect(
        "Select Year(s):",
        options=selectable_years,
        default=[2021, 2023],
        key="multiselect_year_by_location"
    )

    if not selected_labs or not selected_locations or not year:
        st.warning("Please select **at least one PFAS, location, and year** to view the data.")
            
        with st.expander("Interested in viewing individual PFAS and compare results by location?"):
            st.write("Select **View Individual PFAS**. Then select the specific PFAS you are interested in viewing.")

        with st.expander("Interested in viewing clinical guidance for a combination of PFAS?"):
            st.write("Select **View summed PFAS**.")

        with st.expander("What does the NHANES 95th percentile line mean?"):
            st.write("The National Health and Nutrition Examination Survey (NHANES) is a national program of studies designed to assess the health and nutritional status of adults and children in the United States. This line represents the NHANES 95th percentile value for comparison. The 95th percentile line shows which communities have PFAS levels above the 95th percentile of the NHANES data.")
            st.stop()
# sorting so that all plots show up in Pittsboro, Fayetteville, and Lower Cape Fear Region order
selected_locations = sorted(selected_locations, key = lambda x:fixed_location.index(x))

filtered_data = complete[(complete["Location"].isin(selected_locations)) & (complete["PFAS"].isin(selected_labs) & (complete["Year"].isin(year)))]

# do not show boxplot if it is detected in less that 50% of the people
detection_rates = filtered_data.groupby(['Year', "Location",  "PFAS"], observed=True)['detect'].mean().reset_index()
detection_rates.rename(columns={"detect": "detection_rate"}, inplace=True)
locations_above_50_percent = detection_rates[detection_rates["detection_rate"] > 0.5]

filtered_data = filtered_data.merge(locations_above_50_percent[['Year', "Location",  "PFAS"]], on=['Year', "Location",  "PFAS"], how='inner')

group_sizes = filtered_data.groupby(['Year', "Location",  "PFAS"], observed=True).size()
valid_groups = group_sizes[group_sizes >= 5].index
filtered_data_valid = filtered_data.set_index(['Year', "Location",  "PFAS"])
filtered_data_valid = filtered_data_valid.loc[valid_groups].reset_index()

# there is not an in-built function to clip the outliers in seaborn
# so we will calculate the 5th and 95th percentiles and then clip the data
quantiles = filtered_data_valid.groupby(['Year', "Location",  "PFAS"], observed=True)['conc'].quantile([0.05, 0.25, 0.5, 0.75, 0.95])
quantiles_unstacked = quantiles.unstack()
quantiles_unstacked.columns = ['5th percentile', 'lower', 'middle', 'upper', '95th percentile']

df_plot_adjusted = filtered_data_valid.merge(quantiles_unstacked, on=['Year', "Location",  "PFAS"], how='left')
df_plot_adjusted['conc_adjusted'] = df_plot_adjusted['conc']
df_plot_adjusted['conc_adjusted'] = df_plot_adjusted['conc_adjusted'].clip(lower=df_plot_adjusted['5th percentile'], upper=df_plot_adjusted['95th percentile'])

# First dynamic legend for large range
with st.container():
    cols = st.columns([1, 1, 1])
    with cols[1]:
        if selected_labs:
            pfas_colors = {
                'PFOS': "#85AB3D",
                'PFOA': "#e49763",
                'PFO5DoA': "#7bb594",
            }
            
            # Create legend HTML for only selected PFAS in alphabetical order
            legend_items = []
            
            # Get all selected PFAS in specific order of chart
            all_selected_pfas = [pfas for pfas in selected_labs if pfas in pfas_colors]
            
            # Create legend items
            for pfas in all_selected_pfas:
                color = pfas_colors.get(pfas, '#808080')  # Default gray if not found
                legend_items.append(f'<span style="display: inline-block; width: 20px; height: 15px; background-color: {color}; border: 1px solid #333; margin-right: 8px; vertical-align: middle;"></span><span style="font-weight: bold;">{pfas}</span>')
            
            # Join all legend items with spacing
            legend_html = '<div style="text-align: center; padding: 10px;">' + ' &nbsp;&nbsp;&nbsp; '.join(legend_items) + '</div>'
            
            st.markdown(legend_html, unsafe_allow_html=True)
        else:
            st.write("Please select at least one PFAS to view the legend")

    # Large range
    df_large = df_plot_adjusted[df_plot_adjusted['PFAS'].isin(large_range)]
    if not df_large.empty:
        # Use the same order as the legend (based on selected_labs order)
        legend_order = [pfas for pfas in selected_labs if pfas in large_range]
        view_by_location(
            pfas_range=large_range,
            predefined_order=legend_order,  # Use legend order instead of predefined order
            selected_locations=selected_locations,
            y_max=30,
            ax='ax_0',
            df_plot_adjusted=df_plot_adjusted,
            plot_years_numeric=plot_years_numeric,
            plot_years_formatted=plot_years,
            selected_years=year
        )
    
# Second dynamic legend for medium range
with st.container():
    cols = st.columns([1, 1, 1])
    with cols[1]:
        if selected_labs:
            pfas_colors = {
                'PFHxS': "#9ca4ce",
                'PFNA': "#e08617",
                'Nafion byproduct 2': "#f7c7c7",
            }
    
            # Create legend HTML for only selected PFAS in alphabetical order
            legend_items = []
            
            # Get all selected PFAS in specific order of chart
            all_selected_pfas = [pfas for pfas in selected_labs if pfas in pfas_colors]
            
            # Create legend items
            for pfas in all_selected_pfas:
                color = pfas_colors.get(pfas, '#808080')  # Default gray if not found
                legend_items.append(f'<span style="display: inline-block; width: 20px; height: 15px; background-color: {color}; border: 1px solid #333; margin-right: 8px; vertical-align: middle;"></span><span style="font-weight: bold;">{pfas}</span>')
            
            # Join all legend items with spacing
            legend_html = '<div style="text-align: center; padding: 10px;">' + ' &nbsp;&nbsp;&nbsp; '.join(legend_items) + '</div>'
            
            st.markdown(legend_html, unsafe_allow_html=True)
        else:
            st.write("Please select at least one PFAS to view the legend")

    # Medium range
    df_medium = df_plot_adjusted[df_plot_adjusted['PFAS'].isin(medium_range)]
    if not df_medium.empty:
        # Use the same order as the legend (based on selected_labs order)
        legend_order = [pfas for pfas in selected_labs if pfas in medium_range]
        view_by_location(
            pfas_range=medium_range,
            predefined_order=legend_order,  # Use legend order instead of predefined order
            selected_locations=selected_locations,
            y_max=10,
            ax='ax_1',
            df_plot_adjusted=df_plot_adjusted,
            plot_years_numeric=plot_years_numeric,
            plot_years_formatted=plot_years,
            selected_years=year
        )
  
# Third dynamic legend for small range
with st.container():
    cols = st.columns([1, 1, 1])
    with cols[1]:
        if selected_labs:
            pfas_colors = {
                'PFDA': '#5e76a7',
                'PFUnDA': "#47907F",
                'MeFOSAA': "#90a286"
            }
            
            # Create legend HTML for only selected PFAS in alphabetical order
            legend_items = []
            
            # Get all selected PFAS in specific order of chart
            all_selected_pfas = [pfas for pfas in selected_labs if pfas in pfas_colors]

            # Create legend items
            for pfas in all_selected_pfas:
                color = pfas_colors.get(pfas, '#808080')  # Default gray if not found
                legend_items.append(f'<span style="display: inline-block; width: 20px; height: 15px; background-color: {color}; border: 1px solid #333; margin-right: 8px; vertical-align: middle;"></span><span style="font-weight: bold;">{pfas}</span>')
            
            # Join all legend items with spacing
            legend_html = '<div style="text-align: center; padding: 10px;">' + ' &nbsp;&nbsp;&nbsp; '.join(legend_items) + '</div>'
            
            st.markdown(legend_html, unsafe_allow_html=True)
        else:
            st.write("Please select at least one PFAS to view the legend")

    # Small range
    df_small = df_plot_adjusted[df_plot_adjusted['PFAS'].isin(small_range)]
    if not df_small.empty:
        # Use the same order as the legend (based on selected_labs order)
        legend_order = [pfas for pfas in selected_labs if pfas in small_range]
        view_by_location(
            pfas_range=small_range,
            predefined_order=legend_order,  # Use legend order instead of predefined order
            selected_locations=selected_locations,
            y_max=1.5,
            ax='ax_2',
            df_plot_adjusted=df_plot_adjusted,
            plot_years_numeric=plot_years_numeric,
            plot_years_formatted=plot_years,
            selected_years=year
        )

# infoboxes for each chemical, would recommend adjusting layout eventually so these are more visible and not at the bottom
title = f"General {selected_labs} Overview"
columns_per_row = 3
