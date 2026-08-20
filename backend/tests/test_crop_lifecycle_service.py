from datetime import date, timedelta

from app.services.crop_lifecycle_service import (
    calculate_crop_age,
    calculate_expected_harvest_date,
    get_crop_duration,
    get_crop_lifecycle,
    get_growth_stage,
)


def test_supported_crop_returns_supported_lifecycle():
    result = get_crop_lifecycle(
        crop_name="rice",
        sowing_date=date.today() - timedelta(days=30),
    )

    assert result["supported"] is True
    assert result["crop_age_days"] == 30
    assert result["growth_stage"] == "Seedling"
    assert result["expected_harvest_date"] == (
        date.today() + timedelta(days=90)
    )


def test_crop_name_is_normalized():
    result = get_crop_lifecycle(
        crop_name="  RICE  ",
        sowing_date=date.today() - timedelta(days=30),
    )

    assert result["supported"] is True
    assert result["growth_stage"] == "Seedling"


def test_unsupported_crop_is_explicitly_marked():
    result = get_crop_lifecycle(
        crop_name="dragonfruit",
        sowing_date=date.today() - timedelta(days=30),
    )

    assert result["supported"] is False
    assert result["crop_age_days"] is None
    assert result["growth_stage"] is None
    assert result["days_to_harvest"] is None
    assert result["expected_harvest_date"] is None


def test_unsupported_crop_does_not_calculate_duration():
    assert get_crop_duration("dragonfruit") is None


def test_unsupported_crop_does_not_calculate_harvest_date():
    sowing_date = date.today() - timedelta(days=30)

    assert calculate_expected_harvest_date(
        crop_name="dragonfruit",
        sowing_date=sowing_date,
    ) is None


def test_future_sowing_date_returns_not_started():
    sowing_date = date.today() + timedelta(days=10)

    result = get_crop_lifecycle(
        crop_name="rice",
        sowing_date=sowing_date,
    )

    assert result["supported"] is True
    assert result["crop_age_days"] == 0
    assert result["growth_stage"] == "Not Started"
    assert result["expected_harvest_date"] == (
        sowing_date + timedelta(days=120)
    )
    assert result["days_to_harvest"] == 130


def test_missing_sowing_date_returns_not_started():
    result = get_crop_lifecycle(
        crop_name="rice",
        sowing_date=None,
    )

    assert result["supported"] is True
    assert result["crop_age_days"] is None
    assert result["growth_stage"] == "Not Started"
    assert result["days_to_harvest"] is None
    assert result["expected_harvest_date"] is None


def test_expected_harvest_date_uses_crop_duration():
    sowing_date = date(2026, 1, 1)

    result = calculate_expected_harvest_date(
        crop_name="maize",
        sowing_date=sowing_date,
    )

    assert result == date(2026, 4, 11)


def test_crop_age_never_becomes_negative():
    future_date = date.today() + timedelta(days=20)

    assert calculate_crop_age(
        sowing_date=future_date,
        current_date=date.today(),
    ) == 0


def test_crop_beyond_duration_is_maturity():
    assert get_growth_stage(
        crop_name="rice",
        crop_age_days=150,
    ) == "Maturity"