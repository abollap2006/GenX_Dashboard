# GenX Exposure Study Dashboard - Complete Project Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [File Structure](#file-structure)
4. [Data Pipeline](#data-pipeline)
5. [Component Documentation](#component-documentation)
6. [Deployment Guide](#deployment-guide)
7. [Maintenance & Updates](#maintenance--updates)
8. [Troubleshooting](#troubleshooting)
9. [Handover Checklist](#handover-checklist)

## Project Overview

### Purpose
The GenX Exposure Study Dashboard is a Streamlit-based web application that visualizes PFAS (per- and polyfluoroalkyl substances) blood concentration data from three North Carolina communities: Pittsboro, Fayetteville, and the Lower Cape Fear Region.

### Key Features
- **Interactive Visualizations**: Boxplots using Altair for individual PFAS analysis
- **Multi-View Analysis**: Individual PFAS, summed NASEM 7, and location-based comparisons
- **NHANES Integration**: National health survey data for benchmarking
- **Responsive Design**: Works on desktop and mobile devices
- **Educational Content**: Built-in explanations and clinical guidance

### Target Users
- Researchers and scientists studying PFAS exposure
- Public health officials
- Community members from the study areas
- Healthcare providers needing clinical guidance

## System Architecture

### Technology Stack
- **Frontend**: Streamlit (Python web framework)
- **Visualization**: 
  - Altair (primary charting library for boxplots)
  - Plotly (for pie charts and bar charts)
  - Matplotlib/Seaborn (legacy support)
- **Data Processing**: Pandas, NumPy
- **Deployment**: Streamlit Cloud (recommended)

### Application Structure
```
Streamlit App (master_file.py)
├── Tab 1: Home (Home.py)
├── Tab 2: View Individual PFAS (View Individual PFAS.py)
├── Tab 3: View Summed NASEM 7 (View Summed PFAS.py)
├── Tab 4: View by Location (View by Location.py)
└── Tab 5: Learn More (Learn More.py)
```

## File Structure

### Core Application Files
```
GenX_Study_Dashboard/
├── master_file.py              # Main application entry point
├── Home.py                     # Dashboard home page and summary statistics
├── View Individual PFAS.py     # Individual PFAS analysis interface
├── View Summed PFAS.py         # NASEM 7 combined analysis
├── View by Location.py         # Location-based comparison analysis
├── Learn More.py               # Educational content and FAQs
└── requirements.txt            # Python dependencies
```

### Data Files
```
├── GenX_2017-2023_PFAS_Data.csv          # Main PFAS blood concentration data
├── QX_2017-2019_Data.csv                 # Demographics data 2017-2019
├── QX_2020-2021_Data.csv                 # Demographics data 2020-2021
├── QX_2023_Data.csv                      # Demographics data 2023
├── 2017-2020_Nhanes_NASEM7_Summaries.csv # NHANES reference data
└── P_PFAS.xlsx - Sheet1.csv              # Raw NHANES data (optional)
```

### Assets
```
├── study map.png                    # Study area map
├── Median.png                       # Boxplot explanation infographic
├── NAESM_Guidance.png              # NASEM clinical guidance image
├── Clinical Follow Up Graphic.png   # Clinical follow-up flowchart
└── [Various PFAS Legend images]     # Legend graphics
```

## Data Pipeline

### Data Flow Overview
1. **Data Loading** (master_file.py)
   - Load PFAS concentration data
   - Load demographics data from multiple years
   - Load NHANES reference data

2. **Data Preprocessing**
   - Standardize community names
   - Create unique participant IDs
   - Merge demographics with PFAS data
   - Apply categorical data types

3. **Data Filtering & Analysis**
   - Apply 50% detection rate threshold
   - Calculate statistical quantiles (5th, 25th, 50th, 75th, 95th percentiles)
   - Clip outliers to 5th-95th percentile range

### Key Data Transformations

#### Community Name Standardization
```python
# Numeric codes to readable names
{
    1: "Lower Cape Fear Region",
    2: 'Fayetteville', 
    3: 'Pittsboro'
}
```

#### Age Group Categories
```python
age_categories = {
    "1.0": "6-17", "2.0": "6-17", 
    "3.0": "18-50", "4.0": "18-50",
    "5.0": "51-70", "6.0": ">70"
}
```

#### Years Lived Categories
```python
years_lived = ["1-5", "6-10", "11-15", "16-20", "21-25", "26-30", "31-35"]
```

## Component Documentation

### 1. Master File (master_file.py)

**Purpose**: Application entry point and global data setup

**Key Functions**:
- `read_python(file_path)`: Dynamically loads and executes Python files for each tab
- Data loading and preprocessing
- Tab navigation setup
- Global variable definitions

**Important Variables**:
```python
# Color schemes
group_colors = {
    'Pittsboro':'#33bfa7', 
    'Fayetteville':'#f07f2f', 
    'Lower Cape Fear Region':'#6e7ee0'
}

group_colors_pfas = {
    'PFOA':'#FFA07A', 'PFOS':'#B3C774', 'PFNA':'#FF8C42',
    'PFO5DoA':'#66CDAA', 'PFHxS':'#A5B3E0', 'PFDA':'#8093E1',
    'PFUnDA':'#52B8A7', 'MeFOSAA':'#9FC08B', 'Nafion byproduct 2':'#FFB6C1'
}

# PFAS groupings by concentration range
large_range = ["PFOS", "PFOA", "PFO5DoA"]     # 0-30 ng/mL
medium_range = ["PFHxS", "PFNA", "Nafion byproduct 2"]  # 0-10 ng/mL  
small_range = ["PFDA", "PFUnDA", "MeFOSAA"]   # 0-1.6 ng/mL
```

### 2. Home Page (Home.py)

**Purpose**: Welcome page with study overview and demographic summaries

**Key Functions**:
- `summary_stats(location, summary_data, color)`: Creates demographic charts for each location
  - Age distribution (horizontal bar chart)
  - Gender distribution (pie chart)  
  - Years lived in community (horizontal bar chart)

**Chart Specifications**:
- All charts use location-specific colors
- Percentages rounded to whole numbers
- Responsive design with transparent backgrounds
- Custom hover templates showing percentages only

### 3. View Individual PFAS (View Individual PFAS.py)

**Purpose**: Individual PFAS analysis with location comparisons

**Key Functions**:
- `pfas_by_row(pfas_list, y_max, df_plot_adjusted, ...)`: Creates boxplot visualizations
- `format_year_label(year)`: Converts years to abbreviated format (2017, '18, '19, etc.)

**Visualization Features**:
- Custom Altair boxplots with consistent styling
- Location-based color coding
- NHANES reference lines (red horizontal lines)
- Dynamic y-axis scaling based on PFAS concentration ranges
- Grouped by concentration ranges (large/medium/small)

**Data Processing**:
- 50% detection rate filtering
- Minimum 2 samples per group requirement
- 5th-95th percentile outlier clipping
- Quantile calculations for boxplot components

### 4. View Summed PFAS (View Summed PFAS.py)

**Purpose**: NASEM 7 combined PFAS analysis with clinical guidance

**Key Features**:
- Summed concentrations of 7 PFAS chemicals with clinical guidance
- Clinical risk thresholds (2 ng/mL low risk, 20 ng/mL high risk)
- Optional NHANES national comparison
- Educational content about clinical implications

**Key Functions**:
- `process_nhanes_raw_data()`: Processes raw NHANES data for comparison
- PFAS concentration summation for NASEM 7 chemicals
- Risk level visualization with reference lines

**Clinical Guidance Integration**:
- Low Risk: < 2 ng/mL (light blue line)
- High Risk: ≥ 20 ng/mL (red line)
- NASEM 7 chemicals: PFOA, PFOS, PFHxS, PFNA, PFDA, PFUnDA, MeFOSAA

### 5. View by Location (View by Location.py)

**Purpose**: Location-centered analysis showing all PFAS for each community

**Key Functions**:
- `view_by_location(pfas_range, predefined_order, ...)`: Creates location-specific visualizations
- Dynamic legend generation based on selected PFAS
- Consistent styling across all location charts

**Layout**:
- 3x3 grid layout for multiple locations
- Grouped by PFAS concentration ranges
- Individual legends for each PFAS group
- Responsive chart sizing

### 6. Learn More (Learn More.py)

**Purpose**: Educational content and frequently asked questions

**Content Areas**:
- PFAS background information
- Study methodology explanations
- Contact information
- Privacy and data protection policies
- Links to external resources

## Deployment Guide

### Local Development Setup

1. **Environment Setup**:
```bash
# Clone repository
git clone [repository-url]
cd GenX_Study_Dashboard

# Install dependencies
pip install -r requirements.txt
```

2. **Data Setup**:
   - Download data files from Google Drive
   - Place all CSV files in project root directory
   - Verify file paths match those in master_file.py

3. **Run Application**:
```bash
streamlit run master_file.py
```

### Streamlit Cloud Deployment

1. **Repository Preparation**:
   - Ensure all code is committed to GitHub
   - Add requirements.txt with all dependencies
   - Upload data files to repository or cloud storage

2. **Streamlit Cloud Setup**:
   - Visit share.streamlit.io
   - Connect GitHub repository
   - Select master_file.py as main file
   - Configure any environment variables

3. **Data Considerations**:
   - Large CSV files may need external hosting
   - Consider using Streamlit secrets for sensitive data
   - Test data loading performance

### Production Considerations

- **Data Security**: Implement proper access controls for sensitive health data
- **Performance**: Monitor loading times with large datasets
- **Scalability**: Consider caching for frequently accessed data
- **Backup**: Regular backups of both code and data
- **Monitoring**: Set up error tracking and usage analytics

## Maintenance & Updates

### Regular Maintenance Tasks

1. **Data Updates**:
   - Add new year's data following existing file format
   - Update year ranges in dropdown selectors
   - Verify new data compatibility with existing code

2. **Code Maintenance**:
   - Update dependencies in requirements.txt
   - Test compatibility with new Streamlit versions
   - Monitor for deprecated function warnings

3. **Content Updates**:
   - Update educational content in Learn More section
   - Add new FAQs based on user feedback
   - Update contact information as needed

### Adding New Features

1. **New PFAS Chemicals**:
   - Add to appropriate concentration range group
   - Update color scheme in group_colors_pfas
   - Test visualization scaling

2. **New Locations**:
   - Update location lists and color schemes
   - Modify chart layouts if needed
   - Update demographic summary functions

3. **New Analysis Types**:
   - Follow existing tab structure
   - Create new Python file for complex features
   - Update master_file.py tab configuration

## Troubleshooting

### Common Issues

1. **Data Loading Errors**:
   - Verify all CSV files are present
   - Check file paths in master_file.py
   - Ensure column names match expected format

2. **Visualization Problems**:
   - Clear browser cache
   - Check for missing data in selected filters
   - Verify color scheme consistency

3. **Performance Issues**:
   - Monitor dataset size and filtering efficiency
   - Consider data caching strategies
   - Optimize groupby operations

### Error Handling

- All groupby operations include `observed=True` to prevent pandas warnings
- Empty data checks prevent visualization errors
- Graceful degradation when optional features fail

### Debugging Tips

1. **Data Inspection**:
```python
# Add debugging statements
st.write("Debug data shape:", df.shape)
st.write("Debug columns:", df.columns.tolist())
```

2. **Streamlit Debugging**:
   - Use st.write() for variable inspection
   - Enable Streamlit's debugging mode
   - Check browser console for JavaScript errors

## Handover Checklist

### Knowledge Transfer Requirements

- [ ] **Technical Documentation**: Complete understanding of architecture
- [ ] **Data Sources**: Access to all data files and update procedures  
- [ ] **Deployment Access**: Streamlit Cloud account and repository access
- [ ] **Domain Knowledge**: Understanding of PFAS research and clinical guidance
- [ ] **Stakeholder Contacts**: Research team and end-user contact information

### Critical System Knowledge

1. **Data Processing Pipeline**:
   - 50% detection rate threshold rationale
   - Statistical methods for outlier handling
   - NHANES data integration approach

2. **Visualization Design Decisions**:
   - Color scheme rationale (accessibility, branding)
   - Chart type selections for different data types
   - Responsive design considerations

3. **User Experience Priorities**:
   - Educational content balance with data presentation
   - Privacy protection through aggregation
   - Clinical guidance integration

### Ongoing Responsibilities

- **Data Updates**: Annual addition of new study data
- **Content Maintenance**: Educational material updates
- **Technical Support**: User support and bug fixes
- **Compliance**: Health data privacy requirements
- **Performance Monitoring**: Usage analytics and optimization

### Emergency Contacts

- **Technical Issues**: [Your contact information]
- **Data Questions**: GenX Study Team (genx-exposure-study@ncsu.edu)
- **Deployment Issues**: Streamlit support
- **Content Updates**: Research team lead

---

*This documentation was created to ensure smooth project transition and ongoing maintenance. For questions or clarifications, please contact the development team.*
