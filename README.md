# M-PACT: Mammography Pressure and Compression tracking for Quality Control

[!IMPORTANT] 

This is the preliminary version of the M-PACT software
Before continuing, please, check our paper "M-PACT: A mechanics based toolkit to evaluate 
breast compression in mammography and DBT"  currently under review

## Overview

Breast compression plays a critical role in mammography and digital breast tomosynthesis (DBT),
improving image quality while reducing radiation dose and tissue superposition.
Unfortunately, many women experience pain and discomfort during the procedure, 
and current guidelines in mammography acquisition remain vague about how much compression should be applied.

In our paper, we analyse the mamographic compression form a physical and mechanical perspective. 
By modeling the mammography compression as a uniaxial compression problem, we applied continuum mechanics to determine
the physical equations governing the relationship between uncompressed and compressed breast states.

Based  on our findings, we developed **M-PACT**, a framework to assist radiologists, medical physicists, and researchers
in analyzing breast compression. Our software is capable of estimating a suitable thickness
range, and objectively evaluate the degree of compression of already acquired mammograms calculating a quantitative 
compression score. This score enables to categorize the mammograms as *within the normal range*
and potentially *undercompressed*, or *overcompressed*.

This tool has potential applications in quality control, technologist training, and even real-time clinical 
decision support, offering a standardized and reproducible method to monitor and improve compression practices.


## M-PACT

