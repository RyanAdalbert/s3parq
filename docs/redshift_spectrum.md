# Core and Amazon Redshift Spectrum

## Overview

Dataset contracts processed in Core now publish dataframe information to Redshift, exposing published datasets to be queryable via [Amazon Redshift Spectrum](https://docs.aws.amazon.com/redshift/latest/dg/c-getting-started-using-spectrum.html). The Redshift configurations used to create a table are set on `dataset_contract.publish()`. You can manually pass `publish_to_redshift=False` to `publish()` to override this functionality. The process used to expose S3 parquet datasets to Redshift is handled via our open source [s3parq library](https://github.com/IntegriChain1/s3parq/blob/master/README.md).

## Querying Redshift

Any SQL client which supports the [Amazon Redshift JDBC Driver](https://docs.aws.amazon.com/redshift/latest/mgmt/configure-jdbc-connection.html#download-jdbc-driver) can query Dataset Contracts published to S3. I'll be using the free, open source Database Tool [DBeaver](https://dbeaver.io/) for this brief guide. Amazon has written a guide for configuring [SQL Workbench](https://docs.aws.amazon.com/redshift/latest/mgmt/connecting-using-workbench.html) to query Redshift Spectrum.

*NOTE:* The following guide assumes you are running Core *locally using our dev environment.* This document will be updated with UAT/Prod connection instructions once Core is running on our UAT/Prod sandbox account. 

When adding a new database, DBeaver will first ask for the type of database to connect to. Select 'Redshift' and add the following connection settings:

Host: core-sandbox-cluster-1.c3swieqn0nz0.us-east-1.redshift.amazonaws.com\
Database: ichain_core\
Port: 5439\
Username: awsuser\
Password: AWSUserPass4

Once you've configured Redshift, you should see a screen similar to this: \
![DBeaver screen](assets/dbeaver_redshift.png?raw=true)
If you've properly connected to Redshift, you should see your datasets published to the data_core schema in the ichain_core db.

Tables are named with the convention {pharma company}\_{brand}\_{transformation}. The tables in the above screenshot are an example of a series of transformations run in a pipeline for Sun's Odomzo brand. Query tables in ichain_core using the table data_core.{your table name}.

Existing datasets published with new run IDs added to Core will be added to the corresponding existing Redshift table. You can filter your data to a specific Run ID using the `__metadata_run_id` column of published Core datasets.

## Deleting Tables

The data catalog that holds all of the metadata references to the data in S3 is [AWS Glue](https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html). You *must* delete tables through the Glue data catalog to remove them from Redshift Spectrum. Dropping tables via SQL, even on Redshift, will not delete the table references in the Glue data catalog.

You can query tables in the Glue Data Catalog via the AWS console.\
![AWS Glue](assets/glue_spectrum.png?raw=true)

Make sure to filter to the `ichain_core` database before deleting anything! Tables outside of this database are separate from Core.

## Configurations

In dev, most configurations for Redshift are constants defined in `config/core_project.yaml`. The dev configurations in this file used in Redshift are REDSHIFT_DB, REDSHIFT_DB_PORT, REDSHIFT_SCHEMA, REDSHIFT_REGION, DEV_REDSHIFT_DB_HOST, DEV_REDSHIFT_IAM_ROLE, & DEV_REDSHIFT_CLUSTER_ID. These configurations are needed both to write to and read from Redshift Spectrum.

Since we are creating many tables for different pipelines all under the same database name, the naming convention for them is important.  As of now the convention is pharma_brand_transform.  This will help keep the data organized and more manageable.


