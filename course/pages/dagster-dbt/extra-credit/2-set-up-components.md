---
title: 'Extra credit: What are components?'
module: 'dbt_dagster'
lesson: 'extra-credit'
---

# What are components?

You might be wondering what components are and how they can help in this project. Components are an opinionated project layout that supports scaffolding. They can transform configuration files (like YAML) into Dagster definitions without the need for unnecessary code. They are particularly useful for integrations that follow common patterns. dbt is a great example of this.

When you think about the dbt project we converted into assets, most of our logic was contained in our SQL models. That mapping of Dagster onto our project was pretty standard.

Components remove a lot of the boilerplate code we needed to write and allows us to get going much more quickly.

## Setting up components

Components exist in a separate Python package `dagster-dg`. While the core `dagster` package can be specific to a particular code location, `dg` is meant to be installed globally. It also relies on `uv` 

### Install uv

We will use the Python package manager `uv` to install a globally available `dg`.

```bash
brew install uv
```

### Install the dg command line tool

Once you have installed uv, use it to install `dg`.

```bash
uv tool install dagster-dg
```

You now have everything necessary to run components and we can get started with replacing our existing code with the dbt components.