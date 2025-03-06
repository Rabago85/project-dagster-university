---
title: 'Extra credit: dbt component'
module: 'dbt_dagster'
lesson: 'extra-credit'
---

# dbt component

Components are like individual blueprints for different integrations. A Dagster project might have a number of different components. In this project there is only a dbt project and our custom assets so we will only need the dbt component.

```bash
uv add 'dagster-components[dbt]'
```

```bash
dg list component-type
```

```bash
dg scaffold component dagster_components.dagster_dbt.DbtProjectComponent jdbt --project-path analytics
```

If we look at the component YAML produced by the CLI you can see the configuration consists of a single attribute that points to our dbt project.

```yaml
type: dagster_components.dagster_dbt.DbtProjectComponent

attributes:
  dbt:
    project_dir: ../../../analytics
```

We need to make one addition to the YAML and add an attribute for `asset_attributes`.

```yaml
type: dagster_components.dagster_dbt.DbtProjectComponent

attributes:
  dbt:
    project_dir: ../../../analytics
  asset_attributes:
    key: "taxi_{{ node.name }}"
```

This may seem familiar. This key asset mapping was handled by the custom `DagsterDbtTranslator` we defined for the dbt assets.

```python
class CustomizedDagsterDbtTranslator(DagsterDbtTranslator):
    ...

    def get_asset_key(self, dbt_resource_props):
        resource_type = dbt_resource_props["resource_type"]
        name = dbt_resource_props["name"]
        if resource_type == "source":
            return dg.AssetKey(f"taxi_{name}")
        else:
            return super().get_asset_key(dbt_resource_props)
```

But you can see the YAML attribute is much easier.

## Updating definition

Because we already have a functional Dagster project connected to dbt, we need to swap in our new component based code. Most of this will happen within the `definitions.py`

First we need to include import the components library and `build_component_defs` function to generate a definition.  

```python
from dagster_components import build_component_defs
```

Next we can update the definitions object. We had already defined a `dg.Definitions` and can start by removing the dbt pieces. This include the dbt assets and `dbt_resource` which was necessary to execute dbt in Dagster.

```python
defs = dg.Definitions(
    assets=[
        *trip_assets,
        *metric_assets,
        *requests_assets,
        # *dbt_analytics_assets,
    ],
    resources={
        "database": database_resource,
        # "dbt": dbt_resource,
    },
    jobs=all_jobs,
    schedules=all_schedules,
    sensors=all_sensors,
)
```

We want to include this definition as well as the new definition created by the components. Since there are two definitions, we can merge them together to create a single definition.

```python
defs = dg.Definitions.merge(
    dg.Definitions(
        assets=[
            *trip_assets,
            *metric_assets,
            *requests_assets,
        ],
        resources={
            "database": database_resource,
        },
        jobs=all_jobs,
        schedules=all_schedules,
        sensors=all_sensors,
    ),
    build_component_defs(
        components_root=Path(__file__).parent / "lesson_8/defs",
    ),
)
```

There is no longer a need for a dbt resource because that is now handled by the component.

The entire `dbt.py` file can be removed that contains all the asset code. This is a lot of code that can be replaced with just a few lines of YAML.