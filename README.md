# spin-up-docker-compose-action

[![CI](https://github.com/yu-ichiro/spin-up-docker-compose-action/actions/workflows/main.yml/badge.svg)](https://github.com/yu-ichiro/spin-up-docker-compose-action/actions/workflows/main.yml)

An action to spin up your docker compose environment within GitHub Actions. Caching and Optimizing, sharing image between jobs by using localhost registry.

# Basic Usage

```yml
steps:
    - name: Checkout
      uses: actions/checkout@v3
    - name: Setup docker compose
      uses: yu-ichiro/spin-up-docker-compose-action@v1
      with:
          file: compose.yml
    # docker compose environment available below
```

# Options

* `file: required string`: the file to parse targets from, normally compose.yml. supported format: `yaml`
* `project-directory: string`: the path to run docker-compose. defaults to `""`
* `profile`: the profile to run services. defaults to `""`
* `cache-key: string`: the cache key to use for saving build data. defaults to `"default"`
* `shared: bool`: whether to use local registry to share built images. this enables `registry` and `localhost`. defaults to `false`
* `registry: bool`: whether to use a local registry or not. defaults to `false`
* `localhost: bool`: whether to replace targets' registry to localhost or not. `registry` must be `true` to use this. defaults to `false`
* `pull: bool`: whether to pull targets' images. defaults to false
* `pull-opts: string`: options to pass to `docker compose pull`. `pull` must be `true` to use this. defaults to `""`
* `bake: bool`: whether to bake targets. defaults to `false`
* `push: bool`: whether to push targets' images after baking. `bake` must be `true` to use this. defaults to `false`
* `bake-opts: string`: options to pass to `docker buildx bake`. `bake` must be `true` to use this. defaults to `""`
* `up: bool`: whether to boot up docker compose. defaults to `true`
* `up-opts: string`: options to pass to `docker compose up`. `up` must be `true` to use this. defaults to `"-d"`

# Examples

example workflows are located in `./examples`
