from yield_predictor import predict_yield


# Test 1: Rice - Andhra Pradesh
result1 = predict_yield(
    crop="Rice",
    crop_year=2025,
    season="Kharif",
    state="Andhra Pradesh",
    area=5000,
    annual_rainfall=1200,
    fertilizer=150000,
    pesticide=500,
    avg_temperature=27,
    max_temperature=35,
    min_temperature=21
)


# Test 2: Maize - Telangana
result2 = predict_yield(
    crop="Maize",
    crop_year=2025,
    season="Kharif",
    state="Telangana",
    area=4000,
    annual_rainfall=1000,
    fertilizer=120000,
    pesticide=450,
    avg_temperature=28,
    max_temperature=36,
    min_temperature=22
)


# Test 3: Coconut - Kerala
result3 = predict_yield(
    crop="Coconut",
    crop_year=2025,
    season="Whole Year",
    state="Kerala",
    area=3000,
    annual_rainfall=2500,
    fertilizer=180000,
    pesticide=600,
    avg_temperature=26,
    max_temperature=32,
    min_temperature=22
)


# Test 4: Wheat - Punjab
result4 = predict_yield(
    crop="Wheat",
    crop_year=2025,
    season="Rabi",
    state="Punjab",
    area=4500,
    annual_rainfall=700,
    fertilizer=130000,
    pesticide=400,
    avg_temperature=20,
    max_temperature=27,
    min_temperature=12
)


# Test 5: Potato - Karnataka
result5 = predict_yield(
    crop="Potato",
    crop_year=2025,
    season="Rabi",
    state="Karnataka",
    area=3500,
    annual_rainfall=900,
    fertilizer=110000,
    pesticide=350,
    avg_temperature=23,
    max_temperature=30,
    min_temperature=17
)


print("Yield Prediction Test Results")
print("=" * 40)

print(f"1. Rice - Andhra Pradesh : {result1:.2f}")
print(f"2. Maize - Telangana     : {result2:.2f}")
print(f"3. Coconut - Kerala      : {result3:.2f}")
print(f"4. Wheat - Punjab        : {result4:.2f}")
print(f"5. Potato - Karnataka    : {result5:.2f}")