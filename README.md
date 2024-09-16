# mCNN-Glucose
## Introduction
Glucose transporters enable the passive transport of glucose across cell membranes, moving it down its concentration gradient. This process does not require energy (ATP) but relies on the concentration gradient of glucose. They help regulate blood glucose levels by controlling the uptake of glucose from the bloodstream into various tissues, particularly muscle and adipose tissue. They ensure that cells, especially those in high-demand tissues like the brain, muscle, and liver, have a constant supply of glucose for energy production and metabolism.
## Methodology
In the present study we devised a method that utilized evolutionary information from Position-Specific Scoring matrics (PSSM) as the primary features and fed these features to multiple-scanning windows-based covolutional neural networks to derive valuable insight from the evolutionary profiles to effectively classify glucose transporters into three distinct families.
![alt text](http://url/to/img.png)

## Dataset
| Families  | Primary Data | Primary Data |train | test |
| ------------- | ------------- |------------- |------------- |------------- |
| GLUTs  | 9616  | 510 | 408 | 102|
| SGLTs  | 4107  | 225 | 180 | 45|
| SWEETs  | 2026  | 190 | 152 | 38|
| Total  | 15749  | 925 | 740 | 185|
