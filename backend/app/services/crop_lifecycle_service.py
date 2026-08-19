from datetime import date


# Approximate crop lifecycle durations in days.
# These values provide the initial lifecycle foundation.
# They can later be replaced with crop/variety-specific data.
CROP_LIFECYCLE = {
    "rice": {
        "duration_days": 120,
        "stages": [
            (0, 20, "Germination"),
            (21, 45, "Seedling"),
            (46, 75, "Vegetative"),
            (76, 100, "Reproductive"),
            (101, 120, "Maturity"),
        ],
    },
    "wheat": {
        "duration_days": 120,
        "stages": [
            (0, 15, "Germination"),
            (16, 35, "Seedling"),
            (36, 70, "Vegetative"),
            (71, 100, "Reproductive"),
            (101, 120, "Maturity"),
        ],
    },
    "maize": {
        "duration_days": 100,
        "stages": [
            (0, 10, "Germination"),
            (11, 30, "Seedling"),
            (31, 60, "Vegetative"),
            (61, 85, "Reproductive"),
            (86, 100, "Maturity"),
        ],
    },
    "cotton": {
        "duration_days": 160,
        "stages": [
            (0, 15, "Germination"),
            (16, 45, "Seedling"),
            (46, 90, "Vegetative"),
            (91, 130, "Flowering"),
            (131, 160, "Maturity"),
        ],
    },
    "groundnut": {
        "duration_days": 110,
        "stages": [
            (0, 15, "Germination"),
            (16, 35, "Seedling"),
            (36, 65, "Vegetative"),
            (66, 90, "Pegging and Pod Formation"),
            (91, 110, "Maturity"),
        ],
    },
    "tomato": {
        "duration_days": 100,
        "stages": [
            (0, 10, "Germination"),
            (11, 30, "Seedling"),
            (31, 55, "Vegetative"),
            (56, 80, "Flowering and Fruiting"),
            (81, 100, "Maturity"),
        ],
    },
    "potato": {
        "duration_days": 100,
        "stages": [
            (0, 15, "Germination"),
            (16, 35, "Seedling"),
            (36, 60, "Vegetative"),
            (61, 80, "Tuber Formation"),
            (81, 100, "Maturity"),
        ],
    },
    "muskmelon": {
        "duration_days": 90,
        "stages": [
            (0, 10, "Germination"),
            (11, 25, "Seedling"),
            (26, 50, "Vegetative"),
            (51, 70, "Flowering and Fruiting"),
            (71, 90, "Maturity"),
        ],
    },
}


def normalize_crop_name(crop_name: str) -> str:
    return crop_name.strip().lower()


def calculate_crop_age(
    sowing_date: date,
    current_date: date | None = None,
) -> int:
    """
    Calculate the number of days since sowing.
    """

    if current_date is None:
        current_date = date.today()

    age = (current_date - sowing_date).days

    return max(age, 0)


def get_growth_stage(
    crop_name: str,
    crop_age_days: int,
) -> str:
    """
    Determine the current growth stage using crop-specific
    lifecycle ranges.
    """

    crop_key = normalize_crop_name(crop_name)

    lifecycle = CROP_LIFECYCLE.get(crop_key)

    if not lifecycle:
        return "Unknown"

    for start_day, end_day, stage in lifecycle["stages"]:
        if start_day <= crop_age_days <= end_day:
            return stage

    if crop_age_days > lifecycle["duration_days"]:
        return "Maturity"

    return "Unknown"


def get_crop_duration(
    crop_name: str,
) -> int | None:
    """
    Return the default lifecycle duration for a crop.
    """

    crop_key = normalize_crop_name(crop_name)

    lifecycle = CROP_LIFECYCLE.get(crop_key)

    if not lifecycle:
        return None

    return lifecycle["duration_days"]


def calculate_expected_harvest_date(
    crop_name: str,
    sowing_date: date,
) -> date | None:
    """
    Calculate expected harvest date using the default
    lifecycle duration for the crop.
    """

    duration = get_crop_duration(crop_name)

    if duration is None:
        return None

    from datetime import timedelta

    return sowing_date + timedelta(days=duration)


def calculate_days_to_harvest(
    expected_harvest_date: date | None,
    current_date: date | None = None,
) -> int | None:
    """
    Calculate remaining days until expected harvest.
    """

    if expected_harvest_date is None:
        return None

    if current_date is None:
        current_date = date.today()

    return max(
        (expected_harvest_date - current_date).days,
        0,
    )


def get_crop_lifecycle(
    crop_name: str,
    sowing_date: date | None,
    expected_harvest_date: date | None = None,
) -> dict:
    """
    Return complete calculated lifecycle information
    for a crop.
    """

    if sowing_date is None:
        return {
            "crop_age_days": None,
            "growth_stage": "Not Started",
            "days_to_harvest": None,
            "expected_harvest_date": expected_harvest_date,
        }

    today = date.today()

    crop_age_days = calculate_crop_age(
        sowing_date=sowing_date,
        current_date=today,
    )

    growth_stage = get_growth_stage(
        crop_name=crop_name,
        crop_age_days=crop_age_days,
    )

    if expected_harvest_date is None:
        expected_harvest_date = calculate_expected_harvest_date(
            crop_name=crop_name,
            sowing_date=sowing_date,
        )

    days_to_harvest = calculate_days_to_harvest(
        expected_harvest_date=expected_harvest_date,
        current_date=today,
    )

    return {
        "crop_age_days": crop_age_days,
        "growth_stage": growth_stage,
        "days_to_harvest": days_to_harvest,
        "expected_harvest_date": expected_harvest_date,
    }