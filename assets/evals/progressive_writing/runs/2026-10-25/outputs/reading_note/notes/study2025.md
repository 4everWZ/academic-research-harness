# Reading Note: study2025
## Method and Protocol
Study2025 fits one scalar temperature using 500 labeled target images while holding the classifier parameters fixed. Evaluation uses two fog test sets.

## Claim and Evidence
Mean expected calibration error across the two fog test sets falls from 0.13 to 0.09. Classification accuracy is unchanged.

## Use in This Paper
- Relevant role or claim: prior temperature calibration method using labeled target images.
- Safe citation scope: the scalar-temperature operation, 500-image target-label budget, fixed classifier parameters, and stated findings on two fog test sets.
- Must not be cited as: label-free learning or universal superiority.
- Connection to our study: we evaluate the same calibration operation on three target domains and report both calibration error and inference latency.

## Editorial checklist
Metric and supervision checked against source.md: mean expected calibration error and 500 labeled target images. This section and the citation cautions above remain author work notes.
