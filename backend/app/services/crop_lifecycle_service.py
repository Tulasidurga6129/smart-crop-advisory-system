from datetime import date, timedelta


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


def get_crop_lifecycle_config(
    crop_name: str,
) -> dict | None:
    """
    Return lifecycle configuration for a supported crop.
    """
    crop_key = normalize_crop_name(crop_name)
    return CROP_LIFECYCLE.get(crop_key)


def calculate_crop_age(
    sowing_date: date,
    current_date: date | None = None,
) -> int:
    """
    Calculate the number of days since sowing.

    Future sowing dates return 0 because the crop has not
    started yet.
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

    Returns "Unknown" when the crop is unsupported or when
    the age does not fall into a configured range.
    """
    lifecycle = get_crop_lifecycle_config(crop_name)

    if lifecycle is None:
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
    Return the default lifecycle duration for a supported crop.
    """
    lifecycle = get_crop_lifecycle_config(crop_name)

    if lifecycle is None:
        return None

    return lifecycle["duration_days"]


def calculate_expected_harvest_date(
    crop_name: str,
    sowing_date: date,
) -> date | None:
    """
    Calculate expected harvest date using the default
    lifecycle duration for a supported crop.
    """
    duration = get_crop_duration(crop_name)

    if duration is None:
        return None

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
    Return calculated lifecycle information for a crop.

    Supported crops return lifecycle calculations.

    Unsupported crops are explicitly marked as unsupported
    instead of returning misleading lifecycle information.
    """
    lifecycle = get_crop_lifecycle_config(crop_name)

    # Crop is not supported by the lifecycle module.
    if lifecycle is None:
        return {
            "supported": False,
            "crop_age_days": None,
            "growth_stage": None,
            "days_to_harvest": None,
            "expected_harvest_date": None,
        }

    today = date.today()

    # Supported crop without a sowing date.
    if sowing_date is None:
        return {
            "supported": True,
            "crop_age_days": None,
            "growth_stage": "Not Started",
            "days_to_harvest": (
                calculate_days_to_harvest(
                    expected_harvest_date=expected_harvest_date,
                    current_date=today,
                )
                if expected_harvest_date
                else None
            ),
            "expected_harvest_date": expected_harvest_date,
        }

    # Future sowing date.
    if sowing_date > today:
        if expected_harvest_date is None:
            expected_harvest_date = calculate_expected_harvest_date(
                crop_name=crop_name,
                sowing_date=sowing_date,
            )

        return {
            "supported": True,
            "crop_age_days": 0,
            "growth_stage": "Not Started",
            "days_to_harvest": calculate_days_to_harvest(
                expected_harvest_date=expected_harvest_date,
                current_date=today,
            ),
            "expected_harvest_date": expected_harvest_date,
        }

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
        "supported": True,
        "crop_age_days": crop_age_days,
        "growth_stage": growth_stage,
        "days_to_harvest": days_to_harvest,
        "expected_harvest_date": expected_harvest_date,
    }