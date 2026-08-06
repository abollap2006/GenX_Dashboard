"""
GenX Exposure Study Dashboard - Main Application Entry Point

This is the primary application file that configures the Streamlit interface,
loads and processes all data sources, and provides the main navigation system
for the GenX Exposure Study Dashboard.

The dashboard provides interactive visualizations for PFAS exposure data from
three communities in North Carolina: Pittsboro, Lower Cape Fear Region, and Fayetteville.

Author: [Your Name]
Last Updated: [Date]
"""

# === LIBRARY IMPORTS ===
import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
import matplotlib.ticker as mtick
import numpy as np
from matplotlib.patches import PathPatch

# === STREAMLIT CONFIGURATION ===
# Configure page settings for wide layout and custom title
st.set_page_config(page_title="GenX Exposure Study", layout="wide")

# === DATA LOADING SECTION ===
# Load all required datasets for the dashboard
# Note: All CSV files should be in the same directory as this script

# NHANES reference data for national PFAS level comparisons (2017-2020)
nhanes = pd.read_csv('2017-2020_Nhanes_NASEM7_Summaries.csv')

# Main PFAS exposure data from GenX study (2017-2023)
pfas_all = pd.read_csv('GenX_2017-2023_PFAS_Data.csv')

# Demographics data from different collection periods
demographics_2017_19 = pd.read_csv('QX_2017-2019_Data.csv')  # Early study period
demographics_2020_21 = pd.read_csv('QX_2020-2021_Data.csv')  # Mid study period  
demographics_2023 = pd.read_csv('QX_2023_Data.csv')          # Recent study period

# === DATA STANDARDIZATION ===
# Standardize community names across all demographic datasets
# Convert numeric codes to descriptive location names for consistency 

# Standardize 2017-2019 demographic data community names
demographics_2017_19['community'] = demographics_2017_19['community'].replace({
    1: "Lower Cape Fear Region",  # Downstream Cape Fear River communities
    2: 'Fayetteville',            # Private well community near Fayetteville
	3: 'Pittsboro'                # Haw River/Jordan Lake community
})

# Standardize 2020-2021 demographic data community names
demographics_2020_21['community'] = demographics_2020_21['community'].replace({
    1: "Lower Cape Fear Region",  # Consistent naming across datasets
    2: 'Fayetteville',            
	3: 'Pittsboro'                
})

# Standardize 2023 demographic data community names
demographics_2023['community'] = demographics_2023['community'].replace({
    1: "Lower Cape Fear Region",  # Maintain consistent location identifiers
    2: 'Fayetteville',            
	3: 'Pittsboro'                
})

# === DEMOGRAPHIC DATA CONSOLIDATION ===
# Combine all demographic datasets into single comprehensive dataset
demographics = pd.concat([demographics_2017_19, demographics_2020_21, demographics_2023])

# Create unique participant identifiers to handle participants across multiple years
# Format: participant_id + community (prevents confusion between participants with same ID in different locations)
demographics['unique_id'] = demographics['id'].astype(str) + '_' + demographics['community'].astype(str) 

# Remove duplicate participants (keep only one record per unique participant)
demographics = demographics.drop_duplicates('unique_id')

# === PFAS DATA PREPARATION ===
# Create working copy of PFAS data for processing
pfas = pfas_all.copy()

# Standardize location names in PFAS dataset to match demographic data
# Map abbreviated location codes to full descriptive names
pfas['study_loc'] = pfas['study_loc'].replace({
    'LCFR': 'Lower Cape Fear Region',  # Lower Cape Fear Region abbreviation
    'Pittsboro': 'Pittsboro',          # Already standardized
    'Fayetteville': 'Fayetteville'     # Already standardized
})

# === PARTICIPANT ID STANDARDIZATION ===
# Create consistent unique identifiers for PFAS data to match demographic data
pfas['unique_id'] = pfas['id'].astype(str) + '_' + pfas['study_loc'].astype(str) 

# === DATA INTEGRATION ===
# Merge demographic and PFAS datasets on unique participant identifiers
# Right join ensures all PFAS measurements are retained, even if demographic data is missing
joined = pd.merge(demographics, pfas, on=["unique_id"], how="right")

# Remove any duplicate records that may have been created during merge
joined = joined.drop_duplicates()

# Ensure NHANES data is in DataFrame format for consistent processing
nhanes = pd.DataFrame(nhanes)

# === PFAS SUBSET FILTERING ===
# Filter to include only key PFAS compounds for focused analysis
# This subset includes NASEM 7 compounds plus additional compounds of interest
joined_filter = joined[joined['PFAS'].isin([
    "PFOS",                # Perfluorooctanesulfonic acid (NASEM 7)
    "PFOA",                # Perfluorooctanoic acid (NASEM 7)  
    "PFHxS",               # Perfluorohexanesulfonic acid (NASEM 7)
    "PFNA",                # Perfluorononanoic acid (NASEM 7)
    "PFDA",                # Perfluorodecanoic acid (NASEM 7)
    "PFUnDA",              # Perfluoroundecanoic acid (NASEM 7)
    "MeFOSAA",             # N-methylperfluorooctanesulfonamidoacetic acid (NASEM 7)
    "Nafion byproduct 2",  # GenX-related compound of local interest
    "PFO5DoA"              # Additional perfluorinated compound
])] 

# === COMPLETE DATASET PREPARATION ===
# Create final working dataset for all dashboard visualizations
complete = joined_filter.copy()

# === CATEGORICAL DATA TYPE CONVERSION ===
# Convert relevant columns to categorical data types for better performance and memory usage
# This also enables proper ordering in visualizations
complete['age_cat'] = complete['age_cat'].astype('category')              # Age group categories
complete['years_lived_cat'] = complete['years_lived_cat'].astype('category') # Duration in community
complete['community'] = complete['community'].astype('category')          # Study location
complete['gender'] = complete['gender'].astype('category')               # Participant gender
complete['hispanic'] = complete['hispanic'].astype('category')           # Hispanic ethnicity
complete['study_year'] = complete['study_year'].astype('category')       # Year of data collection
complete['PFAS'] = complete['PFAS'].astype("category")                   # PFAS compound names

# === ETHNICITY LABEL STANDARDIZATION ===
# Convert numeric ethnicity codes to descriptive labels for better readability
complete['hispanic'] = complete['hispanic'].cat.rename_categories({
    0: "Non-Hispanic",  # Non-Hispanic participants
    1: "Hispanic"       # Hispanic participants
})

# === DISPLAY ORDER DEFINITIONS ===
# Define consistent ordering for categorical variables across all visualizations
# These orders ensure logical progression and consistent presentation

# Geographic locations ordered by river flow (upstream to downstream)
loc_order = ["Pittsboro", "Fayetteville", "Lower Cape Fear Region"]

# PFAS compounds ordered by typical concentration levels and regulatory importance
pfas_order = ["PFOS", "PFOA", "PFO5DoA", "PFHxS", "PFNA", "PFDA", "PFUnDA", "MeFOSAA", "Nafion byproduct 2"]

# === PFAS GROUPING BY CONCENTRATION RANGES ===
# Group PFAS compounds by typical concentration levels for visualization consistency
# These groupings help organize charts and analysis by expected concentration ranges

# High concentration PFAS (typically >1 ng/mL)
predefined_large_order = ["PFOS", "PFOA", "PFO5DoA"]

# Medium concentration PFAS (typically 0.1-1 ng/mL)  
predefined_medium_order = ["PFHxS", "PFNA", "Nafion byproduct 2"]

# Lower concentration PFAS (typically <0.1 ng/mL)
predefined_small_order = ["PFDA", "PFUnDA", "MeFOSAA"]

# Create working copy for additional data transformations
complete = complete.copy()

# === YEARS LIVED CATEGORY STANDARDIZATION ===
# Standardize and clean years lived in community categories for consistent display

# === YEARS LIVED CATEGORY STANDARDIZATION ===
# Standardize and clean years lived in community categories for consistent display
# Convert numeric codes to readable year ranges
complete['years_lived_cat'] = complete['years_lived_cat'].astype(str).replace({
    "1.0": "1-5",          # 1-5 years in community
    "2.0": "6-10",         # 6-10 years in community
    "3.0": "11-15",        # 11-15 years in community
    "4.0": "16-20",        # 16-20 years in community
    "5.0": "21-25",        # 21-25 years in community
    "6.0": "26-30",        # 26-30 years in community
    "7.0": "31-35",        # 31-35 years in community
    "8.0": "36-40",        # 36-40 years in community
    "9.0": "41-45",        # 41-45 years in community
    "10.0": "46-50",       # 46-50 years in community
    "11.0": "51-55",       # 51-55 years in community
    "12.0": "56-60",       # 56-60 years in community
    "13.0": ">60 years"    # More than 60 years in community
})

# Create working copy for additional transformations
complete = complete.copy()

# === AGE CATEGORY STANDARDIZATION ===
# Convert numeric age codes to descriptive age ranges for analysis
# Consolidate similar age groups for sufficient sample sizes
complete['age_cat'] = complete['age_cat'].astype(str).replace({
    "1.0": "6-17",         # Children and adolescents (combined from multiple pediatric groups)
    "2.0": "6-17",         # Children and adolescents (combined from multiple pediatric groups)
    "3.0": "18-50",        # Young to middle-aged adults
    "4.0": "18-50",        # Young to middle-aged adults (combined for larger sample size)
    "5.0": "51-70",        # Older adults
    "6.0": ">70"           # Elderly participants
})

# === GENDER CATEGORY STANDARDIZATION ===
# Convert numeric gender codes to descriptive labels
# Consolidate categories per study team decision for adequate sample sizes
complete['gender'] = complete['gender'].astype(str).replace({
    "1.0": "Male",         # Male participants
    "2.0": "Female",       # Female participants  
    "3.0": "Female",       # Additional female category (rolled up per meeting decision)
    "nan": "Female"        # Unknown values (2 in Wilmington) - rolled up per meeting, verify with unique_id if needed
})

# === VISUALIZATION CONFIGURATION ===
# Define consistent ordering and color schemes for all dashboard visualizations

# Gender display order for consistent chart presentation
gender_order = ['Female', 'Male']

# Color scheme for geographic locations (consistent across all charts)
group_colors = {
    'Pittsboro': '#33bfa7',            # Teal/green for upstream community
    'Fayetteville': '#f07f2f',         # Orange for mid-region community  
    'Lower Cape Fear Region': '#6e7ee0' # Blue for downstream communities
}

# Color scheme for PFAS compounds (distinct colors for each compound)
group_colors_pfas = {
    'PFOA': '#FFA07A',          # Light salmon
    'PFOS': '#B3C774',          # Light olive green
    'PFNA': '#FF8C42',          # Orange
    'PFO5DoA': '#66CDAA',       # Medium aquamarine
    'PFHxS': '#A5B3E0',         # Light blue
    'PFDA': '#8093E1',          # Medium slate blue
    'PFUnDA': '#52B8A7',        # Teal
    'MeFOSAA': '#9FC08B',       # Light green
    'Nafion byproduct 2': '#FFB6C1'  # Light pink
}

# === MATPLOTLIB/SEABORN STYLE CONFIGURATION ===
# Set consistent styling for matplotlib-based visualizations
plt.rcParams['font.family'] = 'Lato'        # Professional, readable font
plt.rcParams['font.size'] = 12               # Base font size
plt.rcParams['axes.labelsize'] = 12          # Axis label font size
plt.rcParams['axes.titlesize'] = 14          # Chart title font size
sns.set_style("whitegrid")                   # Clean grid style for seaborn plots

# === FINAL COLUMN RENAMING ===
# Rename columns to match expected names throughout the dashboard
complete.rename(columns={
    'study_loc': 'Location',  # Standardize location column name
    'study_year': 'Year'      # Standardize year column name
}, inplace=True)

# === CATEGORICAL ORDERING DEFINITIONS ===
# Define consistent orderings for all categorical variables used in visualizations

# Age group ordering (youngest to oldest)
age_order = ["6-17", "18-50", "51-70", ">70"]

# Years lived in community ordering (shortest to longest duration)
year_cat_order = ["1-5", "6-10", "11-15", "16-20", "21-25", "26-30", "31-35", 
                  "36-40", "41-45", "46-50", "51-55", "56-60", ">60 years"]

# Ensure Year column is categorical for proper handling in visualizations
complete['Year'] = complete['Year'].astype("category")

# Geographic location ordering (consistent with upstream to downstream flow)
fixed_location = ['Pittsboro', 'Fayetteville', 'Lower Cape Fear Region']

# === UTILITY FUNCTIONS ===
# Custom functions for enhanced visualization formatting

def adjust_box_widths(g, fac):
    """
    Adjust the widths of a seaborn-generated boxplot for better visual spacing.
    
    This function modifies boxplot elements to create better separation between
    grouped boxplots, improving readability when multiple categories are displayed.
    
    Args:
        g: Seaborn plot object (FacetGrid or similar)
        fac (float): Scaling factor for box width adjustment (typically 0.6-0.9)
    
    Returns:
        None: Modifies the plot object in place
        
    Note: Remove this function if switching to alternative plotting packages
    """
    for ax in g.axes:
        # Iterate through all chart elements in each axis
        for c in ax.get_children():
            # Look for PathPatch objects (the box elements in boxplots)
            if isinstance(c, PathPatch):
                # Get current box dimensions
                p = c.get_path()
                verts = p.vertices
                verts_sub = verts[:-1]  # Remove last vertex (duplicate of first)
                xmin = np.min(verts_sub[:, 0])  # Left edge of box
                xmax = np.max(verts_sub[:, 0])  # Right edge of box
                xmid = 0.5*(xmin+xmax)          # Center of box
                xhalf = 0.5*(xmax - xmin)       # Half-width of box

                # Calculate new box dimensions with scaling factor
                xmin_new = xmid-fac*xhalf  # New left edge (narrower)
                xmax_new = xmid+fac*xhalf  # New right edge (narrower)
                
                # Apply new dimensions to box vertices
                verts_sub[verts_sub[:, 0] == xmin, 0] = xmin_new
                verts_sub[verts_sub[:, 0] == xmax, 0] = xmax_new

                # Adjust median line width to match new box width
                for l in ax.lines:
                    if np.all(l.get_xdata() == [xmin, xmax]):
                        l.set_xdata([xmin_new, xmax_new])

# === DYNAMIC PYTHON FILE EXECUTION FUNCTION ===
def read_python(file_path):
    """
    Dynamically read and execute Python files for modular dashboard organization.
    
    This function allows the main application to load and run separate Python files
    for each dashboard tab, keeping code organized and maintainable.
    
    Args:
        file_path (str): Path to the Python file to execute
        
    Returns:
        None: Executes the file content in the current namespace
        
    Note: All variables from master_file.py are available to executed files
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        code = file.read()
    exec(code)

# === STREAMLIT TAB STYLING ===
# Inject custom CSS to enhance tab appearance and usability
# This styling makes tabs larger and more accessible for users
st.markdown("""
    <style>
    /* Make tab labels much larger and add more padding for better UX */
    .stTabs [data-baseweb="tab"] {
        font-size: 2rem !important;        /* Larger font for better readability */
        padding: 1.5rem 4rem !important;   /* More padding for easier clicking */
        font-weight: 700 !important;       /* Bold text for prominence */
        min-height: 60px !important;       /* Minimum height for touch-friendly interface */
        line-height: 1.2 !important;       /* Proper line spacing */
    }
    
    /* Add spacing between tabs for cleaner appearance */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important;               /* Space between individual tabs */
    }
    
    /* Ensure tab content has proper spacing from tab headers */
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 2rem !important;      /* Space between tabs and content */
    }
    </style>
""", unsafe_allow_html=True)

# === MAIN NAVIGATION SYSTEM ===
# Create the primary navigation interface for the dashboard
# Each tab corresponds to a different analysis view or information section

# Define tab titles in logical order for user workflow
tab_titles = [
    "Home",                    # Overview and study introduction
    "Understanding Box Plots", # Education on how to read the box plots that we use
    "View Individual PFAS",    # Individual compound analysis
    "View by location",        # Geographic comparison analysis
    "NASEM 7 Summed PFAS",     # Combined PFAS exposure analysis
    "Learn More"               # Educational content and methodology
]

# Create Streamlit tab interface
tabs = st.tabs(tab_titles)

# === TAB CONTENT EXECUTION ===
# Load and execute content for each tab using separate Python files
# This modular approach keeps code organized and maintainable

# Home tab: Study overview and demographic summaries
with tabs[0]:
    read_python('Home.py')

# Understanding Box Plots tab: Education on how to read the box plots that we use
with tabs[1]:
    read_python('Understanding Box Plots.py')

# Individual PFAS analysis tab: Detailed compound-specific visualizations
with tabs[2]:
    read_python('View Individual PFAS2.py')

# Location-based analysis tab: Geographic comparisons
with tabs[3]:
    read_python('View by Location.py')

# NASEM 7 summed analysis tab: Combined exposure assessment
with tabs[4]:
    read_python('View Summed PFAS3.py')

# Educational content tab: Background information and methodology
with tabs[5]:
    read_python('Learn More.py')




#  find how to deploy the page






