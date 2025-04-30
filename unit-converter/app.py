import streamlit as st
import pandas as pd

def main():
    st.title("Unit Converter")
    st.write("Convert between different units of measurement")
    
    # Create tabs for different conversion categories
    categories = ["Length", "Weight/Mass", "Temperature", "Area", "Volume", "Time", "Speed", "Pressure", "Energy"]
    
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs(categories)
    
    with tab1:  # Length
        st.header("Length Conversion")
        length_units = {
            "Meter (m)": 1.0,
            "Kilometer (km)": 0.001,
            "Centimeter (cm)": 100.0,
            "Millimeter (mm)": 1000.0,
            "Mile (mi)": 0.000621371,
            "Yard (yd)": 1.09361,
            "Foot (ft)": 3.28084,
            "Inch (in)": 39.3701
        }
        convert_units(length_units, "Length")
    
    with tab2:  # Weight/Mass
        st.header("Weight/Mass Conversion")
        weight_units = {
            "Kilogram (kg)": 1.0,
            "Gram (g)": 1000.0,
            "Milligram (mg)": 1000000.0,
            "Pound (lb)": 2.20462,
            "Ounce (oz)": 35.274,
            "Metric Ton (t)": 0.001,
            "Stone (st)": 0.157473
        }
        convert_units(weight_units, "Weight/Mass")
    
    with tab3:  # Temperature
        st.header("Temperature Conversion")
        temp_input = st.number_input("Enter value:", value=0.0, key="temp_value")
        from_temp = st.selectbox("From:", ["Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)"], key="from_temp")
        to_temp = st.selectbox("To:", ["Fahrenheit (°F)", "Celsius (°C)", "Kelvin (K)"], key="to_temp")
        
        if st.button("Convert Temperature"):
            result = convert_temperature(temp_input, from_temp, to_temp)
            st.success(f"{temp_input} {from_temp} = {result:.4f} {to_temp}")
    
    with tab4:  # Area
        st.header("Area Conversion")
        area_units = {
            "Square Meter (m²)": 1.0,
            "Square Kilometer (km²)": 0.000001,
            "Square Centimeter (cm²)": 10000.0,
            "Square Millimeter (mm²)": 1000000.0,
            "Square Mile (mi²)": 3.861e-7,
            "Square Yard (yd²)": 1.19599,
            "Square Foot (ft²)": 10.7639,
            "Square Inch (in²)": 1550.0,
            "Acre": 0.000247105,
            "Hectare (ha)": 0.0001
        }
        convert_units(area_units, "Area")
    
    with tab5:  # Volume
        st.header("Volume Conversion")
        volume_units = {
            "Cubic Meter (m³)": 1.0,
            "Liter (L)": 1000.0,
            "Milliliter (mL)": 1000000.0,
            "Gallon (US)": 264.172,
            "Quart (US)": 1056.69,
            "Pint (US)": 2113.38,
            "Fluid Ounce (US)": 33814.0,
            "Cubic Foot (ft³)": 35.3147,
            "Cubic Inch (in³)": 61023.7
        }
        convert_units(volume_units, "Volume")
    
    with tab6:  # Time
        st.header("Time Conversion")
        time_units = {
            "Second (s)": 1.0,
            "Millisecond (ms)": 1000.0,
            "Microsecond (μs)": 1000000.0,
            "Minute (min)": 1/60,
            "Hour (h)": 1/3600,
            "Day (d)": 1/86400,
            "Week (wk)": 1/604800,
            "Month (30 days)": 1/2592000,
            "Year (365 days)": 1/31536000
        }
        convert_units(time_units, "Time")
    
    with tab7:  # Speed
        st.header("Speed Conversion")
        speed_units = {
            "Meter per second (m/s)": 1.0,
            "Kilometer per hour (km/h)": 3.6,
            "Mile per hour (mph)": 2.23694,
            "Foot per second (ft/s)": 3.28084,
            "Knot (kn)": 1.94384
        }
        convert_units(speed_units, "Speed")
    
    with tab8:  # Pressure
        st.header("Pressure Conversion")
        pressure_units = {
            "Pascal (Pa)": 1.0,
            "Kilopascal (kPa)": 0.001,
            "Bar": 0.00001,
            "Atmosphere (atm)": 9.86923e-6,
            "Millimeter of Mercury (mmHg)": 0.00750062,
            "Pound per square inch (psi)": 0.000145038
        }
        convert_units(pressure_units, "Pressure")
    
    with tab9:  # Energy
        st.header("Energy Conversion")
        energy_units = {
            "Joule (J)": 1.0,
            "Kilojoule (kJ)": 0.001,
            "Calorie (cal)": 0.239006,
            "Kilocalorie (kcal)": 0.000239006,
            "Watt-hour (Wh)": 0.000277778,
            "Kilowatt-hour (kWh)": 2.77778e-7,
            "Electronvolt (eV)": 6.242e+18,
            "British Thermal Unit (BTU)": 0.000947817
        }
        convert_units(energy_units, "Energy")
    
    # Add footer
    st.divider()
    st.caption("Unit Converter App - Built with Streamlit")

def convert_units(units_dict, category):
    col1, col2 = st.columns(2)
    
    with col1:
        value = st.number_input(f"Enter {category} value:", value=1.0, key=f"{category}_value")
        from_unit = st.selectbox("From:", list(units_dict.keys()), key=f"from_{category}")
    
    with col2:
        to_unit = st.selectbox("To:", list(units_dict.keys()), key=f"to_{category}")
        if st.button(f"Convert {category}"):
            # Convert to base unit, then to target unit
            base_value = value / units_dict[from_unit]  # Convert to base unit
            result = base_value * units_dict[to_unit]   # Convert to target unit
            st.success(f"{value} {from_unit} = {result:.6g} {to_unit}")
    
    # Show conversion table
    if st.checkbox(f"Show {category} conversion table", key=f"table_{category}"):
        show_conversion_table(units_dict, category)

def convert_temperature(value, from_unit, to_unit):
    # First convert to Celsius as base unit
    if from_unit == "Celsius (°C)":
        celsius = value
    elif from_unit == "Fahrenheit (°F)":
        celsius = (value - 32) * 5/9
    elif from_unit == "Kelvin (K)":
        celsius = value - 273.15
    
    # Then convert from Celsius to target unit
    if to_unit == "Celsius (°C)":
        return celsius
    elif to_unit == "Fahrenheit (°F)":
        return celsius * 9/5 + 32
    elif to_unit == "Kelvin (K)":
        return celsius + 273.15

def show_conversion_table(units_dict, category):
    # Create reference table
    st.subheader(f"{category} Conversion Reference")
    
    # Create a list to store the data
    data = []
    base_unit = list(units_dict.keys())[0]  # Use first unit as reference
    base_value = 1.0  # Convert from 1 of the base unit
    
    for unit in units_dict.keys():
        # Calculate conversion from base unit to current unit
        conversion_factor = units_dict[unit] / units_dict[base_unit]
        result = base_value * conversion_factor
        data.append({
            "Unit": unit,
            f"Value (1 {base_unit} =)": f"{result:.6g}"
        })
    
    # Create and display the DataFrame
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    st.set_page_config(
        page_title="Unit Converter",
        page_icon="🔄",
        layout="wide"
    )
    main()