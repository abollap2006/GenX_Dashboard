"""
View Summed PFAS Tab - NASEM 7 Combined Exposure Analysis

This module provides analysis of combined PFAS exposure using the NASEM 7 compounds
that have official clinical guidance. It creates visualizations showing cumulative
PFAS exposure levels across locations and time periods.

Key Features:
- NASEM 7 combined PFAS exposure analysis
- Clinical guidance threshold visualization
- Multi-location and temporal comparisons
- Interactive boxplots with NHANES reference data
- Population health risk assessment tools

The NASEM 7 compounds include:
PFOA, PFOS, PFHxS, PFNA, PFDA        fig_comparison.update_yaxes(
            range=[0, 51],
            tick0=0,           
            dtick=10,              
            showgrid=True,       
            gridwidth=1,
            griddash = 'dot',
            gridcolor='lightgray'  
        )
        
        fig_comparison.update_xaxes(
            tickmode='array',
            tickvals=list(comparison_year_positions.values()),  # Use position indices
            ticktext=[format_year_label(year) for year in sorted(comparison_years)],  # Use formatted labels
            range=[-0.5, len(comparison_years) - 0.5]  # Constrain to position range
        )A

Author: [Your Name]
Last Updated: [Date]
"""

######### Question: What is complete???? #########

import streamlit as st
import pandas as pd
import plotly.express as px



# Function to process raw NHANES data and create comparison plots
def process_nhanes_raw_data(raw_data_path="P_PFAS.xlsx - Sheet1.csv"): ## Question: Where is this data ????
    """
    Process raw NHANES PFAS data and create summed NASEM 7 concentrations
    """
    import pandas as pd
    import streamlit as st
    
    try: # Try to run this code — if something breaks, we’ll handle it later.
        # Load raw NHANES data
        raw_data = pd.read_csv(raw_data_path)
        
        # Map raw data columns to PFAS names based on NHANES coding
        pfas_column_mapping = {
            'LBXPFDE': 'PFDA',   # Perfluorodecanoic acid
            'LBXPFHS': 'PFHxS',  # Perfluorohexane sulfonic acid
            'LBXPFNA': 'PFNA',   # Perfluorononanoic acid
            'LBXPFUA': 'PFUnDA', # Perfluoroundecanoic acid
            'LBXNFOA': 'PFOA',   # Perfluorooctanoic acid (linear)
            'LBXBFOA': 'PFOA',   # Perfluorooctanoic acid (branched)
            'LBXNFOS': 'PFOS',   # Perfluorooctane sulfonic acid (linear)
            'LBXMFOS': 'MeFOSAA' # Methyl perfluorooctane sulfonamido acetic acid
        }
        
        # Detection flag columns (1 = below detection limit, 0 = detected)
        detection_flags = {
            'LBXPFDE': 'LBDPFDEL',
            'LBXPFHS': 'LBDPFHSL', 
            'LBXPFNA': 'LBDPFNAL',
            'LBXPFUA': 'LBDPFUAL',
            'LBXNFOA': 'LBDNFOAL',
            'LBXBFOA': 'LBDBFOAL',
            'LBXNFOS': 'LBDNFOSL',
            'LBXMFOS': 'LBDMFOSL'
        }
        
        # NASEM 7 PFAS
        nasem7_pfas = ["PFOS", "PFOA", "PFHxS", "PFNA", "PFDA", "PFUnDA", "MeFOSAA"]
        
        # Process raw data to create summed concentrations
        processed_data = []
        
        for _, row in raw_data.iterrows():
            # Skip if no survey weight (invalid participant)
            if pd.isna(row['WTSBAPRP']) or row['WTSBAPRP'] == 0:
                continue
                
            nasem7_sum = 0
            detected_compounds = 0
            
            # Track which compounds we've already processed for PFOA (to avoid double counting)
            pfoa_processed = False
            
            for col, pfas_name in pfas_column_mapping.items():
                if pfas_name in nasem7_pfas and col in raw_data.columns:
                    conc = row[col]
                    detection_flag = row.get(detection_flags.get(col, ''), 1)
                    
                    # Only include if detected (flag = 0) and concentration > 0
                    if detection_flag == 0 and pd.notna(conc) and conc > 0:
                        if pfas_name == 'PFOA':
                            if not pfoa_processed:
                                # For PFOA, sum both linear and branched
                                pfoa_total = 0
                                if row.get('LBDNFOAL', 1) == 0 and pd.notna(row.get('LBXNFOA', 0)):
                                    pfoa_total += row.get('LBXNFOA', 0)
                                if row.get('LBDBFOAL', 1) == 0 and pd.notna(row.get('LBXBFOA', 0)):
                                    pfoa_total += row.get('LBXBFOA', 0)
                                if pfoa_total > 0:
                                    nasem7_sum += pfoa_total
                                    detected_compounds += 1
                                pfoa_processed = True
                        else:
                            nasem7_sum += conc
                            detected_compounds += 1
            
            # Only include if at least some NASEM 7 compounds were detected
            if detected_compounds > 0:
                processed_data.append({
                    'SEQN': row['SEQN'],
                    'Location': 'NHANES (National)',
                    'Year': 2018,  # NHANES 2017-2018 cycle
                    'conc_sum': nasem7_sum,
                    'detected_compounds': detected_compounds,
                    'survey_weight': row['WTSBAPRP']
                })
        
        nhanes_df = pd.DataFrame(processed_data)
        return nhanes_df
        
    except FileNotFoundError: # If the try block didn't work, it is because the data was not found
        st.error("Raw NHANES data file not found. Please ensure 'P_PFAS.xlsx - Sheet1.csv' is in the correct location.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error processing raw NHANES data: {str(e)}")
        return pd.DataFrame()

# === STUDY OVERVIEW SECTION ===
st.markdown("""
### What are the NASEM 7?
In 2022, the National Academy of Science, Engineering and Medicine (NASEM) released clinical guidance for PFAS chemicals for the first time. 7 PFAS chemicals were included in the guidance: MeFOSAA, PFHxS, PFOA, PFDA, PFUnDA, PFOS, and PFNA.
There are over 14,000 PFAS in existence, but these 7 are some the most commonly used since PFAS was introduced to manufacturing in the 1950’s.
""")
    
st.markdown("""
### What are the clinical guidance for the NASEM 7?
Based on simple sum of NASEM 7 in a person’s blood sample, NASEM has clinical guidance.
- For people who have less than 2 ng/mL in their blood sample, adverse health effects are not expected.
- For people who have between 2 and 20 ng/mL of the NASEM 7 PFAS in their blood sample, there is potential for adverse health effects, especially for sensitive populations, such as immunocompromsed or pregnant individuals.
- For people who have 20 or more ng/mL of the NASEM 7 PFAS in the blood sample, there is increased risk of adverse health effects.

Check out the graphic below to learn more about clinical follow-up based on PFAS levels in a person’s blood sample.
""")

st.image("Clinical Follow Up Graphic.png", caption="Clinical Follow Up Graphic", use_container_width=True)
st.markdown("""
*Courtesy of the National Academies of Science, Engineering, and Medicine.*
""")
    
    # CSS styling for enhanced visual presentation and theme compatibility
    #st.markdown("""
    #<style>
    #.big-font {
        #font-size:20px !important;
    #}
    
    #/* Dark mode compatibility improvements */
    #.stApp {
        #color: inherit;
    #}
    
    #/* Make sure text adapts to theme */
    #.markdown-text-container {
        #color: inherit !important;
    #}
    
    #/* Ensure plotly charts adapt to theme */
    #.js-plotly-plot .plotly .main-svg {
        #background: transparent !important;
    #}
    #</style>
    #""", unsafe_allow_html=True)
    
    # === MAIN RESEARCH QUESTIONS ===
    # Highlight the two primary questions this dashboard addresses
    #st.markdown("""
    #<p class="big-font">
    #<b>This tool answers two main questions:</b>
    #</p>
    #<ul>
    #<li><b>How are PFAS levels changing over time?</b></li>
    #<li><b>How are PFAS levels different across these three communities?</b></li>
    #</ul>
    #""", unsafe_allow_html=True)

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
    #st.markdown("""
    #You can use this tool to view the PFAS concentration levels in blood for many demographics, such as age group, sex, and community. You can look at the PFAS levels for specific individual PFAS, such as PFOS, or by important groups like the NASEM 7, (the only PFAS to have official clinical guidance at this time). You can learn more about the NASEM 7 under the “Learn More” tab above.

    #You can also look at PFAS concentration levels in blood by year. However, it is important to note that not all communities were sampled at the same time or every year. More information about when each community joined the study and when they have been sampled can be found on our [timeline](https://genxstudy.ncsu.edu/study-timeline/) page.

    #""")


st.markdown("""
### How do the NASEM 7 compare across GenX Exposure Study locations?
""")

# === YEAR RANGE PREPARATION ===
# Create comprehensive year list including NHANES comparison years
plot_years = sorted(complete['Year'].unique())
comparison_years = sorted(list(set(plot_years + [2018])))  # Include 2018 for NHANES comparison data

# === MAIN USER INTERFACE SECTION ===
with st.container(): # This creates an invisible container in your app that can hold multiple elements
    # === TWO-COLUMN FILTER LAYOUT ===
    col1, col2 = st.columns(2) # Creates two columns in this container
    
    # === LOCATION SELECTION (LEFT COLUMN) ===
    with col1:
        location_options = complete["Location"].unique().tolist()
        
        # Custom CSS styling for enhanced dropdown appearance
        st.markdown("""
            <style>
            div[data-baseweb="select"] > div {
                border: 2px solid #000000 !important;  /* Black border for emphasis */
                border-radius: 8px !important;         /* Rounded corners */
            }
            </style>
        """, unsafe_allow_html=True)
        
        # Location multi-select filter
        location = st.multiselect(
            "Select Location(s):", # Text to display for this multi-select
            options=location_options,           # All available locations are set as options
            default=location_options,           # Default to all locations selected 
            key="nasem location"               # Unique key for this widget
        )
    
    # === YEAR SELECTION (RIGHT COLUMN) ===
    with col2:
        # Filter out years that don't have GenX study data (2018, 2022)
        selectable_years = sorted([y for y in complete['Year'].unique() if y not in [2018, 2022]]) # Creating a list of all Year options (based on what is in the dataset), and don't include 2018 and 2022
        
        # Apply same custom CSS styling
        st.markdown("""
            <style>
            div[data-baseweb="select"] > div {
                border: 2px solid #000000 !important;  /* Consistent black border */
                border-radius: 8px !important;         /* Consistent rounded corners */
            }
            </style>
        """, unsafe_allow_html=True)
        
        # Year multi-select filter
        year = st.multiselect(
            "Select Year(s):",
            options=selectable_years,           # Available study years are set as options
            default=selectable_years,           # Default to all years selected
            key="nasem year"                   # Unique key for this widget
        )
    


# === CHART LAYOUT CONFIGURATION ===
cols = st.columns([2, 1]) # This creates two side by side columns with uneven widths, the first column is twice as wide as the second column
with cols[1]: # Column 1 is the narrower right handed column
    st.title("")
    # We're just adding an image to this column 
    # udpate image path as needed, this image should be in the provided folder
    # Maybe create a new image with better colors and change the colors of the plot in general
    st.image("NAESM_Guidance.png", use_container_width=True)
    
with cols[0]: # Column 0 is the wider left handed column 
    # Function to convert years to abbreviated format for the plot
    def format_year_label(year):
        """Convert year to abbreviated format: 2017, '18, '19, '20, '21, '22, 2023"""
        if year == 2017 or year == 2023:
            return str(year)
        elif 2018 <= year <= 2022:
            return f"'{str(year)[2:]}"
        else:
            return str(year)
    
    filtered_data = complete.copy() #Making a copy of our complete dataset and saving it as filtered_data
    filtered_data = filtered_data[filtered_data["Location"].isin(location)] #Only keep the rows of our dataset where the location matches one of the locations in the "location" list (which is the list of all user selected locations)
    filtered_data = filtered_data[filtered_data["Year"].isin(year)] #Only keep the rows of our dataset where the year matches one of the years in the "year" list (which is the list of all user selected years)
    filtered_data = filtered_data[filtered_data["PFAS"].isin(["PFOS", "PFOA", "PFHxS", "PFNA", "PFDA", "PFUnDA", "MeFOSAA"])] #Only keep the rows of our dataset where the PFA is one of the NASEM compounds
    filtered_data = filtered_data[filtered_data["detect"] == 1] #Only keeping the rows of our dataset where the PFA is detected

    #So at this point, filtered_data contains only:
        #selected locations
        # selected years
        # the 7 NASEM PFAS
        # detected measurements

    #We are resaving the dataset after each filter

    filtered_data_sum = filtered_data.groupby(['Year', 'Location', 'unique_id'], as_index=False, observed=True)['conc'].sum() #Finding the sum of the concentration for each Year, Location, and Unique ID group
    #What does as_index=false do? Normally groupby turns the grouping columns into the index. This prevents that and keeps them as regular columns, which is usually easier to work with.
    #What does observed=True do? Only return combinations of these grouping variables that actually appear in the data. 

    # creating NASEM 7 sum 
    #After summing, the column is still called conc, but that is misleading. Now it represents a sum of concentrations, not individual values. Thus, we rename just that column to conc_sum
    filtered_data_sum = filtered_data_sum.rename(columns={'conc': 'conc_sum'}) 

    #We are finding the quantiles of each 
    quantiles =  filtered_data_sum.groupby(['Year', 'Location'], observed=True)['conc_sum'].quantile([0.05, 0.25, 0.5, 0.75, 0.95]).unstack()
    # The unstack() in the line above makes it so that each Year and Location group has one row with a column for each quantile
    # Inside each group, you have multiple IDs with their conc_sum values, and you are finding the quantiles across all these observations
    #If this quantiles data frame is not empty (meaning the filtered dataset was not empty):
    if not quantiles.empty:
        #Rename the columns
        quantiles.columns = ['5th percentile', '25th percentile', '50th percentile', '75th percentile', '95th percentile']
        #Make sure the index/grouping variables (Year and Location) are also considered columns
        quantiles = quantiles.reset_index()
        #We are now going to round the percentile values and rename the quantile columns
        quantile_cols = ['5th percentile', '25th percentile', '50th percentile', '75th percentile', '95th percentile']
        quantiles[quantile_cols] = quantiles[quantile_cols].round()
    #If the quantiles list and filtered data set is empty (meaning the user selected filters that returned no rows)
    else:
        # This creates an empty table with the correct column structure so the rest of the code doesn’t crash
        # Later in the code you merge quantiles with another dataframe.
        # If quantiles didn’t exist or had different columns, the merge would break.
        quantiles = pd.DataFrame(columns=['Year', 'Location', '5th percentile', '25th percentile', '50th percentile', '75th percentile', '95th percentile'])

    # This joins the two datasets together. Left merge keeps all rows from filtered_data_sum, and attaches the quantile values, if there is a matching year/location group (meaning the quantiles dataset is not empty)
    df_plot_adjusted = filtered_data_sum.merge(quantiles, on=['Year', 'Location'], how='left') #So the rows in the same year/location group but different IDs will have the same values in the quantile column
    df_plot_adjusted['conc_adjusted'] = df_plot_adjusted['conc_sum'].clip( #clip will limit values in the conc_sum column to a range
        lower=df_plot_adjusted['5th percentile'], #If the value of a conc_sum for a specific year/location/id group is less than the 5th percentile of the conc_sum value for the corresponding year/location group, it is just replaced with the 5th percentile value
        upper=df_plot_adjusted['95th percentile'] #If the value of a conc_sum for a specific year/location/id group is greater than the 95th percentile of the conc_sum value for the corresponding year/location group, it is just replaced with the 95th percentile value
    )

    #Select the coc_adjusted column of the df_plot_adjusted data frame
    # .apply() says “Run a function on every value in this column.”
    # A lambda function is just a short, unnamed function. This takes a value x, rounds it, and converts it to an integer
    df_plot_adjusted['conc_adjusted'] = df_plot_adjusted['conc_adjusted'].apply(lambda x: int(round(x))) 

    # Calculate min, max, median for each year-location combination for hover
    # We are saving these statistics in a new data frame
    # Inside each Year + Location group you have multiple conc_sum values (one in each row), one for each unique_id.
    stats_for_hover = filtered_data_sum.groupby(['Year', 'Location'], observed=True)['conc_sum'].agg([ # .agg() means aggregate multiple statistics at once.
        # Each tuple defines: (new_column_name, statistic)
        # So within each Year + Location group, we are finding the min, max, and median conc_sum values across all the ids
        ('min_val', 'min'), 
        ('max_val', 'max'),
        ('median_val', 'median')
    ]).reset_index() # converts the group by variables back into normal columns
    stats_for_hover[['min_val', 'max_val', 'median_val']] = stats_for_hover[['min_val', 'max_val', 'median_val']].round().astype(int) # modifies the statistic column by rounding the values and converting them to integers
    
    # Merge stats into the plot data
    df_plot_adjusted = df_plot_adjusted.merge(stats_for_hover, on=['Year', 'Location'], how='left')

    # Create a mapping for evenly spaced positioning. 
    # We want to create a numeric position for each year so the data can be plotted on an evenly spaced X-axis.
    # Instead of plotting actual years, we convert them to positions because this is easier for plotting libraries to handle
    #First we sort the years
    #Enumerate adds a number to each year
    # Result:
    #(0, 2020)
    #(1, 2021)
    #(2, 2022)
    #Then we build a dictionary
    #Like this:
    #year_positions = {
    #2020: 0,
    #2021: 1,
    #2022: 2
    #}
    year_positions = {year: i for i, year in enumerate(sorted(plot_years))}
    #Add a new column in df_plot_adjusted for the year positions
    df_plot_adjusted['Year_position'] = df_plot_adjusted['Year'].map(year_positions)
    
    # Add formatted year column for display
    df_plot_adjusted['Year_formatted'] = df_plot_adjusted['Year'].apply(format_year_label)
    
    # Clean up any existing hover columns to avoid conflicts
    hover_cols = [col for col in df_plot_adjusted.columns if 'hover' in col.lower()]
    if hover_cols:
        df_plot_adjusted = df_plot_adjusted.drop(columns=hover_cols)
    
    # Create formatted plot_years for category order
    plot_years_formatted = [format_year_label(year) for year in plot_years]

    fig = px.box(
        df_plot_adjusted,
        x='Year_position',  # Use evenly spaced positions for numeric X-axis positions
        y='conc_adjusted', # the data to plot
        color='Location',  # separates boxes by location
        category_orders={'Location': loc_order}, # ensures the colors and order of locations are consistent (loc_order variable is in View Indvidual PFAS)
        title='NASEM 7: Summed PFAS Concentration', # Title of the boxplot
        labels={"conc_adjusted": "Concentration (ng/mL)", "Year_position": "Year"}, # Changes x and y axis labels
        points=False, # do not show individual data points (only the box)
        color_discrete_map=group_colors # assigns specific colors to each location
    )

    # Plotly automatically shows default hover info (median, min, max, etc.) on boxplots.
    # Here, we turn it off so we can add custom hover info later, like the stats we calculated before.
    fig.update_traces(hovertemplate=None, hoverinfo='none')
    
    # Add invisible scatter points for custom hover - create vertical coverage for each location's box
    #Take all unique values of location in the entire data frame and save it as a list 
    location_list = sorted(df_plot_adjusted['Location'].unique())
    
    #Loop through each location that is in the dataset 
    for location in location_list: 
        #We are keeping the rows of the dataset that match the specific location we are looking at 
        location_data = df_plot_adjusted[df_plot_adjusted['Location'] == location]
        # Get unique combinations of Year_position and stats for this specific location
        # hover points is a new data frame (one for each location) containing a new row for each year and columns for each quantile
        hover_points = location_data.groupby(['Year_position', 'Year_formatted'], observed=True).agg({ # Groups the data by year (numeric position + formatted string).
            # 'first' just takes the first value in each group — which works because all rows in the group have identical stats (groups are by year in each location group. there are multiple ids in each group but they all have the same quantiles)
            'min_val': 'first',
            'max_val': 'first', 
            'median_val': 'first',
            '50th percentile': 'first',
            '25th percentile': 'first',
            '75th percentile': 'first',
            '5th percentile': 'first',
            '95th percentile': 'first'
        }).reset_index() # After groupby, the group keys (Year_position, Year_formatted) become the index. Resetting index converts them back to columns, making it easier to use in Plotly hover.
        
        # Calculate location's offset within grouped boxes
        # Use the desired order: Pittsboro (left), Fayetteville (center), Lower Cape Fear Region (right)
        box_plot_order = ['Pittsboro', 'Fayetteville', 'Lower Cape Fear Region']
        location_index = box_plot_order.index(location) if location in box_plot_order else 0 # creates a list of indices Pittsboro = 0, Fayetteville = 1, Lower Cape Hear Region = 2
        num_locations = len(box_plot_order) # saves the number of locations we have 
        
        # Standard Plotly box plot spacing - match the actual box positions
        # If there is only one box we are plotting, no need to shift
        if num_locations == 1:
            base_x_offset = 0
        else:
            # Standard box plot group spacing: left = -0.27, center = 0, right = +0.27
            # Each year has multiple boxes (one per location). But your X-axis only has one position per year (Year_position)
            # thus, we need to spread them slightly left and right around the year's position
            # The following code will center everything around 0 (for 3 boxes, the left most location will get a negative number, the middle will get 0, and the right most will get a positive number)
            # The * 0.8 will control width between the boxes
            base_x_offset = (location_index - (num_locations - 1) / 2) * 0.8 / num_locations
        
        # For each year this location has data, create vertical hover coverage
        # iterrows() is a way to loop through a data frame by row 
        # in this case _ is the index identifier for that row (which will be some integer)
        # The row (called the point in this case) is a Pandas Series object containing all the data from that horizontal line.
        for _, point in hover_points.iterrows():
            # We are saving the year position (the one digit integer for the position of the year)
            year_pos = point['Year_position']
            
            # Create full vertical coverage from whisker bottom to whisker top (5th to 95th percentile)
            y_min = point['5th percentile'] if '5th percentile' in point else point['25th percentile'] # setting the minimum point on the box plot as the 5th percentile if it exists, otherwise it is set to the 25th percentile 
            y_max = point['95th percentile'] if '95th percentile' in point else point['75th percentile'] # setting the maximum point on the box plot as the 95th percentile if it exists, otherwise it is set to the 75th percentile 
            
            # Create dense vertical coverage across the entire box plot height
            # More points for better hover coverage
            # Previously we removed all the default hover stuff that streamlit automatically uses, so now we are adding it back in manually
            # Set some variables first
            num_points = 12  # Increase for smoother coverage
            y_positions = []
            
            # Let's calculate some hover points
            if y_max > y_min:
                for i in range(num_points):
                    # This creates evenly spaced points between y_min and y_max where you will be able to hover
                    # Ex// [5, 8.75, 12.5, 16.25, 20, ....]
                    y_pos = y_min + (y_max - y_min) * i / (num_points - 1)
                    y_positions.append(y_pos)
            else:
                # If min and max are the same, just use that value
                y_positions = [y_min]
            
            # Loop through every point in y positions 
            for i, y_pos in enumerate(y_positions): 
                fig.add_trace(go.Scatter(
                    x=[year_pos + base_x_offset],  # horizontal shift Year pos is which year (like 0, 1, 2). base_x_offset → shift left/right for the location
                    y=[y_pos], # this is the vertical position (that we just created with the code just above this)
                    mode='markers', # This tells Plotly what kind of visual you are drawing (in this case that is points)
                    marker=dict(size=6, opacity=0, color='red'),  # Invisible markers. You can't see the hover points, but you can still see the info when you hover over them 
                    name=f"{location}_hover", # name labels the entire trace (i.e., the group of points you add in that one go.Scatter call ) 
                    showlegend=False,  # Don't show in legend
                    # The information following hovertemplate is what will display when you hover over a specific marker that you generated (for this specific location)
                    # <b> → bold text
                    # <br> → line break
                    hovertemplate="<b>" + location + "</b><br>" +
                                 "Year: " + point['Year_formatted'] + "<br>" +
                                 "5th Percentile: " + str(point['min_val']) + " ng/mL<br>" +
                                 "Median: " + str(point['median_val']) + " ng/mL<br>" +
                                 "95th Percentile: " + str(point['max_val']) + " ng/mL<br>" +
                                 "<extra></extra>"
                ))
                # "<extra></extra>" removes the default Plotly label that normally appears.

    # Summary of what we just did: We loop through each location, then for each year in that location we compute summary stats, and then create multiple 
    # invisible points that span vertically across the box so hover works anywhere on that box.
    
    # For now, let's just keep the year formatting working correctly
    # Custom hover with proper positioning is complex with categorical axes

    fig.update_layout(
        height=700, 
        legend=dict(
            font=dict(size=12, color = "black"),  
            bgcolor='rgba(255,255,255,0.5)', 
            x=5,  # Adjust to the right
            y=1,
            traceorder='normal'),
        boxmode='group',
        title={
        # subtitle
        "text": "NASEM 7: Summed PFAS Concentration<br><sup>PFOA, PFOS, PFHxS, PFNA, PFDA, PFUnDA, MeFOSAA</sup>",
        "x": 0.5, 
        "xanchor": "center"}
    )
    fig.update_yaxes(
        range=[0, 51],
        tick0=0,           
        dtick=10,              
        showgrid=True,       
        gridwidth=1,
        griddash = 'dot',
        gridcolor='lightgray'  
    )
    fig.update_xaxes(
        tickmode='array',
        tickvals=list(year_positions.values()),  # Use position indices
        ticktext=[format_year_label(year) for year in sorted(plot_years)],  # Use formatted labels
        range=[-0.5, len(plot_years) - 0.5]  # Constrain to position range
    )
    # line for NHANES 95th percentile - use position mapping
    fig.add_hline(y = 20, line_dash="solid", line_color="#EC5E57")
    fig.add_trace(go.Scatter(
        x=list(year_positions.values()),  # Use position indices
        y=[20] * len(year_positions),
        mode="lines",
        line=dict(color="#EC5E57", width=2),
        name="20 ng/mL",
        showlegend=True,
        hoverinfo='skip'
    ))
    # line for NHANES median percentile
    '''
    fig.add_hline(y = 6.47, line_dash="solid", line_color="black")
    fig.add_trace(go.Scatter(
        x= [format_year_label(y) for y in year],
        y=[6.47] * len(year),
        mode="lines",
        line=dict(color="black", width=2),
        name="National Median (NHANES)",
        showlegend=True
    ))
    '''
    # line for NHANES 5th percentile - use position mapping
    fig.add_hline(y = 2, line_dash="solid", line_color="#FBBF9A")
    fig.add_trace(go.Scatter(
        x=list(year_positions.values()),  # Use position indices
        y=[2] * len(year_positions),
        mode="lines",
        line=dict(color="#FBBF9A", width=2),
        name="2 ng/mL",
        showlegend=True,
        hoverinfo='skip'
    ))
    
    st.markdown("")
    include_nhanes = st.checkbox("Check this box to include National NHANES data for comparison", value=False, key="include_nhanes_toggle")

    if include_nhanes:
        # Process NHANES raw data
        nhanes_data = process_nhanes_raw_data()
    
        if not nhanes_data.empty:
            # Combine local study data with NHANES data for comparison
            combined_data = pd.concat([filtered_data_sum, nhanes_data[['Location', 'Year', 'conc_sum']]], ignore_index=True)
        
            # Calculate quantiles for combined data including NHANES
            combined_quantiles = combined_data.groupby(['Year', 'Location'], observed=True)['conc_sum'].quantile([0.05, 0.25, 0.5, 0.75, 0.95]).unstack()
            if not combined_quantiles.empty:
                combined_quantiles.columns = ['5th percentile', '25th percentile', '50th percentile', '75th percentile', '95th percentile']
                combined_quantiles = combined_quantiles.reset_index()
                quantile_cols = ['5th percentile', '25th percentile', '50th percentile', '75th percentile', '95th percentile']
                combined_quantiles[quantile_cols] = combined_quantiles[quantile_cols].round()
            else:
                combined_quantiles = pd.DataFrame(columns=['Year', 'Location', '5th percentile', '25th percentile', '50th percentile', '75th percentile', '95th percentile'])
        
            combined_plot_adjusted = combined_data.merge(combined_quantiles, on=['Year', 'Location'], how='left')
            combined_plot_adjusted['conc_adjusted'] = combined_plot_adjusted['conc_sum'].clip(
                lower=combined_plot_adjusted['5th percentile'],
                upper=combined_plot_adjusted['95th percentile']
            )
            combined_plot_adjusted['conc_adjusted'] = combined_plot_adjusted['conc_adjusted'].round().astype(int)
        
            # Create a mapping for evenly spaced positioning for comparison chart
            # Keep the original study years and append NHANES year
            study_years = sorted([year for year in combined_data['Year'].unique() if year != 2018])
            nhanes_years = [2018] if 2018 in combined_data['Year'].unique() else []
            actual_years_in_data = study_years + nhanes_years  # Study years first, then NHANES
        
            comparison_year_positions = {year: i for i, year in enumerate(actual_years_in_data)}
            combined_plot_adjusted['Year_position'] = combined_plot_adjusted['Year'].map(comparison_year_positions)
        
            # Create labels: use format_year_label for study years, force '18 for NHANES
            # Force explicit mapping to avoid any issues
            custom_year_labels = []
            for year in actual_years_in_data:
                if year == 2018:
                    custom_year_labels.append("'18")  # Force NHANES to show as '18
                elif year == 2017:
                    custom_year_labels.append("2017")
                elif year == 2019:
                    custom_year_labels.append("'19")
                elif year == 2020:
                    custom_year_labels.append("'20")
                elif year == 2021:
                    custom_year_labels.append("'21")
                elif year == 2023:
                    custom_year_labels.append("2023")
                else:
                    custom_year_labels.append(str(year))
        
            # Debug print to verify the mapping
            # print(f"Study years: {study_years}")
            # print(f"All years in order: {actual_years_in_data}")
            # print(f"Custom labels: {custom_year_labels}")
            # print(f"Year positions: {comparison_year_positions}")
        
            # Add formatted year column for display using custom labels
            year_to_label_map = dict(zip(actual_years_in_data, custom_year_labels))
            combined_plot_adjusted['Year_formatted'] = combined_plot_adjusted['Year'].map(year_to_label_map)
        
            # Clean up any existing hover columns to avoid conflicts
            hover_cols = [col for col in combined_plot_adjusted.columns if 'hover' in col.lower()]
            if hover_cols:
                combined_plot_adjusted = combined_plot_adjusted.drop(columns=hover_cols)
        
            # Update location order to include NHANES
            all_locations = ['Pittsboro', 'Fayetteville', 'Lower Cape Fear Region', 'NHANES (National)']
        
            # Create formatted comparison years
            comparison_years_formatted = [format_year_label(year) for year in comparison_years]
        
            # Create year colors for the comparison plot  
            year_colors_formatted = {
                format_year_label(2019): '#1f77b4',  # Blue
                format_year_label(2020): '#ff7f0e',  # Orange  
                format_year_label(2021): '#2ca02c',  # Green
                format_year_label(2018): '#d62728'   # Red for NHANES
            }
        
            # Create the comparison visualization with numeric axis like main chart
            fig_comparison = px.box(
                combined_plot_adjusted,
                x='Year_position',  # Use evenly spaced positions
                y='conc_adjusted', 
                color='Location',  
                category_orders={'Location': all_locations}, 
                title='NASEM 7: Local Study vs. National NHANES Data',
                labels={"conc_adjusted": "Concentration (ng/mL)", "Year_position": "Year"},
                points=False,
                color_discrete_map={
                    'Pittsboro': group_colors.get('Pittsboro', '#1f77b4'),
                    'Fayetteville': group_colors.get('Fayetteville', '#ff7f0e'), 
                    'Lower Cape Fear Region': group_colors.get('Lower Cape Fear Region', '#2ca02c'),
                    'NHANES (National)': '#d62728'  # Red for NHANES
                }
            )
        
            # Disable default hover and add custom hover for comparison chart
            fig_comparison.update_traces(hovertemplate=None, hoverinfo='none')
        
            # Calculate min, max, median for comparison chart hover
            combined_stats_for_hover = combined_data.groupby(['Year', 'Location'], observed=True)['conc_sum'].agg([
                ('min_val', 'min'),
                ('max_val', 'max'),
                ('median_val', 'median')
            ]).reset_index()
            combined_stats_for_hover[['min_val', 'max_val', 'median_val']] = combined_stats_for_hover[['min_val', 'max_val', 'median_val']].round().astype(int)
        
            # Merge stats into comparison plot data
            combined_plot_adjusted = combined_plot_adjusted.merge(combined_stats_for_hover, on=['Year', 'Location'], how='left')
        
            # Add invisible scatter points for custom hover - same approach as main chart
            for location in all_locations:
                location_data = combined_plot_adjusted[combined_plot_adjusted['Location'] == location]
                if location_data.empty:
                    continue
                
                # Get unique combinations of Year_position and stats for this location
                hover_points = location_data.groupby(['Year_position', 'Year_formatted'], observed=True).agg({
                    'min_val': 'first',
                    'max_val': 'first', 
                    'median_val': 'first',
                    '50th percentile': 'first',
                    '25th percentile': 'first',
                    '75th percentile': 'first',
                    '5th percentile': 'first',
                    '95th percentile': 'first'
                }).reset_index()
            
                # Calculate location's offset within grouped boxes - same as main chart
                box_plot_order = ['Pittsboro', 'Fayetteville', 'Lower Cape Fear Region', 'NHANES (National)']
                location_index = box_plot_order.index(location) if location in box_plot_order else 0
                num_locations = len(box_plot_order)
            
                # Standard Plotly box plot spacing - match the actual box positions
                if num_locations == 1:
                    base_x_offset = 0
                else:
                    # Standard box plot group spacing
                    base_x_offset = (location_index - (num_locations - 1) / 2) * 0.8 / num_locations
            
                # For each year this location has data, create vertical hover coverage
                for _, point in hover_points.iterrows():
                    year_pos = point['Year_position']
                
                    # Create full vertical coverage from whisker bottom to top
                    y_min = point['5th percentile'] if '5th percentile' in point else point['25th percentile']
                    y_max = point['95th percentile'] if '95th percentile' in point else point['75th percentile'] 
                
                    # Create dense vertical coverage across the entire box plot height
                    num_points = 12
                    y_positions = []
                
                    if y_max > y_min:
                        for i in range(num_points):
                            y_pos = y_min + (y_max - y_min) * i / (num_points - 1)
                            y_positions.append(y_pos)
                    else:
                        # If min and max are the same, just use that value
                        y_positions = [y_min]
                
                    for i, y_pos in enumerate(y_positions):
                        fig_comparison.add_trace(go.Scatter(
                            x=[year_pos + base_x_offset],
                            y=[y_pos],
                            mode='markers',
                            marker=dict(size=6, opacity=0, color='red'),  # Invisible markers
                            name=f"{location}_hover_comparison",
                            showlegend=False,
                            hovertemplate="<b>" + location + "</b><br>" +
                                         "Year: " + point['Year_formatted'] + "<br>" +
                                         "5th Percentile: " + str(point['min_val']) + " ng/mL<br>" +
                                         "Median: " + str(point['median_val']) + " ng/mL<br>" +
                                         "95th Percentile: " + str(point['max_val']) + " ng/mL<br>" +
                                         "<extra></extra>"
                        ))
        
            fig_comparison.update_layout(
                height=700, 
                legend=dict(
                    font=dict(size=12, color="black"),  
                    bgcolor='rgba(255,255,255,0.5)', 
                    x=1.02,
                    y=0.98,
                    traceorder='normal'
                ),
                boxmode='group',
                title={
                    "text": "NASEM 7: Local Study vs. National NHANES Data<br><sup>Comparison of summed PFAS concentrations with national reference data (2018)</sup>",
                    "x": 0.5, 
                    "xanchor": "center"
                }
            )
        
            fig_comparison.update_yaxes(
                range=[0, 51],
                tick0=0,           
                dtick=10,              
                showgrid=True,       
                gridwidth=1,
                griddash='dot',
                gridcolor='lightgray'  
            )
        
            fig_comparison.update_xaxes(
                tickmode='array',
                tickvals=list(comparison_year_positions.values()),  # Use position indices
                ticktext=custom_year_labels,  # Use custom labels that force '18 for NHANES
                range=[-0.5, len(actual_years_in_data) - 0.5]  # Constrain to position range
            )
        
            # Add NHANES reference lines using position mapping like main chart
            fig_comparison.add_hline(y=20, line_dash="solid", line_color="darkred")
            fig_comparison.add_trace(go.Scatter(
                x=list(comparison_year_positions.values()),  # Use position indices
                y=[20] * len(comparison_year_positions),
                mode="lines",
                line=dict(color="darkred", width=2),
                name="20 ng/mL",
                showlegend=True,
                hoverinfo='skip'
            ))
        
            fig_comparison.add_hline(y=2, line_dash="solid", line_color="#FBBF9A")
            fig_comparison.add_trace(go.Scatter(
                x=list(comparison_year_positions.values()),  # Use position indices
                y=[2] * len(comparison_year_positions),
                mode="lines",
                line=dict(color="#FBBF9A", width=2),
                name="2 ng/mL",
                showlegend=True,
                hoverinfo='skip'
            ))
        
            st.plotly_chart(fig_comparison, use_container_width=True, key="NASEM7_comparison")
            
            # NHANES Reference Data Explanation
            st.markdown("""
            #### What does the NHANES median line mean?
            The median line shows which communities have PFAS levels above the 50th percentile of the NHANES data. In other words, 50% of the participants in the national study had a summed PFAS concentration at or below this level.     
            """)
            
            # Add interpretation guide
            st.markdown("#### How to Interpret the Comparison:")
            st.markdown("""
            - **Higher than NHANES**: If your local study shows higher concentrations than NHANES, it suggests elevated PFAS exposure in your study population
            - **Similar to NHANES**: Concentrations similar to national averages indicate typical exposure levels
            - **Lower than NHANES**: Lower concentrations suggest potentially less exposure compared to the national average
            - **Reference Lines**: The 2 ng/mL and 20 ng/mL lines represent clinical guidance thresholds for health risk assessment
            """)
            
        else:
            st.warning("NHANES data could not be loaded. Please check the file path and format.")
    else:
        st.plotly_chart(fig, use_container_width=True, key="NASEM7")
