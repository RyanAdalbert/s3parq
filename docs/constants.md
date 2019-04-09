# CONSTANTS

    from core.constants import ENVIRONMENT, AWS_ACCOUNT

## Why? 
A key part of drying out code that is deployed to multiple environments is external context management. CORE takes the kiss approach with `core.constants`

## What Are They? 
each constant exposed by `core.constants` is set in order of:
- `ICHAIN_xxx` environment variable; if you set `ICHAIN_ENV_BUCKET=hamburger` in your environment, it will populate throughout core. 
- Dynamically set constants: we set `ENV_BUCKET`, `AWS_ACCOUNT`, `BRANCH_NAME` and `BATCH_JOB_QUEUE` dynamically based on the value of `ENVIRONMENT`. 
- `config/core_project.yml` defaults - these are fallbacks

## The _BRANCH\_NAME_ Constant
This one is special. It is set:
- by `ICHAIN_BRANCH_NAME` always, first and foremost
- if `ENVIRONMENT` is "dev", core will first attempt to sniff out and set based on the checked out git branch (if there is one). If no git branch is found, it falls back to the `BRANCH_NAME` envar (this is a Jenkins thing).
- if `ENVIRONMENT` is "uat" or "prod", it will be set to that ("uat" or "prod", respectively). 
