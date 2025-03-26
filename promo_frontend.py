import streamlit as st
import pandas as pd

def main():
    st.title("Offer Management System")
    
    # Section 1: Offer Selection
    st.header("1. Offer Selection")
    offer_type = st.radio(
        "Select Offer Type",
        ["Choose Preset offers", "Build a custom offer"]
    )
    
    # Initialize session state for filters if not present
    if 'filters' not in st.session_state:
        st.session_state.filters = {
            'discount_type': '% discount',
            'discount_value': 10,
            'country': 'All',
            'city': 'All',
            'age': 'All',
            'gender': 'All',
            'trigger': 'First order',
            'duration_unit': 'days',
            'duration_value': 30,
            'min_order': 10,
            'max_order': 'ANY',
            'product': 'All products',
            'channel': 'Pop-up notification'
        }
    
    # Preset offers
    if offer_type == "Choose Preset offers":
        preset_offers = ["First Purchase offer", "Subscribe to the newsletter and get"]
        selected_preset = st.selectbox("Select a preset offer", preset_offers)
        
        # Set filters based on selected preset
        if selected_preset == "First Purchase offer":
            st.session_state.filters = {
                'discount_type': '% discount',
                'discount_value': 10,
                'country': 'All',
                'city': 'All',
                'age': 'All',
                'gender': 'All',
                'trigger': 'First order',
                'duration_unit': 'days',
                'duration_value': 30,
                'min_order': 10,
                'max_order': 'ANY',
                'product': 'All products',
                'channel': 'Pop-up notification'
            }
        elif selected_preset == "Subscribe to the newsletter and get":
            st.session_state.filters = {
                'discount_type': 'Fixed discount',
                'discount_value': 5,
                'country': 'All',
                'city': 'All',
                'age': 'All',
                'gender': 'All',
                'trigger': 'Subscribe to newsletter',
                'duration_unit': 'days',
                'duration_value': 14,
                'min_order': 0,
                'max_order': 'ANY',
                'product': 'Playing Sets',
                'channel': 'E-mails'
            }
    
    # Section 2: Filters
    st.header("2. Filters")
    
    # Filter 1: What (Value)
    st.subheader("Filter 1: What (Value)")
    col1, col2 = st.columns(2)
    with col1:
        discount_types = ["% discount", "Fixed discount", "Cashback", "Freebies"]
        st.session_state.filters['discount_type'] = st.selectbox(
            "Discount Type", 
            discount_types,
            index=discount_types.index(st.session_state.filters['discount_type']) if st.session_state.filters['discount_type'] in discount_types else 0
        )
    with col2:
        st.session_state.filters['discount_value'] = st.number_input(
            "Value", 
            min_value=0, 
            value=st.session_state.filters['discount_value'] if isinstance(st.session_state.filters['discount_value'], int) else 10
        )
    
    # Filter 2: Who (Segment)
    st.subheader("Filter 2: Who (Segment)")
    
    # Country and City selection
    countries = ["All", "Saudi Arabia", "United Arab Emirates", "Qatar", "Bahrain", "Oman", "Kuwait"]
    
    # Cities by country
    city_by_country = {
        "Saudi Arabia": ["All", "Riyadh", "Jeddah", "Mecca", "Medina", "Dammam"],
        "United Arab Emirates": ["All", "Dubai", "Abu Dhabi", "Sharjah", "Ajman", "Al Ain"],
        "Qatar": ["All", "Doha", "Al Rayyan", "Al Wakrah", "Al Khor", "Mesaieed"],
        "Bahrain": ["All", "Manama", "Riffa", "Muharraq", "Hamad Town", "A'ali"],
        "Oman": ["All", "Muscat", "Salalah", "Sohar", "Sur", "Nizwa"],
        "Kuwait": ["All", "Kuwait City", "Hawalli", "Ahmadi", "Farwaniya", "Jahra"],
        "All": ["All"]
    }
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.filters['country'] = st.selectbox(
            "Country", 
            countries,
            index=countries.index(st.session_state.filters['country']) if st.session_state.filters['country'] in countries else 0
        )
    
    with col2:
        # Get cities based on selected country
        available_cities = city_by_country.get(st.session_state.filters['country'], ["All"])
        
        # Reset city if it's not in the list for the selected country
        if st.session_state.filters['city'] not in available_cities:
            st.session_state.filters['city'] = "All"
            
        st.session_state.filters['city'] = st.selectbox(
            "City", 
            available_cities,
            index=available_cities.index(st.session_state.filters['city']) if st.session_state.filters['city'] in available_cities else 0
        )
    
    col1, col2 = st.columns(2)
    with col1:
        age_options = ["All"] + [str(i) for i in range(1, 101)]
        age_index = 0
        if st.session_state.filters['age'] != 'All':
            try:
                age_index = age_options.index(str(st.session_state.filters['age']))
            except ValueError:
                age_index = 0
        
        selected_age = st.selectbox("Age", age_options, index=age_index)
        st.session_state.filters['age'] = selected_age
    
    with col2:
        gender_options = ["All", "Male", "Female"]
        st.session_state.filters['gender'] = st.selectbox(
            "Gender", 
            gender_options,
            index=gender_options.index(st.session_state.filters['gender']) if st.session_state.filters['gender'] in gender_options else 0
        )
    
    # Filter 3: Why (Trigger)
    st.subheader("Filter 3: Why (Trigger)")
    trigger_options = ["First order", "Referral", "Birthday", "Subscribe to newsletter"]
    st.session_state.filters['trigger'] = st.selectbox(
        "Trigger", 
        trigger_options,
        index=trigger_options.index(st.session_state.filters['trigger']) if st.session_state.filters['trigger'] in trigger_options else 0
    )
    
    # Filter 4: When (Validity)
    st.subheader("Filter 4: When (Validity)")
    
    col1, col2 = st.columns(2)
    with col1:
        duration_options = ["days", "weeks", "hours"]
        st.session_state.filters['duration_unit'] = st.radio(
            "Duration Unit", 
            duration_options,
            index=duration_options.index(st.session_state.filters['duration_unit']) if st.session_state.filters['duration_unit'] in duration_options else 0
        )
    
    with col2:
        st.session_state.filters['duration_value'] = st.number_input(
            f"Duration in {st.session_state.filters['duration_unit']}", 
            min_value=1, 
            value=st.session_state.filters['duration_value'] if isinstance(st.session_state.filters['duration_value'], int) else 30
        )
    
    col1, col2 = st.columns(2)
    with col1:
        min_value = 0
        if st.session_state.filters['min_order'] == 'ANY' or st.session_state.filters['min_order'] == 'N/A':
            min_value = 0
        else:
            min_value = st.session_state.filters['min_order']
            
        st.session_state.filters['min_order'] = st.number_input(
            "Minimum order value (SAR)", 
            min_value=0, 
            value=min_value if isinstance(min_value, int) else 0
        )
    
    with col2:
        max_value = 1000
        if st.session_state.filters['max_order'] == 'ANY' or st.session_state.filters['max_order'] == 'N/A':
            use_max = st.checkbox("Set maximum order value", value=False)
            if use_max:
                st.session_state.filters['max_order'] = st.number_input(
                    "Maximum order value (SAR)", 
                    min_value=0, 
                    value=1000
                )
            else:
                st.session_state.filters['max_order'] = 'ANY'
                st.text("Maximum order value: ANY")
        else:
            use_max = st.checkbox("Set maximum order value", value=True)
            if use_max:
                st.session_state.filters['max_order'] = st.number_input(
                    "Maximum order value (SAR)", 
                    min_value=0, 
                    value=st.session_state.filters['max_order'] if isinstance(st.session_state.filters['max_order'], int) else 1000
                )
            else:
                st.session_state.filters['max_order'] = 'ANY'
                st.text("Maximum order value: ANY")
    
    # Filter 5: Which (Product)
    st.subheader("Filter 5: Which (Product)")
    product_options = [
        "All products",
        "Ride-On And Scooters",
        "Dolls & Collectables",
        "Cars & Vehicles",
        "Fashion & Cosmetics",
        "Playing Sets",
        "Arts & Crafts"
    ]
    st.session_state.filters['product'] = st.selectbox(
        "Product Category", 
        product_options,
        index=product_options.index(st.session_state.filters['product']) if st.session_state.filters['product'] in product_options else 0
    )
    
    # Filter 6: How (Channel)
    st.subheader("Filter 6: How (Channel)")
    channel_options = [
        "Pop-up notification",
        "Notifications",
        "Banners",
        "E-mails",
        "Whatsapp / Social media"
    ]
    st.session_state.filters['channel'] = st.selectbox(
        "Channel", 
        channel_options,
        index=channel_options.index(st.session_state.filters['channel']) if st.session_state.filters['channel'] in channel_options else 0
    )
    
    # Summary
    st.header("Offer Summary")
    st.write(f"""
    **Selected Offer Details:**
    
    - **What:** {st.session_state.filters['discount_type']} - {st.session_state.filters['discount_value']}
    - **Who:** Country: {st.session_state.filters['country']}, City: {st.session_state.filters['city']}, Age: {st.session_state.filters['age']}, Gender: {st.session_state.filters['gender']}
    - **Why:** {st.session_state.filters['trigger']}
    - **When:** {st.session_state.filters['duration_value']} {st.session_state.filters['duration_unit']}, Min: {st.session_state.filters['min_order']} SAR, Max: {st.session_state.filters['max_order']}
    - **Which:** {st.session_state.filters['product']}
    - **How:** {st.session_state.filters['channel']}
    """)
    
    if st.button("Create Offer"):
        st.success("Offer successfully created!")
        st.balloons()

if __name__ == "__main__":
    st.set_page_config(
        page_title="Offer Management System",
        page_icon="🎁",
        layout="wide"
    )
    main()