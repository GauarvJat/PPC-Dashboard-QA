PPC Dashboard QA Automation

Overview

This project automates the quality assurance (QA) process for validating media performance data between source advertising platforms and a centralized reporting dashboard.
The solution compares platform-reported metrics from Search, Social, and Video channels against data available in the reporting dashboard and identifies discrepancies for investigation and resolution.
Business Problem

Media reporting dashboards are often populated using multiple data pipelines and transformation processes. Manual validation of dashboard data against source platforms is time-consuming, repetitive, and prone to human error.
The objective of this project was to automate the validation process and provide a reliable mechanism to identify data mismatches quickly.
Solution

A combination of Python, VBA, Excel, SQL, and Power BI was used to:
•	Extract and process media platform reports.
•	Retrieve reporting data from Databricks SQL.
•	Compare source platform metrics with dashboard metrics.
•	Identify discrepancies based on predefined validation rules.
•	Generate reports for investigation and stakeholder review.
•	Visualize QA results through interactive Power BI dashboards.

Data Sources Media Platforms

•	SA360

•	YouTube

•	Facebook


Reporting Source

•	Databricks SQL

Validation Process
1.	Download reports from media platforms.
2.	Import platform data into the validation framework.
3.	Retrieve corresponding dashboard data.
4.	Standardize dimensions and metrics.
5.	Perform automated comparisons.
6.	Flag variances exceeding acceptable thresholds.
7.	Publish QA summary through Power BI.
8.	Share findings with Project Managers and Data Engineering teams.


Technology Stack - Technology	Purpose

Python -	Data extraction, transformation, validation

VBA	- Outlook automation

SQL -	Data retrieval and analysis

Power BI - Dashboarding and visualization

Excel -	QA review and reconciliation 

Key Features

•	Automated data validation workflow

•	Cross-platform metric comparison

•	Variance detection and reporting

•	Interactive Power BI dashboard

•	Reduced manual QA effort

•	Scalable framework for multiple channels


Dashboard Components

QA Summary

Provides an overview of validation status across all channels.

Variance Analysis

Highlights discrepancies between source and dashboard data.

Trend Monitoring
Tracks validation performance over time.

Exception Reporting

Lists records requiring investigation.

Project Structure

PPC-Dashboard-QA/

├── VBA/

├── Python/

├── PowerBI/

├── Documentation/

├── Sample_Data/

└── README.md

Results

•	Reduced manual validation effort.

•	Improved confidence in dashboard reporting.

•	Faster identification of reporting discrepancies.

•	Streamlined communication between analytics and engineering teams.


Future Enhancements

•	Automated API-based report retrieval.

•	Email notifications for validation failures.

•	Scheduled execution using orchestration tools.

•	Expanded support for additional media platforms.


Disclaimer

This repository contains a portfolio version of the solution. All client-specific information, proprietary business logic, credentials, and confidential data have been removed or anonymized. Sample data has been used where applicable.
