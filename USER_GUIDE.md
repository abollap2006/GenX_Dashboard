# GenX Exposure Study Dashboard - User Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Dashboard Overview](#dashboard-overview)
3. [Navigation Guide](#navigation-guide)
4. [Feature Explanations](#feature-explanations)
5. [Data Interpretation](#data-interpretation)
6. [Frequently Asked Questions](#frequently-asked-questions)
7. [Support](#support)

## Getting Started

### What is this Dashboard?
The GenX Exposure Study Dashboard is an interactive web application that visualizes PFAS (Per- and polyfluoroalkyl substances) exposure data from the Cape Fear River Basin study. It allows researchers, public health officials, and community members to explore PFAS concentrations across different locations, time periods, and demographic groups.

### How to Access
1. **Web Browser**: Visit the dashboard URL (provided by your administrator)
2. **Supported Browsers**: Chrome, Firefox, Safari, Edge (latest versions)
3. **Device Compatibility**: Desktop, tablet, and mobile devices
4. **No Installation Required**: The dashboard runs entirely in your web browser

### First-Time Users
When you first visit the dashboard:
1. The application will load the main interface
2. Default data will be displayed
3. All interactive features are immediately available
4. No login or registration required

## Dashboard Overview

### Main Interface Components

#### 1. Navigation Tabs
Located at the top of the screen, five main sections:
- **Home**: Overview and study background
- **Learn More**: Detailed information about PFAS and methodology
- **View by Location**: Compare PFAS levels across geographic locations
- **View Individual PFAS**: Analyze specific PFAS compounds
- **View Summed PFAS**: Examine combined PFAS exposure (NASEM 7)

#### 2. Sidebar Controls
Interactive filters and options (varies by tab):
- **Location Selection**: Choose specific geographic areas
- **Year Range**: Filter data by time period
- **PFAS Selection**: Choose specific compounds to analyze
- **Demographic Filters**: Age groups, gender, etc.

#### 3. Main Content Area
Displays visualizations, data tables, and analysis results based on your selections.

#### 4. Information Panels
Contextual information, legends, and explanations appear alongside visualizations.

## Navigation Guide

### Home Tab
**Purpose**: Provides study overview and demographic summaries

**What You'll See**:
- Study background and objectives
- Participant demographics by location
- Summary statistics
- Key findings highlights

**How to Use**:
- Read the overview to understand the study context
- Explore demographic charts to understand participant populations
- No interactive controls - informational only

### Learn More Tab
**Purpose**: Educational content about PFAS and study methodology

**What You'll See**:
- PFAS background information
- Health implications
- Study methodology
- Data collection details
- Scientific references

**How to Use**:
- Scroll through sections for comprehensive background
- Use as reference material for understanding results
- Links to external resources for deeper learning

### View by Location Tab
**Purpose**: Compare PFAS exposure levels across different geographic locations

**Interactive Controls**:
- **Select Locations**: Choose multiple locations to compare
- **Select PFAS**: Choose which compounds to display
- **Year Filter**: Adjust time period for analysis

**What You'll See**:
- Box plots showing PFAS concentration distributions
- Median lines indicating typical exposure levels
- Whiskers showing data range
- Individual data points (when appropriate)
- NHANES comparison data for context

**How to Interpret**:
- Higher box positions = higher PFAS concentrations
- Longer boxes = more variability in exposure
- Points above whiskers = potential outliers
- Compare locations to identify geographic patterns

### View Individual PFAS Tab
**Purpose**: Deep dive into specific PFAS compounds across locations

**Interactive Controls**:
- **Select PFAS**: Choose one compound for detailed analysis
- **Select Locations**: Choose locations to compare
- **Year Filter**: Adjust time period

**What You'll See**:
- Detailed distribution for selected PFAS
- Location-specific patterns
- Temporal trends (if multiple years selected)
- NHANES reference lines for population context

**How to Interpret**:
- Focus on one compound at a time for clarity
- Compare exposure levels across locations
- Identify which areas have highest/lowest levels
- Use NHANES data as national reference point

### View Summed PFAS Tab
**Purpose**: Analyze combined exposure to NASEM 7 PFAS compounds

**Interactive Controls**:
- **Select Locations**: Choose areas to analyze
- **Clinical Guidance Toggle**: Show/hide risk thresholds

**What You'll See**:
- Combined PFAS exposure levels (sum of 7 key compounds)
- Clinical guidance thresholds (when enabled)
- Population risk distribution
- Comparison with national data

**How to Interpret**:
- Higher values = greater combined PFAS exposure
- Clinical thresholds indicate potential health concern levels
- Use for overall exposure assessment
- Identify populations at potentially higher risk

## Feature Explanations

### Interactive Filters

#### Location Selection
- **Multi-select**: Choose multiple locations simultaneously
- **Clear All**: Reset to no selections
- **Select All**: Choose all available locations
- **Geographic Context**: Locations represent specific communities in the Cape Fear Basin

#### PFAS Selection
- **Individual Compounds**: Choose specific PFAS chemicals
- **Chemical Names**: Both common and scientific names provided
- **Compound Information**: Hover for additional details
- **Health Relevance**: Focus on compounds with known health implications

#### Year Filtering
- **Range Selection**: Choose start and end years
- **Data Availability**: Only years with data are selectable
- **Temporal Analysis**: Compare trends over time
- **Study Period**: Covers 2017-2023 collection period

### Visualization Features

#### Box Plots
- **Central Box**: Shows 25th to 75th percentile (middle 50% of data)
- **Median Line**: Thick line shows typical exposure level
- **Whiskers**: Extend to show full data range
- **Outliers**: Individual points beyond whiskers

#### Interactive Elements
- **Hover Information**: Point to data for detailed values
- **Zoom**: Click and drag to zoom into specific regions
- **Pan**: Drag to move around zoomed views
- **Reset View**: Double-click to return to full view

#### Color Coding
- **Location Colors**: Each location has consistent color scheme
- **Transparency**: Overlapping data uses transparency for clarity
- **NHANES Data**: Reference population data in distinct styling

## Data Interpretation

### Understanding PFAS Concentrations

#### Units of Measurement
- **ng/mL**: Nanograms per milliliter (parts per billion)
- **Serum Concentrations**: Measured in blood serum
- **Detection Limits**: Values below detection marked appropriately

#### Concentration Ranges
- **Low**: < 1 ng/mL
- **Moderate**: 1-10 ng/mL  
- **High**: > 10 ng/mL
- **Very High**: > 100 ng/mL

*Note: These ranges are general guidelines; health significance varies by compound*

#### Statistical Concepts

**Median vs. Mean**:
- **Median**: Middle value when data is sorted (less affected by outliers)
- **Mean**: Average value (can be skewed by extreme values)
- **Dashboard Focus**: Primarily uses medians for robustness

**Percentiles**:
- **25th Percentile**: 25% of people have lower exposure
- **75th Percentile**: 75% of people have lower exposure
- **Box**: Represents 25th to 75th percentile range

**Outliers**:
- **Definition**: Values significantly higher or lower than typical
- **Causes**: Individual variation, measurement factors, exposure circumstances
- **Interpretation**: May warrant individual investigation

### Comparing Populations

#### Geographic Comparisons
- **Upstream vs. Downstream**: Consider river flow direction
- **Distance from Sources**: Proximity to industrial activities
- **Community Characteristics**: Demographics, water sources, lifestyle factors

#### Temporal Trends
- **Increasing Trends**: May indicate ongoing contamination
- **Decreasing Trends**: Could suggest remediation effectiveness
- **Seasonal Variation**: Some PFAS may show temporal patterns
- **Study Duration**: Consider timeframe when interpreting trends

#### NHANES Context
- **National Reference**: NHANES provides U.S. population context
- **Comparison Value**: Local levels relative to national background
- **Population Differences**: Consider demographic and geographic factors

### Clinical Significance

#### Risk Assessment
- **No Safe Level**: No established "safe" levels for many PFAS
- **Relative Risk**: Compare across locations and compounds
- **Combined Exposure**: NASEM 7 provides cumulative assessment
- **Individual Variation**: Personal risk depends on multiple factors

#### Health Guidance
- **Clinical Thresholds**: Based on available health studies
- **Evolving Science**: Guidelines may change as research advances
- **Medical Consultation**: Individual health decisions require medical expertise
- **Population Health**: Dashboard supports public health assessment

## Frequently Asked Questions

### General Questions

**Q: What is PFAS?**
A: PFAS (Per- and polyfluoroalkyl substances) are synthetic chemicals used in various industrial and consumer products. They're often called "forever chemicals" because they don't break down naturally and can accumulate in people and the environment.

**Q: Why study the Cape Fear Basin?**
A: This region has documented PFAS contamination from industrial sources, making it important for understanding community exposure patterns and health implications.

**Q: Who can use this dashboard?**
A: Researchers, public health officials, community members, policymakers, and anyone interested in understanding PFAS exposure in this region.

### Technical Questions

**Q: How current is the data?**
A: Data covers the period 2017-2023, with the most recent data incorporated as it becomes available through the ongoing study.

**Q: What do the error messages mean?**
A: If you see errors, try refreshing the page or contact support. Common issues include internet connectivity or browser compatibility.

**Q: Can I download the data?**
A: Contact the research team for data access requests. Some data may be available for research purposes following appropriate protocols.

**Q: Why do some locations have more data points?**
A: Participant recruitment and study design factors may result in different sample sizes across locations and time periods.

### Interpretation Questions

**Q: What levels should I be concerned about?**
A: The dashboard provides context through comparisons and reference data, but individual health decisions should involve medical consultation.

**Q: Why do PFAS levels vary so much between people?**
A: Individual exposure depends on many factors including occupation, diet, consumer product use, environmental exposure, and genetic factors affecting elimination.

**Q: How do these levels compare nationally?**
A: NHANES reference data provides national context, though direct comparison requires considering demographic and geographic differences.

**Q: What does it mean if my location has high levels?**
A: Higher levels indicate greater exposure in that community. This information supports public health assessment and potential intervention decisions.

### Dashboard Use Questions

**Q: Why can't I select certain options?**
A: Some filters may be disabled when insufficient data is available for meaningful analysis.

**Q: How do I reset the view?**
A: Use the clear/reset buttons in filters, or refresh the page to return to default settings.

**Q: Can I save my analysis?**
A: Currently, analyses are not saved automatically. Consider taking screenshots of important findings.

**Q: Why is the dashboard slow?**
A: Large datasets and complex visualizations may take time to load. Reducing the number of selected filters can improve performance.

## Support

### Getting Help

#### Technical Issues
- **Browser Problems**: Try refreshing page, clearing cache, or using a different browser
- **Loading Issues**: Check internet connection; large datasets may take time to load
- **Display Problems**: Ensure browser is updated to latest version

#### Content Questions
- **Data Interpretation**: Refer to Learn More section for background
- **Study Methods**: Contact research team for detailed methodology
- **Health Questions**: Consult healthcare providers for personal health decisions

#### Feature Requests
- **Enhancements**: Contact development team with suggestions
- **New Analyses**: Describe desired functionality for future consideration
- **Accessibility**: Report any accessibility issues for improvement

### Contact Information

#### Research Team
- **Email**: genx-exposure-study@ncsu.edu
- **Purpose**: Scientific questions, data interpretation, collaboration
- **Response Time**: 2-3 business days

#### Technical Support
- **Purpose**: Dashboard functionality, technical issues
- **Response Time**: 1-2 business days

#### Data Requests
- **Purpose**: Access to underlying data for research
- **Process**: Formal data request with research proposal
- **Requirements**: IRB approval may be required

### Training and Resources

#### Workshops
- **Public Sessions**: Periodic community workshops on dashboard use
- **Research Training**: Sessions for academic and agency users
- **Custom Training**: Available for organizations upon request

#### Educational Materials
- **Video Tutorials**: Step-by-step guidance for common tasks
- **Webinars**: Periodic presentations on new features and findings
- **Publications**: Peer-reviewed papers describing methods and results

#### Updates and News
- **Newsletter**: Subscribe for updates on new features and findings
- **Social Media**: Follow for community engagement and updates
- **Website**: Check main study website for comprehensive information

---

This user guide provides comprehensive support for all dashboard users, from community members to researchers, ensuring effective and informed use of the GenX Exposure Study Dashboard.
