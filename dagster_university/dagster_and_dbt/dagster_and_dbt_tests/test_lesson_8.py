from pathlib import Path

import dagster as dg
import pytest
import yaml

from dagster_and_dbt_tests.fixtures import setup_dbt_env  # noqa: F401


@pytest.mark.parametrize("setup_dbt_env", ["lesson_8"], indirect=True)
def test_trips_partitioned_assets(setup_dbt_env):  # noqa: F811
    from dagster_and_dbt.lesson_8.assets import metrics, requests, trips
    from dagster_and_dbt.lesson_8.resources import database_resource

    assets = [
        trips.taxi_trips_file,
        trips.taxi_zones_file,
        trips.taxi_trips,
        trips.taxi_zones,
        metrics.manhattan_stats,
        metrics.manhattan_map,
        metrics.airport_trips,
        requests.adhoc_request,
    ]
    result = dg.materialize(
        assets=assets,
        resources={
            "database": database_resource,
        },
        partition_key="2023-01-01",
        run_config=yaml.safe_load(
            (Path(__file__).absolute().parent / "run_config.yaml").open()
        ),
    )
    assert result.success


@pytest.mark.parametrize("setup_dbt_env", ["lesson_8"], indirect=True)
def test_trips_by_week_partitioned_assets(setup_dbt_env):  # noqa: F811
    from dagster_and_dbt.lesson_8.assets import metrics
    from dagster_and_dbt.lesson_8.resources import database_resource

    assets = [
        metrics.trips_by_week,
    ]
    result = dg.materialize(
        assets=assets,
        resources={
            "database": database_resource,
        },
        partition_key="2023-01-01",
    )
    assert result.success


# TODO: Get access to components assets
@pytest.mark.skip
@pytest.mark.parametrize("setup_dbt_env", ["lesson_8"], indirect=True)
def test_dbt_partitioned_incremental_assets(setup_dbt_env):  # noqa: F811
    from dagster_components import build_component_defs

    (
        build_component_defs(
            components_root=Path(__file__).parent
            / "../dagster_and_dbt/lesson_8/lesson_8/defs",
        ),
    )

    result = dg.materialize(
        assets=[build_component_defs.assets],
        partition_key="2023-01-01",
    )
    assert result.success


@pytest.mark.parametrize("setup_dbt_env", ["lesson_8"], indirect=True)
def test_def_can_load(setup_dbt_env):  # noqa: F811
    from dagster_and_dbt.lesson_8.definitions import defs

    assert defs
