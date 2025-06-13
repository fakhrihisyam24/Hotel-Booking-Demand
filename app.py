import streamlit as st
import joblib
import numpy as np
import pandas as pd

# Load model
model = joblib.load('BEST_MODEL_for_hotel_booking_demand.pkl')

st.title("Prediksi Pembatalan Booking Hotel")

st.markdown("### Masukkan Data Pelanggan")

# Input numerik
lead_time = st.number_input("Lead Time (0-700)", min_value=0, max_value=700, value=100)
arrival_date_year = st.selectbox("Arrival Year", [2015, 2016, 2017])
arrival_date_month = st.selectbox("Arrival Month", [
    "January", "February", "March", "April", "May", "June", 
    "July", "August", "September", "October", "November", "December"])
arrival_date_week_number = st.number_input("Week Number (1-53)", min_value=1, max_value=53, value=32)
arrival_date_day_of_month = st.number_input("Day of Month (1-31)", min_value=1, max_value=31, value=15)
stays_in_weekend_nights = st.number_input("Weekend Nights (0-19)", min_value=0, max_value=19, value=2)
stays_in_week_nights = st.number_input("Week Nights (0-50)", min_value=0, max_value=50, value=3)
adults = st.number_input("Adults (0-4)", min_value=0, max_value=4, value=2)
children = st.number_input("Children (0-3)", min_value=0, max_value=3)
babies = st.number_input("Babies (0-2)", min_value=0, max_value=2, value=0)
is_repeated_guest = st.selectbox("Repeated Guest", [0, 1])
previous_cancellations = st.number_input("Previous Cancellations", min_value=0, max_value=26, value=0)
previous_bookings_not_canceled = st.number_input("Previous Bookings Not Canceled", min_value=0, max_value=72, value=0)
booking_changes = st.number_input("Booking Changes", min_value=0, max_value=18, value=0)
days_in_waiting_list = st.number_input("Days in Waiting List", min_value=0, max_value=391, value=0)
adr = st.number_input("Average Daily Rate", min_value=0.0, max_value=510.0, value=100.0)
required_car_parking_spaces = st.number_input("Parking Spaces", min_value=0, max_value=3, value=0)
total_of_special_requests = st.number_input("Special Requests", min_value=0, max_value=5, value=0)

# Input kategorikal
hotel = st.selectbox("Hotel Type", ["Resort Hotel", "City Hotel"])
meal = st.selectbox("Meal Type", ["BB", "FB", "HB", "SC"])
country = st.selectbox("Country", ['GBR', 'PRT', 'USA', 'ESP', 'IRL', 'FRA', 'ROU', 'NOR', 'OMN',
       'ARG', 'POL', 'DEU', 'BEL', 'CHE', 'CN', 'GRC', 'ITA', 'NLD',
       'DNK', 'RUS', 'SWE', 'AUS', 'EST', 'CZE', 'BRA', 'FIN', 'MOZ',
       'BWA', 'LUX', 'SVN', 'ALB', 'IND', 'CHN', 'MEX', 'MAR', 'UKR',
       'SMR', 'LVA', 'PRI', 'SRB', 'CHL', 'AUT', 'BLR', 'LTU', 'TUR',
       'ZAF', 'ISR', 'CYM', 'ZMB', 'CPV', 'ZWE', 'DZA', 'KOR', 'CRI',
       'HUN', 'ARE', 'TUN', 'JAM', 'HRV', 'HKG', 'IRN', 'GEO', 'AND',
       'GIB', 'URY', 'JEY', 'CAF', 'CYP', 'COL', 'GGY', 'KWT', 'NGA',
       'MDV', 'VEN', 'SVK', 'AGO', 'FJI', 'KAZ', 'PAK', 'IDN', 'LBN',
       'PHL', 'SEN', 'SYC', 'AZE', 'BHR', 'NZL', 'THA', 'DOM', 'MKD',
       'MYS', 'ARM', 'JPN', 'LKA', 'CUB', 'CMR', 'BIH', 'MUS', 'COM',
       'SUR', 'UGA', 'BGR', 'CIV', 'JOR', 'SYR', 'SGP', 'BDI', 'SAU',
       'VNM', 'PLW', 'EGY', 'PER', 'MLT', 'MWI', 'ECU', 'MDG', 'ISL',
       'UZB', 'NPL', 'BHS', 'MAC', 'TGO', 'TWN', 'DJI', 'STP', 'KNA',
       'ETH', 'IRQ', 'HND', 'RWA', 'QAT', 'KHM', 'MCO', 'BGD', 'IMN',
       'TJK', 'NIC', 'BEN', 'VGB', 'TZA', 'GAB', 'GHA', 'TMP', 'GLP',
       'KEN', 'LIE', 'GNB', 'MNE', 'UMI', 'MYT', 'FRO', 'MMR', 'PAN',
       'BFA', 'LBY', 'MLI', 'NAM', 'BOL', 'PRY', 'BRB', 'ABW', 'AIA',
       'SLV', 'DMA', 'PYF', 'GUY', 'LCA', 'ATA', 'GTM', 'ASM', 'MRT',
       'NCL', 'KIR', 'SDN', 'ATF', 'SLE', 'LAO'])  # Sesuaikan jika ingin daftar lengkap
market_segment = st.selectbox("Market Segment", ["Direct", "Corporate", "Online TA", "Offline TA/TO", "Groups", "Complementary", "Aviation"])
distribution_channel = st.selectbox("Distribution Channel", ["Direct", "Corporate", "TA/TO", "GDS"])
reserved_room_type = st.selectbox("Reserved Room Type", ["A", "C", "D", "E", "G", "F", "H", "L", "B"])
assigned_room_type = st.selectbox("Assigned Room Type", ["A", "C", "D", "E", "G", "F", "H", "I", "B", "K"])
deposit_type = st.selectbox("Deposit Type", ["No Deposit", "Refundable", "Non Refund"])
customer_type = st.selectbox("Customer Type", ["Transient", "Contract", "Transient-Party", "Group"])
agent_list = [str(i) for i in range(1, 334)]  # Agent dari 1 sampai 333 dalam bentuk string
agent = st.selectbox("Agent", agent_list)

# Prediksi
if st.button("Prediksi Pembatalan"):
    input_data = pd.DataFrame([{
        'lead_time': lead_time,
        'arrival_date_year': arrival_date_year,
        'arrival_date_month': arrival_date_month,
        'arrival_date_week_number': arrival_date_week_number,
        'arrival_date_day_of_month': arrival_date_day_of_month,
        'stays_in_weekend_nights': stays_in_weekend_nights,
        'stays_in_week_nights': stays_in_week_nights,
        'adults': adults,
        'children': children,
        'babies': babies,
        'is_repeated_guest': is_repeated_guest,
        'previous_cancellations': previous_cancellations,
        'previous_bookings_not_canceled': previous_bookings_not_canceled,
        'booking_changes': booking_changes,
        'days_in_waiting_list': days_in_waiting_list,
        'adr': adr,
        'required_car_parking_spaces': required_car_parking_spaces,
        'total_of_special_requests': total_of_special_requests,
        'hotel': hotel,
        'meal': meal,
        'country': country,
        'market_segment': market_segment,
        'distribution_channel': distribution_channel,
        'reserved_room_type': reserved_room_type,
        'assigned_room_type': assigned_room_type,
        'deposit_type': deposit_type,
        'customer_type': customer_type,
        'agent': agent
    }])

    # Prediksi label
    prediction = model.predict(input_data)

    # Prediksi probabilitas
    probability = model.predict_proba(input_data)[0][1]  # probabilitas untuk kelas '1' = DIBATALKAN
    if prediction[0] == 1:
        st.error(f"Booking diprediksi AKAN DIBATALKAN. (Probabilitas: {probability:.2%})")
    else:
        st.success(f"Booking diprediksi TIDAK dibatalkan. (Probabilitas: {1 - probability:.2%})")

