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


def view_by_location(pfas_range, predefined_order, selected_locations, ax, df_plot_adjusted, plot_years_numeric, plot_years_formatted, selected_years=None):
    import math as math
    import pandas as pd
    import altair as alt
    
    num_cols = 3  
    cols = st.columns(num_cols)
    i = 0

    def calc_nice_y_axis(max_value, target_ticks=6, headroom=1.05):
        """
        Compute a round-number axis max and matching tick values for dynamic scaling.
        """
        if max_value is None or pd.isna(max_value) or max_value <= 0:
            max_value = 1

        padded_max = max_value * headroom
        raw_step = padded_max / target_ticks
        magnitude = 10 ** math.floor(math.log10(raw_step))
        normalized = raw_step / magnitude

        if normalized <= 1:
            nice_step = 1 * magnitude
        elif normalized <= 2:
            nice_step = 2 * magnitude
        elif normalized <= 2.5:
            nice_step = 2.5 * magnitude
        elif normalized <= 5:
            nice_step = 5 * magnitude
        else:
            nice_step = 10 * magnitude

        nice_max = math.ceil(padded_max / nice_step) * nice_step
        num_ticks = int(round(nice_max / nice_step)) + 1
        tick_values = [round(i * nice_step, 10) for i in range(num_ticks)]

        return nice_max, tick_values

    def format_year_label(year):
        if year == 2017 or year == 2023:
            return str(year)
        elif 2018 <= year <= 2022:
            return f"'{str(year)[2:]}"
        else:
            return str(year)

    df_range = df_plot_adjusted[df_plot_adjusted['PFAS'].isin(pfas_range)]
    
    for i, loc in enumerate(selected_locations):
        df_plot = df_range[df_range['Location'] == loc].copy()
        
        if not df_plot.empty:
            year_mapping = {year: format_year_label(year) for year in plot_years_numeric}
            df_plot['Year_formatted'] = df_plot['Year'].map(year_mapping)
            
            color_domain = []
            color_range = []
            for pfas in predefined_order:
                if pfas in df_plot['PFAS'].unique():
                    color_domain.append(pfas)
                    color_range.append(group_colors_pfas.get(pfas, '#808080'))
            
            if selected_years and len(selected_years) > 0:
                min_year = min(selected_years)
                max_year = max(selected_years)
                complete_year_range = list(range(min_year, max_year + 1))
                complete_year_formatted = [format_year_label(y) for y in complete_year_range]
            else:
                complete_year_formatted = plot_years_formatted
            
            # === DYNAMIC Y-AXIS SCALING FOR THIS SPECIFIC LOCATION PLOT ===
            loc_max_whisker = df_plot['95th percentile'].max()
            dynamic_y_max, dynamic_ticks = calc_nice_y_axis(loc_max_whisker)

            alt.data_transformers.disable_max_rows()
            base = alt.Chart(df_plot)
            
            # Box
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
                       scale=alt.Scale(domain=[0, dynamic_y_max]),
                       axis=alt.Axis(values=dynamic_ticks)),
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
            
            # Median line
            median_line = base.mark_tick(
                size=8,
                thickness=1,
                color='black',
                stroke='black',
                strokeWidth=0.75,
                opacity=1
            ).encode(
                x=alt.X('Year_formatted:O', sort=complete_year_formatted),
                y=alt.Y('middle:Q', 
                       scale=alt.Scale(domain=[0, dynamic_y_max]),
                       axis=alt.Axis(values=dynamic_ticks)),
                xOffset=alt.XOffset('PFAS:N', sort=predefined_order),
                tooltip=[
                    alt.Tooltip('PFAS:N', title='PFAS'),
                    alt.Tooltip('Year_formatted:O', title='Year'),
                    alt.Tooltip('5th percentile:Q', title='5th Percentile (ng/mL)', format='.1f'),
                    alt.Tooltip('middle:Q', title='Median (ng/mL)', format='.1f'),
                    alt.Tooltip('95th percentile:Q', title='95th Percentile (ng/mL)', format='.1f')
                ]
            )
            
            # Lower Whiskers
            lower_whiskers = base.mark_rule(
                strokeWidth=1.5,
                opacity=1,
                stroke='black'
            ).encode(
                x=alt.X('Year_formatted:O', sort=complete_year_formatted),
                y=alt.Y('5th percentile:Q', 
                       scale=alt.Scale(domain=[0, dynamic_y_max]),
                       axis=alt.Axis(values=dynamic_ticks)),
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
            
            # Upper Whiskers
            upper_whiskers = base.mark_rule(
                strokeWidth=1.5,
                opacity=1,
                stroke='black'
            ).encode(
                x=alt.X('Year_formatted:O', sort=complete_year_formatted),
                y=alt.Y('upper:Q', 
                       scale=alt.Scale(domain=[0, dynamic_y_max]),
                       axis=alt.Axis(values=dynamic_ticks)),
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
            
            # Min Tick
            min_tick = base.mark_tick(
                size=6,
                thickness=0.75,
                stroke='black',
                strokeWidth=0.5
            ).encode(
                x=alt.X('Year_formatted:O', sort=complete_year_formatted),
                y=alt.Y('5th percentile:Q', 
                       scale=alt.Scale(domain=[0, dynamic_y_max]),
                       axis=alt.Axis(values=dynamic_ticks)),
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
            
            # Max Tick
            max_tick = base.mark_tick(
                size=6,
                thickness=0.75,
                stroke='black',
                strokeWidth=0.5
            ).encode(
                x=alt.X('Year_formatted:O', sort=complete_year_formatted),
                y=alt.Y('95th percentile:Q', 
                       scale=alt.Scale(domain=[0, dynamic_y_max]),
                       axis=alt.Axis(values=dynamic_ticks)),
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
            
            chart = (box + median_line + lower_whiskers + upper_whiskers + min_tick + max_tick).resolve_scale(
                color='independent'
            ).properties(
                width=300,
                height=320,
                title=alt.TitleParams(
                    text=loc,
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

            if len(selected_locations) == 1:
                col_index = 1
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
        legend_order = [pfas for pfas in selected_labs if pfas in large_range]
        view_by_location(
            pfas_range=large_range,
            predefined_order=legend_order,
            selected_locations=selected_locations,
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
        legend_order = [pfas for pfas in selected_labs if pfas in medium_range]
        view_by_location(
            pfas_range=medium_range,
            predefined_order=legend_order,
            selected_locations=selected_locations,
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
        legend_order = [pfas for pfas in selected_labs if pfas in small_range]
        view_by_location(
            pfas_range=small_range,
            predefined_order=legend_order,
            selected_locations=selected_locations,
            ax='ax_2',
            df_plot_adjusted=df_plot_adjusted,
            plot_years_numeric=plot_years_numeric,
            plot_years_formatted=plot_years,
            selected_years=year
        )

# infoboxes for each chemical, would recommend adjusting layout eventually so these are more visible and not at the bottom
title = f"General {selected_labs} Overview"
columns_per_row = 3

st.markdown("""
*Please note, PFAS levels in blood are generally decreasing because exposure to certain PFAS is generally decreasing. The data included in this dashboard currently reflects blood sampling collected by the GenX Exposure Study from 2017-2023. This dashboard does NOT include PFAS in water data.*
""")